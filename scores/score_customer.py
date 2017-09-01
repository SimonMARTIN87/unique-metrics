# -*- coding: utf-8 -*-
from pymongo import MongoClient
import pandas as pd
import numpy as np
from bson.objectid import ObjectId
import json
from datetime import timedelta, datetime, date
from pprint import pprint
from sklearn import linear_model
from sklearn import preprocessing
import sklearn.feature_selection as FS
#from ua_parser import user_agent_parser
from user_agents import parse as UAParse
import re


### MongoDB
client = MongoClient()
db = client.app64723109

conversations = db['conversations']
messages = db['messages']
dialogues = db['_dialogues']
events = db['events']
nps = db['nps']
sessions = db['sessions']


# Badly Recompute the score...
def customer_score(company,start,end) :
	if company == 'Macdo' :
		ids_company = ObjectId("58d12d7c9dab1c0004485209")
		scripts = [ObjectId("58d17ce5f8b2a3000427d26f"),ObjectId("58d4f3b1c8201d0004e31905"),ObjectId("58db5d158663ee0004ed1bee"),\
		ObjectId("58e6bd70c38a0c000454640e"),ObjectId("58e91846f7dc2c000405f4f4"),ObjectId("59009ce26f83c60004c33a98"),\
		ObjectId("590302c2cc1e4700041b0b9b"),ObjectId("59133908dad1a700048ea734")]
	if company == 'Jamba' :
		ids_company = ObjectId('591996f98a37080004bdbdda')
		scripts = [ObjectId("591998368a37080004bdbddc"),ObjectId("591a337476dce10004bf0c87"),ObjectId("591c989689f587000402db8e"),\
		ObjectId("59271a0300f28e00045655f5"),ObjectId("592842f77dd1bd0004164b27"),ObjectId("5928ac644ffef700041de24b")]
	if company == 'Halal' :
		ids_company = ObjectId('591d0580161f480004e6501a')
		scripts = [ObjectId("591d3307161f480004e650ee"),ObjectId("591debe0161f480004e6515c")]

	start = datetime.strptime(start, '%d/%m/%Y')
	end = datetime.strptime(end, '%d/%m/%Y')

	all_conversations = conversations.find({'meta.completionLevel':{'$gte':80},'meta.createdOn': {'$lt': end , '$gte': start},'company' : ids_company})
	totalLen = all_conversations.count()
	n=1
	scores_unique = []
	score_costumers = []
	for conversation in all_conversations :
		print n, ' / ', totalLen
		n+=1
		id_conv = conversation.get('_id')
		scores_unique.append(conversation.get('score'))
		all_messages = messages.find({'conversation' : id_conv})
		score_temp = 0
		score_temp2 = 0
		for m in all_messages :
			payload = m.get('payload')
			if payload is not None and payload != u"" :
				d = dialogues.find_one({'continueRef' : payload, 'script' : {'$in' : scripts}})
				if d is not None : 
					score_temp += d.get(u'score')

		score_costumers.append(score_temp)

	scores = [[scores_unique[i],score_costumers[i]] for i in range(len(scores_unique))]
	return scores

# print "building tabScore..."
# tabScore = customer_score('Macdo','1/7/2017','20/7/2017')
# print "==>OK"
# df = pd.DataFrame(tabScore, columns=['score unique.ai ', 'score costumer methode'])
# df.to_csv('score_comparisons.csv',sep=';')


