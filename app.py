import os
import requests
import operator
import re
import nltk
from flask import Flask, render_template, request
#from flask.ext.sqlalchemy import SQLAlchemy
from stop_words import stops
from collections import Counter
from bs4 import BeautifulSoup
from nltk import FreqDist
import json
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
import pastTweetsExtract
import pasttweetSent
import emotion
import personality
from watson_developer_cloud import AlchemyLanguageV1
import subprocess
import scrapData
import Search_engine



app = Flask(__name__)
CORS(app)
#app.config.from_object(os.environ['APP_SETTINGS'])
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#db = SQLAlchemy(app)

@app.route('/')
def home_page():
    return "Welcome to ARTADYS Innovation"

@app.route('/<name>')
def hello_name(name):
    #print (name)
    return "Hello {}!".format(name)


@app.route('/wordcountAPI', methods=['GET', 'POST'])
def wordcountAPI():
    errors = []
    results = {}
    url=''

    if 'url' in request.args:
        url = request.args['url']
        #print (url)


    #print (request.method)
    if request.method == "GET":
        # get url that the person has entered
        try:
        	#print ("1")
            #url = urlParse
	        r = requests.get(url)
	        #print ("2", r)
        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )
            return jsonify([{'error':errors}])
        if r:
            # text processing
            #print ("3")
            raw = BeautifulSoup(r.text, 'html.parser').get_text()
            nltk.data.path.append('./nltk_data/')  # set the path
            tokens = nltk.word_tokenize(raw)
            text = nltk.Text(tokens)
            # remove punctuation, count raw words
            nonPunct = re.compile('.*[A-Za-z].*')
            raw_words = [w for w in text if nonPunct.match(w)]
            raw_word_count = Counter(raw_words)
            # stop words
            no_stop_words = [w for w in raw_words if w.lower() not in stops]
            #no_stop_words_count = Counter(no_stop_words)
            no_stop_words_count = FreqDist(no_stop_words).most_common()
            s = len(no_stop_words_count)
            no_stop_words_count0 = sorted(no_stop_words_count, key=lambda tup: tup[1])[s-10:s+10]
            no_stop_words_count1 =sorted(no_stop_words_count, key=lambda tup: tup[1])[:10]
            no_stop_words_count2 = sorted(no_stop_words_count, key=lambda tup: tup[1])[-10:]

            no_stop = no_stop_words_count0 + no_stop_words_count1 + no_stop_words_count2
            rs1 =list(map(lambda x: {'word': x[0], 'count':x[1] }, no_stop))

            #print (rs1)

    return  jsonify(rs1)



@app.route('/pasttweetsapi', methods=['GET', 'POST'])
def pasttweetsapi():
    errors = []
    results =()
    keyword=''
    #print (request.method)
    if request.method == "GET":
        # get url that the person has entered
        try:
            #print ("inside")
            #keyword = request.form['key']
            if 'key' in request.args:
                #print ('key')
                keyword = request.args['key']
                #keyword =requests.get(key)
            #print (keyword)
        except:
            errors.append(
                "Unable to get key word. Please make sure it's valid and try again."
            )
            return jsonify([{'error': errors}])

        if keyword:
            #print ("keyword:", keyword)
            try:
                results = pastTweetsExtract.getInfo(keyword)
                #results =list(map(lambda x: {'created': x[0], 'tweet':x[1] }, results))
                #print  ("app.py : ",results)
            except:
                errors=["Unable to get key word. Please make sure it's valid and try again."]
                return jsonify({"results":[{'error': errors}]})

    return jsonify({"results":results})

@app.route('/sentimentapi', methods=['GET', 'POST'])
def sentimentapi():
    errors = []
    results =''
    keyword=''
    #print (request.method)
    if request.method == "GET":
        # get url that the person has entered
        try:
            #print ("inside")
            if 'sent' in request.args:

                keyword = request.args['sent']
                #keyword =requests.get(key)
                #print (keyword)
        except:
            errors.append(
                "Unable to get sentence. Please make sure it's valid and try again."
            )
            return jsonify([{'error': errors}])

        if keyword:
            #print ("keyword:", keyword)
            try:
                url1 = "http://www.sentiment140.com/api/classify?text=" + keyword
                r = requests.get(url1)
                polarity = json.loads(r.text)['results']['polarity']
                if (polarity==0):
                    results = 'Negative'
                elif (polarity == 2):
                    results = 'Neutral'
                elif (polarity ==4):
                    results = "Positive"
                #print  (results)
            except:
                errors=["Unable to get sentence. Please make sure it's valid and try again."]
                return jsonify([{'error': errors}])

    return jsonify({"results":[{'text':keyword, 'polarity':results, 'powered by':'Sentiment140'}]})


