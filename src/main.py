from fastapi import FastAPI, Depends, APIRouter
from src.repository import *
from src.routers import *
from src.middlewares import AuthMiddleware, LoggingMiddleware, CorsMiddleware


app = FastAPI(title="TicTacToe", version="1.0.0")

#! Include API routers
api = APIRouter(prefix="/api/v1", tags=[])

api.include_router(arenaRouter, tags=["Arena"])
api.include_router(gameRouter, tags=["Game"])

app.include_router(api)
app.add_middleware(CorsMiddleware)
app.add_middleware(LoggingMiddleware)
# app.add_middleware(AuthMiddleware)


