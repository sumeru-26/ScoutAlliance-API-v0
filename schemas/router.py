from fastapi import APIRouter,Depends

from .helpers import add_team,update_schema
from models import Schema
from auth import get_user

schemaRouter = APIRouter()

@schemaRouter.post("/new")
async def new_team_schema(
    team_number : int = Depends(get_user)):
    add_team(team_number)

@schemaRouter.post("/update")
async def update_team_schema(
    schema : Schema,
    type : str,
    team_number : int = Depends(get_user)):
    update_schema(schema.model_dump()['schema'],type,team_number)