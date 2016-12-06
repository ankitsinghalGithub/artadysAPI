#Import the necessary methods from tweepy library
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import csv
import sys
import requests

access_token = "957322597-WKkHivBIUdnpmSatQIihoPJXDgWJhHdYg3qN38ZS"
access_token_secret = "TsPBrBPyaSYFdoaAahXa8gbu8YUsfW6HnIDNGsNUbvtye"
consumer_key = "nx6dBWLS26TYkm3KhJOEUwWAM"
consumer_secret = "qOiWzPzFLWvh8zFciklihIjmYfYW76QU8oQSYDllvcqz4PBfnJ"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def getInfo(word):
	c = 10
	tweetsList=[]
	#print ("word::",word)
	for tweet in tweepy.Cursor(api.search,q=word,since='2016-12-02',lang='en').items():
		#print ("1",c)
		if (c ==0):
			break
		else:
			#j = ("date":tweet.created_at, "tweet": tweet.text.encode('utf-8'))
			j = (tweet.created_at, tweet.text.encode('utf-8'))
			tweetsList.append(j)
			#print (j)
			c=c-1

	return (tweetsList)
