import logging

import requests
import config

bearer_token = config.bearer_token

URL = "https://api.twitter.com/2/users"


def get_user_id_by_username(username):
    headers = {"Authorization": f"Bearer {bearer_token}"}

    response = requests.get(url=URL + f"/by/username/{username}", headers=headers)
    data = response.json()

    if response.status_code == 200:
        logging.info(username + " ID received: " + data["data"]["id"])
        return data["data"]["id"]
    else:
        logging.info("Get user id API response error: " + str(response))
        return None
