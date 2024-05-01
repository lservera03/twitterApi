import pandas as pd
import config

path = config.excel_file_path

USERNAME_COLUMN = "Username"


def get_usernames_from_excel():
    df = pd.read_excel(path)

    # TODO: Check if the usernames are with the @ at the beginning
    return df[USERNAME_COLUMN]
