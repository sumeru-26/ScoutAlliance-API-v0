from typing import List,Dict

from pydantic import BaseModel,ValidationError,create_model
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
    if team not in cached_models.keys():
        cache_model(team)
    try:
        cached_models[team](**entry.model_dump())
        return True
    except ValidationError:
        return False

def add_entry(entry : Entry, team : int):   
    teamdb = client['entries'][str(team)]
    teamdb.insert_one(entry.model_dump())

def add_many_entries(entries : Many_Entries, team : int):
    teamdb = client['entries'][str(team)]
    uploadable_data = jsonable_encoder(entries)
    teamdb.insert_many(uploadable_data['entries'])

def delete_entries(team : int, query : dict):
    teamdb = client['entries'][str(team)]
    teamdb.delete_many(query)

def get_entries(team : int, query : dict) -> dict:
    teamdb = client['entries'][str(team)]
    cursor = teamdb.find(query)
    re = [x for x in cursor]
    for x in re:
        del x['_id']
    return {'entries' : re}

def convert_type(entry):
    if isinstance(entry,dict):
        convert_schema(entry)
    if entry == 'int':
        return (int,...)
    elif entry == 'str':
        return (str,...)
    else:
        return (type(entry),entry)    

def convert_schema(schema : dict) -> dict:
    new_schema = {}
    for k,v in schema.items():
        new_schema[k] = convert_type(v)
    return new_schema

def cache_model(team : int):
    teamdb = client['schemas'][str(team)]
    schema_types = ['metadata','abilities','counters','data','ratings','timers']
    models : Dict[str,BaseModel] = {}
    for type in schema_types:
        schema = teamdb.find_one({"type" : f"{type}"})
        del schema['_id']
        models[type] = create_model(f'{type}_model',**convert_schema(schema))
    
    class Model(BaseModel):
        metadata : models['metadata']  # type: ignore # noqa: F821
        abilities : models['abilities']  # type: ignore # noqa: F821
        counters : models['counters']  # type: ignore # noqa: F821
        data : models['data']  # type: ignore # noqa: F821
        ratings : models['ratings']  # type: ignore # noqa: F821
        timers : models['timers']  # type: ignore # noqa: F821

    cached_models[team] = Model