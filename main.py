import argparse
import logging
from datetime import datetime
import platform
import config

import controller.controller as controller


def main():
    check_excel = args.check_excel
    execution_type = config.execution_type
    save_date = config.save_date
    logging.info("Check excel set to: " + str(check_excel))
    logging.info("Execution type: " + str(execution_type))
    logging.info("Save date: " + save_date)
    controller.execute(check_excel, execution_type, save_date)


# Function to detect correctly boolean argument passed to execution
def boolean_string(s):
    if s == "True":
        return True
    else:
        return False


if __name__ == "__main__":
    # Needed to receive arguments when executing the script
    parser = argparse.ArgumentParser()
    parser.add_argument("--check_excel", required=True, type=boolean_string)
    args = parser.parse_args()

    if platform.system() == "Darwin":
        # Needed to keep track of the execution logs
        execution_datetime = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        file_string = "logs/" + execution_datetime + ".log"
    else:
        file_string = "logs/execution.log"

    # Create log file
    file = open(file_string, 'a')
    file.close()

    logging.basicConfig(level=logging.DEBUG, filename=file_string, filemode="a")

    main()
