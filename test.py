from pydantic import BaseModel,create_model # noqa: F401
from pprint import pprint

def convert_type(entry):
    if entry == 'int':
        return (int,...)
    elif entry == 'str':
        return (str,...)
    else:
        return (type(entry),entry)    

def convert_schema(schema : dict) -> dict:
    for k,v in schema.items():
        schema[k] = convert_type(v)
    #pprint(schema)
    return schema

counters_schema_input = {
    'id' : 2,
    'auto-scoring-amp-2024' : 0,
    'auto-scoring-speaker-2024' : 'int',
    'teleop-scoring-amp-2024' : 'asdf',
    'teleop-scoring-speaker-2024' : 'str',
}

d = convert_schema(counters_schema_input)

model = create_model('model',**d)
#pprint(model.model_json_schema())

test_entry = {
    'auto-scoring-speaker-2024' : 7,
    'teleop-scoring-speaker-2024' : 'qwer',
}
pprint(model.model_validate(test_entry))