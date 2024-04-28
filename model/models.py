class User:
    def __init__(self, username, twitter_id):
        self.username = username
        self.twitter_id = twitter_id


class Tweet:
    def __init__(self, tweet_id, text, author_id, lang):
        self.tweet_id = tweet_id
        self.text = text
        self.author_id = author_id
        self.lang = lang
