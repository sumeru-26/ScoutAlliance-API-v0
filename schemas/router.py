from typing import Annotated

from fastapi import APIRouter,HTTPException,status,Path,Depends

from .helpers import add_team,update_schema
from models import Schema
from auth import get_user

schemaRouter = APIRouter()

def check_key(team: int, user: int):
    if team != user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid API Key"
            )

@schemaRouter.post("/{team_number}/new")
async def new_team_schema(
    
    team_number : Annotated[int, Path(title="The scouting team's number")],
    user : int = Depends(get_user)):
    check_key(team_number,user)
    add_team(team_number)

@schemaRouter.post("/{team_number}/update")
async def update_team_schema(
    team_number : Annotated[str, Path(title="The scouting team's number")], 
    schema : Schema,
    type : str,
    user : int = Depends(get_user)):
    check_key(team_number,user)
    update_schema(schema.model_dump()['schema'],type,team_number)