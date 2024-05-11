import logging
from time import sleep

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
    if len(users) != 0:
        for user in users:
            download_tweets(user)
            download_replies(user)
            sleep(60)  # 1min delay between requests needed to not exceed Twitter API max requests allowed per endpoint


def check_users_excel():
    stop = False
    start = 0
    end = 99
    aux_usernames = []

    usernames = excel.get_usernames_from_excel()

    # save all the users that are not already saved in mongodb
    for username in usernames:
        if mongo.check_user_exists_by_username(username) is False:
            aux_usernames.append(username)

    while stop is False:
        aux_list = aux_usernames[start:end]
        if len(aux_list) != 0:
            users = users_api.get_users_id_by_username_list(aux_list)
            mongo.save_users_list(users)
            start = end
            end += 100
        else:
            stop = True


def download_tweets(user: User):
    logging.info("Downloading tweets from " + user.username)
    last_tweet = mongo.get_last_tweet_by_user(user.twitter_id)

    if last_tweet is None:
        last_tweet_id = None
    else:
        last_tweet_id = last_tweet.tweet_id

    tweets = tweets_api.get_user_tweets_by_user_id(user, last_tweet_id)

    if tweets is not None:
        mongo.save_user_tweets(tweets, user)


def download_replies(user: User):
    logging.info("Downloading replies from " + user.username)
    last_reply = mongo.get_last_reply_by_user(user.twitter_id)

    if last_reply is None:
        last_reply_id = None
    else:
        last_reply_id = last_reply.tweet_id

    replies = replies_api.get_user_replies(user.twitter_id, last_reply_id)

    if replies is not None:
        mongo.save_user_replies(replies)
