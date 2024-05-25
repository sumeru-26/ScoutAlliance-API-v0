import os
from dotenv import load_dotenv

from pymongo.mongo_client import MongoClient

if os.path.exists(".env"):
    load_dotenv(override=True)
user = os.environ.get("USER")
password = os.environ.get("PASSWORD")

uri = f"mongodb+srv://{user}:{password}@openscouting.xsr04sk.mongodb.net/?retryWrites=true&w=majority&appName=OpenScouting"
client = MongoClient(uri)

schema_db = client.schemas
entries_db = client.entries
match_db = client.entries.match
keys_db = client.security.keys
alliances_db = client.security.alliances
rate_db = client.security.rate
data_schema_db = schema_db['data']

RATE_PER_DAY = int(os.environ.get("RATE_PER_DAY"))