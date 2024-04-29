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


def get_last_tweet_by_user_id(user_id):
    db = client[db_database]
    collection = db[db_tweet_collection]

    query = {"$and": [{"author_id": user_id}, {"type": "tweet"}]}

    tweets = collection.find(query).sort("tweet_id", pymongo.DESCENDING).limit(1)

    if tweets.alive is True:  # If there are results
        return Tweet(tweets[0]["tweet_id"], tweets[0]["text"], tweets[0]["author_id"], tweets[0]["lang"],
                     tweets[0]["type"])
    else:
        return None


def get_last_reply_by_user_id(user_id):
    db = client[db_database]
    collection = db[db_tweet_collection]

    query = {"$and": [{"reply_to": user_id}, {"type": "reply"}]}

    replies = collection.find(query).sort("tweet_id", pymongo.DESCENDING).limit(1)

    if replies.alive is True:  # If there are results
        return Reply(replies[0]["tweet_id"], replies[0]["text"], replies[0]["author_id"], replies[0]["lang"],
                     replies[0]["type"], replies[0]["reply_to"])
    else:
        return None
