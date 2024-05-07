from fastapi import APIRouter,Depends

from .helpers import get_access
from auth import get_user

allianceRouter = APIRouter()

@allianceRouter.get("/test")
async def test(
    team_number: int = Depends(get_user)):
    return get_access(team_number)