from typing import Dict

from fastapi import APIRouter,Depends,HTTPException

from .helpers import add_team,update_schema,get_schema
from app.auth import get_user

schemaRouter = APIRouter()

@schemaRouter.post("/new")
async def new_team_schema(
    team_number: int = Depends(get_user),
    team_override: int | None = None):
    if team_override:
        if team_number == 9999:
            add_team(team_override)
        else:
            raise HTTPException(403, "Only master key can override")
    else:
        add_team(team_number)

@schemaRouter.post("/update")
async def update_team_schema(
    schema: Dict[str, str],
    team_number: int = Depends(get_user)):
    update_schema(schema,team_number)

@schemaRouter.get("/get")
async def get_team_schema(
    team_number: int = Depends(get_user)):
    return get_schema(team_number)