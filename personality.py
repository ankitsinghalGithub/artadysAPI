import pandas
import nltk
from nltk import word_tokenize, FreqDist
from nltk.corpus import stopwords
import time
import numpy as np

def getPersonality(text):

	nltk.data.path.append('./nltk_data/')  # set the path
	personality_a = pandas.read_csv("personality_traits/A.csv", header=None)
	personality_a.columns = ["WORDS", "AVG", "SD"]
	personality_c = pandas.read_csv("personality_traits/C.csv", header=None)
	personality_c.columns = ["WORDS", "AVG", "SD"]
	personality_e = pandas.read_csv("personality_traits/E.csv", header=None)
	personality_e.columns = ["WORDS", "AVG", "SD"]
	personality_n = pandas.read_csv("personality_traits/N.csv", header=None)
	personality_n.columns = ["WORDS", "AVG", "SD"]
	personality_o = pandas.read_csv("personality_traits/O.csv", header=None)
	personality_o.columns = ["WORDS", "AVG", "SD"]
	
	personality_a = personality_a.dropna()
	personality_a.ix[:,1:]=personality_a.ix[:,1:].astype('float')
	personality_c = personality_c.dropna()
	personality_c.ix[:,1:]=personality_c.ix[:,1:].astype('float')
	personality_e = personality_e.dropna()
	personality_e.ix[:,1:]=personality_e.ix[:,1:].astype('float')
	personality_n = personality_n.dropna()
	personality_n.ix[:,1:]=personality_n.ix[:,1:].astype('float')
	personality_o = personality_o.dropna()
	personality_o.ix[:,1:]=personality_o.ix[:,1:].astype('float')


	# In[94]:

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
		
		i=0
		scores = []
		scores_a = pandas.merge(word_features,personality_a,how='inner', on=['WORDS'])
		
		if len(scores_a)==0:
			scores_a.loc[0]= ["NA",0,0,0]
		scores_a[["AVG"]] = scores_a[["AVG"]].astype(float).apply(lambda x:np.exp(x))

		scores_c = pandas.merge(word_features,personality_c,how='inner', on=['WORDS'])
		if len(scores_c)==0:
			scores_c.loc[0]= ["NA",0,0,0]
		scores_c[["AVG"]] = scores_c[["AVG"]].astype(float).apply(lambda x:np.exp(x))

		scores_e = pandas.merge(word_features,personality_e,how='inner', on=['WORDS'])
		if len(scores_e)==0:
			scores_e.loc[0]= ["NA",0,0,0]
		scores_e[["AVG"]] = scores_e[["AVG"]].astype(float).apply(lambda x:np.exp(x))
			
		scores_n = pandas.merge(word_features,personality_n,how='inner', on=['WORDS'])
		if len(scores_n)==0:
			scores_n.loc[0]= ["NA",0,0,0]
		scores_n[["AVG"]] = scores_n[["AVG"]].astype(float).apply(lambda x:np.exp(x))
		
		scores_o = pandas.merge(word_features,personality_o,how='inner', on=['WORDS'])
		if len(scores_o)==0:
			scores_o.loc[0]= ["NA",0,0,0]
		scores_o[["AVG"]] = scores_o[["AVG"]].astype(float).apply(lambda x:np.exp(x))
		
		scores = [scores_a,scores_c,scores_e,scores_n,scores_o]
		return scores


	def personalityScoresWithDuplicates(scores):

		data_result_p = []
		i=0
		for s in scores:
			
			data_result = s
			data_result['AVG'] *= data_result['COUNT']
			sumData=data_result.sum(axis=0)
			sumData['WORDS']='TOTAL'
			
			if(sumData['COUNT'] !=0):
				sumData['AVG'] /= sumData['COUNT']
			
			data_result_p.append(sumData['AVG'])
		
		return data_result_p

    	#from pd import DataFrame
    	#output_filename = "emotionalScore_" + input_filename + ".csv"
    	#data_result.to_csv(output_filename, sep = ',', encoding='utf-8', index=False)


	
	header = ["AGREEABLENESS", "CONSCIENTIOUS", "EXTROVERT", "NEUROTIC", "OPEN"]			
	
	personality_lexicon = [personality_a, personality_c, personality_e, personality_n, personality_o]
	finalScores_P = personalityScoresWithDuplicates( scores(wordcount(tokenize(text)),personality_lexicon) )
	s= finalScores_P
	results = {"AGREEABLENESS": s[0], "CONSCIENTIOUS": s[1], "EXTROVERT": s[2], "NEUROTIC":s[3], "OPEN":s[4]}
	return results



