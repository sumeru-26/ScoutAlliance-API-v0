from typing import Dict

from fastapi import APIRouter,Depends,HTTPException

from .helpers import add_team_new,update_schema_new
from models import Schema
from auth import get_user

schemaRouter = APIRouter()

@schemaRouter.post("/new")
async def new_team_schema(
    team_number: int = Depends(get_user),
    team_override: int | None = None):
    if team_override:
        if team_number == 9999:
            add_team_new(team_override)
        else:
            raise HTTPException(403, "Only master key can override")
    else:
        add_team_new(team_number)

@schemaRouter.post("/update")
async def update_team_schema(
    schema: Dict[str, str],
    team_number: int = Depends(get_user)):
    update_schema_new(schema,team_number)