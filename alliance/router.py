from fastapi import APIRouter,Depends

from .helpers import get_access,add_access
from auth import get_user

allianceRouter = APIRouter()

@allianceRouter.get("/get")
async def get(
    team_number: int = Depends(get_user)):
    return get_access(team_number)

@allianceRouter.post("/add")
async def add(
    team: int,
    alliance: str,
    user: int = Depends(get_user)):
    if user == 9999:
        add_access(team, alliance)