@app.route('/tweetsSentapi', methods=['GET', 'POST'])
def tweetsSentapi():
    errors = []
    results =()
    keyword=''
    locations=[]
    locations1=[]
    labels=''
    #print (request.method)
    if request.method == "GET":
        # get url that the person has entered
        try:
            #print ("inside")
            #keyword = request.form['url']
            if 'key' in request.args:
                #print ('key')
                keyword = request.args['key']
                #keyword =requests.get(key)
            #print (keyword)
            #print (keyword)
        except:
            errors.append(
                "Unable to get key word. Please make sure it's valid and try again."
            )
            return jsonify([{'error': errors}])
        if keyword:
            try:
                results = pasttweetSent.getInfo(keyword)
            except:
                errors=["Unable to get key word. Please make sure it's valid and try again."]
                return jsonify([{'error': errors}])


    return jsonify({"results":results})



@app.route('/getAttitudeAPI', methods=['GET', 'POST'])
def getAttitudeAPI():
    errors = []
    remotion =[]
    rpersonality = []
    keyword=''
    results=[]
    text=''



    if request.method == "GET":
        # get url that the person has entered
        try:
            if 'text' in request.args:
                text = request.args['text']

        except:
            errors.append(
                "Unable to get key word. Please make sure it's valid and try again."
            )
            return jsonify({'Status':'error'})
        if text:
            try:
                #print ("$$$$$$$$$$$$$$$$$$",text)
                getemotion = emotion.getEmotion(text)
                #print ("emotion",getemotion)
                #remotion = list(getemotion.items())
                getpersonality = personality.getPersonality(text)
                #rpersonality = list(getpersonality.items())
                #print ('personality', getpersonality)
                results.append({'text':text,'emotion_score':getemotion,'personality_score':getpersonality})
                #print (results)
                #results.append(getemotion)
                #print ("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@22", results)
                #results.append(getpersonality)
                #print ("results:", results)
                results=getemotion

            except:
                errors=["Unable to get key word. Please make sure it's valid and try again."]
                return jsonify({'Status':'error'})

    #print ("%%%%%%%%%%%%%%%%%%%%", results)
    return jsonify({"results":results})
    #return jsonify(results)


@app.route('/getConceptAPI', methods=['GET', 'POST'])
def getConceptAPI():
    errors = []
    results = [['text','relevance']]
    url1=''
    rs1=''

    if 'url' in request.args:
        url1 = request.args['url']
        #print (url1)
    try:
        
        alchemy_language = AlchemyLanguageV1(api_key='cf58ea656e04426e98c30b9b6fca569b7690d17f')
        
        a = json.dumps(alchemy_language.concepts(url=url1),indent=2)
        b = json.loads(a)['concepts']
        for i in b:
           results.append([i['text'],float(i['relevance'])])
           #print ('3333333333333', results)
            
        return  jsonify(results)
    except:
            errors.append(
                "Unable to get URL1. Please make sure it's valid and try again."
            )
            return jsonify([{'error':errors}])


@app.route('/scrapyAPI', methods=['GET', 'POST'])
def scrapyAPI():
    errors = []
    results = {}
    url=''

    scrapData.data=[]
    if 'url' in request.args:
        url = request.args['url']
        #print (url)


    #print (request.method)
    if request.method == "GET":
        # get url that the person has entered
        try:
        	#print ("1")
            #url = urlParse
	        r = requests.get(url)
	        #print ("2", r)
        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )
            return jsonify([{'error':errors}])
        if r:
            # text processing
            #print ("3")
            spider_name = "quotes"
            with open('quotes12.json', 'w'): pass
            #scrapy runspider quotes_spider.py -o quotes.json
            subprocess.check_output(['scrapy', 'runspider', 'quotes_spider.py', '-o', 'quotes12.json'])
            #subprocess.check_output(['scrapy', 'runspider', 'quotes_spider.py'])
            #rs=scrapData.data
            
            with open('quotes12.json') as data_file:  
                rs = json.load(data_file)
            #print ("$$$$$$$$$$$$$",type(rs))
            #rs1 = json.loads(rs)
            #print ("#######################")
            #print (rs)
            

            #print (rs1)

    return  jsonify(rs)

@app.route('/searchengineAPI', methods=['GET', 'POST'])
def searchengineAPI():
    errors = []
    results = {}
    url=''
    word=''
    r=''

    
    if 'url' in request.args:
        url = request.args['url']
        #print (url)

    if 'word' in request.args:
        word = request.args['word']
        #print (word)


    #print (request.method)
    if request.method == "GET":
        # get url that the person has entered
        try:
        	
	        #r = requests.get(search)
            r= str(url)
            w = str(word)
            print (r, w)
        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )
            return jsonify([{'error':errors}])
        
        if (len(r) !=0 and len(w)!=0):
            rs = Search_engine.getSearch(r,w)
            

    return  jsonify(rs)


if __name__ == '__main__':
    app.run()



