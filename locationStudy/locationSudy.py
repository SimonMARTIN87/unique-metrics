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

##funcs
def getCompanyId(company):
	if company == 'Macdo' :
		return ObjectId("58d12d7c9dab1c0004485209")
	if company == 'Jamba' :
		return ObjectId('591996f98a37080004bdbdda')
	if company == 'Halal' :
		return ObjectId('591d0580161f480004e6501a')

	if company == 'Mcdo-Bordeaux':
		return ObjectId('596e45882a581c0004936b8f')
	if company == 'Mcdo-Magny':
		return ObjectId('596f5cce97a38d000405e0d0')
	if company == 'Mcdo-Alpes':
		return ObjectId('59b7a1f762fb42000494d183')
	if company == 'Mcdo-Pontarlier':
		return ObjectId('596e38ee2a581c0004936b03')
	if company == 'Mcdo-bessin':
		return ObjectId('593663c5c14afd00040e3e11')
	if company == 'Mcdo-Nord-isere':
		return ObjectId('596e33fb2a581c0004936a77')
	if company == 'Mcdo-Marseille':
		return ObjectId('596e08f22a581c00049368e0')
	if company == 'Mcdo-Yvelines':
		return ObjectId('59ba478a50af8700040879d9')
	if company == 'Mcdo-Limoges':
		return ObjectId('59366ce4c14afd00040e3e9c')

def locationDistribution(company, start, end):
	company = getCompanyId(company);
	start = datetime.strptime(start, '%d/%m/%Y')
	end = datetime.strptime(end, '%d/%m/%Y')

	lvl3 = conversations.count({
		'meta.createdOn': {
			'$lt': end,
			'$gte': start
		},
		'company': company,
		'meta.completionLevel': {
			'$gte': 15
		},
		'appliedProfession': 'Équipier'
	})
	lvl4 = conversations.count({
		'meta.createdOn': {
			'$lt': end,
			'$gte': start
		},
		'company': company,
		'meta.completionLevel': {
			'$gte': 20
		},
		'appliedProfession': 'Équipier'
	})

	print lvl3, lvl4

	allLocations = conversations.find({
		'meta.createdOn': {
			'$lt': end,
			'$gte': start
		},
		'company': company,
		'meta.completionLevel': {
			'$gte': 15
		},
		'appliedProfession': 'Équipier'
	},{
		'preferedLocation': 1
	})
	res = {}
	for conv in allLocations:
		try:
			res[conv.get('preferedLocation')] += 1
		except Exception, e:
			res[conv.get('preferedLocation')] = 1

	print res


##params
company = 'Macdo'
start = '1/10/2017'
end = '15/10/2017'
locationDistribution(company, start, end);

start = '15/10/2017'
end = '01/11/2017'
locationDistribution(company, start, end);


