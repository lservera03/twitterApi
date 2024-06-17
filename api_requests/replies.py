import logging
from datetime import datetime
from time import sleep

import requests
import config
from model.models import *

bearer_token = config.bearer_token
api_start_date = config.api_start_date

URL = "https://api.twitter.com/2/users"


def get_user_replies(user: User, last_reply_id):
    tweets = []
    pagination = None
    stop = False

    headers = {"Authorization": f"Bearer {bearer_token}"}

    params = {
        "start_time": api_start_date,
        "tweet.fields": "author_id,id,lang,conversation_id",
        "max_results": 100
    }

    if last_reply_id is not None:  # If it is not the first time we request this user's replies
        logging.info(
            "Requesting user replies of user " + user.username + " with last reply id query parameter: " + last_reply_id)
        params["since_id"] = last_reply_id

    execution_datetime = datetime.now().strftime("%d-%m-%Y")

    while stop is False:
        if pagination is not None:  # If it is not the first request
            logging.info("User replies request with pagination")
            params["pagination_token"] = pagination
            sleep(60)  # 1min delay between requests needed to not exceed Twitter API max requests allowed per endpoint

        response = requests.get(url=URL + f"/{user.twitter_id}/mentions", headers=headers, params=params)
        data = response.json()

        # Check if it has found replies
        if data["meta"]["result_count"] != 0:

            if response.status_code == 200:
                for tweet in data["data"]:
                    tweets.append(
                        Reply(tweet["id"], tweet["text"], tweet["author_id"], tweet["lang"], "reply", user.username,
                              tweet["conversation_id"], execution_datetime, "false"))

                if "next_token" in data["meta"]:  # Continue to send requests
                    pagination = data["meta"]["next_token"]
                else:
                    logging.info("Found " + str(tweets.__len__()) + " replies for user " + user.username)
                    return tweets
            else:
                logging.info("User replies API request error: " + str(data))
                return None
        else:
            logging.info("No replies found for user: " + user.username)
            return None
