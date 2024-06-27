from contextlib import asynccontextmanager

from mangum import Mangum

from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse

from app.mongodb import client, rate_db, RATE_PER_DAY
from app.auth import get_user
from app.entries.helpers import cache_model

from app.entries.router import entryRouter
from app.schemas.router import schemaRouter
from app.alliance.router import allianceRouter

pre_cached = [9999]

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
handler = Mangum(app)

app.include_router(
    entryRouter,
    prefix="/entries",
    dependencies=[Depends(get_user)]
    )

app.include_router(
    schemaRouter,
    prefix="/schema",
    dependencies=[Depends(get_user)]
    )

app.include_router(
    allianceRouter,
    prefix="/alliance",
    dependencies=[Depends(get_user)]
    )

# rate limiting
@app.middleware("http")
async def rate_limit(request: Request, call_next):
    try:
        user = get_user(request.headers["X-OS-Auth-Key"])
    except KeyError:
        return JSONResponse(status_code=401, content={"detail": "Missing API Key"})
    rate_info = rate_db.find_one({"user": user})
    if rate_info is None:
        rate_db.insert_one({"user": user, "requests": 1})
        rate_count = 1
    else:
        rate_db.update_one({"user": user}, {"$inc": {"requests": 1}})
        rate_count = rate_info["requests"] + 1
    if user != 9999 and rate_count > RATE_PER_DAY:
        return JSONResponse(status_code=429, content={"detail": "Rate Limit Exceeded"})

    response = await call_next(request)
    return response

# nice little home page :)
@app.get("/")
async def root(team_number: int = Depends(get_user)):
    return {
        "detail": "Welcome to the ScoutAlliance API created by ScoutAlliance",
        "team": team_number,
        }