import logging

import pandas as pd
from openpyxl.reader.excel import load_workbook
from openpyxl.worksheet.datavalidation import DataValidation

import config
from model.models import Tweet

path = config.excel_file_path
tweets_path = config.tweet_excel_file_path

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


def save_tweets_to_excel_by_date(tweets: [Tweet]):
    id_list = []
    text_list = []

    for tweet in tweets:
        id_list.append(tweet.tweet_id)
        text_list.append(tweet.text)

    # TODO: fix some issues with categories and labels in columns

    df = pd.DataFrame({"Tweet id": id_list, "Tweet": text_list})

    df.to_excel(tweets_path)

    # Test of creating dropdown list
    wb = load_workbook(filename=tweets_path)
    ws = wb.active

    dv = DataValidation(type="list", formula1='"Prueba 1, Prueba 2"', allow_blank=False)

    dv.error = 'Your entry is not in the list'
    dv.errorTitle = 'Invalid Entry'

    dv.prompt = 'Please select from the list'
    dv.promptTitle = 'List Selection'

    aux = "D2:D" + str(len(tweets))

    dv.showInputMessage = True
    dv.showErrorMessage = True

    dv.add(aux)

    ws.add_data_validation(dv)

    wb.save(tweets_path)

    logging.info(f"Tweets saved to {tweets_path}")
