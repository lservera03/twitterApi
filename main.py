import api_requests.users as users_api
import api_requests.tweets as tweets_api
import api_requests.replies as replies_api
import read_excel.excel as excel
import mongodb.mongo as mongo
from model.models import *


def main():
    last_tweet = mongo.get_last_tweet_by_user_id("1359418375076773888")

    # tweets = tweets_api.get_user_tweets_by_user_id("1359418375076773888", last_tweet.tweet_id)


if __name__ == "__main__":
    main()
