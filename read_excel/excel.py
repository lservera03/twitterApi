import pandas as pd
import config

path = config.excel_file_path

username_column = config.excel_username_column


def get_usernames_from_excel():
    df = pd.read_excel(path)

    # Check if the usernames are with the @ at the beginning
    aux = []
    usernames = df[username_column]

    for username in usernames:
        if username[0] == "@":
            aux.append(username[1:])
        else:
            aux.append(username)

    return aux


def write_followers_to_excel(users_info: [{}], first_position: int):
    df = pd.read_excel(path)

    i = first_position
    for user in users_info:
        df["Followers"][i] = user["followers_count"]
        df["Tweet count"][i] = user["tweet_count"]
        i += 1

    df.to_excel(path)
