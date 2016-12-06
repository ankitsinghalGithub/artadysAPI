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

    if 'url' in request.args:
         url = request.args['url']
         #print (url)
    if request.method == "GET":
        # get url that the person has entered
        try:
        	#print ("1")
            #url = urlParse
	        r = requests.get(url)
	        #print ("2")
        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )
            return render_template('wordcount.html', errors=errors)
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


@app.route('/wordcount', methods=['GET', 'POST'])
def wordcount():
    errors = []
    results = {}
    if request.method == "POST":
        # get url that the person has entered
        try:
            url = request.form['url']
            r = requests.get(url)
        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )
            return render_template('wordcount.html', errors=errors)
        if r:
            # text processing
            
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
            no_stop_words_count = Counter(no_stop_words)
            # save the results
            
            results = sorted(
                no_stop_words_count.items(),
                key=operator.itemgetter(1),
                reverse=True
            )
            try:
                result = Result(
                    url=url,
                    result_all=raw_word_count,
                    result_no_stop_words=no_stop_words_count
                )
                #db.session.add(result)
                #db.session.commit()
            except:
                errors.append("")

            #print (results)
    return render_template('wordcount.html', errors=errors, results=results)

@app.route('/pasttweets', methods=['GET', 'POST'])
def pasttweets():
    errors = []
    results =()
    keyword=''
    #print (request.method)
    if request.method == "POST":
        # get url that the person has entered
        try:
            #print ("inside")
            keyword = request.form['url']
            #print (keyword)
        except:
            errors.append(
                "Unable to get key word. Please make sure it's valid and try again."
            )
            return render_template('tweetsSent.html', errors=errors)

        if keyword:
            #print ("keyword:", keyword)
            try:
                results = pastTweetsExtract.getInfo(keyword)
                #print  (results)
            except:
                errors=["Unable to get key word. Please make sure it's valid and try again."]
                return render_template('pasttweets.html', errors=errors)

    return render_template('pasttweets.html', errors=errors, results=results, keyword=keyword)

@app.route('/sentiment', methods=['GET', 'POST'])
def sentiment():
    errors = []
    results =''
    keyword=''
    #print (request.method)
    if request.method == "POST":
        # get url that the person has entered
        try:
            #print ("inside")
            keyword = request.form['url']
            #print (keyword)
        except:
            errors.append(
                "Unable to get sentence. Please make sure it's valid and try again."
            )
            return render_template('sentiment.html', errors=errors)

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
                return render_template('sentiment.html', errors=errors)

    return render_template('sentiment.html', errors=errors, results=results, keyword=keyword)



@app.route('/mapTest', methods=['GET', 'POST'])
def maps():
    locations = [
    -31.563910,-33.718234,-33.727111,
    -33.848588,-33.851702,
    -34.671264,-35.304724,
    -36.817685,-36.828611,
    -37.750000,-37.759859,
    -37.765015,-37.770104,
    -37.773700,-37.774785,
    -37.819616,-38.330766,
    -39.927193,-41.330162,
    -42.734358,-42.734358,
    -42.735258,-43.999792,
    ]

    locations1= [
    147.154312,150.363181,
    150.371124,151.209834,
    151.216968,150.863657,
    148.662905,175.699196,
    175.790222,145.116667,
    145.128708,145.133858,
    145.143299,145.145187,
    145.137978,144.968119,
    144.695692,175.053218,
    174.865694,147.439506,
    147.501315,147.438000,
    170.463352
    ]

    return render_template('googleMapTest.html', lat=locations, lng=locations1)


@app.route('/heatMapTest', methods=['GET', 'POST'])
def heatMapTest():
    return render_template('heatMapTest.html')


@app.route('/tweetsSent', methods=['GET', 'POST'])
def tweetsSent():
    errors = []
    results =()
    keyword=''
    locations=[]
    locations1=[]
    labels=''
    #print (request.method)
    if request.method == "POST":
        # get url that the person has entered
        try:
            #print ("inside")
            keyword = request.form['url']
            #print (keyword)
        except:
            errors.append(
                "Unable to get key word. Please make sure it's valid and try again."
            )
            return render_template('tweetsSent.html', errors=errors)
        if keyword:
            try:
                results = pasttweetSent.getInfo(keyword)
                for x in results:
                    locations.append(x[1]['lat'])
                    locations1.append(x[1]['lng'])
                    labels=labels + x[-1]
                    
            except:
                errors=["Unable to get key word. Please make sure it's valid and try again."]
                return render_template('tweetsSent.html', errors=errors)


    return render_template('tweetsSent.html', errors=errors, results=results, keyword=keyword,lat=locations, lng=locations1, lab=labels)


@app.route('/getAttitude', methods=['GET', 'POST'])
def getAttitude():
    errors = []
    remotion =[]
    rpersonality = []
    keyword=''
    results=''
    
    #print (request.method)
    if request.method == "POST":
        # get url that the person has entered
        try:
            #print ("inside")
            keyword = request.form['url']
            #print (keyword)
        except:
            errors.append(
                "Unable to get key word. Please make sure it's valid and try again."
            )
            return render_template('getAttitude.html', errors=errors)
        if keyword:
            try:
                #print (keyword)
                getemotion = emotion.getEmotion(keyword)
                remotion = list(getemotion.items())
                #print (remotion)

                getpersonality = personality.getPersonality(keyword)
                rpersonality = list(getpersonality.items())
                #print (rpersonality)

                results='YES'
                    
            except:
                errors=["Unable to get key word. Please make sure it's valid and try again."]
                return render_template('getAttitude.html', errors=errors)


    return render_template('getAttitude.html', errors=errors, emotion=remotion, keyword=keyword, personality=rpersonality, results=results)



if __name__ == '__main__':
    app.run()
