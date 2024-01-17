from fastapi import FastAPI

from team_db import team_db

app = FastAPI()


@app.get("/")
async def root():
    return "Welcome to OpenScouting! This API is created by Sumeru Gowda of 2374 Jesuit Robotics."

#access example team data
@app.get("/teams/{team_number}")
async def team(team_number: int):
    return team_db[team_number]

