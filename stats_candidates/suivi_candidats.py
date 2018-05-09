# -*- coding: utf-8 -*-
from pymongo import MongoClient
import pandas as pd
from bson.objectid import ObjectId
import json
from datetime import timedelta, datetime, date
from pprint import pprint
import sys
import numpy as np
import os
import re

### MongoDB
client = MongoClient()
db = client.app64723109

candidates = db['candidates']
conversations = db['conversations']
messages = db['messages']
sessions = db['sessions']


def candidatures_vs_candidats(filepath, dictToFill):
	print "opening ", filepath, '...'

	df = pd.read_excel(filepath)
	listNum = df['Num']
	listNumUnique = list(set(listNum))

	nbCandidats = len(listNumUnique)
	nbCandidatures = len(listNum)

	n=1;
	perc=0
	sys.stdout.write("\r"+str(perc)+' %')
	sys.stdout.flush()
	for num in listNumUnique:
		if (n*100)/nbCandidats > perc:
			perc += 1
			sys.stdout.write("\r"+str(perc)+' %')
			sys.stdout.flush()
		n+=1

		linesByNum = df.loc[df[u"Num"] == num]
		dates = linesByNum[u"Date Candidature"];

		for day in dates:
			if not isinstance(day,basestring):
				continue
			dt = datetime.strptime(day, '%d/%m/%Y')
			if dt.month in dictToFill.keys():
				dictToFill[dt.month]['candidatures'] += 1
				dictToFill[dt.month]['candidats'].add(num)
			else:
				dictToFill[dt.month] = {
					'candidats': set([num]),
					'candidatures': 1
				}



# resultDict = {}
# path = './suivi MCDO 2017/'
# files = os.listdir(path)
# print files
# for f in files:
# 	if f.endswith('.xlsx'):
# 		candidatures_vs_candidats(path+f, resultDict)
# for month in resultDict.keys():
# 	print "Mont ",month, ' : '
# 	print "=> ", resultDict[month]['candidatures'],' candidatures pour ', len(resultDict[month]['candidats']), 'candidats'

def recompute_new_score(filepath):
	df = pd.read_excel(filepath)
	newSc = pd.read_excel('./nouveau_score.xlsx')

	final = []

	mailRow = list(newSc['Email'])
	listEmail = []

	print len(df.index)
	found = 0
	n=1

	for index, conv in df.iterrows():
		sys.stdout.write("\r"+str(n))
		sys.stdout.flush()
		n+=1
		if isinstance(conv['nom'], basestring):
			cNom = re.compile( re.escape(conv['nom']), re.IGNORECASE)
		else:
			cNom = ""
		if isinstance(conv['prenom'], basestring):
			cPrenom = re.compile( re.escape(conv['prenom']), re.IGNORECASE)
		else:
			cPrenom = ""
		cand = candidates.find({'name.last': cNom, 'name.first': cPrenom})
		cand2 = candidates.find({'name.first': cNom, 'name.last': cPrenom})
		listEmail = []
		if cand.count() > 0:
			for c in cand:
				listEmail.append(c['contact']['email'])
		if cand2.count() > 0:
			for c in cand2:
				listEmail.append(c['contact']['email'])

		for email in listEmail:
			linesByMail = newSc.loc[newSc['Email']==email]
			for ind2, line in linesByMail.iterrows():
				if line['Score'] == conv['score']:
					found+=1
					conv['newScore'] = line['newScore']
					final.append(conv)

	print found
	final_df = pd.DataFrame(final)

	writer = pd.ExcelWriter('matching.xlsx')
	final_df.to_excel(writer,sheet_name='score sans dispo')
	writer.save()

recompute_new_score('./suivi_unique.xlsx')


