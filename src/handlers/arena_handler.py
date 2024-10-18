from fastapi.responses import JSONResponse
from fastapi import Response, Request, HTTPException
from fastapi import Path,Query

from src.dao.game_dao import GameDAO
from src.models import Game
from src.schemas import *



gameDAO = GameDAO()


async def arenaLobbyHandler(request:ArenaLobbyRequestSchema):
    pass



async def arenaGameHandler( gameId:str):
    try:
        game = gameDAO.get_game(gameId=gameId)
    except Exception as e:
        print(e)
        
    game:Game
    response = JSONResponse(status_code = 201,
                        content     = {"gameId":gameId})
    return response






