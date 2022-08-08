from fastapi import FastAPI, APIRouter
from src.endpoints.router import api_router
from src.config import settings

default_router = APIRouter(
    responses={404: {"description": "Not found"}},
)

def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(api_router)
    return app

app = create_app()