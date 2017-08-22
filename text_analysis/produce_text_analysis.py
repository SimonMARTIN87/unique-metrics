from pymongo import MongoClient
import pandas as pd
import numpy as np
from bson.objectid import ObjectId
from nltk import word_tokenize, FreqDist
from keywords_extraction import rake
import json, os, collections, grammar_check
from nltk.util import ngrams
from collections import Counter
from nltk.stem import PorterStemmer
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
import string

with open('stop_words_french.txt', 'r') as df :
	stop = [s.replace('\n','') for s in df.readlines()]
	stop = [s.encode('utf8') for s in df.readlines()]

rake_object = rake.Rake('stop_words_french.txt')


## MongoDB
client = MongoClient()
db = client.test2
candidates = db['candidates']
conversations = db['conversations']
messages = db['messages']

dirname, filename = os.path.split(os.path.abspath(__file__))
df_macdo= pd.read_excel(dirname + '/../stats_candidates/GenEmbaucheReportV2.xlsx',header=2)

emails_macdo = [e.encode('utf8') for e in df_macdo['Email'].values.tolist()]
candidates_recruted_macdo = [c.get('_id') for c in candidates.find() if c.get('contact').get('email') in emails_macdo]
# emails_jamba = df_jamba['Email'].values.tolist()
# candidates_recruted_jamba = [c.get('_id') for c in candidates.find() if c.get('contact').get('email') in emails_jamba]
# emails_halal = df_halal['Email'].values.tolist()
# candidates_recruted_halal = [c.get('_id') for c in candidates.find() if c.get('contact').get('email') in emails_halal]

def score_messages(company) : 
	if company == 'Macdo' :
		ids_company = ObjectId("58d12d7c9dab1c0004485209")
		candidates_recruted = candidates_recruted_macdo
	# if company == 'Jamba' :
	# 	ids_company = ObjectId('591996f98a37080004bdbdda')
	# 	candidates_recruted = candidates_recruted_jamba
	# if company == 'Halal' :
	# 	ids_company = ObjectId('591d0580161f480004e6501a')
	# 	candidates_recruted = candidates_recruted_halal

	welcomingQuestion = []
	satisfactionQuestionReply = []
	whyMcDonalds = []

	for conv in conversations.find({'company' : ids_company, 'score' : {'$gt' : 0}}) : 
		id_conv = conv.get('_id')
		score = conv.get('score')
		id_candidate = conv.get('candidate')
		r = 0
		if id_candidate in candidates_recruted : 
			r = 1
		for message in messages.find({'conversation' : id_conv,'atsValueName' : {'$in' : ["welcomingQuestion", \
			"satisfactionQuestionReply","whyMcDonalds"]}}) :

			if message.get('atsValueName') == 'welcomingQuestion':
				key = rake_object.run(message.get('text'))
				if len(key) > 1 : 
					welcomingQuestion.append({'recuted' : r,
						'score' : score,
						'message' : unicode(message.get('text')),
						'keywords' : unicode(key[0][0])})

			if message.get('atsValueName') == 'satisfactionQuestionReply' :
				key = rake_object.run(message.get('text'))
				if len(key) > 1 : 
					satisfactionQuestionReply.append({'recuted' : r,
						'score' : score,
						'message' : unicode(message.get('text')),
						'keywords' : unicode(key[0][0])})

			if message.get('atsValueName') == 'whyMcDonalds' :
				key = rake_object.run(message.get('text'))
				if len(key) > 1 : 
					whyMcDonalds.append({'recuted' : r,
						'score' : score,
						'message' : unicode(message.get('text')),
						'keywords' : unicode(key[0][0])})

	return [welcomingQuestion, satisfactionQuestionReply, whyMcDonalds]


# welcomingQuestion, satisfactionQuestionReply, whyMcDonalds = score_messages('Macdo')

# with open('welcomingQuestion1.json','w') as df :
# 	json.dump(welcomingQuestion,df)

# with open('satisfactionQuestionReply1.json','w') as df :
# 	json.dump(satisfactionQuestionReply,df)

# with open('whyMcDonalds1.json','w') as df :
# 	json.dump(whyMcDonalds,df)


## open jsons saved
with open('welcomingQuestion.json','r') as df :
	welcomingQuestion = json.load(df)
	welcomingQuestion_key = [d.get('keywords').encode('utf8') for d in welcomingQuestion]
	welcomingQuestion_key = [d.translate(None, string.punctuation) for d in welcomingQuestion_key]
	welcomingQuestion_message = [d.get('message').encode('utf8') for d in welcomingQuestion]
	welcomingQuestion_message = [d.translate(None, string.punctuation) for d in welcomingQuestion_message]

