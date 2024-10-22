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
    #! MatchMake
    
    
    # ! Initiate game
    date :Date = Date()
    date.add_time(minutes=60)
    
    game = Game(gameId=ulid.ulid(),
                playerO="Sulaiman",
                playerX="Mohamed",
                currentPlayerToMove="Mohamed",
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
        game = gameDAO.get_game(gameId=gameId)
        if game == False:
            content = {
                "error": f"Game of Id {gameId} is not found !",
                "error_code":404
            }
            return JSONResponse(content=content, status_code=404)
        
    except Exception as e:
        print(e)
        
    game:Game
    response = JSONResponse(status_code = 201,
                        content     = {"gameId":gameId})
    return response






