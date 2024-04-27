import api_requests.users as users


def main():
    user_id = users.get_user_id_by_username("FormulaDirecta")
    print(user_id)


if __name__ == "__main__":
    main()
