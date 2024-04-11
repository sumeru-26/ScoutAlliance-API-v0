from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends

from mongodb import client
from auth import get_user
from entries.helpers import cache_model

from entries.router import entryRouter
from schemas.router import schemaRouter

pre_cached = []

# things to run when starting up
@asynccontextmanager
async def lifespan(app : FastAPI):
    try:
        client.admin.command('ping')
    except Exception as e:
        raise e
    for team in pre_cached:
        cache_model(team)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(
    entryRouter,
    prefix="/entries",
    dependencies=[Depends(get_user)]
    )

app.include_router(
    schemaRouter,
    prefix="/schemas"
    )

# nice little home page :)
@app.get("/")
async def root():
    return "Welcome to OpenScouting! This API is created by Sumeru Gowda of 2374 Jesuit Robotics."