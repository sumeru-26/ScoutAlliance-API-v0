from pydantic import BaseModel,create_model # noqa: F401
from pprint import pprint  # noqa: F401

tps_metadata_schema = {
    'id' : 0,
    'bot' : '',
    'event' : '',
    'match' : {
        'level' : '',
        'number' : 0,
        'set' : 0
    },
    'scouter' : {
        'name' : '',
        'team' : '',
        'app' : ''
    },
    'timestamp' : 0
}

tps_abilities_schema = {
    'id' : 1,
    'auto-center-line-pick-up' : False,
    'auto-leave-starting-zone' : False,
    'bricked' : False,
    'defense' : False,
    'ground-pick-up' : False,
    'teleop-spotlight-2024' : False,
    'teleop-stage-level-2024' : 0
}

tps_counters_schema = {
    'id' : 2,
    'auto-scoring-amp-2024' : 0,
    'auto-scoring-speaker-2024' : 0,
    'teleop-scoring-amp-2024' : 0,
    'teleop-scoring-amplified-speaker-2024' : 0,
    'teleop-scoring-speaker-2024' : 0,
    'teleop-scoring-trap-2024' : 0
}

tps_data_schema = {
    'id' : 3,
    'auto-scoring-2024' : [''],
    'notes' : '',
    'teleop-scoring-2024' : ['']
}

tps_ratings_schema = {
    'id' : 4,
    'defense-skill' : 0,
    'driver-skill' : 0,
    'intake-consistency' : 0,
    'speed' : 0,
    'stability' : 0
}

tps_timers_schema = {
    'id' : 5,
    'brick-time' : 0,
    'defense-time' : 0,
    'stage-time-2024' : 0
}

tps_schemas = [tps_metadata_schema,tps_abilities_schema,tps_counters_schema,tps_data_schema,tps_ratings_schema,tps_timers_schema]

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



converted_tps_schemas = [convert_schema(schema) for schema in tps_schemas]

metadata_schema = create_model('metadata_schema',**converted_tps_schemas[0])
abilities_schema = create_model('abilities_schema',**convert_schema(tps_abilities_schema))
counters_schema = create_model('counters_schema',**convert_schema(tps_counters_schema))
data_schema = create_model('data_schema',**convert_schema(tps_data_schema))
ratings_schema = create_model('ratings_schema',**convert_schema(tps_ratings_schema))
timers_schema = create_model('timers_schema',**convert_schema(tps_timers_schema))

entry = {
    'id' : 0,
    'bot' : '',
    'event' : '',
    'match' : {
        'level' : '',
        'number' : 0,
        'set' : 0
    },
    'scouter' : {
        'name' : '',
        'team' : '',
        'app' : ''
    },
    'timestamp' : 0
}

class Model(BaseModel):
    metadata : metadata_schema
    abilities : abilities_schema
    counters : counters_schema
    data : data_schema
    ratings : ratings_schema
    timers : timers_schema

#pprint(Model.model_json_schema())


entry = {
        'metadata' : tps_metadata_schema,
        'abilities' : tps_abilities_schema,
        'counters' : tps_counters_schema,
        'data' : tps_data_schema,
        'ratings' : tps_ratings_schema,
        'timers' : tps_timers_schema
}

print(Model.model_validate(entry))