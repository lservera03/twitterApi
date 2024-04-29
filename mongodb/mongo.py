import pymongo
import config
from model.models import *

db_path = config.mongodb_path
db_database = config.mongodb_database
db_user_collection = config.mongodb_user_collection
db_tweet_collection = config.mongodb_tweet_collection

client = pymongo.MongoClient(db_path)


def save_user(user: User):
    db = client[db_database]
    collection = db[db_user_collection]

    inserted = collection.insert_one(user.__dict__)

    if inserted.inserted_id is not None:
        print("User " + user.username + " inserted successfully")
    else:
        print("User insertion failed")


def save_user_tweets(tweets: [Tweet]):
    db = client[db_database]
    collection = db[db_tweet_collection]

    # convert Tweet list to list of tweet dictionaries
    aux = []
    for tweet in tweets:
        aux.append(tweet.__dict__)

    inserted = collection.insert_many(aux)

    if inserted.acknowledged is True:
        print("Tweets of user " + tweets[0].author_id + " inserted successfully")
    else:
        print("Tweets insertion failed")


def save_user_replies(tweets: [Reply]):
    db = client[db_database]
    collection = db[db_tweet_collection]

    # convert Tweet list to list of tweet dictionaries
    aux = []
    for tweet in tweets:
        aux.append(tweet.__dict__)

    inserted = collection.insert_many(aux)

    if inserted.acknowledged is True:
        print("Replies to user " + tweets[0].reply_to + " inserted successfully")
    else:
        print("Replies insertion failed")
