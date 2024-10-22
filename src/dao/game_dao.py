from src.repository import RedisRepository
from src.models.game import Game
import asyncio
from redis.exceptions import RedisError

class GameDAO:
    def __init__(self):
        self.redis_repo = RedisRepository(cluster_name="GAME_CLUSTER")
        
        
    async def subscribe_to_game(self, gameId: str):
        """Subscribe to a Redis Pub/Sub channel for a specific game asynchronously."""
        await self.redis_repo.connect()
        pubsub = self.redis_repo.redis.pubsub()
        await pubsub.subscribe(f"GAME:{gameId}")
        return pubsub



    async def publish_to_game(self, gameId: str, message: str):
        """Publish a message to the game's Redis channel asynchronously."""
        await self.redis_repo.connect()
        return await self.redis_repo.redis.publish(f"GAME:{gameId}", message)



    async def create_game(self, game:Game):
        """Create a new game and store it in Redis."""
       
        
        try:
            key = f"GAME:{game.gameId}"
            await self.redis_repo.connect()
            await self.redis_repo.redis.json().set(key, "$", game.__dict__)
            return f"Game {game.gameId} created successfully"
        except RedisError as e:
            print(f"Error creating game: {e}")
            raise



    async def get_game(self, gameId: str)-> Game:
        """Retrieve a game by its ID from Redis."""
        key = f"GAME:{gameId}"
        redis = self.redis_repo.redis
        try:
            game_data = await redis.json().get(key)
            if game_data:
                return Game(**game_data)
            else:
                raise ValueError(f"Game {gameId} not found.")
        except RedisError as e:
            print(f"Error retrieving game {gameId}: {e}")
            raise



    async def update_game(self, gameId: str, update_data: dict)->Game:
        """Update a game in Redis with new data."""
        key = f"GAME:{gameId}"
        redis = self.redis_repo.redis
        try:
            for field, value in update_data.items():
                path = f"$.{field}"
                await redis.json().set(key, path, value)

            return f"Game {gameId} updated successfully"
        except RedisError as e:
            print(f"Error updating game {gameId}: {e}")
            raise



    async def delete_game(self, gameId: str) -> None:
        """Delete a game from Redis."""
        key = f"GAME:{gameId}"
        redis = self.redis_repo.redis
        try:
            result = await redis.delete(key)
            if result == 1:
                return f"Game {gameId} deleted successfully"
            else:
                raise ValueError(f"Game {gameId} not found.")
        except RedisError as e:
            print(f"Error deleting game {gameId}: {e}")
            raise
