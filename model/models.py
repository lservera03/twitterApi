class User:
    def __init__(self, username, twitter_id):
        self.username = username
        self.twitter_id = twitter_id


class Tweet:
    def __init__(self, tweet_id, text, author_id, lang, tweet_type):
        self.tweet_id = tweet_id
        self.text = text
        self.author_id = author_id
        self.lang = lang
        self.type = tweet_type


class Reply(Tweet):
    def __init__(self, tweet_id, text, author_id, lang, tweet_type, reply_to, conversation_id):
        super().__init__(tweet_id, text, author_id, lang, tweet_type)
        self.reply_to = reply_to
        self.conversation_id = conversation_id
