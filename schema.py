from pydantic import BaseModel

from mongodb import client

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

'''
By default, schemas will be set to align with The Purple Standard.
More info about this standard can be found here: https://thepurplewarehouse.com/tps-press-release.pdf
The default schemas will be based off of the info found here: https://github.com/HarkerRobo/the-purple-standard/blob/main/reference.md
'''

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

def add_team(team : str):
    schemadb = client['schemas']
    if team in schemadb.list_collection_names():
        raise ValueError("Team already exists")
    teamdb = schemadb[team]
    teamdb.insert_many(tps_schemas)
    

def update_schema(schema: dict, schema_type: str, team : str):
    if schema_type not in schema_types:
        raise ValueError("Invalid schema type")
    schemadb = client['schemas']
    if team not in schemadb.list_collection_names():
        raise ValueError("Team does not exist")
    id = schema_type_to_id[schema_type]
    teamdb = schemadb[team]
    teamdb.replace_one({'_id':id},schema)

    