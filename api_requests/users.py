import logging

import requests
import config
from model.models import User

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


def get_users_id_by_username_list(usernames: []) -> [User]:
    aux = ""
    length = len(usernames)
    for username in usernames:
        aux = aux + username
        if username != usernames[length - 1]:
            aux = aux + ","

    headers = {"Authorization": f"Bearer {bearer_token}"}
    params = {"usernames": aux}

    response = requests.get(url=URL + "/by", headers=headers, params=params)
    data = response.json()

    user_list = []

    if response.status_code == 200:
        logging.info("Received users in get ID request")
        for user in data["data"]:
            user_list.append(User(user["username"], user["name"], user["id"]))

        return user_list
    else:
        logging.info("Get users id API response error: " + str(response))
        return None
