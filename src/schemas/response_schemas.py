from pydantic import BaseModel
from typing import List, Optional

class GameResponseSchema(BaseModel):
    gameId: str
    playerX: str 
    playerO: str
    currentPlayerToMove: str
    currentShape: Optional[str] = "X"  # Optional with default value "X"
    isGameOver: Optional[bool] = False  # Optional with default value False
    winner: Optional[str] = None  # Optional, default is None
    makeMoveBefore: Optional[int] = 0  # Optional with default value 0
    boardState: List[str] = "..........."  # List of 9 spaces as default
    
    
class LobbyResponseSchema(BaseModel):
    gameId: str
    
    
    
class ErrorResponse(BaseModel):
    status_code:int
    error :str
    