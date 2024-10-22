from fastapi import APIRouter
from fastapi.responses import JSONResponse, HTMLResponse

from src.schemas import *

from src.handlers.arena_handler import arenaGameHandler, arenaLobbyHandler


arenaRouter = APIRouter(prefix="/arena")



arenaRouter.add_api_route(path              = "/lobby",
                          response_class    = JSONResponse,
                          response_model    = LobbyResponseSchema,
                          status_code       = 202,
                          methods           = ["POST"],
                          description       = "API to put player in queue . Reponse has new gameId using which we can enter game",
                          name              = "Enter arena lobby",
                          endpoint          = arenaLobbyHandler)

arenaRouter.add_api_route(path              = "/game/{gameId}",
                          response_class    = JSONResponse,
                          response_model    = GameResponseSchema,
                          status_code       = 200,
                          methods           = ["GET"],
                          description       = "Fetch game state. Incase of initial staging of game page or when user reconnects to fecth game state",
                          name              = "Get game",
                          endpoint          = arenaGameHandler
                          )




