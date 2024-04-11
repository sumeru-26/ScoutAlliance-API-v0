from typing import Annotated

from fastapi import APIRouter,HTTPException,Path

from .helpers import add_entry,add_many_entries,delete_entries,get_entries,verify_entry
from models import Entry,Many_Entries,Query

entryRouter = APIRouter()

@entryRouter.post("/{team_number}/add")
async def new_entry(
    team_number : Annotated[int, Path(title="The scouting team's number")],
    entry: Entry):
    if verify_entry(entry,team_number) is False:
        raise HTTPException(status_code=400,detail="Bad entry format")
    add_entry(entry,team_number)

@entryRouter.post("/{team_number}/add_many")
async def new_entries(
    team_number : Annotated[int, Path(title="The scouting team's number")],
    entries: Many_Entries):
    try:
        type = entries.entries[0].metadata["type"]
    except AttributeError:
        raise HTTPException(status_code=400,detail="Bad entry format")
    for entry in entries.entries:
        if verify_entry(entry,team_number) is False or entry.metadata["type"] != type:
            raise HTTPException(status_code=400,detail="Bad entry format")
    add_many_entries(entries,team_number)

@entryRouter.get("/{team_number}/get")
async def find_entries(
    team_number : Annotated[int, Path(title="The scouting team's number")],
    query : Query):
    return get_entries(team_number,query.query)

@entryRouter.delete("/{team_number}/delete")
async def del_entries(
    team_number : Annotated[int, Path(title="The scouting team's number")],
    query : Query):
    delete_entries(team_number,query.query)
