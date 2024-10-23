import asyncio
import json


from fastapi import Path
from fastapi import WebSocket, WebSocketDisconnect
from src.dao import GameDAO
from src.utilities.date_helper import Date
from src.models import Game
from src.logic.TicTacToe import TicTacToeGame, check_winner

#! Initialisations

gameDAO = GameDAO()



async def gameHandler(websocket: WebSocket,
                      gameId :str):
    """WebSocket endpoint for the game, handling real-time communication."""
    await websocket.accept()
    
    #! Autheticate user for gameId
    #! Implement authorization

    # Subscribe to the Redis channel for this game
    pubsub = await gameDAO.subscribe_to_game(gameId)

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
            returnMessage = await handlePlayerEvent(gameId=gameId,playerId=1,event=data)
            if returnMessage : await websocket.send_json(data = returnMessage)
            
    except WebSocketDisconnect:
        print(f"Client disconnected from game {gameId}")
        listen_task.cancel()
        await pubsub.unsubscribe(f"GAME:{gameId}")  # Unsubscribe from the Redis channel





async def handlePlayerEvent(    gameId :str, 
                                playerId : str,
                                event:dict
                            ):
    #! Parse player message 
    eventType = event.get("type")
    eventData = event.get("data")
    if eventType not in ["MESSAGE","MOVE","COMMAND"]:
        reponse = {
            "type" :"ERROR",
            "error": "UNKNOWN_COMMAND"
        }
        return reponse
    
    #! Chat message
    if eventType == "MESSAGE":
        date = Date()
        eventData["time"] = date.get_unix_timestamp()
        return event
    
    
    game = await gameDAO.get_game(gameId=gameId)
    TicTacToe = TicTacToeGame(game=game)
    
    #! Resign / Claim Victory
    if eventType == "COMMAND":
        action = eventData.get("action")
        if action == "RESIGN":
            playerId = eventData.get("playerId")
            game = await gameDAO.get_game(gameId=gameId)
            game :Game
            if game.isGameOver == True:
                reponse = {
                            "type" :"ERROR",
                            "error": "GAME IS ALREADY OVER"
                        }
                return reponse
            
            if game.currentPlayerToMove == playerId:
                
                updateFields = {
                                "isGameOver":True,
                                "winner":game.playerX if game.playerX != playerId else game.playerO
                            }
                await gameDAO.update_game(gameId=gameId, update_data=updateFields)
                game = await gameDAO.get_game(gameId=gameId)
                response = {
                    "type":"UPDATE",
                    "data": game.__dict__
                }
                return response
            
            
            
        elif action == "CLAIM_VICTORY":
            #! Check if makeMoveBefore timestamp is passed and claim is made 
            playerId = eventData.get("playerId")
            game = await gameDAO.get_game(gameId=gameId)
            game :Game
            date = Date()
            if game.makeMoveBefore <= date.get_unix_timestamp() :
                updateFields = {
                                "isGameOver":True,
                                "winner":game.playerX if game.currentPlayerToMove == game.playerO else game.playerO
                            }
                await gameDAO.update_game(gameId=gameId, update_data=updateFields)
                game = await gameDAO.get_game(gameId=gameId)
                response = {
                    "type":"UPDATE",
                    "data": game.__dict__
                }
                return response
            else:
                
                response = {
                    "type":"UPDATE",
                    "data": game.__dict__
                }
                return response 
            
            
    if eventType == "MOVE":
        target = eventData.get("target")
        playerId = eventData.get("playerId")
        game = await gameDAO.get_game(gameId=gameId)
        game :Game
        #! Check if game is over or resiged or timeover
        if game.isGameOver == True:
                reponse = {
                            "type" :"ERROR",
                            "error": "GAME IS ALREADY OVER"
                        }
                return reponse
        #! Pure game logics
        if target > 8:
            reponse = {
                        "type" :"ERROR",
                        "error": "Invalid position"
                    }
            return reponse
        
        board = game.boardState
        if board[target] != ".":
            reponse = {
                        "type" :"ERROR",
                        "error": "Position is already taken"
                    }
            return reponse
        
       
        updatedBoard = board[:target] + game.currentShape + board[target+1:]
        winner = check_winner(updatedBoard)
        updateFields = {
                        "boardState": updatedBoard,
                        "currentPlayerToMove":  game.playerO if game.currentPlayerToMove == game.playerX else game.playerX,
                        "currentShape": "O" if game.currentShape == "X" else "X",
                        "isGameOver":True if winner else False,
                        "winner":game.currentPlayerToMove if winner else None
                        }

        await gameDAO.update_game(gameId=gameId, update_data=updateFields)
        game = await gameDAO.get_game(gameId=gameId)
        response = {
                        "type":"UPDATE",
                        "data": game.__dict__
                    }
        return response
            
    
    #! Make Move
    # await game_repo.publish_to_game(gameId=gameId,message=json.dumps(event))
    # return {"error":"ILLEGAL_MOVE"}


