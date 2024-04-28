import api_requests.users as users
import read_excel.excel as excel


def main():
    # user_id = users.get_user_id_by_username("FormulaDirecta")
    # print(user_id)
    usernames = excel.get_usernames_from_excel()
    print(usernames)


if __name__ == "__main__":
    main()