with open('satisfactionQuestionReply.json','r') as df :
	satisfactionQuestionReply = json.load(df)
	satisfactionQuestionReply_key = [d.get('keywords').encode('utf8') for d in satisfactionQuestionReply]
	satisfactionQuestionReply_key = [d.translate(None, string.punctuation) for d in satisfactionQuestionReply_key]
	satisfactionQuestionReply_message = [d.get('message').encode('utf8') for d in satisfactionQuestionReply]
	satisfactionQuestionReply_message = [d.translate(None, string.punctuation) for d in satisfactionQuestionReply_message]
with open('whyMcDonalds.json','r') as df :
	whyMcDonalds = json.load(df)
	whyMcDonalds_key = [d.get('keywords').encode('utf8') for d in whyMcDonalds]
	whyMcDonalds_key = [d.translate(None, string.punctuation) for d in whyMcDonalds_key]
	whyMcDonalds_message = [d.get('message').encode('utf8') for d in whyMcDonalds]
	whyMcDonalds_message = [d.translate(None, string.punctuation) for d in whyMcDonalds_message]

### Functions 
def count_errors(sentence,langue) :
	lentgh_sentence = len(sentence.split(' '))
	tool = grammar_check.LanguageTool(langue)
	matches = tool.check(sentence)
	errors= len(matches)

	correction = grammar_check.correct(sentence, matches)
	return errors , lentgh_sentence, correction

def most_ngram(messages,number) :
	ngram = []
	for message in messages :
		tokens = message.replace('.','').split(' ')
		tokens = [t for t in tokens if t not in stop]
		ngram += [' '.join(n) for n in ngrams(tokens,number)]
	fdist= FreqDist(ngram)
	freq = fdist.most_common(200)
	docs = [f[0] for f in freq if f[1] > 1 and len(f[0])>2]
	return docs

def most_things_said(messages) :
	fdist= FreqDist(messages)
	freq = fdist.most_common(50)
	docs = [f[0] for f in freq if f[1] > 1 and len(f[0])>2]
	return docs

def frequence_by(messages,by=None) :
	if by == 'score' : 
		scores = [d.get('score') for d in df]
		scores = [int(s) for s in scores if s is not None]
		messages = [messages[i] for i in range(len(messages)) if scores[i] is not None]
		liste_inf = [messages[i] for i in range(len(messages)) if scores[i] <= 80]
		liste_sup = [messages[i] for i in range(len(messages)) if scores[i] > 80]
		return most_things_said(liste_inf), most_things_said(liste_sup)

	if by == 'recruted' : 
		scores = [d.get('recruted') for d in df]
		messages = [messages[i] for i in range(len(messages)) if scores[i] is not None]
		scores = [int(s) for s in scores if s is not None]
		liste_inf = [messages[i] for i in range(len(messages)) if scores[i]== 0 ]
		liste_sup = [messages[i] for i in range(len(messages)) if scores[i]  == 1 ]
		return most_things_said(liste_inf), most_things_said(liste_sup)


def word_tokenizer(text):
	stemmer = PorterStemmer()
	tokens = [stemmer.stem(t) for t in text.split(' ') if t not in stop]
	return tokens

def cluster_sentences(sentences, nb_of_clusters=4):
	tfidf_vectorizer = TfidfVectorizer(tokenizer=word_tokenizer,
	                                stop_words=stop,
	                                max_df=0.9,
	                                min_df=0.1,
	                                lowercase=True)
    #builds a tf-idf matrix for the sentences
	tfidf_matrix = tfidf_vectorizer.fit_transform(sentences)
	kmeans = KMeans(n_clusters=nb_of_clusters)
	kmeans.fit(tfidf_matrix)
	clusters = collections.defaultdict(list)
	for i, label in enumerate(kmeans.labels_):
	        clusters[label].append(i)
	clusters = dict(clusters)

	for key in clusters.keys() : 
		print sentences[clusters[key][0]],len(clusters[key])
	# for cluster in range(nb_of_clusters):
	#         print "cluster ",cluster,":"
	#         for i,sentence in enumerate(clusters[cluster]):
	#                 print "\tsentence ",i,": ",sentences[sentence]

print 'satisfactionQuestionReply'
print cluster_sentences(satisfactionQuestionReply_key,15)
# print ''
# print cluster_sentences(most_ngram(satisfactionQuestionReply_message,3),5)
print ''
print ''
print 'welcomingQuestion'
print cluster_sentences(welcomingQuestion_message,15)
# print ''
# print cluster_sentences(most_ngram(welcomingQuestion_message,3),5)
print ''
print ''
print 'whyMcDonalds'
print cluster_sentences(whyMcDonalds_key,15)
# print ''
# print cluster_sentences(most_ngram(whyMcDonalds_message,3),5)

