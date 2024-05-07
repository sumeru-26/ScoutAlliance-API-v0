from mongodb import alliances_db

access_cache = {}

def get_access(team: int):
    if team not in access_cache:
        cache_access(team)
    return access_cache[team]

def cache_access(team: int):
    data = alliances_db.find_one({"teams" : team},{"_id" : 0})
    if data is None:
        raise ValueError("Team does not exist")
    access_cache[team] = data["teams"]