import os
import json
import pickle
import hashlib
from typing import Any, Optional
from redis.asyncio import Redis
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession


# Get Redis credentials
redis_credentials = json.loads(os.environ["REDISCRED"])


class CachingMixin:
    """
    Enhanced mixin for caching data using Redis, featuring:

    - Personalized hash key generation specific to Wardrobers' data models.
    - Robust serialization with pickle for complex data structures.
    - Optimized Redis interaction using aioredis for asynchronous operations.
    - Configurable cache expiry (TTL).
    - Cache invalidation methods.
    """

    _redis = None

    @classmethod
    async def get_redis(cls):
        """Get or create a Redis client."""
        if cls._redis is None:
            cls._redis = Redis(
                host=redis_credentials['host'],
                port=redis_credentials['port'],
                password=redis_credentials['password'],
                decode_responses=True
            )
        return cls._redis

    @classmethod
    def _generate_cache_key(
        cls, _id: UUID, extra_params: Optional[dict[str, Any]] = None
    ) -> str:
        """
        Generates a personalized cache key incorporating model name, ID, and optional parameters.

        Example: 'User:e9ab3302-9887-11ec-a439-02488537b83c:{"role": "admin"}'
        """
        base_key = f"{cls.__name__}:{str(_id)}"
        if extra_params:
            extra_str = json.dumps(extra_params, sort_keys=True)
            base_key += f":{extra_str}"
        return hashlib.sha256(
            base_key.encode()
        ).hexdigest()  # Use SHA256 for robust hashing

    @classmethod
    async def cached_get_by_id(
        cls,
        db_session: AsyncSession,
        _id: UUID,
        ttl: int = 3600,
        extra_params: Optional[dict[str, Any]] = None,
    ):
        """
        Retrieves an entry by ID, utilizing Redis caching.

        Args:
            db_session (AsyncSession): The async database session.
            _id (UUID): The ID of the object to retrieve.
            ttl (int): Time-to-live for the cached data in seconds (default: 1 hour).
            extra_params (Optional[Dict[str, Any]]): Additional parameters to personalize the cache key.
        """
        redis = await cls.get_redis()
        cache_key = cls._generate_cache_key(_id, extra_params)
        data = await redis.get(cache_key)

        if data:
            return pickle.loads(data)  # Deserialize using pickle

        instance = await cls.get_by_id(db_session, _id)
        if instance:
            await redis.set(cache_key, pickle.dumps(instance), expire=ttl)
        return instance

    @classmethod
    async def invalidate_cache_by_id(
        cls, _id: UUID, extra_params: Optional[dict[str, Any]] = None
    ):
        """Invalidate the cache for a specific ID and optional parameters."""
        redis = await cls.get_redis()
        cache_key = cls._generate_cache_key(_id, extra_params)
        await redis.delete(cache_key)

    @classmethod
    async def invalidate_all_cache(cls):
        """Invalidate all cache entries for this model."""
        redis = await cls.get_redis()
        pattern = f"{cls.__name__}:*"
        async for key in redis.iscan(match=pattern):
            await redis.delete(key)
