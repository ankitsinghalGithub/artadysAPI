# coding: utf-8

import pandas
import nltk
from nltk import word_tokenize, FreqDist
from nltk.corpus import stopwords
import time

def getEmotion(text):
    
    nltk.data.path.append('./nltk_data/')  # set the path
    emotion_lexicon = pandas.read_csv("data_emotions_words_list.csv")
    emotion_lexicon.columns = ["WORDS", "HAP-AVG", "HAP-SD", "ANG-AVG", "ANG-SD", "SAD-AVG", "SAD-SD", "FEA-AVG", "FEA-SD", "DIS-AVG", "DIS-SD"]
    emotion_lexicon=emotion_lexicon.dropna()
    emotion_lexicon.ix[:,1:]=emotion_lexicon.ix[:,1:].astype('float')
    emotion_lexicon.head()

    def tokenize(doc):
        tokens = nltk.wordpunct_tokenize(doc)
        text = nltk.Text(tokens)
        words_punc = [w.lower() for w in text if w.isalpha()]
        doc_punc = " ".join(words_punc)
        tokens=word_tokenize(doc_punc)
        fdist = FreqDist(tokens)
        return fdist

    def wordcount(wordsList):
        word_count = dict(wordsList)
        word_features = pandas.DataFrame(list(word_count.items()), columns=['WORDS', 'COUNT'])
        word_features1 = word_features.sort(['WORDS'], ascending=True)
        return word_features1

    def scores(word_features,lexicon):
        scores = pandas.merge(word_features,lexicon,how='inner', on=['WORDS'])
        
        if len(scores)==0:
            scores.loc[0]= ["NA",1,0,0,0,0,0,0,0,0,0,0]

        return scores

    def emotionScoresWithDuplicates(scores):
   
        data_result = scores
        data_result['HAP-AVG'] *= data_result['COUNT']
        data_result['ANG-AVG'] *= data_result['COUNT']
        data_result['SAD-AVG'] *= data_result['COUNT']
        data_result['FEA-AVG'] *= data_result['COUNT']
        data_result['DIS-AVG'] *= data_result['COUNT']

        sumData=data_result.sum(axis=0)
        sumData['WORDS']='TOTAL'

        data_result= data_result.append(sumData,ignore_index=True)

        data_result['HAP-AVG'].iloc[-1] /= data_result['COUNT'].iloc[-1]
        data_result['ANG-AVG'].iloc[-1] /= data_result['COUNT'].iloc[-1]
        data_result['SAD-AVG'].iloc[-1] /= data_result['COUNT'].iloc[-1]
        data_result['FEA-AVG'].iloc[-1] /= data_result['COUNT'].iloc[-1]
        data_result['DIS-AVG'].iloc[-1] /= data_result['COUNT'].iloc[-1]
        #print data_result.tail(n=1)
        #data_result =data_result.drop('COUNT', axis=1)
        data_result = data_result.drop('HAP-SD',axis=1)
        data_result = data_result.drop('ANG-SD',axis=1)
        data_result = data_result.drop('SAD-SD',axis=1)
        data_result = data_result.drop('FEA-SD',axis=1)
        data_result = data_result.drop('DIS-SD',axis=1)
        #emotion123 = pandas.DataFrame(data_result.tail(n=1)).ix[:,1:].T
        #print "bsd:  ",emotion123
        #print data_result
        return data_result

        #from pd import DataFrame
        #output_filename = "emotionalScore_" + input_filename + ".csv"
        #data_result.to_csv(output_filename, sep = ',', encoding='utf-8', index=False)

    
    header = ["HAPPY", "ANGER", "SAD", "FEAR", "DISGUST"]

    #finalScores_E = (emotionScoresWithDuplicates( scores(wordcount(tokenize(text)),emotion_lexicon) ).tail(1).values).tolist()
    finalScores_E = emotionScoresWithDuplicates( scores(wordcount(tokenize(text)),emotion_lexicon) )

    fs= finalScores_E[-1:]
    results = {"HAPPY": list(fs['HAP-AVG'])[0], "ANGER": list(fs['ANG-AVG'])[0], "SAD": list(fs['SAD-AVG'])[0], "FEAR":list(fs['FEA-AVG'])[0], "DISGUST":list(fs['DIS-AVG'])[0]}
    return results

#text1 = "He is"
#print (getEmotion(text1))
