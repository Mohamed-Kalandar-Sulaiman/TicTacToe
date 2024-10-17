import os
from redis.cluster import RedisCluster
from redis.exceptions import RedisError

class RedisRepository:
    _instances = {}  

    def __new__(cls, cluster_name:str)->RedisCluster:
        if cluster_name not in cls._instances:
            cls._instances[cluster_name] = super(RedisRepository, cls).__new__(cls)
        return cls._instances[cluster_name]

    def __init__(self, cluster_name):
        if not hasattr(self, 'BASE'):  # Initialize only once per cluster
            self.redis = self._create_redis_cluster_client(cluster_name)

    def _create_redis_cluster_client(self, cluster_name):
        try:
            
            startup_nodes = [
                {"host": os.getenv(f"{cluster_name}_REDIS_NODE_1", "localhost"), "port": 6379},
                {"host": os.getenv(f"{cluster_name}_REDIS_NODE_2", "localhost"), "port": 6379},
                # Add more nodes as necessary, or handle dynamically
            ]
            return RedisCluster(
                startup_nodes=startup_nodes,
                username=os.getenv(f"{cluster_name}REDIS_USERNAME", None),
                password=os.getenv(f"{cluster_name}REDIS_PASSWORD", None),
                decode_responses=True
            )
        except RedisError as e:
            print(f"Error connecting to {cluster_name} Redis Cluster: {e}")
            raise

