import asyncio
import json


from fastapi import Path
from fastapi import WebSocket, WebSocketDisconnect
from src.dao import GameDAO

#! Initialisations

game_repo = GameDAO()



async def gameHandler(websocket: WebSocket,
                      gameId :str):
    """WebSocket endpoint for the game, handling real-time communication."""
    await websocket.accept()
    
    #! Autheticate user for gameId
    #! Implement authorization

    # Subscribe to the Redis channel for this game
    pubsub = await game_repo.subscribe_to_game(gameId)

    async def listen_to_redis_channel():
        """Listen for messages from Redis Pub/Sub."""
        async for message in pubsub.listen():
            #! Read from channel and push gameaState changes back to connected player 
            try:
                if message["type"] == "message":
                    try:
                        print(f"Sending data {message['data']} to user")
                        # Send game state changes back to the player
                        await websocket.send_json(data=json.loads(message['data']))
                    except Exception as e:
                        print(f"Error sending data to user: {e}")
            except Exception as e:
                print(e)
                

    try:
        listen_task = asyncio.create_task(listen_to_redis_channel())
        while True:
            #! Wait for messages from the WebSocket client
            data = await websocket.receive_json()
            print(f"Data {data} is recieved from player")
            # await game_repo.publish_to_game(gameId, data)
            await handlePlayerMessage(gameId=gameId,playerId=1,data=data)
            
    except WebSocketDisconnect:
        print(f"Client disconnected from game {gameId}")
        listen_task.cancel()
        await pubsub.unsubscribe(f"GAME:{gameId}")  # Unsubscribe from the Redis channel





async def handlePlayerMessage(  gameId :str, 
                                playerId : str,
                                data:dict
                            ):
    
    await game_repo.publish_to_game(gameId=gameId,message=json.dumps(data))


