import os
from redis.asyncio import Redis
from redis.exceptions import RedisError

class RedisRepository:
    def __init__(self, cluster_name: str):
        self.redis = None
        self.cluster_name = cluster_name
        self.host = os.getenv(f"{cluster_name}_REDIS_HOST", "localhost")
        self.port = int(os.getenv(f"{cluster_name}_REDIS_PORT", 6379))
        self.password = os.getenv(f"{cluster_name}_REDIS_PASSWORD", None)


    async def connect(self):
        """Initialize a connection to Redis."""
        try:
            if self.redis is None:
                self.redis = Redis(
                                    host=self.host,
                                    port=self.port,
                                    password=self.password,
                                    decode_responses=True  # Converts bytes to strings
                                )
                print(f"Connected to Redis at {self.host}:{self.port}")
        except RedisError as e:
            print(f"Error connecting to Redis: {e}")
            raise

    

    async def close(self):
        """Close the Redis connection."""
        if self.redis:
            await self.redis.close()
            print("Redis connection closed.")
