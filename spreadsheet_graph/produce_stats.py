from pymongo import MongoClient
import pymongo
from bson.objectid import ObjectId
from bson.code import Code
import pandas as pd 
from datetime import timedelta, datetime, date
import numpy as np
import json
from ua_parser import user_agent_parser
from user_agents import parse as UAParse
from collections import OrderedDict
import operator
import re
import logging

client = MongoClient()
db = client.heroku_r9gxmdvq

## Levels for Macdo and Jamba
with open('levels_macdo.json','r') as df :
	levels_m = json.load(df)

with open('levels_jamba.json','r') as df :
	levels_j = json.load(df)

with open('levels_halal.json','r') as df :
	levels_h = json.load(df)

##id in ObjectId
for i in range(9) :
	levels_m[str(i)] = [ObjectId(element) for element in levels_m[str(i)]]
	levels_j[str(i)] = [ObjectId(element) for element in levels_j[str(i)]]
	levels_h[str(i)] = [ObjectId(element) for element in levels_h[str(i)]]

### databases
messages = db['messages']
dialogues = db['_dialogues']
candidates = db['candidates']
conversations = db['conversations']
nps = db['nps']
events = db['events']
sessions = db['sessions']

def getCompanyId(company):
	if company == 'Macdo' :
		return ObjectId("58d12d7c9dab1c0004485209")
	if company == 'Jamba' :
		return ObjectId('591996f98a37080004bdbdda')
	if company == 'Halal' :
		return ObjectId('591d0580161f480004e6501a')
		
	if company == 'McDo-Bessin': 
		return ObjectId('593663c5c14afd00040e3e11')
	if company == 'McDo-Bordeaux': 
		return ObjectId('596e45882a581c0004936b8f')
	if company == 'McDo-Pontarlier': 
		return ObjectId('596e38ee2a581c0004936b03')
	if company == 'McDo-Limoges': 
		return ObjectId('59366ce4c14afd00040e3e9c')
	if company == 'McDo-Yvelines': 
		return ObjectId('59ba478a50af8700040879d9')
	if company == 'McDo-Marseille': 
		return ObjectId('596e08f22a581c00049368e0')
	if company == 'McDo-Nord Isere':  
		return ObjectId('596e33fb2a581c0004936a77')
	if company == 'McDo-Alpes-de-Haute-Provence':  
		return ObjectId('59b7a1f762fb42000494d183')
	if company == 'McDo-Magny': 
		return ObjectId('596f5cce97a38d000405e0d0')
	if company == 'McDo-Beaujolais': 
		return ObjectId('5a44d76c0d61950004f57337')

	if company == 'McDo-ALLFranchises':
		return {
			'$in': [
				ObjectId('593663c5c14afd00040e3e11'),
				ObjectId('596e45882a581c0004936b8f'),
				ObjectId('596e38ee2a581c0004936b03'),
				ObjectId('59366ce4c14afd00040e3e9c'),
				ObjectId('59ba478a50af8700040879d9'),
				ObjectId('596e08f22a581c00049368e0'),
				ObjectId('596e33fb2a581c0004936a77'),
				ObjectId('59b7a1f762fb42000494d183'),
				ObjectId('596f5cce97a38d000405e0d0')
			]
		}
	
	return None

### Percentage completion level
def ids_conv(start,end, company) :
	levels = []
	ids_company = getCompanyId(company);

	ids_conv = []
	all_conversations = conversations.find({'meta.createdOn': {'$lt': end , '$gte': start},'company': ids_company})
	for conversation in all_conversations :
		ids_conv.append(conversation.get('_id'))

	return ids_conv, ids_company,levels

def count_conversations(ids_conv, ids_company, levels,start,end) :
	
	poppedup = conversations.find({'_id':{'$in':ids_conv}, "company": ids_company}).count()
	return poppedup

def count_level_reached(ids_conv, ids_company, levels,start,end) :
	levels = [15,20,30,45,70,80,90];
	poppedup = len(ids_conv)
	started = conversations.count({'_id':{'$in':ids_conv}, 'meta.isStarted':True})
	level_1 = started
	level_2 = conversations.count({'_id':{'$in':ids_conv}, 'meta.completionLevel':{'$gte':15}})
	level_3 = conversations.count({'_id':{'$in':ids_conv}, 'meta.completionLevel':{'$gte':20}})
	level_4 = conversations.count({'_id':{'$in':ids_conv}, 'meta.completionLevel':{'$gte':30}})
	level_5 = conversations.count({'_id':{'$in':ids_conv}, 'meta.completionLevel':{'$gte':45}})
	level_6 = conversations.count({'_id':{'$in':ids_conv}, 'meta.completionLevel':{'$gte':70}})
	level_7 = conversations.find({'_id':{'$in':ids_conv}, 'meta.completionLevel':{'$gte':80}})
	level_8 = conversations.count({'_id':{'$in':ids_conv}, 'meta.completionLevel':{'$gte':90}})
	
	exported = 0

	for l in level_7 :
		if l['meta']['exported']:
			exported += 1

	return [poppedup,started, level_1, level_2, level_3, level_4,level_5,level_6,level_7.count(),level_8,exported]

