from typing import Dict

from pymongo import ReturnDocument
from pymongo.errors import OperationFailure
from fastapi import HTTPException

from mongodb import schema_db, data_schema_db


# def add_team(team : int) -> None:
#     if schema_db.metadata.find_one({"team" : team}) is not None:
#         raise ValueError("Team already exists")
#     for schema in universal_schemas:
#         schema_entry = deepcopy(schema)
#         schema_entry['team'] = team
#         schema_db[schema_entry.get('schema_type')].insert_one(schema_entry)

def add_team_new(team: int):
    if data_schema_db.find_one({'team': team}) is not None:
        raise HTTPException(422, "Team already exists")
    data_schema_db.insert_one({"team": team})

# def update_schema(schema: dict, schema_type: str, team : int) -> None:
#     if schema_type not in schema_types:
#         raise ValueError("Invalid schema type")
#     if schema_db[schema_type].find_one({"team" : team}) is None:
#         raise ValueError("Team does not exist")
#     acknowledged = schema_db[schema_type].replace_one({"team"},schema)
#     if not acknowledged:
#         raise OperationFailure("failed to replace document")
    
def update_schema_new(schema: Dict, team: int):
    schema["team"] = team
    if data_schema_db.find_one_and_replace({"team": team}, schema, return_document=ReturnDocument.BEFORE) is None:
        raise HTTPException(422, "Team does not exist") 

def get_schema(team : int, type : str) -> dict:
    data = data_schema_db.find_one({"team" : team},{"_id" : 0})
    if data is None:
        raise ValueError("Team does not exist")
    return data