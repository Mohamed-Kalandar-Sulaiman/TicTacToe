from fastapi import APIRouter
from fastapi import Response, Request, HTTPException
from fastapi import WebSocket


gameRouter = APIRouter(prefix="/game")

# WebSocket endpoint for game
@gameRouter.websocket("{gameId}")
async def game(websocket: WebSocket,
               gameId: str):
    await websocket.accept()  # Accept the WebSocket connection
    try:
        while True:
            # Wait for a message from the client
            data = await websocket.receive_text()
            print(f"Received from client: {data}")

            # Here you can implement the game logic (e.g., broadcasting messages)
            # For example, echoing the received message back to the client
            await websocket.send_text(f"Message from game {gameId}: {data}")
    except WebSocketDisconnect:
        print(f"Client disconnected from game {gameId}")