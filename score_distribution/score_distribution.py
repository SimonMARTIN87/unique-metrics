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
company = 'Mcdo-bessin'
date_debut = '01/06/2017'
date_fin = '01/11/2017'

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


	if company == 'All-Franchises':
		return {
			'$in': [
				ObjectId('596e45882a581c0004936b8f'),#bordeaux
				ObjectId('596f5cce97a38d000405e0d0'),#Magny
				ObjectId('59b7a1f762fb42000494d183'),#Alpes
				ObjectId('596e38ee2a581c0004936b03'),#Pontarlier
				ObjectId('593663c5c14afd00040e3e11'),#bessin
				ObjectId('596e33fb2a581c0004936a77'),#Nord-isere
				ObjectId('596e08f22a581c00049368e0'),#Marseille
				ObjectId('59ba478a50af8700040879d9'),#Yvelines
				ObjectId('59366ce4c14afd00040e3e9c') #Limoges
			]
		}
	return None



def create_data(company, debut, fin):
	id_comp = getCompanyId(company)

	#get all scores for LVl >=7
	all_conversations = conversations.find({
		'meta.createdOn': {
			'$lt': fin ,
			'$gte': debut
		},
		'company' : id_comp,
		'meta.completionLevel': {
			'$gte':80
		}
	})

	scores = []
	scores_V2 = []
	totalConv = all_conversations.count()
	timeLimit = datetime.strptime('20/10/2017', '%d/%m/%Y')
	for doc in all_conversations:
		sc = doc['score']
		if sc != 0 and sc < 300:
			if doc['meta']['createdOn'] < timeLimit :
				scores.append(doc['score'])
			else :
				scores_V2.append(doc['score'])

	meanV1 = np.mean(scores)
	stdV1 = np.std(scores)
	meanV2 = np.mean(scores_V2)
	stdV2 = np.std(scores_V2)
	scMin = min(min(scores), min(scores_V2))
	scMax = max(max(scores), max(scores_V2))

	frequency = np.bincount(scores, minlength=scMax+1)
	frequency_V2 = np.bincount(scores_V2, minlength=scMax+1)

	print scMin, ' -- ', scMax

	res = []
	for x in range(scMin,scMax+1):
		res.append({
			'Score': x,
			'Frequence ChatV1': frequency[x] if frequency[x] else 0,
			'Frequence ChatV2': frequency_V2[x] if frequency_V2[x] else 0
		})
	res_df = pd.DataFrame(res, columns=['Score','Frequence ChatV1','Frequence ChatV2'])

	writer = pd.ExcelWriter('Scores_'+str(company)+'.xlsx',engine='xlsxwriter')
	res_df.to_excel(writer,sheet_name='score_frequency',index = False)

	workbook = writer.book
	worksheet = writer.sheets['score_frequency']
	chart = workbook.add_chart({'type':'line'})
	chart.add_series({
		'categories': '=score_frequency!$A$2:$A$'+str(scMax),
		'values': '=score_frequency!$B$2:$B$'+str(scMax),
		'name': 'Chat V1 - AVANT 20 0ctobre'
	})
	chart.add_series({
		'categories': '=score_frequency!$A$2:$A$'+str(scMax),
		'values': '=score_frequency!$C$2:$C$'+str(scMax),
		'name': 'Chat V2 - APRES 20 0ctobre'
	})
	chart.set_x_axis({'name': 'Score'})
	chart.set_y_axis({'name': u'Fréquence'})
	chart.set_title({'name':'Distribution du Score par version du chat '+company})
	chart.set_size({'x_scale':2.0,'y_scale':2.0})
	worksheet.insert_chart('D1', chart)

	normSheet = workbook.add_worksheet('Score_norm')
	normSheet.write('A1','Score')
	normSheet.write('B1', 'Chat V1 - AVANT 20 0ctobre')
	normSheet.write('C1', 'Chat V2 - APRES 20 0ctobre')
	normSheet.write('E1', meanV1)
	normSheet.write('E2', stdV1)
	normSheet.write('F1', meanV2)
	normSheet.write('F2', stdV2)
	for x in range(2, 300):
		normSheet.write('A'+str(x), x)
		normSheet.write_formula('B'+str(x), '=NORMDIST(A%s,$E$1,$E$2,0)*100'%x )
		normSheet.write_formula('C'+str(x), '=NORMDIST(A%s,$F$1,$F$2,0)*100'%x )

	chart2 = workbook.add_chart({'type':'line'})
	chart2.add_series({
		'categories': '=Score_norm!$A$2:$A$'+str(scMax),
		'values': '=Score_norm!$B$2:$B$'+str(scMax),
		'name': 'Chat V1 - AVANT 20 0ctobre'
	})
	chart2.add_series({
		'categories': '=Score_norm!$A$2:$A$'+str(scMax),
		'values': '=Score_norm!$C$2:$C$'+str(scMax),
		'name': 'Chat V2 - APRES 20 0ctobre'
	})

	chart2.set_x_axis({'name': 'Score'})
	chart2.set_y_axis({'name': u'Fréquence'})
	chart2.set_title({'name':'Distribution du Score par version du chat '+company+u' - normalisé'})
	chart2.set_size({'x_scale':2.0,'y_scale':2.0})
	normSheet.insert_chart('D1', chart2)

	writer.save()

####RUN 
data = create_data(company, debut, fin)