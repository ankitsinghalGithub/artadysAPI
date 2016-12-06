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
# Open/Create a file to append data
#csvFile = open('tweetsHistory_1234.csv', 'a')
#tweet_RSS_file = open('tweets_RSS.json', 'a')
	#Use csv Writer
#csvWriter = csv.writer(csvFile)

def getInfo(word):
	c = 5
	tweetsList=[]

	for tweet in tweepy.Cursor(api.search,q=word,since='2016-12-03',lang='en').items():
		#print ("1",c)
		#print ("1:",c, tweet)
		if (c ==0):
			#return tweetsList
			#print ("2:",c, tweet)
			break
		else:
			d = tweet.created_at
			t = tweet.text.encode('utf-8')
			l = tweet.author.location
			print (d,t,l)
			print ("ddd:",l)
			if (l):
				pass
			else:
				l = 'NA'

			t1=""

			try:

				data123 = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+l+'&key=AIzaSyBPniJUxYnftn0QCRA5nJuUA0gu2PXJLKM')
				#print (data123.text)
				t1 = json.loads(data123.text)
			except:
				l='NA'
				data123 = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+l+'&key=AIzaSyBPniJUxYnftn0QCRA5nJuUA0gu2PXJLKM')
				#print (data123.text)
				t1 = json.loads(data123.text)
				
			cord= t1['results'][0]['geometry']['location']
			#print (cord)
			#print (t)
			url1 = "http://www.sentiment140.com/api/classify?text=" + str(t)
			#print (url1)
			r = requests.get(url1)
			#print (r)
			polarity = json.loads(r.text)['results']['polarity']
			results=''
			#print (polarity)
			if (polarity==0):
				results = 'N'
			elif (polarity == 2):
				results = 'L'
			elif (polarity ==4):
				results = "P"

			j=(d,cord,t,l, results)
			tweetsList.append(j)
			c=c-1
	#print (tweetsList)

	return tweetsList

			
		#csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])
		#csvWriter.writerow([tweet])


	#csvFile.close()
