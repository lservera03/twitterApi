import argparse
import logging
from datetime import datetime

import controller.controller as controller


# TODO: improve/implement error handling
# TODO: maybe send get user id request with a list (10 -> 100)

def main():
    check_excel = args.check_excel
    logging.info("Check excel set to: " + check_excel)
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
