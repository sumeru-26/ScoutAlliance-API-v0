from pydantic import BaseModel
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

class Entry(BaseModel):
    metadata : dict | None = None
    abilities : dict | None = None
    counters : dict | None = None
    data : dict | None = None
    ratings : dict | None = None
    timers : dict | None = None
    

def add_entry(entry : Entry, team : int):
    
    uri = "mongodb+srv://code_aven:Uaca4pnur@openscouting.xsr04sk.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri, server_api=ServerApi('1'))
    teamdb = client['entries'][str(team)]
    teamdb.insert_one(entry.model_dump())