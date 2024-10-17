import os
import aioredis
from redis.exceptions import RedisError

class RedisRepository:
    _instances = {}

    def __new__(cls, cluster_name: str) -> aioredis.Redis:
        if cluster_name not in cls._instances:
            cls._instances[cluster_name] = super(RedisRepository, cls).__new__(cls)
        return cls._instances[cluster_name]

    def __init__(self, cluster_name: str):
        if not hasattr(self, 'redis'):  # Initialize only once per cluster
            self.redis = None
            self.cluster_name = cluster_name
            self.startup_nodes = [
                (os.getenv(f"{cluster_name}_REDIS_NODE_1", "localhost"), 6379),
                (os.getenv(f"{cluster_name}_REDIS_NODE_2", "localhost"), 6379),
                
            ]

    async def connect(self):
        """Initialize the connection asynchronously."""
        if not self.redis:
            try:
                self.redis = await self._create_redis_cluster_client(self.cluster_name)
            except RedisError as e:
                print(f"Error connecting to {self.cluster_name} Redis Cluster: {e}")
                raise

    async def _create_redis_cluster_client(self, cluster_name: str) -> aioredis.Redis:
        """Create the Redis cluster client asynchronously."""
        try:
            # Create an aioredis client for cluster setup
            pool = await aioredis.from_cluster_startup_nodes(
                startup_nodes=self.startup_nodes,
                username=os.getenv(f"{cluster_name}_REDIS_USERNAME", None),
                password=os.getenv(f"{cluster_name}_REDIS_PASSWORD", None),
                decode_responses=True
            )
            return pool
        except RedisError as e:
            print(f"Error connecting to {cluster_name} Redis Cluster: {e}")
            raise
