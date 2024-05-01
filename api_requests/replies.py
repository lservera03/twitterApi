from time import sleep

import requests
import config
from model.models import *

bearer_token = config.bearer_token

URL = "https://api.twitter.com/2/users"


def get_user_replies(user_id, last_reply_id):
    tweets = []
    pagination = None
    stop = False

    headers = {"Authorization": f"Bearer {bearer_token}"}

    params = {
        "start_time": "2024-04-29T00:00:00Z",  # TODO: manage better the date (not hardcoded)
        "tweet.fields": "author_id,id,lang"
    }

    if last_reply_id is not None:  # If it is not the first time we request this user's replies
        params["since_id"] = last_reply_id

    while stop is False:
        if pagination is not None:  # If it is not the first request
            params["pagination_token"] = pagination
            sleep(60)  # 1min delay between requests needed to not exceed Twitter API max requests allowed per endpoint

        response = requests.get(url=URL + f"/{user_id}/mentions", headers=headers, params=params)
        data = response.json()

        # Check if it has found replies
        if data["meta"]["result_count"] != 0:

            if response.status_code == 200:
                for tweet in data["data"]:
                    tweets.append(
                        Reply(tweet["id"], tweet["text"], tweet["author_id"], tweet["lang"], "reply", user_id))

                if "next_token" in data["meta"]:  # Continue to send requests
                    pagination = data["meta"]["next_token"]
                else:
                    return tweets
            else:
                print(response)
                print(response.status_code)
                return None
        else:
            print("No replies found")
            return None