def correlation_nps_score_device(company,start,end) :
	if company == 'Macdo' :
		ids_company = ObjectId("58d12d7c9dab1c0004485209")
	if company == 'Jamba' :
		ids_company = ObjectId('591996f98a37080004bdbdda')
	if company == 'Halal' :
		ids_company = ObjectId('591d0580161f480004e6501a')

	start = datetime.strptime(start, '%d/%m/%Y')
	end = datetime.strptime(end, '%d/%m/%Y')

	correl = []
	y = []
	x = []
	all_conversations = conversations.find({'company' : ids_company,'meta.exported' : True})
	totalLen = all_conversations.count()
	n=1
	sourceReg = re.compile('"origin":"([^\"]+)"')

	for conversation in all_conversations:
		print n, ' / ', totalLen
		n+=1
		score = conversation.get('score')
		date_start = conversation.get('meta').get('createdOn')
		date_end = conversation.get('meta').get('lastMessageOn')
		duration = (date_end - date_start).seconds

		day = int(date_start.weekday())
		time = int(str(date_start.time())[:2])
		id_conv = conversation.get('_id')

		#sourcing
		origin = 'website'
		refData = conversation.get('refData')
		if refData is not None:
			groups = sourceReg.findall(refData)

			if len(groups) > 0:
				origin = groups[0]
				parts = origin.split('.')
				if len(parts) >= 2 :
					origin = parts[len(parts) - 2]
					if origin in ['co','com']:
						origin = parts[len(parts) - 3]
		# UA
		user_agent = UAParse(conversation.get('userAgent'))

		device = 'Desktop'
		if user_agent.is_mobile:
			device = 'Mobile'
		elif user_agent.is_tablet:
			device = 'Tablet'

		browser = user_agent.browser.family
		if 'Mobile Safari' in browser:
			browser = 'Mobile Safari'
		
		osys = user_agent.os.family
		if 'Windows' in osys:
			osys = 'Windows'

		#sessions
		nbsessions = sessions.count({'conversation': id_conv })
		
		# sentinel??
		# returned = events.find({'conversation' : id_conv,'eventType' : 'return'}).count()
		# reminder = events.find({'conversation' : id_conv,'eventSubType': {'$in' : ['reminder1','reminder2','reminder3']}}).count()

		currNps = nps.find_one({'conversation' : id_conv})
		if currNps is not None : 
			np = currNps.get('score_value')
		else :
			np = -1

		#location
		location = conversation.get('preferedLocation')
		if location is None:
			location = 'None'

		correl.append([score,day,origin,time,np,duration,device,osys,browser, nbsessions, location.encode('utf-8')])

	return correl

# print 'build correlation CSV...'
# correl = correlation_nps_score_device('Macdo','1/7/2017','1/8/2017')

# df = pd.DataFrame(correl, columns=['score','day','origin','time','np','duration','device','osys','browser', 'nbsessions','location'])
# df.to_csv('correlation.csv',sep=';')

# print '=>Done'


#### GET CORRELATION ####
def columns_to_index(columns) :
	columns_unique = list(set(columns))
	columns_index = [columns_unique.index(element) for element in columns]
	return columns_index
##load file
correl = pd.read_csv('correlation.csv',sep=';',names=['score','day','origin','time','np','duration','device','osys','browser', 'nbsessions','location'], header=1)

## score & features
y = correl['score'].values.tolist()
correl['device'] = columns_to_index(correl['device'])
correl['browser'] = columns_to_index(correl['browser'])
correl['osys'] = columns_to_index(correl['osys'])
correl['origin'] = columns_to_index(correl['origin'])
correl['location'] = columns_to_index(correl['location'])
x = preprocessing.scale(correl.as_matrix()[:, 1:])  ## center features

# Show which features impact the most the score
featSelection = []
selection = FS.SelectKBest(FS.f_regression,k=6).fit(x,y)
featSelection.append(['f_regression']+list(selection.scores_))

selection = FS.SelectKBest(FS.f_classif, k=6).fit(x,y)
featSelection.append(['f_classif']+list(selection.scores_))

selection = FS.SelectKBest(FS.mutual_info_classif, k=6).fit(x,y)
featSelection.append(['mutual_info_classif']+list(selection.scores_))

selection = FS.SelectKBest(FS.mutual_info_regression, k=6).fit(x,y)
featSelection.append(['mutual_info_regression']+list(selection.scores_))

df = pd.DataFrame(featSelection, columns=['func','day','origin','time','np','duration','device','osys','browser', 'nbsessions','location'])
df.to_csv('feature_selection.csv', sep=';')

# Coeff in the calculation of the score
regr = linear_model.LinearRegression(normalize=True,fit_intercept = True)

for col in ['score','day','origin','time','np','duration','device','osys','browser', 'nbsessions','location']:
	x = preprocessing.scale(correl.as_matrix(columns=[col]))
	regr.fit(x,y)
	print col," => ","{:1.10f}".format(regr.score(x, y))

