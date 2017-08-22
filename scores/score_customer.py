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
from sklearn.feature_selection import SelectKBest , f_regression
from ua_parser import user_agent_parser


### MongoDB
client = MongoClient()
db = client.test2

conversations = db['conversations']
messages = db['messages']
dialogues = db['_dialogues']
events = db['events']
nps = db['nps']
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

	all_conversations = conversations.find({'score' : {'$gt' : 0 },'meta.createdOn': {'$lt': end , '$gte': start},'company' : ids_company})
	scores_unique = []
	score_costumers = []
	for conversation in all_conversations :
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


df = pd.DataFrame(customer_score('Macdo','1/4/2017','1/7/2017'), columns=['score unique.ai ', 'score costumer methode'])
df.to_csv('score_comparisons.csv',sep=';')


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
	for conversation in conversations.find({'company' : ids_company,'meta.completedOn' : {'$ne' : None}}) :
		score = conversation.get('score')
		date_start = conversation.get('meta').get('createdOn')
		date_end = conversation.get('meta').get('completedOn')
		duration = (date_end - date_start).seconds

		day = int(date_start.weekday())
		time = int(str(date_start.time())[:2])
		id_conv = conversation.get('_id')
		source = None
		# if conversation.get('refData') is not None : 
		# 	source = conversation.get('refData')

		useragent = conversation.get('userAgent')
		browser = user_agent_parser.ParseUserAgent(useragent).get('family')
		device_temp = user_agent_parser.ParseDevice(useragent).get('family')

		if device_temp == 'Other' and 'Mobile' not in browser:
			device = 'Desktop'
		if 'Mobile' not in browser and device_temp != 'Other' :
			device = 'Tablet'
		if 'Mobile' in browser :
			device = 'Mobile'
		
		returned = events.find({'conversation' : id_conv,'eventType' : 'return'}).count()
		reminder = events.find({'conversation' : id_conv,'eventSubType': {'$in' : ['reminder1','reminder2','reminder3']}}).count()

		if nps.find_one({'conversation' : id_conv}) is not None : 
			np = int(nps.find_one({'conversation' : id_conv}).get('score_value'))
		else :
			np = -1
		
		correl.append([score,day,source,time,np,duration,device, browser, returned,reminder])

	return correl

correl = correlation_nps_score_device('Macdo','1/4/2017','1/7/2017')

df = pd.DataFrame(correl, columns=['score', 'day','source','time','nps','duration','device', 'browser', 'returned','reminder'])
df.to_csv('correlation.csv',sep=';')


#### GET CORRELATION ####
def columns_to_index(columns) :
	columns_unique = list(set(columns))
	columns_index = [columns_unique.index(element) for element in columns]
	return columns_index
##load file
correl = pd.read_csv('correlation.csv',sep=';',names=['score', 'day','source','time','nps','duration','device','browser','returned','reminder'], header=1)

## score & features
y = correl['score'].values.tolist()
del correl['source']
del correl['reminder']
correl['device'] = columns_to_index(correl['device'])
correl['browser'] = columns_to_index(correl['browser'])
x = preprocessing.scale(correl.as_matrix()[:, 1:])  ## center features

## Show which features impact the most the score
selection = SelectKBest(f_regression,k=6).fit(x,y)
print selection.scores_

## Coeff in the calculation of the score
regr = linear_model.LinearRegression(normalize=True,fit_intercept = False)
regr.fit(x,y)

print 'Coeff of [day,time,nps,duration,device,returned]', regr.coef_
