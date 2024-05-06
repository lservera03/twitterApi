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


def get_user_id_and_followers_by_username_list(usernames: []) -> [{}]:
    aux = ""
    length = len(usernames)
    for username in usernames:
        aux = aux + username
        if username != usernames[length - 1]:
            aux = aux + ","

    headers = {"Authorization": f"Bearer {bearer_token}"}
    params = {"user.fields": "public_metrics", "usernames": aux}

    response = requests.get(url=URL + "/by", headers=headers, params=params)
    data = response.json()

    user_info_list = []

    if response.status_code == 200:
        # logging.info(username + " ID received: " + data["data"]["id"])
        for user in data["data"]:
            user_info_list.append({"followers_count": user["public_metrics"]["followers_count"],
                                   "tweet_count": user["public_metrics"]["tweet_count"]})

        return user_info_list
    else:
        logging.info("Get user id API response error: " + str(response))
        return None
