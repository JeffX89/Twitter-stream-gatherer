from __future__ import absolute_import, print_function

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import os
import json
import tweepy
import ConfigParser
import time
import datetime
import threading
import sys
import urllib2
import urllib
import requests
# make a list for top 100 shares($) tweets for last 15min
# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
#consumer_key="78VWJGi4vahhe7uFR5iFRbi99"
#consumer_secret="ZWOZxVr1u7NKJQqYsJmxOO15UZ2icwVNJ0VItLqLGFPotrlpnl"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
#access_token="2952137164-zm2pv0DBWxMj4O0foTS6HCbSafsZnAjywk7MB1O"
#access_token_secret="CwfBd7CjyxrP2rxUMZYSC2VqzZQXMwU3aaYOYfJZng9uS"
tweet_hash = {}
tweet_cash = {} 
ct_updater = 0
savefile=''
savepath=''
date=''
machine=''
maxsize=0
partcount=1
def config():
    try:
        global machine
        global path
        global savepath
        global maxsize
        config = ConfigParser.RawConfigParser()
        config.read('config.cfg')
        consumer_key = str(config.get("Twitter","consumer_key"))
        consumer_secret = str(config.get("Twitter","consumer_secret"))
        access_token = str(config.get("Twitter","access_token"))
        access_token_secret = str(config.get("Twitter","access_token_secret"))
        machine = str(config.get("Config","machine"))
        savepath = str(config.get("Config","savepath"))
        maxsize = str(config.get("Config","maxsize"))
        maxsize = int(maxsize) * 1073741824 #convert MB to bytes
        hashtrack = str(config.get("Config","hashtrack")
        #check if savefile directory exists and creates it if not
        try: 
            os.makedirs(savepath)
        except OSError:
            if not os.path.isdir(savepath):
                raise
        return consumer_key, consumer_secret, access_token, access_token_secret, hashtrack
    except Exception as e:
        print(e)


    
def f():
    #this function gets executed every 60 seconds
    #save the tweet_cash data every 60 seconds
    #get the filename that you save to (size limit included)
    try:
        global date
        global savefile
        global savepath
        global maxsize
        global partcount
        date = datetime.date.today() 
        #print(urllib2.getproxies())
        if os.path.isfile(savefile):
            size = os.path.getsize(savefile)
            if int(size)>int(maxsize):
                partcount+=1
                savefile = str('%s%s-%s_part%d.txt'%(savepath, date, machine, partcount))
        else:
            savefile = str('%s%s-%s_part%d.txt'%(savepath, date, machine, partcount))



##        url = 'http://127.0.0.1:5000/base'
##        data = urllib.urlencode([('query', tweet_cash)])
##        #print(data)
##        req = urllib2.Request(url, headers={'Content-Type': 'application/json'})
##        #fd = urllib2.urlopen(req, data)
##        fd = urllib2.urlopen(req, data=json.dumps({'text': 'lalala'}))
##        print("server response:")
##        print(fd.read())






        
        threading.Timer(60, f).start()
    except Exception as e:
        print(e)
        return True
        
class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """
    
    def on_data(self, data):
        try:
            global date
            global ct_updater
            global tweet_cash
            global savefile
            # print(data)
            # Save JSON data to txt

            with open(savefile,"a+") as text:
                text.write(data)
            text.close()
            #Counts the number of cashtags and hashtags
            #Stores in dictionaries tweet_hash and tweet_cash
            
##            line = json.loads(data)
##            if "entities" in line.keys():                    # Check whether entities tags present
##              hashtags = line["entities"]["hashtags"]        #  - if present then extract the hashtags
##              for ht in hashtags:                             # For every hashtag get the hashtag text value
##                if ht != None:
##                  #print(ht["text"])
##                  #check for cashtag here?
##                  if ht["text"].encode("utf-8") in tweet_hash.keys():  # Check whether hashtag already in dictionary
##                    tweet_hash[ht["text"].encode("utf-8")] += 1        # - If it is then increment its frequency by 1 
##                  else:
##                    tweet_hash[ht["text"].encode("utf-8")] = 1         # - Else initialise the hashtag with frequency as 1
##              cashtags = line["entities"]["symbols"]
##              for ct in cashtags:
##                if ct != None:
##                  print(ct["text"])
##                  #print(line['text'])
##                  if ct["text"].encode("utf-8") in tweet_cash.keys():  # Check whether hashtag already in dictionary
##                    tweet_cash[ct["text"].encode("utf-8")] += 1        # - If it is then increment its frequency by 1 
##                  else:
##                    tweet_cash[ct["text"].encode("utf-8")] = 1         # - Else initialise the hashtag with frequency as 1
##                  if ct_updater<20:            
##                      ct_updater += 1
##                  else:
##                      for key, value in tweet_cash.items():
##                          print("cashtag: %s  --  times: %d" % (key, value))
##                      ct_updater=0
##                          


            return True
        
        except Exception as e:
            print(e)
            
    def on_error(self, status):
        print >> sys.stderr, 'Encountered error with status code:', status
        return True
        
    def on_status(self, status):
        print(status.text)
        
    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        time.sleep(10)
        return True
    
if __name__ == '__main__':
    try:
        consumer_key, consumer_secret, access_token, access_token_secret, hashtrack = config()
        f()
        l = StdOutListener()
        #print(consumer_key, consumer_secret, access_token, access_token_secret)
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)

        stream = Stream(auth, l)
        stream.filter(track=hashtrack)
        #stream.sample()
    except Exception as e:
        print(e)