### NPS 
def nps_by_time(ids_conv, ids_company, levels,start,end) :

	one = nps.find({'$and' : [{'conversation' : {'$in': ids_conv},'score_value' : 1}]}).count()
	two = nps.find({'$and' : [{'conversation' : {'$in': ids_conv},'score_value' : 2}]}).count()
	three = nps.find({'$and' : [{'conversation' : {'$in': ids_conv},'score_value' : 3}]}).count()
	four = nps.find({'$and' : [{'conversation' : {'$in': ids_conv},'score_value' : 4}]}).count()
	five = nps.find({'$and' : [{'conversation' : {'$in': ids_conv},'score_value' : 5}]}).count()

	return [one,two,three,four,five]

### Sentinel
def sentinel_level(ids_conv, ids_company, levels, start, end) : 

	##CAN BE REMADE WITH ONE CALL ONLY (?)
	
	send_cv = events.find({'$and' : [{'conversation' : {'$in' : ids_conv}, 'createdOn':{'$lt' : end, '$gt' :start}, 'eventType' : 'sendMail', 'eventSubType' : 'forCV'}]}).count()
	opened_cv = events.find({'$and' : [{'conversation' : {'$in' : ids_conv},'createdOn':{'$lt' : end, '$gt' :start}, 'eventType' : 'openMail', 'eventSubType' : 'forCV'}]}).count()
	upload_cv = events.find({'$and' : [{'conversation' : {'$in' : ids_conv},'createdOn':{'$lt' : end, '$gt' :start}, 'eventType' : 'upload'}]}).count()
	export_cv = events.find({'$and' : [{'conversation' : {'$in' : ids_conv},'createdOn':{'$lt' : end, '$gt' :start}, 'eventType' : 'export'}]}).count()
	reminder1 = events.find({'$and' : [{'conversation' : {'$in' : ids_conv},'createdOn':{'$lt' : end, '$gt' :start}, 'eventSubType' : 'reminder1'}]}).count()
	reminder2 = events.find({'$and' : [{'conversation' : {'$in' : ids_conv},'createdOn':{'$lt' : end, '$gt' :start}, 'eventSubType' : 'reminder2'}]}).count()
	reminder3 = events.find({'$and' : [{'conversation' : {'$in' : ids_conv},'createdOn':{'$lt' : end, '$gt' :start}, 'eventSubType' : 'reminder3'}]}).count()
	returned = events.find({'$and' : [{'conversation' : {'$in' : ids_conv},'createdOn':{'$lt' : end, '$gt' :start}, 'eventType' : 'return' }]}).count()
	recover = events.find({'$and' : [{'conversation' : {'$in' : ids_conv},'createdOn':{'$lt' : end, '$gt' :start}, 'eventType' : 'recover'}]}).count()

	return [send_cv,opened_cv,upload_cv,export_cv,reminder1, reminder2, reminder3,returned,recover]

