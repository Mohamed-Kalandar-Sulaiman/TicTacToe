from pydantic import BaseModel
from typing import List, Optional

class ArenaLobbyRequestSchema(BaseModel):
    playerId :str # Player ID
    rating :int


