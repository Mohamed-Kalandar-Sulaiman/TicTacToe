from src.repository import RedisRepository
from src.models.game import Game
import asyncio

class GameDAO:
    def __init__(self):
        self.redis_repo = RedisRepository(cluster_name="GAME")
        
        
    async def subscribe_to_game(self, gameId: str):
        """Subscribe to a Redis Pub/Sub channel for a specific game asynchronously."""
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(f"GAME:{gameId}")
        return pubsub



    async def publish_to_game(self, gameId: str, message: str):
        """Publish a message to the game's Redis channel asynchronously."""
        await self.redis.publish(f"GAME:{gameId}", message)



    async def create_game(self, **kwargs):
        """Create a new game and store it in Redis."""
        newgame = Game(**kwargs)
        key = f"GAME:{newgame.gameId}"
        await self.redis_repo.connect()  # Ensure connection to Redis
        try:
            await self.redis_repo.redis.json().set(key, "$", newgame.__dict__)
            return f"Game {newgame.gameId} created successfully"
        except Exception as e:
            raise str(e)



    async def get_game(self, gameId: str)-> Game:
        """Retrieve a game by its ID from Redis."""
        key = f"GAME:{gameId}"
        await self.redis_repo.connect()
        try:
            game_data = await self.redis_repo.redis.json().get(key)
            if game_data:
                return Game(**game_data)
            else:
                return f"Game {gameId} not found."
        except Exception as e:
            raise str(e)



    async def update_game(self, gameId: str, update_data: dict):
        """Update a game in Redis with new data."""
        key = f"GAME:{gameId}"
        await self.redis_repo.connect()
        try:
            # Perform partial updates on the JSON object
            for field, value in update_data.items():
                path = f"$.{field}"
                await self.redis_repo.redis.json().set(key, path, value)

            return f"Game {gameId} updated successfully"
        except Exception as e:
            raise str(e)



    async def delete_game(self, gameId: str):
        """Delete a game from Redis."""
        key = f"GAME:{gameId}"
        await self.redis_repo.connect()
        try:
            result = await self.redis_repo.redis.delete(key)
            if result == 1:
                return f"Game {gameId} deleted successfully"
            else:
                raise f"Game {gameId} not found."
        except Exception as e:
            raise str(e)