### Time spent by sessions and opened question
def time_by_session(ids_conv, ids_company, levels,start,end) : 
	duration,welcomingQuestion, satisfactionQuestion, satisfactionQuestionReply, whyMcDonalds, unhappyClientQuestionReply = 0,0,0,0,0,0
	session_count,welcomingQuestion_count, satisfactionQuestion_count, satisfactionQuestionReply_count, whyMcDonalds_count,\
	unhappyClientQuestionReply_count = 0,0,0,0,0,0

	for session in sessions.find({'dateStart' : {'$lt' : end, '$gt' : start}}) :
		duration += (session.get('dateEnd') - session.get('dateStart')).seconds/60
		session_count +=1
		# for message in messages.find({'$and' : [{'session' : session.get('_id'), 'atsValueName' : {'$in' : ["welcomingQuestion", "satisfactionQuestionReply",\
		# 	"whyMcDonalds", "satisfactionQuestion", "unhappyClientQuestionReply"]}}]}) : 
		# 	if message.get('atsValueName') == 'welcomingQuestion' :
		# 		welcomingQuestion += (message.get('meta').get('answeredOn') - message.get('meta').get('askedOn')).seconds/60
		# 		welcomingQuestion_count += 1

		# 	if message.get('atsValueName') == 'satisfactionQuestion' :
		# 		satisfactionQuestion += (message.get('meta').get('answeredOn') - message.get('meta').get('askedOn')).seconds/60
		# 		satisfactionQuestion_count +=1

		# 	if message.get('atsValueName') == 'satisfactionQuestionReply' :
		# 		satisfactionQuestionReply += (message.get('meta').get('answeredOn') - message.get('meta').get('askedOn')).seconds/60
		# 		satisfactionQuestionReply_count +=1

		# 	if message.get('atsValueName') == 'whyMcDonalds' :
		# 		whyMcDonalds += (message.get('meta').get('answeredOn') - message.get('meta').get('askedOn')).seconds/60
		# 		whyMcDonalds_count +=1

		# 	if message.get('atsValueName') == 'unhappyClientQuestionReply':
		# 		unhappyClientQuestionReply += (message.get('meta').get('answeredOn') - message.get('meta').get('askedOn')).seconds/60
		# 		unhappyClientQuestionReply_count +=1

	duration = duration/(session_count + 1e-17)
	# welcomingQuestion = welcomingQuestion/(welcomingQuestion_count + 1e-17)
	# satisfactionQuestion = satisfactionQuestion/(satisfactionQuestion_count + 1e-17)
	# satisfactionQuestionReply = satisfactionQuestionReply/(satisfactionQuestionReply_count + 1e-17)
	# whyMcDonalds = whyMcDonalds/(whyMcDonalds_count + 1e-17)
	# unhappyClientQuestionReply = unhappyClientQuestionReply/(unhappyClientQuestionReply_count + 1e-17)
	
	return [duration,welcomingQuestion, whyMcDonalds, satisfactionQuestion, satisfactionQuestionReply, unhappyClientQuestionReply]

## At which level people come back
def which_return(ids_conv, ids_company, levels,start, end) :
	returned_on_JO = [0]*6
	returned_on_J1 = [0]*6
	returned_on_J2 = [0]*6
	returned_on_J3 = [0]*6

	listEvents = events.find({'$and' : [{'eventType' : 'recover', "createdOn" : {'$lt' : end, '$gt' : start}}]})
	totalNb = str(listEvents.count())
	n=1
	print "which_return"
	logging.info("which_return")
	for event in listEvents:
		print str(n)+' / '+totalNb
		logging.info('%s on %s',n,totalNb)
		n += 1
		id_conv = event.get('conversation')
		if id_conv in ids_conv :
			date_event = event.get('createdOn')

			returned = -1
			message = messages.find({'$and' : [{'conversation' : id_conv, 'meta.askedOn' : {'$gt':date_event},'_dialogue' : {'$ne': None}}]}).sort("meta.askedOn",pymongo.ASCENDING)
			for i in range(3,9) : 
				if message.count() > 0: 
					if message[0].get('_dialogue') in levels[str(i)] :
						returned = i
						break
			
			message =  messages.find({'$and' : [{'conversation' : id_conv, 'meta.askedOn' : {'$lt':date_event}}]}).sort("meta.askedOn",pymongo.DESCENDING)
			if message.count()>0: 
				datb = message[0].get('meta').get('askedOn')
				delta = date_event.weekday() - datb.weekday()

			if returned >= 3 : 
				j = returned - 3
				if delta == 0 : 
					returned_on_JO[j] += 1
				if delta == 1 : 
					returned_on_J1[j] += 1
				if delta == 2 : 
					returned_on_J2[j] += 1
				if delta == 3 : 
					returned_on_J3[j] += 1

	return [returned_on_JO,returned_on_J1, returned_on_J2,returned_on_J3]

