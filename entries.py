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
    

def add_entry(entry : Entry, team : int):   
    teamdb = client['entries'][str(team)]
    teamdb.insert_one(entry.model_dump())

def add_many_entries(entries : Many_Entries, team : int):
    teamdb = client['entries'][str(team)]
    uploadable_data = jsonable_encoder(entries)
    teamdb.insert_many(uploadable_data['entries'])