import api_requests.users as users_api
import api_requests.tweets as tweets_api
import api_requests.replies as replies_api
import read_excel.excel as excel
import mongodb.mongo as mongo
from model.models import *


def main():
    replies = replies_api.get_user_replies("1359418375076773888")

    print(replies)
    print(replies.__len__())

    mongo.save_user_replies(replies)


# user_id = users.get_user_id_by_username("FormulaDirecta")
# print(user_id)
# usernames = excel.get_usernames_from_excel()
# for username in usernames:
#   user_id = users_api.get_user_id_by_username(username)
#  mongo.save_user(User(username, user_id))


if __name__ == "__main__":
    main()
