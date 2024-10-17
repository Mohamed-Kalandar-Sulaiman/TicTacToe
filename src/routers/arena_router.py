from fastapi import APIRouter
from fastapi import Response, Request, HTTPException



arenaRouter = APIRouter(prefix="/arena")


@arenaRouter.post(path="/lobby")
async def enter_arena():
    return Response(content="Joining a game ")





