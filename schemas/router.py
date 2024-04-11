from typing import Annotated

from fastapi import APIRouter, Path

from .helpers import add_team,update_schema
from models import Schema

schemaRouter = APIRouter()

@schemaRouter.post("/{team_number}/new")
async def new_team_schema(
    team_number : Annotated[int, Path(title="The scouting team's number")]
):
    add_team(team_number)

@schemaRouter.post("/{team_number}/update")
async def update_team_schema(
    team_number : Annotated[str, Path(title="The scouting team's number")], 
    schema : Schema,
    type : str
):
    update_schema(schema.model_dump()['schema'],type,team_number)