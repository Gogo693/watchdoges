import tweepy
import re

class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        '''
        Insert action to perform on detected tweets
        :param tweet:
        :return:
        '''
        if re.search("doge|Doge|dogecoin|Dogecoin", tweet.text):
            print(f"{tweet.user.name}:{tweet.text}")

    def on_error(self, status):
        print("Error detected")

## Authenticate to Twitter
# pub key + secret key
# access key + access secret key
auth = tweepy.OAuthHandler("",
    "")
auth.set_access_token("",
    "")

api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)

tweets_listener = MyStreamListener(api)
stream = tweepy.Stream(api.auth, tweets_listener)

## Filter elon tweets - ID below
# elon: 44196397
# CrepaldiGiorgi2: 991048124
stream.filter(follow=['44196397'])


