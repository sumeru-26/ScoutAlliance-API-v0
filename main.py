from typing import Annotated
from fastapi import FastAPI, Path

from entries import Entry,Many_Entries, add_entry,add_many_entries
from schema import Schema,add_team,update_schema

app = FastAPI()


@app.get("/")
async def root():
    return "Welcome to OpenScouting! This API is created by Sumeru Gowda of 2374 Jesuit Robotics."

@app.post("/{team_number}/entries/add")
async def new_entry(
    team_number : Annotated[int, Path(title="The scouting team's number")],
    entry: Many_Entries,
    many: bool = False):
    if many is True:
        add_many_entries(entry, team_number)
    else:
        add_many_entries(entry,team_number)

@app.post("/{team_number}/schema/new")
async def new_team_schema(
    team_number : Annotated[str, Path(title="The scouting team's number")]
):
    add_team(team_number)

@app.post("/{team_number}/schema/update")
async def update_team_schema(
    team_number : Annotated[str, Path(title="The scouting team's number")], 
    schema : Schema,
    type : str
):
    update_schema(schema.model_dump()['schema'],type,team_number)