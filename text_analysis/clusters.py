from nltk import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
import string, json, collections

with open('welcomingQuestion.json','r') as df :
	welcomingQuestion = json.load(df)
	welcomingQuestion_key = [d.get('keywords').encode('utf8').replace('-',' ').replace("'","") for d in welcomingQuestion]
	welcomingQuestion_key = [d.translate(None, string.punctuation) for d in welcomingQuestion_key]
	welcomingQuestion_message = [d.get('message').encode('utf8').replace('-',' ').replace("'","") for d in welcomingQuestion]
	welcomingQuestion_message = [d.translate(None, string.punctuation) for d in welcomingQuestion_message]

with open('satisfactionQuestionReply.json','r') as df :
	satisfactionQuestionReply = json.load(df)
	satisfactionQuestionReply_key = [d.get('keywords').encode('utf8').replace('-',' ').replace("'","") for d in satisfactionQuestionReply]
	satisfactionQuestionReply_key = [d.translate(None, string.punctuation) for d in satisfactionQuestionReply_key]
	satisfactionQuestionReply_message = [d.get('message').encode('utf8').replace('-',' ').replace("'","") for d in satisfactionQuestionReply]
	satisfactionQuestionReply_message = [d.translate(None, string.punctuation) for d in satisfactionQuestionReply_message]

with open('whyMcDonalds.json','r') as df :
	whyMcDonalds = json.load(df)
	whyMcDonalds_key = [d.get('keywords').encode('utf8').replace('-',' ').replace("'","") for d in whyMcDonalds]
	whyMcDonalds_key = [d.translate(None, string.punctuation) for d in whyMcDonalds_key]
	whyMcDonalds_message = [d.get('message').encode('utf8').replace('-',' ').replace("'","") for d in whyMcDonalds]
	whyMcDonalds_message = [d.translate(None, string.punctuation) for d in whyMcDonalds_message]


with open('stop_words_french.txt', 'r') as df :
	stop_w = [s.replace('\n','') for s in df.readlines()]

stop_w = [s.decode('utf8') for s in stop_w]

def word_tokenizer(text):
	stemmer = PorterStemmer()
	tokens = word_tokenize(text)
	tokens = [stemmer.stem(t) for t in tokens if t not in stop_w]
	return tokens

def cluster_sentences(sentences, nb_of_clusters=4):
	tfidf_vectorizer = TfidfVectorizer(tokenizer=word_tokenizer,
									stop_words=stop_w,
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


# print cluster_sentences(satisfactionQuestionReply_key,40)

# print cluster_sentences(welcomingQuestion_message,30)

print cluster_sentences(whyMcDonalds_key,7)