### Information by browser
def conv_by_browser(ids_conv, ids_company, levels, start, end) :

	dico_conv_id = {'Desktop' : [],'Mobile' : [], 'Tablet' : []}
	dico_percentage = {}
	dico_nps = {}
	dico_sentinel = {}

	listConvs = conversations.find({'_id' : {'$in' : ids_conv}})
	totalNb = listConvs.count()
	n=1
	for conv in  listConvs:
		print n, ' / ', totalNb
		n+=1
		user_agent = UAParse(conv['userAgent'])

		if user_agent.is_mobile:
			dico_conv_id['Mobile'].append(conv.get('_id'))
		elif user_agent.is_tablet:
			dico_conv_id['Tablet'].append(conv.get('_id'))
		else:
			dico_conv_id['Desktop'].append(conv.get('_id'))
	
	levels = [15,20,30,45,70,80,90];
	for key in dico_conv_id.keys() :
		started = conversations.count({'_id':{'$in':dico_conv_id[key]}, 'meta.isStarted':True})
		level_1 = conversations.count({'_id':{'$in':dico_conv_id[key]}, 'meta.completionLevel':{'$gt':0}})
		level_2 = conversations.count({'_id':{'$in':dico_conv_id[key]}, 'meta.completionLevel':{'$gte':15}})
		level_3 = conversations.count({'_id':{'$in':dico_conv_id[key]}, 'meta.completionLevel':{'$gte':20}})
		level_4 = conversations.count({'_id':{'$in':dico_conv_id[key]}, 'meta.completionLevel':{'$gte':30}})
		level_5 = conversations.count({'_id':{'$in':dico_conv_id[key]}, 'meta.completionLevel':{'$gte':45}})
		level_6 = conversations.count({'_id':{'$in':dico_conv_id[key]}, 'meta.completionLevel':{'$gte':70}})
		level_7 = conversations.count({'_id':{'$in':dico_conv_id[key]}, 'meta.completionLevel':{'$gte':80}})
		level_8 = conversations.count({'_id':{'$in':dico_conv_id[key]}, 'meta.completionLevel':{'$gte':90}})
		exported = conversations.count({'_id':{'$in':dico_conv_id[key]}, 'meta.exported':True})

		## nps
		one = nps.find({'$and' : [{'conversation' : {'$in': dico_conv_id[key]},'score_value' : 1}]}).count()
		two = nps.find({'$and' : [{'conversation' : {'$in': dico_conv_id[key]},'score_value' : 2}]}).count()
		three = nps.find({'$and' : [{'conversation' : {'$in': dico_conv_id[key]},'score_value' : 3}]}).count()
		four = nps.find({'$and' : [{'conversation' : {'$in': dico_conv_id[key]},'score_value' : 4}]}).count()
		five = nps.find({'$and' : [{'conversation' : {'$in': dico_conv_id[key]},'score_value' : 5}]}).count()

		## sentinel conversion
		send_cv = events.find({'$and' : [{'conversation' : {'$in' : dico_conv_id[key]},'eventType' : "sendMail", 'eventSubType' : 'for CV'}]}).count()
		opened_cv = events.find({'$and' : [{'conversation' : {'$in' : dico_conv_id[key]},'eventType' : "openMail", 'eventSubType' : 'for CV'}]}).count()
		upload_cv = events.find({'$and' : [{'conversation' : {'$in' : dico_conv_id[key]},'eventType' : "upload"}]}).count()
		export_cv = events.find({'$and' : [{'conversation' : {'$in' : dico_conv_id[key]},'eventType' : "export"}]}).count()
		reminder1 = events.find({'$and' : [{'conversation' : {'$in' : dico_conv_id[key]},'eventType' : "sendMail", 'eventSubType' : 'reminder1'}]}).count()
		reminder2 = events.find({'$and' : [{'conversation' : {'$in' : dico_conv_id[key]},'eventType' : "sendMail", 'eventSubType' : 'reminder2'}]}).count()
		reminder3 = events.find({'$and' : [{'conversation' : {'$in' : dico_conv_id[key]},'eventType' : "sendMail", 'eventSubType' : 'reminder3'}]}).count()
		returned = events.find({'$and' : [{'conversation' : {'$in' : dico_conv_id[key]},'eventType' : "return"}]}).count()
		recover = events.find({'$and' : [{'conversation' : {'$in' : dico_conv_id[key]},'eventType' : "recover"}]}).count()


		### conversion level
		dico_percentage[key] = [len(dico_conv_id[key]),started,level_1, level_2, level_3, level_4, level_5, level_6, level_7, exported, level_8]

		### nps
		dico_nps[key] = [one,two,three,four,five]

		## sentinel
		dico_sentinel[key] = [send_cv,opened_cv,upload_cv,export_cv,reminder1,reminder2,reminder3,returned,recover]

	dico_percentage['indexes'] = ['PoppedUp','Started', 'level 1', 'level 2', 'level 3', 'level 4','level 5','level 6','level 7','Exported','level 8']
	dico_nps['indexes'] = ['1 star', '2 stars', '3 stars', '4 stars','5 stars']
	dico_sentinel['indexes'] = ['send_cv','opened_cv','upload','export','reminder1','reminder2','reminder3','return','recover']
	
	return dico_percentage, dico_nps, dico_sentinel

