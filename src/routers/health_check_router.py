from fastapi import APIRouter
from fastapi.responses import JSONResponse


from src.repository import RedisRepository

healthCheckRouter = APIRouter(prefix="/healthcheck")

redis = RedisRepository(cluster_name="GAME")

@healthCheckRouter.get(path="", response_model=JSONResponse, status_code=200)
async def healthCheck():
    response = await redis.ping()
    response
    response = JSONResponse()
    return response

