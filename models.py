from pydantic import BaseModel

class MetaData(BaseModel):
    bot: int
    match: int

class Entry(BaseModel):
    metadata: MetaData
    data: dict