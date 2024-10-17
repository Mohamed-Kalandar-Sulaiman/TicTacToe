from src.database import RedisRepository
from models.game import Game


class GameRepo:
    def __init__(self):
        self.redis = RedisRepository(cluster_name="GAME")
    
    def create_game(self, **kwargs):
        """Create a new game and store it in Redis."""
        newgame = Game(**kwargs)
        key = f"GAME:{newgame.gameId}"
        try:
            self.redis.redis.json().set(key, "$", newgame.__dict__)
            return f"Game {newgame.gameId} created successfully"
        except Exception as e:
            return str(e)

    def get_game(self, gameId: str):
        """Retrieve a game by its ID from Redis."""
        key = f"GAME:{gameId}"
        try:
            game_data = self.redis.redis.json().get(key)
            if game_data:
                return Game(**game_data)
            else:
                return f"Game {gameId} not found."
        except Exception as e:
            return str(e)

    def update_game(self, gameId: str, update_data: dict):
        """Update a game in Redis with new data."""
        key = f"GAME:{gameId}"
        try:
            # Perform partial updates on the JSON object
            for field, value in update_data.items():
                path = f"$.{field}"
                self.redis.redis.json().set(key, path, value)

            return f"Game {gameId} updated successfully"
        except Exception as e:
            return str(e)

    def delete_game(self, gameId: str):
        """Delete a game from Redis."""
        key = f"GAME:{gameId}"
        try:
            result = self.redis.redis.delete(key)
            if result == 1:
                return f"Game {gameId} deleted successfully"
            else:
                return f"Game {gameId} not found."
        except Exception as e:
            return str(e)
