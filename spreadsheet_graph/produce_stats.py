from pymongo import MongoClient
import pymongo
from bson.objectid import ObjectId
from bson.code import Code
import pandas as pd 
from datetime import timedelta, datetime, date
import numpy as np
import json
# from ua_parser import user_agent_parser
from user_agents import parse as UAParse
from collections import OrderedDict


client = MongoClient()
db = client.app64723109

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
	return None

### Percentage completion level
def ids_conv(start,end, company) :
	if company == 'Macdo' :
		ids_company = ObjectId("58d12d7c9dab1c0004485209")
		levels = levels_m

	if company == 'Jamba' :
		ids_company = ObjectId('591996f98a37080004bdbdda')
		levels = levels_j
	if company == 'Halal' :
		ids_company = ObjectId('591d0580161f480004e6501a')
		levels = levels_h

	ids_conv = []
	all_conversations = conversations.find({'meta.createdOn': {'$lt': end , '$gte': start},'company': ids_company})
	for conversation in all_conversations :
		ids_conv.append(conversation.get('_id'))

	return ids_conv, ids_company,levels

def count_conversations(ids_conv, ids_company, levels,start,end) :
	
	poppedup = conversations.find({'_id':{'$in':ids_conv}, "company": ids_company}).count()
	return poppedup

