from typing import Dict

from pymongo import ReturnDocument
from fastapi import HTTPException

from mongodb import data_schema_db
#from entries.helpers import cache_model

def add_team(team: int):
    if data_schema_db.find_one({'team': team}) is not None:
        raise HTTPException(422, "Team already exists")
    data_schema_db.insert_one({"team": team})
    
def update_schema(schema: Dict, team: int):
    schema["team"] = team
    if data_schema_db.find_one_and_replace({"team": team}, schema, return_document=ReturnDocument.BEFORE) is None:
        raise HTTPException(422, "Team does not exist")
    #cache_model(team)

def get_schema(team : int) -> dict:
    data = data_schema_db.find_one({"team" : team},{"_id" : 0})
    if data is None:
        raise ValueError("Team does not exist")
    return data