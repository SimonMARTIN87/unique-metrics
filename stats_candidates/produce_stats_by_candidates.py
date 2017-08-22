# -*- coding: utf-8 -*-
from pymongo import MongoClient
import pandas as pd
from bson.objectid import ObjectId
import json
from datetime import timedelta, datetime, date
from pprint import pprint

### MongoDB
client = MongoClient()
db = client.test2

candidates = db['candidates']
conversations = db['conversations']
messages = db['messages']
sessions = db['sessions']

## candidates Macdo and JJ
df_macdo= pd.read_excel('GenEmbaucheReportV2.xlsx',)

emails_macdo = df_macdo['Unnamed: 9'].values.tolist()
emails_jamba = []
emails_halal = []

def recruted_by_chat_informations(company) : 
	if company == 'Macdo' :
		ids_company = ObjectId("58d12d7c9dab1c0004485209")
		emails = emails_macdo

	if company == 'Jamba' :
		ids_company = ObjectId('591996f98a37080004bdbdda')
		emails = emails_jamba

	if company == 'Halal' :
		ids_company = ObjectId('591d0580161f480004e6501a')
		emails = emails_halal

	email_r=[]
	nb_from_chat,nb_candidates= 0,0
	for candidate in candidates.find({'contact.email' : {'$ne' : None}, 'files.cv' : {'$ne' : None}}) :
		email = candidate.get('contact').get('email')
		nb_candidates += 1
		if email in emails :
			if email not in email_r : 
				email_r.append(email)
			else :
				nb_candidates -= 1

	email_r = list(set(email_r))
	return [len(email_r),len(emails), nb_candidates]

def average_time_recruted(company) : 
	if company == 'Macdo' :
		ids_company = ObjectId("58d12d7c9dab1c0004485209")
		emails = emails_macdo

	if company == 'Jamba' :
		ids_company = ObjectId('591996f98a37080004bdbdda')
		emails = emails_jamba

	if company == 'Halal' :
		ids_company = ObjectId('591d0580161f480004e6501a')
		emails = emails_halal

	nb_from_chat,average_time= 0,0
	for candidate in candidates.find({'contact.email' : {'$ne' : None}, 'files.cv' : {'$ne' : None}}) :
		email = candidate.get('contact').get('email')
		if email in emails :
			conv_id = conversations.find_one({'candidate' : candidate.get('_id')}).get('_id')
			session_id = messages.find_one({'conversation' : conv_id}).get('session')
			session = sessions.find_one({'_id' : session_id})
			duration = session.get('dateEnd') - session.get('dateStart')
			average_time += duration.seconds
			nb_from_chat += 1

	return average_time/((nb_from_chat + 1e-17)*60)

def telephone_number(company) :
	if company == 'Macdo' :
		ids_company = ObjectId("58d12d7c9dab1c0004485209")
		tel = ['0','33','+33','wrong', 'all']
		nb_tels = [0]*4

		ids_can =[conv.get('candidate') for conv in conversations.find({'company' : ids_company})]
		all_canditates = candidates.find({'$and' : [{'_id' :{ '$in' : ids_can}, 'contact.phone' : {'$ne' : None}}]})

		nb_candidates = all_canditates.count()
		for candidate in all_canditates:
			phone  = candidate.get('contact').get('phone')
			phone = phone.replace('(','').replace(')','').replace('-','').replace(' ','')
			if phone[0] == tel[0] and len(phone) == 10:
				if phone[1] != '0' :  
					nb_tels[0] += 1
				else : 
					nb_tels[tel.index('wrong')] += 1

			elif phone[:2] == tel[1] and len(phone) == 11 :
				nb_tels[1] += 1

			elif phone[:3] == tel[2] and len(phone) == 12 :
				nb_tels[2] += 1

			else :
				nb_tels[tel.index('wrong')] += 1

		nb_tels.append(nb_candidates)
		return 'identifiant', tel, nb_tels

	if company == 'Jamba' :
		ids_company = ObjectId('591996f98a37080004bdbdda')
		length = [10,9,11,'wrong', 'all']
		nb_tels = [0]*4
	if company == 'Halal' :
		ids_company = ObjectId('591d0580161f480004e6501a')
		length = [10,9,11,'wrong', 'all']
		nb_tels = [0]*4

	
	ids_can =[conv.get('candidate') for conv in conversations.find({'company' : ids_company})]
	all_canditates = candidates.find({'$and' : [{'_id' :{ '$in' : ids_can}, 'contact.phone' : {'$ne' : None}}]})

	nb_candidates = all_canditates.count()
	for candidate in all_canditates:
		phone  = candidate.get('contact').get('phone')
		phone = phone.replace('(','').replace(')','').replace('-','').replace(' ','')
		if len(phone) == length[0] : 
			nb_tels[0] += 1

		elif len(phone) == length[1] :
			nb_tels[1] += 1

		elif len(phone) == length[2] :
			if '+' in phone : 
				nb_tels[2] += 1
			else : 
				nb_tels[length.index('wrong')] += 1
		else :
			nb_tels[length.index('wrong')] += 1

	nb_tels.append(nb_candidates)
	return 'longueur', length, nb_tels


############################################################## Results ##############################################################
### Number of people recruted
nb_email_r, nb_emails , nb_candidates = recruted_by_chat_informations('Macdo') 

print 'Number of people recruted: ', nb_email_r
print "Number of people in McDonald's spreadsheet: ", nb_email
print 'Number of candidates with CV in DB: ', nb_candidates

### Average time spent by chat
print "Time spent in average by candidates recruted by McDonald's: ", average_time_recruted('Macdo')
print "Time spent in average by candidates recruted by Jamba Juice: ", average_time_recruted('Jamba')
print "Time spent in average by candidates recruted by Halal Guys: ", average_time_recruted('Halal')

### Lentgh of phone number
b0,b33,b33p,wrong, alls = telephone_number('Macdo')
print 'Number of phone number begining by 0: ', b0
print 'Number of phone number begining by 33: ', b33
print 'Number of phone number begining by +33: ', b33p
print 'Number of wrong phone number: ', wrong
print 'Number of phone number (all) : ', alls

l10, l9, l11, wrong, alls  = telephone_number('Jamba')
print 'Number of phone number of lentgh 10: ', l10
print 'Number of phone number of lentgh 9: ', l9
print 'Number of phone number of lentgh 11: ', l11
print 'Number of wrong phone number: ', wrong
print 'Number of phone number (all) : ', alls

l10, l9, l11, wrong, alls  = telephone_number('Halal')
print 'Number of phone number of lentgh 10: ', l10
print 'Number of phone number of lentgh 9: ', l9
print 'Number of phone number of lentgh 11: ', l11
print 'Number of wrong phone number: ', wrong
print 'Number of phone number (all) : ', alls

