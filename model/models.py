class User:
    def __init__(self, username, name, twitter_id):
        self.username = username
        self.name = name
        self.twitter_id = twitter_id


class Tweet:
    def __init__(self, tweet_id, text, author, lang, tweet_type, save_date):
        self.tweet_id = tweet_id
        self.text = text
        self.author = author
        self.lang = lang
        self.type = tweet_type
        self.save_date = save_date


class Reply(Tweet):
    def __init__(self, tweet_id, text, author_id, lang, tweet_type, reply_to, conversation_id, save_date):
        super().__init__(tweet_id, text, author_id, lang, tweet_type, save_date)
        self.reply_to = reply_to
        self.conversation_id = conversation_id
