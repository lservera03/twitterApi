import argparse

import api_requests.users as users_api
import api_requests.tweets as tweets_api
import api_requests.replies as replies_api
import read_excel.excel as excel
import mongodb.mongo as mongo
import controller.controller as controller
from model.models import *


# TODO: create log management

def main():
    check_excel = args.check_excel
    controller.execute(check_excel)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check_excel", required=True, type=bool)
    args = parser.parse_args()
    main()
