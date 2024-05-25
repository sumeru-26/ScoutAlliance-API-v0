from fastapi import APIRouter,Depends

from .helpers import get_access,add_access,remove_access
from app.auth import get_user

allianceRouter = APIRouter()

@allianceRouter.get("/get")
async def get(
    team_override: int = None,
    team_number: int = Depends(get_user)):
    if (team_number == 9999 and team_override is not None):
        return get_access(team_override)
    return get_access(team_number)

@allianceRouter.post("/add")
async def add(
    team: int,
    alliance: str,
    user: int = Depends(get_user)):
    if user == 9999:
        add_access(team, alliance)

@allianceRouter.delete("/remove")
async def remove(
    team: int,
    alliance: str,
    user: int = Depends(get_user)):
    if user == 9999:
        remove_access(team, alliance)