def return_with_new_conv(ids_conv, ids_company, levels, start, end) :
	ids_candidates_company = []
	for conv in conversations.find({'_id' : {'$in' : ids_conv}}) :
		ids_candidates_company.append(conv.get('candidate'))

	ids_candidates_return = []
	emails = []
	for candidate in candidates.find({'$and' : [{'_id' : {'$in' : ids_candidates_company},'contact.email' : {'$ne' : None}}]}):
		email = candidate.get('contact').get('email')
		if email not in emails :
			emails.append(email)
		else :
			ids_candidates_return.append(candidate.get('_id'))

	nb_candidates_return = len(ids_candidates_return)
	nb_candidates_unique = len(emails)
	nb_candidates_total = len(ids_candidates_company)

	return [nb_candidates_return, nb_candidates_unique, nb_candidates_total]

source_mapper = Code("""
		function () {
			if (this.refData) {
				var origin = this.refData.match(/"origin":"([^\"]+)"/);
				if (origin) {
					origin = origin[1];
					var parts = origin.split('.');
					if (parts.length >= 2) {
						origin = parts[parts.length - 2];
						if (origin === 'co' || origin === 'com') {
							origin = parts[parts.length - 3];
						}
					}
				} else {
					origin = 'website';
				}
				emit(origin ,1);
			} else {
				emit('website' ,1);
			}
		}
	""")

source_reducer = Code("""
		function (key, value) {
			var total = 0;
          	for (var i = 0; i < value.length; i++) {
        	    total += value[i];
        	}
            return parseInt(total);
		}
	""")

device_mapper = Code("""
		function () {
			var regex = /Mobile|iP(hone|od)|Android|BlackBerry|IEMobile|Kindle|NetFront|Silk-Accelerated|(hpw|web)OS|Fennec|Minimo|Opera M(obi|ini)|Blazer|Dolfin|Dolphin|Skyfire|Zune/;
			if (regex.test(this.userAgent)) {
				emit('mobile', 1);
			} else {
				if (/Tablet/.test(this.userAgent)) {
					emit('tablet',1);
				} else {
					emit('desktop',1);
				}
			}
		}
	""")



def convs_by_source(ids_conv, ids_company, levels, start, end) :
	results = conversations.map_reduce(source_mapper, source_reducer, "my_res", query = {'_id':{'$in': ids_conv}} )
	finalResult = [];
 	for doc in results.find():
 		finalResult.append(doc);
 	return finalResult;

def lvl7_by_source(ids_conv, ids_company, levels, start, end) :
	results = conversations.map_reduce(source_mapper, source_reducer, "my_res", query = {'_id':{'$in': ids_conv}, 'meta.completionLevel':{'$gte':80}} )
	finalResult = [];
 	for doc in results.find():
 		finalResult.append(doc);
 	return finalResult;


def convs_by_device(ids_conv, ids_company, levels, start, end) :
	results = conversations.map_reduce(device_mapper, source_reducer, "my_res", query = {'_id':{'$in': ids_conv}} )
	finalResult = [];
 	for doc in results.find():
 		finalResult.append(doc);
 	return finalResult;

def lvl7_by_device(ids_conv, ids_company, levels, start, end) :
 	results = conversations.map_reduce(device_mapper, source_reducer, "my_res", query = {'_id':{'$in': ids_conv}, 'meta.completionLevel':{'$gte':80}} )
	finalResult = [];
 	for doc in results.find():
 		finalResult.append(doc);
 	return finalResult;

def exported_by_device(ids_conv, ids_company, levels, start, end) :
 	results = conversations.map_reduce(device_mapper, source_reducer, "my_res", query = {'_id':{'$in': ids_conv}, 'meta.exported':True} )
	finalResult = [];
 	for doc in results.find():
 		finalResult.append(doc);
 	return finalResult

