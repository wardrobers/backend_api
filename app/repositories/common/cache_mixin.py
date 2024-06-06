import hashlib
import json
import os
import pickle
from typing import Any, Optional

from redis.asyncio import Redis
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.common import BaseMixin


ENV = os.getenv("ENV", default="development")

# Get Redis credentials
if ENV == "production":
    redis_credentials = json.loads(os.environ["REDISCRED"])
else:
    from dotenv import load_dotenv

    load_dotenv()
    redis_credentials = json.loads(os.getenv("REDISCRED", "{}"))


class CachingMixin(BaseMixin):
    """
    Enhanced mixin for caching data using Redis, featuring:

    - Personalized hash key generation specific to Wardrobers' data models.
    - Robust serialization with pickle for complex data structures.
    - Optimized Redis interaction using aioredis for asynchronous operations.
    - Configurable cache expiry (TTL).
    - Cache invalidation methods.
    """
    
    _redis = None

    async def get_redis(self):
        """Get or create a Redis client."""
        if self._redis is None:
            self._redis = Redis(
                host=redis_credentials["host"],
                port=redis_credentials["port"],
                password=redis_credentials["password"],
                decode_responses=True,
            )
        return self._redis

    def _generate_cache_key(
        self, _id: UUID, extra_params: Optional[dict[str, Any]] = None
    ) -> str:
        """
        Generates a personalized cache key incorporating model name, ID, and optional parameters.

        Example: 'Users:e9ab3302-9887-11ec-a439-02488537b83c:{"role": "admin"}'
        """
        base_key = f"{self.model.__name__}:{str(_id)}" 
        if extra_params:
            extra_str = json.dumps(extra_params, sort_keys=True)
            base_key += f":{extra_str}"
        return hashlib.sha256(
            base_key.encode()
        ).hexdigest() 

    async def cached_get_by_id(
        self,
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
        redis = await self.get_redis()
        cache_key = self._generate_cache_key(_id, extra_params)
        data = await redis.get(cache_key)

        if data:
            return pickle.loads(data)

        async with db_session.begin():
            instance = await self.get_by_id(db_session, _id)
            if instance:
                await redis.set(cache_key, pickle.dumps(instance), expire=ttl)
            return instance

    async def invalidate_cache_by_id(
        self, _id: UUID, extra_params: Optional[dict[str, Any]] = None
    ):
        """Invalidate the cache for a specific ID and optional parameters."""
        redis = await self.get_redis()
        cache_key = self._generate_cache_key(_id, extra_params)
        await redis.delete(cache_key)

    async def invalidate_all_cache(self):
        """Invalidate all cache entries for this model."""
        redis = await self.get_redis()
        pattern = f"{self.__name__}:*"
        async for key in redis.iscan(match=pattern):
            await redis.delete(key)
