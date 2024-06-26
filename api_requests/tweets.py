import logging
from datetime import datetime
from time import sleep

import requests
import config
from model.models import Tweet, User

bearer_token = config.bearer_token
api_start_date = config.api_start_date

URL = "https://api.twitter.com/2/users"


def get_user_tweets_by_user_id(user: User, last_tweet_id):
    tweets = []
    pagination = None
    stop = False

    headers = {"Authorization": f"Bearer {bearer_token}"}

    params = {
        "start_time": api_start_date,
        "tweet.fields": "author_id,id,lang",
        "max_results": 100
    }

    if last_tweet_id is not None:  # If it is not the first time we request this user's tweets
        logging.info(
            "Requesting user tweets of user " + user.username + " with last tweet id query parameter: " + last_tweet_id)
        params["since_id"] = last_tweet_id

    execution_datetime = datetime.now().strftime("%d-%m-%Y")

    while stop is False:
        if pagination is not None:  # If it is not the first request
            logging.info("User tweets request with pagination")
            params["pagination_token"] = pagination
            sleep(60)  # 1min delay between requests needed to not exceed Twitter API max requests allowed per endpoint

        response = requests.get(url=URL + f"/{user.twitter_id}/tweets", headers=headers, params=params)
        data = response.json()

        # Check if it has found tweets
        if data["meta"]["result_count"] != 0:

            if response.status_code == 200:
                for tweet in data["data"]:
                    tweets.append(Tweet(tweet["id"], tweet["text"], user.username, tweet["lang"], "tweet",
                                        execution_datetime, "false"))

                if "next_token" in data["meta"]:  # Continue to send requests
                    pagination = data["meta"]["next_token"]
                else:
                    logging.info("Found " + str(tweets.__len__()) + " tweets for user " + user.username)
                    return tweets
            else:
                logging.info("User tweets API request error: " + str(data))
                return None
        else:
            logging.info("No tweets found for user: " + user.username)
            return None