def levels_by_source(company, start, end) :
 	id_comp = getCompanyId(company)
 	res = {}
 	total = 0
 	poppedUp = conversations.map_reduce(source_mapper, source_reducer, "my_res", query= {'meta.createdOn': {'$lt': end , '$gte': start}, 'company':id_comp} ).find()
 	for doc in poppedUp:
 		res[doc[u"_id"]] = {
 			'PoppedUp': doc[u"value"]
 		}
 		total += doc[u"value"]
 	started = conversations.map_reduce(source_mapper, source_reducer, "my_res", query= {'meta.createdOn': {'$lt': end , '$gte': start}, 'company':id_comp, 'meta.isStarted':True} ).find()
 	for doc in started:
 		res[doc[u"_id"]]['Started'] = doc[u"value"]
 	lvl1 = conversations.map_reduce(source_mapper, source_reducer, "my_res", query= {'meta.createdOn': {'$lt': end , '$gte': start}, 'company':id_comp, 'meta.completionLevel':{'$gt':0} } ).find()
 	for doc in lvl1:
 		res[doc[u"_id"]]['Lvl1'] = doc[u"value"]

 	levels = [15,20,30,45,70,80,90];
 	for x in range(2,9):
 		table = conversations.map_reduce(source_mapper, source_reducer, "my_res", query= {'meta.createdOn': {'$lt': end , '$gte': start}, 'company':id_comp, 'meta.completionLevel':{'$gte':levels[x-2]} } ).find()
 		for doc in table:
 			res[doc[u"_id"]]['Lvl'+str(x)] = doc[u"value"]

 # 	###keep only the 5 major ones
	percOfVolume = {}
	for doc in res.keys():
		percOfVolume[doc] = (res[doc]['PoppedUp']/total)*100

	sortedPerc = sorted(percOfVolume.items(), key=operator.itemgetter(1))
	sortedPerc.reverse()
	sortedPerc = sortedPerc[:6]

	##remove sorted from dict
	totalPerc = 0
	for (doc,p) in sortedPerc:
		percOfVolume.pop(doc)
		totalPerc += p
	##group others
	others = {}
	for doc in percOfVolume.keys():
		for k in res[doc].keys():
			if k in others.keys():
				others[k] += res[doc][k]
			else:
				others[k] = res[doc][k]
	sortedPerc.append(('others',100 - totalPerc))

	res['others'] = others
	ratios = []

	for (doc,p) in sortedPerc:
		title = doc + ' (' + "{:2.2f}".format(p) + " % of volume)"

		try:
			staOnPop = res[doc]['Started']/float(res[doc]['PoppedUp'])
		except Exception, e:
			staOnPop = 0

		try:
			l1OnSta = res[doc]['Lvl1']/float(res[doc]['Started'])
		except Exception, e:
			l1OnSta = 0
		line = {
			'name':title, 
			'Started / PoppedUp':staOnPop,
			'Lvl1 / Started':l1OnSta
		}
		for x in range(2,8):
			try:
				val = min( res[doc]['Lvl'+str(x)] / float(res[doc]['Lvl'+str(x-1)] ), 1 )
				line['Lvl'+str(x)+' / Lvl'+str(x-1)] = val
			except Exception, e:
				line['Lvl'+str(x)+' / Lvl'+str(x-1)] = 0
		ratios.append(line)

	return ratios


def volume_by_UA(ids_conv, ids_company, levels, start, end) :
	nbOfConv = len(ids_conv)
	convs = conversations.find({'_id':{'$in': ids_conv}})

	res = {}

	for conv in convs:
		useragent = conv.get('userAgent')
		parsed = user_agent_parser.Parse(useragent)
		os = parsed['os']['family']
		if 'Windows' in os:
			os = 'Windows'
		remade = os + ' : ' + parsed['user_agent']['family']

		if remade in res.keys() :
			res[remade] += 1
		else :
			res[remade] = 1

	resKeys = sorted(res, key=res.get, reverse=True)
	resKeys = resKeys[:6]
	newRes = [{'_id':k, 'value': (float(res[k])/float(nbOfConv) * 100)} for k in resKeys]
	return newRes

def safari_version_stats(ids_conv, ids_company, levels, start, end) :
	nbOfConv = len(ids_conv)
	versionRE = re.compile('Version/(\S+)')
	convs = conversations.find({'_id':{'$in': ids_conv}})
	res = {}
	for conv in convs:
		useragent = conv.get('userAgent')
		parsed = user_agent_parser.Parse(useragent);
		if 'Safari' in parsed['user_agent']['family'] :
			strRes = parsed['user_agent']['family']+' : '+parsed['user_agent']['major'] + '.'+parsed['user_agent']['minor']
			if strRes in res.keys():
				res[strRes] += 1
			else :
				res[strRes] = 1
	newRes = [{'_id':k, 'value': res[k]} for k in res.keys()]
	return newRes




def volume_lvl7_by_UA(ids_conv, ids_company, levels, start, end) :
	nbOfConv = conversations.count({'_id':{'$in': ids_conv}, 'meta.completionLevel':{'$gte':80}})
	convs = conversations.find({'_id':{'$in': ids_conv}, 'meta.completionLevel':{'$gte':80}})

	res = {}

	for conv in convs:
		useragent = conv.get('userAgent')
		parsed = user_agent_parser.Parse(useragent)
		os = parsed['os']['family']
		if 'Windows' in os:
			os = 'Windows'
		remade = os + ' : ' + parsed['user_agent']['family']

		if remade in res.keys() :
			res[remade] += 1
		else :
			res[remade] = 1

	resKeys = sorted(res, key=res.get, reverse=True)
	resKeys = resKeys[:6]
	newRes = [{'_id':k, 'value': (float(res[k])/float(nbOfConv) * 100)} for k in resKeys]
	return newRes

