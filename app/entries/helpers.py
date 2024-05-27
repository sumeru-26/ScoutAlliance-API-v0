from typing import List

from pydantic import ValidationError,create_model
from fastapi import HTTPException

from app.models import Entry
from app.mongodb import entries_db
from app.schemas.helpers import get_schema
from app.alliance.helpers import get_access

cached_models = {}

def verify_entry(entry : Entry, team : int):
    if team not in cached_models.keys():
        cache_model(team)
    try:
        cached_models[team](**entry.dict()["data"])
    except ValidationError:
        return False
    return True

def add_entry(entry : List[Entry], team : int):
    db = entries_db[str(team)]
    re = [e.dict() for e in entry]
    db.insert_many(re)

def delete_entries(team: int, query: dict):
    entries_db[str(team)].delete_many(query)

def get_entries(team : int, query : list) -> dict:
    re = []
    for x in get_access(team):
        cursor = entries_db[str(x)].find({}, {"_id" : 0})
        re.extend([i for i in cursor])
    filtered = []
    for entry in re:
        for q in query:
            f, v = q
            if find_by_key(entry, f) != v:
                break
        else:
            filtered.append(entry)
    return {'entries' : filtered}

def filter_access(team : int, entries_list : list) -> bool:
    for x in entries_list:
        if x['metadata']['scouter']['team'] == team:
            return True
        if 'sharedWith' in x['metadata']:
            for sharedWithTeam in x['metadata']['sharedWith']:
                if sharedWithTeam == team:
                    return True
    return False


def find_by_key(x: dict, key: str):
    key = key.split('.')
    try:
        for k in key:
            x = x[k]
        return x
    except KeyError:
        raise HTTPException(422, detail="Invalid query")
    

def convert_type(entry):
    if isinstance(entry,dict):
        convert_schema(entry)
    if entry == 'int':
        return (int,...)
    elif entry == 'str':
        return (str,...)
    elif entry == 'bool':
        return (bool,...)
    else:
        return (type(entry),entry)    

def convert_schema(schema : dict) -> dict:
    new_schema = {}
    for k,v in schema.items():
        new_schema[k] = convert_type(v)
    return new_schema

def cache_model(team: int):
    schema = get_schema(team)
    del schema['team']
    cached_models[team] = create_model(f'{team}_data_model', **convert_schema(schema))