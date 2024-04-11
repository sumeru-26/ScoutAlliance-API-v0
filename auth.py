from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

from mongodb import keys_db

cached_keys = {}
api_key_header = APIKeyHeader(name="X-OS-Auth-Key")

def get_user(api_key_header: str = Security(api_key_header)):
    if api_key_header not in cached_keys.keys():
        re = keys_db.find_one({"key": api_key_header}, {"_id": 0})
        if not re:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing or invalid API Key"
            )
        cached_keys[re['key']] = re['team']
    return cached_keys[api_key_header]