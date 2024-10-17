from dataclasses import dataclass, field

@dataclass
class Game:
    gameId : str
    players :list
    currentPlayerToMove:str
    isGameOver : bool = False
    winner : str = None
    makeMoveBefore: int
    boardState : str = field(default_factory=lambda: [" " for _ in range(9)])
    
   

@dataclass
class Profile:
    userName : str 
    email:str
    password :str
    
    