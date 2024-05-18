from mongodb import alliances_db

from pprint import pprint

# stores teams on alliance e.g. { "test-alliance": [254, 1678, 4414] }
alliance_cache = {}
# stores alliances that team is on e.g. { 2374: ["alliance1", "alliance2", "alliance3"] }
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
    pprint(alliance_cache)
    pprint(access_cache)

def update_access_locally(team: int, alliance: str, remove: bool = False):
    if team not in access_cache.keys():
        cache_access(team)
    alliance_cache[alliance].remove(team) if remove else alliance_cache[alliance].append(team)
    access_cache[team].remove(alliance) if remove else access_cache[team].append(alliance)
    pprint(alliance_cache)
    pprint(access_cache)

def add_access(team: int, alliance_name: str):
    alliances_db.update_one({"name": alliance_name},
                            {"$push": {
                                "teams": team
                            }})
    update_access_locally(team, alliance_name)
    

def remove_access(team: int, alliance_name: str):
    alliances_db.update_one({"name": alliance_name},
                            {"$pull": {
                                "teams": team
                            }})
    update_access_locally(team, alliance_name, remove=True)