def volume_exp_by_UA(ids_conv, ids_company, levels, start, end) :
	nbOfConv = conversations.count({'_id':{'$in': ids_conv}, 'meta.exported':True})
	convs = conversations.find({'_id':{'$in': ids_conv}, 'meta.exported':True})

	res = {}

	for conv in convs:
		useragent = conv.get('userAgent')
		parsed = user_agent_parser.Parse(useragent)
		os = parsed['os']['family']
		if 'Windows' in os:
			os = 'Windows'
		remade = os + ' : ' + parsed['user_agent']['family']

		if remade in res.keys() :
			res[remade] += 1
		else :
			res[remade] = 1

	resKeys = sorted(res, key=res.get, reverse=True)
	resKeys = resKeys[:6]
	newRes = [{'_id':k, 'value': (float(res[k])/float(nbOfConv) * 100)} for k in resKeys]
	return newRes

def candidats_unique_exported(company, start, end) :
	id_company = getCompanyId(company)
	exported = list(conversations.find({'meta.createdOn': {'$lt': end , '$gte': start},'company': id_company,'meta.exported':True},{'candidate':True}))
	
	candidateIdList = []
	for exp in exported:
		candidateIdList.append(exp.get('candidate'))

	candidateList = candidates.find({'_id':{'$in': candidateIdList}})
	res = {}
	for cand in candidateList:
		email = cand['contact']['email']
		if email in res.keys():
			res[email] += 1
		else :
			res[email] = 1

	freq = {
		'1 candidature':0,
		'2-4 candidatures':0,
		'5-10 candidatures':0,
		'10+ candidatures':0
	}
	for mail in res.keys():
		nb = res[mail]
		if nb > 1:
			if nb > 4 :
				if nb > 10 :
					freq['10+ candidatures'] += 1
				else:
					freq['5-10 candidatures'] += 1
			else :
				freq['2-4 candidatures'] += 1
		else :
			freq['1 candidature'] += 1

	return res, freq

def average_conversion_by_UA(company, start, end):
	id_company = getCompanyId(company)

	levels = [15,20,30,45,70,80,90];

	poppedup = list(conversations.find({'meta.createdOn': {'$lt': end , '$gte': start},'company': id_company}))

	res = {}
	keys = []
	n=1
	total = float(len(poppedup))
	lastPerc = -1
	for conv in poppedup:
		user_agent = UAParse(conv['userAgent'])

		remade = user_agent.os.family
		if 'Windows' in remade:
			remade = 'Windows'

		if user_agent.is_mobile:
			remade = 'Mobile / '+remade
		elif user_agent.is_tablet:
			remade = 'Tablet / '+remade
		elif user_agent.is_pc:
			remade = 'Desktop / '+remade
		else:
			remade = 'Other / '+remade

		family = user_agent.browser.family
		if 'Mobile Safari' in family:
			family = 'Mobile Safari'
		remade += ' / '+ family

		# pop
		if remade in keys:
			res[remade]['poppedup'] += 1
		else:
			res[remade] = {
				'poppedup': 1,
				'started':0,
				'exported':0
			}
			for x in range(1,9):
				res[remade]['lvl'+str(x)] = 0
			keys.append(remade)

		#start
		if conv['meta']['isStarted']:
			res[remade]['started'] += 1
			mFound = messages.count({'conversation': conv['_id']})
			if mFound > 1:
				res[remade]['lvl1'] += 1

		lvlFound = 0
		

		for l in range(0,len(levels)):
			try:
				if conv['meta']['completionLevel'] >= levels[l]:
					res[remade]['lvl'+str(l+2)] += 1
					lvlFound = l+2
				else :
					continue
			except Exception, e:
				continue
			

		if lvlFound >= 7:
			#exported - it's here to avoid conversation exported by the sentinel
			if conv['meta']['exported']:
				res[remade]['exported'] += 1			
			
		perc =  int( (n / total)*100)
		print n, '/', total
		logging.info('%s on %s',n,total)
		if perc > lastPerc :
			print perc, ' %'
			lastPerc = perc
		n+=1


	volumes = []
	ratios = []

	#keep only the 5 major ones
	percOfVolume = {}
	for doc in keys:
		percOfVolume[doc] = (res[doc]['poppedup']/total)*100

	sortedPerc = sorted(percOfVolume.items(), key=operator.itemgetter(1))
	sortedPerc.reverse()
	sortedPerc = sortedPerc[:5]

	#remove sorted from dict
	totalPerc = 0
	for (doc,p) in sortedPerc:
		percOfVolume.pop(doc)
		totalPerc += p
	#group others
	others = {}
	for doc in percOfVolume.keys():
		for k in res[doc].keys():
			if k in others.keys():
				others[k] += res[doc][k]
			else:
				others[k] = res[doc][k]
	sortedPerc.append(('others',100 - totalPerc))

	res['others'] = others


	for (doc,p) in sortedPerc:
		title = doc + ' (' + "{:2.2f}".format(p) + " % of volume)"

		line = [title, p ]
		try:
		 	line.append(res[doc]['poppedup']);
		except Exception, e:
		 	line.append(0);

		try:
		 	line.append(res[doc]['started']);
	 	except Exception, e:
		 	line.append(0);
		
		for x in range(1,9):
			try:
				line.append( res[doc]['lvl'+str(x)] )
			except Exception, e:
				line.append(0);
			
		try:
			line.append(res[doc]['exported'])
		except Exception, e:
			line.append(0);
		
		volumes.append(line)

		staOnPop = 0
		l2OnSta = 0
		try:
			staOnPop = res[doc]['started']/float(res[doc]['poppedup'])
		except Exception, e:
			staOnPop = 0
			
		try:
			l2OnSta = res[doc]['lvl1']/float(res[doc]['started'])
		except Exception, e:
			l2OnSta = 0
			
		line = [title, staOnPop , l2OnSta ]
		for x in range(2,8):
			try:
				line.append( min( res[doc]['lvl'+str(x)] / float(res[doc]['lvl'+str(x-1)] ), 1 ) )
			except Exception, e:
				line.append(0)

		try:
			line.append( min(res[doc]['exported'] / float(res[doc]['lvl7']),1))
		except Exception, e:
			line.append(0)
		ratios.append(line)

	return volumes, ratios

