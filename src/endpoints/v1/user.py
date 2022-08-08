from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get('')
async def get_users():
    return JSONResponse(content={'message': 'ok'})