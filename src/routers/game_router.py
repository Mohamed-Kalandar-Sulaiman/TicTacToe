import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from src.repository import GameRepo
from src.database import RedisRepository

gameRouter = APIRouter(prefix="/game")

game_repo = GameRepo()



@gameRouter.websocket("/{gameId}")
async def game(websocket: WebSocket, gameId: str):
    """WebSocket endpoint for the game, handling real-time communication."""
    await websocket.accept()

    # Subscribe to the Redis channel for this game
    pubsub = await game_repo.subscribe_to_game(gameId)

    async def listen_to_redis_channel():
        """Listen for messages from Redis Pub/Sub."""
        async for message in pubsub.listen():
            try:
                websocket.send_json(data=message)
            except Exception as e:
                print(e)
                

    try:
        listen_task = asyncio.create_task(listen_to_redis_channel())
        while True:
            # Wait for messages from the WebSocket client
            data = await websocket.receive_json()
            await game_repo.publish_to_game(gameId, data)
    except WebSocketDisconnect:
        print(f"Client disconnected from game {gameId}")
        listen_task.cancel()
        await pubsub.unsubscribe(f"GAME:{gameId}")  # Unsubscribe from the Redis channel
