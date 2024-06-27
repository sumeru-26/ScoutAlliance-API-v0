from typing import List, Union

from fastapi import APIRouter,Request,HTTPException,Depends

from .helpers import add_entry,delete_entries,get_entries,verify_entry  # noqa: F401
from app.models import Entry
from app.auth import get_user

entryRouter = APIRouter()

special_queries = ['alliance_data']

@entryRouter.post("/add")
async def new_entry(
    entry: Union[Entry, List[Entry]],
    team_number: int = Depends(get_user)):
    if isinstance(entry, Entry):
        entry = [entry]
    for e in entry:
        if verify_entry(e,team_number) is False:
            raise HTTPException(status_code=400,detail="Bad entry format; failed schema verification")
    add_entry(entry,team_number)

@entryRouter.get("/get")
async def find_entries(
    request: Request,
    alliance_data: bool = False,
    team_number: int = Depends(get_user)):
    return get_entries(team_number, format_query(request.query_params), alliance_data)

@entryRouter.delete("/delete")
async def del_entries(
    request: Request,
    team_number: int = Depends(get_user)):
    delete_entries(team_number,format_query(request.query_params, dict=True))

def format_query(query_params, dict: bool = False):
    query_list = {} if dict is True else []
    for field,val in query_params.items():
        if field in special_queries:
                continue
        if val.isnumeric():
            val = int(val)
        if dict is True:
            query_list[field] = val
        else:
            query_list.append((field, val))
    return query_list