def average_conversation_time_by_level(company, start, end) :
	id_company = getCompanyId(company)
	# levels = [15,20,30,45,70,80,90];
	levels = [15,20,40,50,70,80,90];
	timesByLvl = OrderedDict()
	for x in range(2,9):
		timesByLvl['Lvl'+str(x)] = []

	convs = conversations.find({'meta.createdOn': {'$lt': end , '$gte': start},'company': id_company})
	for currConv in convs:
		try:
			datesDict = currConv['meta']['completionDates']
			if len(datesDict) > 0:
				for d in datesDict:
					for l in range(0,7):
						if d['level'] == levels[l]:
							diff = d['date'] - currConv['meta']['createdOn']
							timesByLvl['Lvl'+str(l+2)].append(diff.total_seconds())
		except Exception, e:
			continue
		
	for lvl in timesByLvl:
		serie = timesByLvl[lvl];
		currMean = np.mean(serie)
		currStd = np.std(serie)
		delta = 1

		timesByLvl[lvl] = [x for x in serie if abs(x-currMean)< (delta*currStd)]

	return timesByLvl

def time_spent_on_questions(company, start, end) :
	logging.info('time_spent_on_questions')
	id_company = getCompanyId(company)

	#get all conversations
	ids_conv = conversations.find({'meta.createdOn': {'$lt': end , '$gte': start},'company': id_company},{'_id':True})
	conversations_list = []
	for c in ids_conv:
		conversations_list.append(c['_id'])

	#get all questions from the conversations set
	messagesList = messages.find({'conversation':{'$in':conversations_list}, '_dialogue':{'$ne':None}})
	print '***',messagesList.count()

	for mess in messagesList:
		answer = messages.find_one({'message':mess['_id']})
		if answer != None :
			ansDate = answer['']

def nps_by_device(company, start, end) : 
	print 'nps_by_device'
	logging.info('nps_by_device')
	id_company = getCompanyId(company)

	ids_conv = conversations.find({'meta.createdOn': {'$lt': end , '$gte': start},'company': id_company},{'_id':True, 'userAgent':True})
	results = {}
	totalNb = float(ids_conv.count())
	n = 0
	perc = 0

	for conv in ids_conv:
		#first, is there an associated nps?
		vote = nps.find_one({'conversation':conv['_id']})
		if vote:
			#...if so, analyse userAgent
			user_agent = UAParse(conv['userAgent'])
			device = 'Other'
			if user_agent.is_mobile:
				device = 'Mobile'
			elif user_agent.is_tablet:
				device = 'Tablet'
			elif user_agent.is_pc:
				device = 'Desktop'

			if device not in results.keys():
				results[device] = {
					'1 stars':0,
					'2 stars':0,
					'3 stars':0,
					'4 stars':0,
					'5 stars':0
				}
			results[device][str(vote['score_value'])+' stars'] += 1
		x = int((n / totalNb)*100)
		if x > perc:
			print str(x)+' %'
			perc = x
		n+=1

	return results


