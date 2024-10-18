from dataclasses import dataclass, field

@dataclass
class Game:
    gameId  : str
    playerX :str
    playerO :str
    currentPlayerToMove:str
    currentShape:str = "X"
    isGameOver : bool = False
    winner : str = None
    makeMoveBefore: int = 0
    boardState : str = "........."
    
   