from typing import Annotated

from fastapi import APIRouter,HTTPException,status,Path,Depends

from .helpers import add_entry,add_many_entries,delete_entries,get_entries,verify_entry
from models import Entry,Many_Entries,Query
from auth import get_user

entryRouter = APIRouter()

@entryRouter.post("/add")
async def new_entry(
    entry : Entry,
    team_number : int = Depends(get_user)):
    if verify_entry(entry,team_number) is False:
        raise HTTPException(status_code=400,detail="Bad entry format")
    add_entry(entry,team_number)

@entryRouter.post("/add_many")
async def new_entries(
    entries: Many_Entries,
    team_number : int = Depends(get_user)):
    try:
        type = entries.entries[0].metadata["type"]
    except AttributeError:
        raise HTTPException(status_code=400,detail="Bad entry format")
    for entry in entries.entries:
        if verify_entry(entry,team_number) is False or entry.metadata["type"] != type:
            raise HTTPException(status_code=400,detail="Bad entry format")
    add_many_entries(entries,team_number)

@entryRouter.get("/get")
async def find_entries(
    query : Query,
    team_number : int = Depends(get_user)):
    return get_entries(team_number,query.query)

@entryRouter.delete("/delete")
async def del_entries(
    query : Query,
    team_number : int = Depends(get_user)):
    delete_entries(team_number,query.query)
