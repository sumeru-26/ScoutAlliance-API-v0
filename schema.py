from copy import deepcopy

from pydantic import BaseModel
from pymongo.errors import OperationFailure

from mongodb import schema_db

schema_types = ['metadata','abilities','counters','data','ratings','timers']
schema_type_to_id = {
    'metadata' : 0,
    'abilities' : 1,
    'counters' : 2,
    'data' : 3,
    'ratings' : 4,
    'timers' : 5
}

class Schema(BaseModel):
    schema: dict

universal_metadata_schema = {
    'schema_type' : 'metadata',
    'bot' : 'string',
    'event' : 'string',
    'match' : {
        'level' : '',
        'number' : 0,
        'set' : 0
    },
    'scouter' : {
        'name' : '',
        'team' : 'int',
        'app' : ''
    },
    'timestamp' : 0
}

universal_abilities_schema = {
    'schema_type' : 'abilities',
    'type' : 'str', # "match" or "pit"
    'auto-center-line-pick-up' : False,
    'auto-leave-starting-zone' : False,
    'bricked' : False, # bricked = is robot disabled or unable to play
    'defense' : False,
    'ground-intake' : False,
    'spotlight' : False,
    'stage-climb-level' : 0 # 0 = none, 1  =parked, 2 = onstage, 3 = onstage + 1 harmony, 4 = onstage + 2 harmonies
}

universal_counters_schema = {
    'schema_type' : 'counters',
    'auto-amp-scored' : 0,
    'auto-speaker-scored' : 0,
    'teleop-amp-scored' : 0,
    'teleop-amplified-speaker-scored' : 0,
    'teleop-speaker-scored' : 0,
    'teleop-trap-scored' : 0
}

universal_data_schema = {
    'schema_type' : 'data',
    'auto-scoring' : [''], # as = note scored in amp, am = note missed in amp, ss = note score in non-amplified speaker, sm = note missed in speakers
    'teleop-scoring' : [''], # as = note scored in amp, am = note missed in amp, ss = note score in non-amplified speaker, sm = note missed in speakers
    'failures' : '', # any mechanical or software breaks/failures during the match
    'notes' : '' # any text about the robot

}

# all ratings on a scale of 1-10
universal_ratings_schema = {
    'schema_type' : 'ratings',
    'defense-skill' : 0,
    'driver-skill' : 0,
    'intake-consistency' : 0,
    'speed' : 0,
    'stability' : 0
}

universal_timers_schema = {
    'schema_type' : 'timers',
    'bricked-time' : 0,
    'stage-time' : 0, # time spent between entering stage zone and robot reaching onstage position
    'amp-stamps' : [], # time stamp of amp attempt (score or miss)
    'speaker-stamps' : [], # time stamp of amp attempt (score or miss)
    'amplified-speaker-stamps' : [] # time stamp of amp attempt (score or miss)
}

universal_schemas = [universal_metadata_schema,universal_abilities_schema,universal_counters_schema,universal_data_schema,universal_ratings_schema,universal_timers_schema]

def add_team(team : int):
    if schema_db.metadata.find_one({"team" : team}) is not None:
        raise ValueError("Team already exists")
    for schema in universal_schemas:
        schema_entry = deepcopy(schema)
        schema_entry['team'] = team
        schema_db[schema_entry.get('schema_type')].insert_one(schema_entry)

def update_schema(schema: dict, schema_type: str, team : int):
    if schema_type not in schema_types:
        raise ValueError("Invalid schema type")
    if schema_db[schema_type].find_one({"team" : team}) is None:
        raise ValueError("Team does not exist")
    acknowledged = schema_db[schema_type].replace_one({"team"},schema)
    if not acknowledged:
        raise OperationFailure("failed to replace document")

def get_schema(team : int, type : str):
    if type not in schema_types:
        raise ValueError("Invalid schema type")
    return schema_db[type].find_one({"team" : team},{"_id" : 0})