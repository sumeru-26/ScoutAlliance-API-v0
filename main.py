from typing import Annotated
from contextlib import asynccontextmanager

from fastapi import FastAPI,HTTPException,Path

from entries import Entry,Many_Entries,Query,add_entry,add_many_entries,delete_entries,get_entries,cache_model,verify_entry
from schema import Schema,add_team,update_schema
from mongodb import client

app = FastAPI()
pre_cached = []

@asynccontextmanager
async def lifespan(app : FastAPI):
    try:
        client.admin.command('ping')
    except Exception as e:
        print(e)
    for team in pre_cached:
        cache_model(team)

@app.post("/{team_number}/entries/add")
async def new_entry(
    team_number : Annotated[int, Path(title="The scouting team's number")],
    entry: Entry):
    if verify_entry(entry,team_number) is False:
        raise HTTPException(status_code=400,detail="Bad entry format")
    add_entry(entry,team_number)

@app.post("/{team_number}/entries/add_many")
async def new_entries(
    team_number : Annotated[int, Path(title="The scouting team's number")],
    entries: Many_Entries):
    for entry in entries.entries:
        if verify_entry(entry,team_number) is False:
            raise HTTPException(status_code=400,detail="Bad entry format")
    add_many_entries(entries,team_number)

@app.get("/{team_number}/entries/get")
async def find_entries(
    team_number : Annotated[int, Path(title="The scouting team's number")],
    query : Query):
    return get_entries(team_number,query.query)

@app.delete("/{team_number}/entries/delete")
async def del_entries(
    team_number : Annotated[int, Path(title="The scouting team's number")],
    query : Query):
    delete_entries(team_number,query.query)

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

@app.get("/")
async def root():
    return "Welcome to OpenScouting! This API is created by Sumeru Gowda of 2374 Jesuit Robotics."