from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from user import user,password

uri = f"mongodb+srv://{user}:{password}@openscouting.xsr04sk.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))

schema_db = client.schemas
entries_db = client.entries