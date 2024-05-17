from mongodb import alliances_db

alliance_cache = {}
access_cache = {}

def get_access(team: int):
    if team not in access_cache:
        cache_access(team)
    teams = []
    for alliance in access_cache[team]:
        teams.extend(alliance_cache[alliance])
    return teams

def cache_access(team: int):
    data = alliances_db.find({"teams" : team}, {"_id" : 0})
    if data is None:
        raise ValueError("Team does not exist")
    if team not in access_cache.keys():
        access_cache[team] = []
    for x in data:
        alliance_cache[x["name"]] = x["teams"]
        access_cache[team].append(x["name"])

def add_access(team: int, alliance_name: str):
    alliances_db.update_one({"name": alliance_name},
                            {"$push": {
                                "teams": team
                            }})
    cache_access(team)