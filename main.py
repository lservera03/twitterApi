import argparse
import logging
from datetime import datetime

import api_requests.users
from read_excel import excel
from api_requests import *

import controller.controller as controller


# TODO: improve/implement error handling

def main():
    check_excel = args.check_excel
    logging.info("Check excel set to: {}".format(check_excel))
    controller.execute(check_excel)


if __name__ == "__main__":
    # Needed to receive arguments when executing the script
    parser = argparse.ArgumentParser()
    parser.add_argument("--check_excel", required=True, type=bool)
    args = parser.parse_args()

    # Needed to keep track of the execution logs
    execution_datetime = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    # Create log file
    file = open("logs/" + execution_datetime + ".log", 'a')
    file.close()

    logging.basicConfig(level=logging.DEBUG, filename="logs/" + execution_datetime + ".log", filemode="a")

    main()
