# -*- coding: utf-8 -*-
from pymongo import MongoClient
import pandas as pd
import numpy as np
from bson.objectid import ObjectId
import json
from datetime import timedelta, datetime, date
from collections import Counter
import re

### databases
client = MongoClient()
db = client.app64723109
messages = db['messages']
dialogues = db['_dialogues']
candidates = db['candidates']
conversations = db['conversations']
nps = db['nps']
events = db['events']
sessions = db['sessions']

######params
company = 'Macdo'
date_debut = '01/07/2017'
date_fin = '23/08/2017'

debut = datetime.strptime(date_debut, '%d/%m/%Y')
fin = datetime.strptime(date_fin, '%d/%m/%Y')

##funcs
def getCompanyId(company):
	if company == 'Macdo' :
		return ObjectId("58d12d7c9dab1c0004485209")
	if company == 'Jamba' :
		return ObjectId('591996f98a37080004bdbdda')
	if company == 'Halal' :
		return ObjectId('591d0580161f480004e6501a')
	return None


def create_data(company, debut, fin):
	writer = pd.ExcelWriter('Scores_'+str(company)+'.xlsx',float_format = int)

	id_comp = getCompanyId(company)

	#get all scores for LVl >=7
	total = conversations.count({'meta.createdOn': {'$lt': fin , '$gte': debut},'company' : id_comp, 'meta.completionLevel':{'$gte':80}})
	exported_convs = conversations.count({'meta.createdOn': {'$lt': fin , '$gte': debut},'company' : id_comp, 'meta.completionLevel':{'$gte':80}, 'meta.exported':True})
	all_conversations = conversations.find({'meta.createdOn': {'$lt': fin , '$gte': debut},'company' : id_comp, 'meta.completionLevel':{'$gte':80}, 'meta.exported':False})

	print total, exported_convs, all_conversations.count()

	scores = []
	distri_by_store = {}
	for doc in all_conversations:
		sc = doc['score']
		if sc != 0 and sc < 300:
			scores.append(doc['score'])
			if 'preferedLocation' in doc:
				store = doc['preferedLocation']
				if store not in distri_by_store:
					distri_by_store[store] = []

				distri_by_store[store].append(sc)

	scMin = min(scores)
	scMax = max(scores)
	frequency = np.bincount(scores)

	res = []
	for x in range(scMin,scMax+1):
		res.append({'score': x, 'frequency': frequency[x]})
	res_df = pd.DataFrame(res)
	res_df.to_excel(writer,sheet_name='score frequency',index = False)

	#formalize distri_by_store
	frequency_by_store = {}
	storesList = distri_by_store.keys()
	for store in storesList:
		frequency_by_store[store] = np.bincount(distri_by_store[store])
	storeRes = []
	for x in range(scMin, scMax+1):
		line = {'score':x}
		for store in storesList:
			if x < len(frequency_by_store[store]):
				line[store] = frequency_by_store[store][x]
			else:
				line[store] = 0
		storeRes.append(line)

	storeRes_df = pd.DataFrame(storeRes, columns=['score']+storesList)
	storeRes_df.to_excel(writer, sheet_name='score frequency by store', index=False)

	writer.save()

####RUN 
data = create_data(company, debut, fin)