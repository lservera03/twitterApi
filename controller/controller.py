import read_excel.excel as excel
import mongodb.mongo as mongo
import api_requests.tweets as tweets_api
import api_requests.replies as replies_api
import api_requests.users as users_api
from model.models import *


# Function that includes all the program sequence
def execute(check_excel: bool):
    # Check excel users
    if check_excel:
        check_users_excel()

    # Save all the users' tweets
    users = mongo.get_all_users()
    if users.count() != 0:
        for user in users:
            download_tweets(user)
            download_replies(user)

    # (Maybe) save all the quotes for every tweet

    # Log management in between


def check_users_excel():
    usernames = excel.get_usernames_from_excel()
    #  save all the users that are not already saved in mongodb
    for username in usernames:
        if mongo.check_user_exists_by_username(username) is False:
            user_id = users_api.get_user_id_by_username(username)
            mongo.save_user(User(username, user_id))


def download_tweets(user: User):
    last_tweet_id = mongo.get_last_tweet_by_user_id(user.twitter_id)
    tweets = tweets_api.get_user_tweets_by_user_id(user.twitter_id, last_tweet_id)

    if tweets is not None:
        mongo.save_user_tweets(tweets)


def download_replies(user: User):
    last_reply_id = mongo.get_last_reply_by_user_id(user.twitter_id)
    replies = replies_api.get_user_replies(user.twitter_id, last_reply_id)

    if replies is not None:
        mongo.save_user_replies(replies)
