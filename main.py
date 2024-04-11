from contextlib import asynccontextmanager

from fastapi import FastAPI

#from entries.helpers import cache_model
#from schema import add_team,update_schema
from mongodb import client
from entries.helpers import cache_model

from entries.router import entryRouter
from schemas.router import schemaRouter

app = FastAPI()
pre_cached = []

# things to run when starting up
@asynccontextmanager
async def lifespan(app : FastAPI):
    try:
        client.admin.command('ping')
    except Exception as e:
        print(e)
    for team in pre_cached:
        cache_model(team)

app.include_router(
    entryRouter,
    prefix="/entries"
    )

app.include_router(
    schemaRouter,
    prefix="/schemas"
    )

# nice little home page :)
@app.get("/")
async def root():
    return "Welcome to OpenScouting! This API is created by Sumeru Gowda of 2374 Jesuit Robotics."