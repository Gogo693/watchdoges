#JUNK FILE FOR TESTING NEW APPROACHES

import os
import time
import pickle
from urllib.request import urlopen
import smtplib
from bs4 import BeautifulSoup
import requests

def my_action(tweet):
    if tweet.username == "CrepaldiGiorgi2":
        print(tweet)

#UserWatcher("CrepaldiGiorgi2", action=my_action).watch_every(30)

class Tweet:
    """ A class to make tweets from HTML data.

    Finds tweet.text, tweet.username, tweet.date, tweet.link
    from the HTML attributes of the tweet.

    See PageWatcher.get_new_tweets() to understand how it's used.
    """

    def __init__(self, text, attrs):
        self.text = text.encode('utf8')
        self.username = (attrs["href"].split("/")[1]).encode('utf8')
        self.date = attrs['title'].encode('utf8')
        self.link = ("https://twitter.com" + attrs["href"]).encode('utf8')

    def __eq__(self, other):
        """ Two tweets are the same if they have the same address."""
        return self.link == other.link

    def __str__(self):
        return ("\n".join(["%(text)s",
                           "  Author: %(username)s",
                           "  Date: %(date)s",
                           "  Link: %(link)s"])%self.__dict__)

class PageWatcher:
    """ General class for (username/search) page watchers """

    def __init__(self, action, database=None):

        self.action = action
        self.database = database

        if (database is not None) and os.path.exists(database):
            with open(database, 'r') as f:
                self.seen_tweets = pickle.load(f)
        else:
            self.seen_tweets = []


    def get_new_tweets(self):
        """ Go watch the page, return all new tweets. """

        url = urlopen(self.url)
        page = BeautifulSoup( url )
        url.close()

        texts = [p.text for p in page.findAll("p")
                 if ("class" in p.attrs) and
                 (self.p_class in p.attrs["class"])]

        attrs = [a.attrs for a in page.findAll("a")
                 if ("class" in a.attrs) and
                 (self.a_class in a.attrs["class"])]

        tweets = [Tweet(txt, a) for (txt, a) in zip(texts, attrs)]
        new_tweets = [t for t in tweets if t not in self.seen_tweets]

        self.seen_tweets += new_tweets

        if self.database is not None:
            with open(self.database, "w+") as f:
                pickle.dump(self.seen_tweets, f,
                            protocol = pickle.HIGHEST_PROTOCOL)

        return new_tweets

    def watch(self):

        for new_tweet in self.get_new_tweets():
            self.action(new_tweet)

    def watch_every(self, seconds):

        while True:
            self.watch()
            time.sleep(seconds)


class UserWatcher(PageWatcher):
    """ Gets tweets from a user page.

    >>> from twittcher import UserWatcher
    >>> def my_action(tweet):
            if tweet.username == "JohnDCook":
                print(tweet)
    >>> bot=UserWatcher("JohnDCook", action=my_action)
    >>> bot.watch_every(120)
    """

    def __init__(self, username, action=print, database=None):
        PageWatcher.__init__(self, action, database)
        self.url = "https://twitter.com/"+username
        self.username = username
        self.p_class = "ProfileTweet-text"
        self.a_class = "ProfileTweet-timestamp"



class SearchWatcher(PageWatcher):
    """ Gets tweets from a search page.

    Examples:
    ---------

    >>> from twittcher import SearchWatcher
    >>> bot=SearchWatcher("milk chocolate")
    >>> # watch every 120s. Print all new tweets.
    >>> bot.watch_every(120)

    """

    def __init__(self, search_term, action=print, database=None):
        PageWatcher.__init__(self, action, database)
        self.url ="https://twitter.com/search?f=realtime&q="+search_term
        self.search_term = search_term
        self.p_class = "tweet-text"
        self.a_class = "tweet-timestamp"

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome()
username = "elonmusk"
url = "https://twitter.com/"+username

browser.get(url)
print(browser)

'''
username = "elonmusk"
url = "https://twitter.com/"+username
url = requests.get(url)
#print(url)
content = url.content
#print(content)
page = BeautifulSoup(content, features='html.parser')
for tweet in page.select('.tweet-text'):
    print(tweet.text.strip())

#print(page.prettify())

print(page.find("span"))
#print(page.get_text())
#("css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"))
#<span class="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0">
#<span class="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0">WatchDoges</span>

texts = [p.text for p in page.findAll("p")
         if ("class" in p.attrs)]

#print(texts)

attrs = [a.attrs for a in page.findAll("a")
         if ("class" in a.attrs)]

tweets = [Tweet(txt, a) for (txt, a) in zip(texts, attrs)]
new_tweets = [t for t in tweets if t]# not in self.seen_tweets]

#print(new_tweets)

'''