def count_level_reached(ids_conv, ids_company, levels,start,end) :

	# poppedup = conversations.find({'_id' : {'$in' : ids_conv}}).count()
	# started = messages.find({'$and' : [{'conversation' : {'$in' : ids_conv},'_dialogue': {'$in' : levels['0']}}]}).count()
	# level_1 = messages.find({'$and' : [{'conversation' : {'$in' : ids_conv},'_dialogue': {'$in' : levels['1']}}]}).count()
	# level_2 = messages.find({'$and' : [{'conversation' : {'$in' : ids_conv},'_dialogue': {'$in' : levels['2']}}]}).count()
	# level_3 = messages.find({'$and' : [{'conversation' : {'$in' : ids_conv},'_dialogue': {'$in' : levels['3']}}]}).count()
	# level_4 = messages.find({'$and' : [{'conversation' : {'$in' : ids_conv},'_dialogue': {'$in' : levels['4']}}]}).count()
	# level_5 = messages.find({'$and' : [{'conversation' : {'$in' : ids_conv},'_dialogue': {'$in' : levels['5']}}]}).count()
	# level_6 = messages.find({'$and' : [{'conversation' : {'$in' : ids_conv},'_dialogue': {'$in' : levels['6']}}]}).count()
	# level_7 = messages.find({'$and' : [{'conversation' : {'$in' : ids_conv},'_dialogue': {'$in' : levels['7']}}]})
	# level_8 = messages.find({'$and' : [{'conversation' : {'$in' : ids_conv},'_dialogue': {'$in' : levels['8']}}]}).count()
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
		exported += candidates.find({'_id' : l['candidate'] ,'files.cv' : {'$ne': None }}).count()

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
	
	send_cv = events.find({'$and' : [{'conversation' : {'$in' : ids_conv}, 'createdOn':{'$lt' : end, '$gt' :start}, 'eventType' : 'sendEmail', 'eventSubType' : 'for CV'}]}).count()
	opened_cv = events.find({'$and' : [{'conversation' : {'$in' : ids_conv},'createdOn':{'$lt' : end, '$gt' :start}, 'eventType' : 'openedEmail', 'eventSubType' : 'for CV'}]}).count()
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

	for event in events.find({'$and' : [{'eventType' : 'recover', "createdOn" : {'$lt' : end, '$gt' : start}}]}) :
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

	dico_conv_id = {'desktop' : [],'mobile' : [], 'tablet' : []}
	dico_can_id = {'desktop' : [],'mobile' : [], 'tablet' : []}
	dico_percentage = {}
	dico_nps = {}
	dico_sentinel = {}

	for conv in conversations.find({'_id' : {'$in' : ids_conv}}) :
		useragent = conv.get('userAgent')
		browser = user_agent_parser.ParseUserAgent(useragent).get('family')
		device_temp = user_agent_parser.ParseDevice(useragent).get('family')

		if device_temp == 'Other' and 'Mobile' not in browser:
			dico_conv_id['desktop'].append(conv.get('_id'))
			dico_can_id['desktop'].append(conv.get('candidate'))
		if 'Mobile' not in browser and device_temp != 'Other' :
			dico_conv_id['tablet'].append(conv.get('_id'))
			dico_can_id['tablet'].append(conv.get('candidate'))
		if 'Mobile' in browser :
			dico_conv_id['mobile'].append(conv.get('_id'))
			dico_can_id['mobile'].append(conv.get('candidate'))


	dico_conv_id['mobile'] = list(set(dico_conv_id['mobile']))
	dico_can_id['mobile'] = list(set(dico_can_id['mobile']))
	dico_conv_id['desktop'] = list(set(dico_conv_id['desktop']))
	dico_can_id['desktop'] = list(set(dico_can_id['desktop']))
	dico_conv_id['tablet'] = list(set(dico_conv_id['desktop']))
	dico_can_id['tablet'] = list(set(dico_can_id['tablet']))

	for key in dico_conv_id.keys() :

		started = messages.find({'$and' : [{'conversation' : {'$in' : dico_conv_id[key]} ,'_dialogue': {'$in' : levels['0']}}]}).count()
		level_1 = messages.find({'$and' : [{'conversation' : {'$in' : dico_conv_id[key]} ,'_dialogue': {'$in' : levels['1']}}]}).count()
		level_2 = messages.find({'$and' : [{'conversation' : {'$in' : dico_conv_id[key]} ,'_dialogue': {'$in' : levels['2']}}]}).count()
		level_3 = messages.find({'$and' : [{'conversation' : {'$in' : dico_conv_id[key]} ,'_dialogue': {'$in' : levels['3']}}]}).count()
		level_4 = messages.find({'$and' : [{'conversation' : {'$in' : dico_conv_id[key]} ,'_dialogue': {'$in' : levels['4']}}]}).count()
		level_5 = messages.find({'$and' : [{'conversation' : {'$in' : dico_conv_id[key]} ,'_dialogue': {'$in' : levels['5']}}]}).count()
		level_6 = messages.find({'$and' : [{'conversation' : {'$in' : dico_conv_id[key]} ,'_dialogue': {'$in' : levels['6']}}]}).count()
		level_7 = messages.find({'$and' : [{'conversation' : {'$in' : dico_conv_id[key]} ,'_dialogue': {'$in' : levels['7']}}]}).count()
		level_8 = messages.find({'$and' : [{'conversation' : {'$in' : dico_conv_id[key]} ,'_dialogue': {'$in' : levels['8']}}]}).count()
		exported = candidates.find({'$and' : [{'_id': {'$in' : dico_can_id[key]},'files.cv' : {'$ne': None }}]}).count()

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
		dico_percentage[key] = [len(dico_conv_id[key]),started,level_1, level_2, level_3, level_4, level_5, level_6, level_7, level_8,exported]

		### nps
		dico_nps[key] = [one,two,three,four,five]

		## sentinel
		dico_sentinel[key] = [send_cv,opened_cv,upload_cv,export_cv,reminder1,reminder2,reminder3,returned,recover]

	dico_percentage['indexes'] = ['PoppedUp','Started', 'level 1', 'level 2', 'level 3', 'level 4','level 5','level 6','level 7','level 8','Exported']
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
 	return finalResult;


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
			for x in range(2,9):
				res[remade]['lvl'+str(x)] = 0
			keys.append(remade)

		#start
		if conv['meta']['isStarted']:
			res[remade]['started'] += 1

		lvlFound = 0
		for l in range(0,len(levels)):
			if conv['meta']['completionLevel'] >= levels[l]:
				res[remade]['lvl'+str(l+2)] += 1
				lvlFound = l+2
			else :
				continue

		if lvlFound >= 7:
			#exported - it's here to avoid conversation exported by the sentinel
			if conv['meta']['exported']:
				res[remade]['exported'] += 1			
			
		perc =  int( (n / total)*100)
		if perc > lastPerc :
			print perc, ' %'
			lastPerc = perc
		n+=1


	volumes = []
	ratios = []

	for doc in res:
		perc = (res[doc]['poppedup']/total)*100
		if perc > 0.5:
			title = doc + ' (' + "{:2.2f}".format(perc) + " % of volume)"

			line = [title, perc ,res[doc]['poppedup'], res[doc]['started'] ]
			for x in range(2,9):
				line.append( res[doc]['lvl'+str(x)] )
			line.append(res[doc]['exported'])
			volumes.append(line)

			line = [title, res[doc]['started']/float(res[doc]['poppedup']), res[doc]['lvl2']/float(res[doc]['started']) ]
			for x in range(3,9):
				line.append( min( res[doc]['lvl'+str(x)] / float(res[doc]['lvl'+str(x-1)] ), 1 ) )
			line.append( min(res[doc]['exported'] / float(res[doc]['lvl8'])),1)
			ratios.append(line)

	return volumes, ratios

def average_conversation_time_by_level(company, start, end) :
	id_company = getCompanyId(company)
	levels = [15,20,30,45,70,80,90];
	timesByLvl = OrderedDict()
	for x in range(2,9):
		timesByLvl['Lvl'+str(x)] = []

	convs = conversations.find({'meta.createdOn': {'$lt': end , '$gte': start},'company': id_company})
	for currConv in convs:
		datesDict = currConv['meta']['completionDates']
		if len(datesDict) > 0:
			for d in datesDict:
				for l in range(0,7):
					if d['level'] == levels[l]:
						diff = d['date'] - currConv['meta']['createdOn']
						timesByLvl['Lvl'+str(l+2)].append(diff.total_seconds())

	for lvl in timesByLvl:
		serie = timesByLvl[lvl];
		currMean = np.mean(serie)
		currStd = np.std(serie)
		delta = 1

		timesByLvl[lvl] = [x for x in serie if abs(x-currMean)< (delta*currStd)]

	return timesByLvl

def time_spent_on_questions(company, start, end) :
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
