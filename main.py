import api_requests.users as users
import read_excel.excel as excel
import mongodb.mongo as mongo
from model.models import *


def main():
    # user_id = users.get_user_id_by_username("FormulaDirecta")
    # print(user_id)
    usernames = excel.get_usernames_from_excel()
    for username in usernames:
        user_id = users.get_user_id_by_username(username)
        mongo.save_user(User(username, user_id))


if __name__ == "__main__":
    main()
