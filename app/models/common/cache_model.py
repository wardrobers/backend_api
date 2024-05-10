import os
import json
import redis
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID


# Get Redis credentials from the REDISCRED environment variable
redis_credentials = json.loads(os.environ["REDISCRED"])


class RedisCache:
    """
    Simple Redis Cache class to handle caching operations.
    """

    def __init__(self, host="localhost", port=6379, password="password"):
        self.r = redis.Redis(host=host, port=port, password=password)

    def get(self, key):
        """
        Retrieve a key from Redis.
        """
        try:
            return self.r.get(key)
        except redis.RedisError:
            return None

    def set(self, key, value, ttl=None):
        """
        Set a key in Redis with an optional TTL.
        """
        try:
            if ttl:
                self.r.setex(key, ttl, value)
            else:
                self.r.set(key, value)
        except redis.RedisError:
            pass

    def delete(self, key):
        """
        Delete a key from Redis.
        """
        try:
            self.r.delete(key)
        except redis.RedisError:
            pass


class CachingMixin:
    """
    Mixin to add caching using Redis for frequently accessed data.
    """

    _redis_cache = RedisCache(
        host=redis_credentials["host"],
        port=redis_credentials["port"],
        password=redis_credentials["password"],
    )

    @classmethod
    def cached_find_by_id(cls, db_session: Session, _id: UUID):
        """
        Retrieves an entry by ID with caching to reduce database load.
        """
        key = f"{cls.__name__}:{str(_id)}"
        cached_result = cls._redis_cache.get(key)
        if cached_result:
            return cached_result

        result = (
            db_session.query(cls)
            .filter(cls.id == _id, cls.deleted_at.is_(None))
            .first()
        )
        if result:
            cls._redis_cache.set(key, result, ttl=3600)  # Cache for 1 hour
        return result

    @classmethod
    def invalidate_cache(cls, _id: UUID):
        """
        Invalidate cache entry when data is updated or deleted.
        """
        key = f"{cls.__name__}:{str(_id)}"
        cls._redis_cache.delete(key)
