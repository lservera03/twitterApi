import logging

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
        logging.info(user.username + " inserted into database successfully")
    else:
        logging.info(user.username + " insertion into database failed")


def save_users_list(users_list: [User]):
    db = client[db_database]
    collection = db[db_user_collection]

    list_insert = []
    for user in users_list:
        list_insert.append(user.__dict__)

    inserted = collection.insert_many(list_insert)

    if inserted.acknowledged is True:
        logging.info("Users inserted into database successfully")
    else:
        logging.info("Users insertion into database failed")


def check_user_exists_by_username(username) -> bool:
    db = client[db_database]
    collection = db[db_user_collection]

    users = collection.find({"username": username})

    try:
        user = users[0]
        return True
    except IndexError:
        return False


def get_number_of_users() -> int:
    db = client[db_database]
    collection = db[db_user_collection]

    return collection.count_documents({})


def get_all_users() -> [User]:
    db = client[db_database]
    collection = db[db_user_collection]

    users = collection.find()

    users_list = []

    for result in users:
        users_list.append(User(result["username"], result["name"], result["twitter_id"]))

    logging.info("Requested all the users from the database, found: " + str(users_list.__len__()))

    return users_list


def save_user_tweets(tweets: [Tweet], user: User):
    db = client[db_database]
    collection = db[db_tweet_collection]

    # convert Tweet list to list of tweet dictionaries
    aux = []
    for tweet in tweets:
        aux.append(tweet.__dict__)

    inserted = collection.insert_many(aux)

    if inserted.acknowledged is True:
        logging.info("Tweets of user " + user.username + " inserted into database successfully")
    else:
        logging.info("Tweets of user " + user.username + " insertion into database failed")


def save_user_replies(tweets: [Reply], user: User):
    db = client[db_database]
    collection = db[db_tweet_collection]

    # convert Tweet list to list of tweet dictionaries
    aux = []
    for tweet in tweets:
        aux.append(tweet.__dict__)

    inserted = collection.insert_many(aux)

    if inserted.acknowledged is True:
        logging.info("Replies to user " + user.username + " inserted into database successfully")
    else:
        logging.info("Replies to user " + user.username + " insertion into database failed")


def get_last_tweet_by_user(user: User):
    db = client[db_database]
    collection = db[db_tweet_collection]

    query = {"$and": [{"author": user.username}, {"type": "tweet"}]}

    tweets = collection.find(query).sort("tweet_id", pymongo.DESCENDING).limit(1)

    # Try and except to catch when there are no results of the query
    try:
        logging.info("Found last tweet of user " + user.username + " with tweet id: " + str(tweets[0]["tweet_id"]))
        return Tweet(tweets[0]["tweet_id"], tweets[0]["text"], tweets[0]["author"], tweets[0]["lang"],
                     tweets[0]["type"], tweets[0]["save_date"], tweets[0]["labeled"])
    except IndexError:
        logging.info("No last tweet found for user " + user.username)
        return None


def get_last_reply_by_user(user: User):
    db = client[db_database]
    collection = db[db_tweet_collection]

    query = {"$and": [{"reply_to": user.username}, {"type": "reply"}]}

    replies = collection.find(query).sort("tweet_id", pymongo.DESCENDING).limit(1)

    # Try and except to catch when there are no results of the query
    try:
        logging.info("Found last reply for user " + user.username + " with tweet id: " + str(replies[0]["tweet_id"]))
        return Reply(replies[0]["tweet_id"], replies[0]["text"], replies[0]["author"], replies[0]["lang"],
                     replies[0]["type"], replies[0]["reply_to"], replies[0]["conversation_id"], replies[0]["save_date"],
                     replies[0]["labeled"])
    except IndexError:
        logging.info("No last reply found for user " + user.username)
        return None


def get_all_tweets_by_save_date(date) -> [Tweet]:
    db = client[db_database]
    collection = db[db_tweet_collection]

    query = {"save_date": date}

    tweets = collection.find(query)

    tweets_list = []

    for result in tweets:
        if result["type"] == "tweet":
            tweets_list.append(
                Tweet(result["tweet_id"], result["text"], result["author"], result["lang"], result["type"],
                      result["save_date"], result["labeled"]))
        else:
            tweets_list.append(
                Reply(result["tweet_id"], result["text"], result["author"], result["lang"], result["type"],
                      result["reply_to"], result["conversation_id"], result["save_date"], result["labeled"]))

    return tweets_list


def get_all_tweets_not_labeled_by_user(user) -> [Tweet]:
    db = client[db_database]
    collection = db[db_tweet_collection]

    query = {"$and": [{"author": user}, {"labeled": "false"}, {"type": "tweet"}]}

    tweets = collection.find(query)

    tweets_list = []

    for result in tweets:
        tweets_list.append(Tweet(result["tweet_id"], result["text"], result["author"], result["lang"], result["type"],
                                 result["save_date"], result["labeled"]))

    return tweets_list


def get_all_replies_not_labeled_by_user(user) -> [Tweet]:
    db = client[db_database]
    collection = db[db_tweet_collection]

    query = {"$and": [{"reply_to": user}, {"labeled": "false"}, {"type": "reply"}]}

    tweets = collection.find(query)

    tweets_list = []

    for result in tweets:
        tweets_list.append(Reply(result["tweet_id"], result["text"], result["author"], result["lang"], result["type"],
                                 result["reply_to"], result["conversation_id"], result["save_date"], result["labeled"]))

    return tweets_list


def set_labeled_state_true_for_tweets(tweets: [Tweet]):
    db = client[db_database]
    collection = db[db_tweet_collection]

    for tweet in tweets:
        myquery = {"tweet_id": tweet.tweet_id}
        newvalues = {"$set": {"labeled": "true"}}
        collection.update_one(myquery, newvalues)

    logging.info("Set labeled state for tweets")


# TODO: create function to retrieve a number of tweets and responses to create excel

def remove_duplicated_tweets():
    db = client[db_database]
    collection = db[db_tweet_collection]

    tweets = collection.find()

    ids = []

    for tweet in tweets:
        ids.append(tweet["tweet_id"])

    print("Before: " + str(ids.__len__()))

    unique_list = []
    duplicate_list = []

    for i in ids:
        if i not in unique_list:
            unique_list.append(i)
        elif i not in duplicate_list:
            duplicate_list.append(i)

    print("After: " + str(unique_list.__len__()))

    print(duplicate_list)

    for duplicate in duplicate_list:
        collection.delete_one({"tweet_id": duplicate})

    logging.info(str(duplicate_list.__len__()) + " duplicated tweets removed")
