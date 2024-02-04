from typing import List

from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

from mongodb import client

class Entry(BaseModel):
    metadata : dict | None = None
    abilities : dict | None = None
    counters : dict | None = None
    data : dict | None = None
    ratings : dict | None = None
    timers : dict | None = None

class Many_Entries(BaseModel):
    entries : List[Entry]

class Query(BaseModel):
    query : dict
    
cached_models = {}

def verify_entry(entry : Entry, team : int):
    if team in cached_models.keys():
        pass
    else:
        pass

def add_entry(entry : Entry, team : int):   
    teamdb = client['entries'][str(team)]
    teamdb.insert_one(entry.model_dump())

def add_many_entries(entries : Many_Entries, team : int):
    teamdb = client['entries'][str(team)]
    uploadable_data = jsonable_encoder(entries)
    teamdb.insert_many(uploadable_data['entries'])

def get_entries(team : int, query : dict) -> dict:
    teamdb = client['entries'][str(team)]
    cursor = teamdb.find(query)
    print(cursor)
    re = [x for x in cursor]
    for x in re:
        del x['_id']
    return {'entries' : re}