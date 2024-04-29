from fastapi import APIRouter,Request,HTTPException,Depends

from .helpers import add_entry,add_many_entries,delete_entries,get_entries,verify_entry,get_entries_new  # noqa: F401
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
    #query : Query,
    request: Request,
    team_number : int = Depends(get_user)):
    print(request.query_params)
    #print(format_query(request.query_params))
    #return get_entries(team_number,query.query)
    return get_entries_new(team_number, format_query(request.query_params))

@entryRouter.delete("/delete")
async def del_entries(
    query : Query,
    team_number : int = Depends(get_user)):
    delete_entries(team_number,query.query)

def format_query(query_params):
    query_list = []
    for field,val in query_params.items():
        if val.isnumeric():
            val = int(val)
        query_list.append((field, val))
    return query_list