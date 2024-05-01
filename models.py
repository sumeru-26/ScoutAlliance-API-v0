from typing import List

from pydantic import BaseModel

# class Entry(BaseModel):
#     metadata : dict | None = None
#     abilities : dict | None = None
#     counters : dict | None = None
#     data : dict | None = None
#     ratings : dict | None = None
#     timers : dict | None = None

class MetaData(BaseModel):
    bot: int
    match: int

class Entry(BaseModel):
    metadata: MetaData
    data: dict

class Query(BaseModel):
    query : dict

class Schema(BaseModel):
    schema: dict