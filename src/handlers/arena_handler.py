import ulid 
import time
from fastapi.responses import JSONResponse
from fastapi import Response, Request, HTTPException
from fastapi import Path,Query

from src.dao.game_dao import GameDAO
from src.models import Game
from src.schemas import *

from src.utilities.date_helper import Date

gameDAO = GameDAO()


async def arenaLobbyHandler(request:ArenaLobbyRequestSchema):
    #! MatchMake Logic is to be implemented ...
    playerX = "Sulaiman"
    playerO= "Mohamed"
    
    # ! Initiate game
    date :Date = Date()
    date.add_time(seconds=60)
    
    game = Game(gameId  =ulid.ulid(),
                playerO =playerO,
                playerX = playerX,
                currentPlayerToMove=playerX,
                makeMoveBefore= date.get_unix_timestamp()
                )
    await gameDAO.create_game(game=game)
    content = {
        "gameId":game.gameId
    }
    response = JSONResponse(content=content)
    return response





async def arenaGameHandler( gameId:str):
    try:
        game = await gameDAO.get_game(gameId=gameId)
        game:Game
        response = JSONResponse(status_code = 201,
                            content     = {"data":game.__dict__})
        return response
    except Exception as e:
        content = {
            "error": f"{e}",
            "error_code":404
        }
        return JSONResponse(content=content, status_code=404)
    






