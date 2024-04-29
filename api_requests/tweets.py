from time import sleep

import requests
import config
from model.models import Tweet

bearer_token = config.bearer_token

URL = "https://api.twitter.com/2/users"


def get_user_tweets_by_user_id(user_id):
    tweets = []
    pagination = None
    stop = False

    headers = {"Authorization": f"Bearer {bearer_token}"}

    params = {
        "start_time": "2024-04-26T00:00:00Z",  # TODO: manage better the date (not hardcoded)
        "tweet.fields": "author_id,id,lang"
    }

    while stop is False:
        if pagination is not None:  # If it is not the first request
            params["pagination_token"] = pagination
            sleep(60)  # 1min delay between requests needed to not exceed Twitter API max requests allowed per endpoint

        response = requests.get(url=URL + f"/{user_id}/tweets", headers=headers, params=params)
        data = response.json()

        # TODO: manage when there are 0 results (meta object)

        if response.status_code == 200:
            for tweet in data["data"]:
                tweets.append(Tweet(tweet["id"], tweet["text"], tweet["author_id"], tweet["lang"]))

            if "next_token" in data["meta"]:  # Continue to send requests
                pagination = data["meta"]["next_token"]
            else:
                return tweets
        else:
            print(response)
            print(response.status_code)
            return None
