import pymongo
import config
from model.models import *

db_path = config.mongodb_path
db_database = config.mongodb_database
db_user_collection = config.mongodb_user_collection

client = pymongo.MongoClient(db_path)


def save_user(user: User):
    db = client[db_database]
    collection = db[db_user_collection]

    inserted = collection.insert_one(user.__dict__)

    if inserted.inserted_id is not None:
        print("User " + user.username + " inserted successfully")
    else:
        print("User insertion failed")
