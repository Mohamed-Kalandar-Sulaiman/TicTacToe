import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from src.handlers.game_handler import gameHandler



gameRouter = APIRouter(prefix="/game")


gameRouter.add_api_websocket_route(path="/{gameId}",
                                   endpoint=gameHandler,
                                   name="Get realtime game updates via Websockets"
                                   )


