# -*- coding: utf-8 -*-
from pymongo import MongoClient
import pandas as pd
from bson.objectid import ObjectId
import json
from datetime import timedelta, datetime, date
from pprint import pprint
import sys
import numpy as np

### MongoDB
# client = MongoClient()
# db = client.app64723109

# candidates = db['candidates']
# conversations = db['conversations']
# messages = db['messages']
# sessions = db['sessions']


##open Eolia file
df = pd.read_excel('SuiviCandidatures - 07 01 17 to 08 31 17.xlsx')
#df = pd.read_excel('SuiviTest.xlsx')

print df.columns

listNum = df['Num']
listNumUnique = list(set(listNum))

nbCandidats = len(listNumUnique)
nbCandidatures = len(listNum)

print nbCandidatures, ' candidatures || ', nbCandidats, ' candidats'

###% of unique.ai candidates
fromUniqueAI = []
n=1
perc = 0
sys.stdout.write("\r"+str(perc)+' %')
sys.stdout.flush()
for num in listNumUnique:
	if (n*100)/nbCandidats > perc:
		perc += 1
		sys.stdout.write("\r"+str(perc)+' %')
		sys.stdout.flush()
	n+=1
	linesByNum = df.loc[df[u"Num"] == num]

	scoreVal = set(linesByNum[u"Score"]).pop()

	if scoreVal > 0:
		fromUniqueAI.append(num)
print ''
print len(fromUniqueAI), ' chat candidates on ', nbCandidats

nbUniques = len(fromUniqueAI)

#### fetch infos for unique.ai candidates
candidats_unique_as_dicos = []
n=1
perc = 0
sys.stdout.write("\r"+str(perc)+' %')
sys.stdout.flush()
for num in fromUniqueAI:
	if (n*100)/nbUniques > perc:
		perc += 1
		sys.stdout.write("\r"+str(perc)+' %')
		sys.stdout.flush()
	n+=1
	linesByNum = df.loc[df[u"Num"] == num]

	currCandidate = {}

	#names
	nom = set(linesByNum[u"Nom"]).pop()
	if isinstance(nom, basestring):		
		currCandidate['nom'] = nom.encode('utf-8')
	else:
		print "=>",nom
		currCandidate['nom'] = nom
	prenom = set(linesByNum[u"Prenom"]).pop()
	if isinstance(prenom, basestring):		
		currCandidate['prenom'] = prenom.encode('utf-8')
	else:
		print "=>",prenom
		currCandidate['prenom'] = prenom

	#score
	currCandidate['score'] = set(linesByNum[u"Score"]).pop()

	#prequa
	listPq = list(linesByNum[u"Pré-qualification"])
	setPq = set(listPq)
	if len(setPq) == 1:
		if setPq.pop() == 'OK':
			currCandidate['prequa'] = 1
			currCandidate['prequaDisc'] = 1
		else:
			currCandidate['prequa'] = 0
			currCandidate['prequaDisc'] = 0
	else:
		listVal = []
		for item in listPq:
			if item == u"X":
				listVal.append(0)
			elif item == u"OK":
				listVal.append(1)
			else:
				listVal.append(0.5)
		currCandidate['prequa'] = np.mean(listVal)
		currCandidate['prequaDisc'] = 0.5

	#entretiens
	currCandidate['entretien'] = 0
	entretien = set(linesByNum[u"Date Entretien"]).pop()
	if isinstance(entretien, basestring):
		entretien = entretien.strip()
		if len(entretien)>0:
			currCandidate['entretien'] = 1

	#recruté
	currCandidate['recrute'] = 0
	recrute = set(linesByNum[u"Date Recruté"]).pop()
	if isinstance(recrute, basestring):
		recrute = recrute.strip()
		if len(recrute) >0:
			currCandidate['recrute'] = 1
			print 'candidat recruté! ', currCandidate

	candidats_unique_as_dicos.append(currCandidate)


writer = pd.ExcelWriter('suivi_candidats_unique.xlsx')

unique_df = pd.DataFrame(candidats_unique_as_dicos, columns=['nom','prenom','score','prequaDisc','prequa','entretien','recrute'])
unique_df.to_excel(writer,sheet_name='liste candidats Eolia')

writer.save()



#### Préqua candidatures
# prequa = df[u"Pré-qualification"]
# freqPrequa = {}
# freqPrequaKeys = []
# n=1
# for obj in prequa:
# 	print n,'/',nbCandidatures
# 	n+=1
# 	if obj in freqPrequaKeys:
# 		freqPrequa[obj] += 1
# 	else:
# 		freqPrequa[obj] = 1
# 		freqPrequaKeys.append(obj)

# print freqPrequa


#### Préqua candidats
# freqPrequa = {0:0, 0.5:0, 1:0}
# n=1
# for num in listNumUnique:
# 	print n, '/', nbCandidats
# 	n+=1
# 	candByNum = df.loc[df[u"Num"] == num]
# 	pqByNum = candByNum[u"Pré-qualification"]
# 	listPq = []

# 	for pq in pqByNum:
# 		listPq.append(pq)

# 	listPq = list(set(listPq))
# 	scorePq = 0
# 	if len(listPq) == 1:
# 		scorePq = 1 if listPq[0]==u"OK" else 0
# 	else:
# 		scorePq = 0.5

# 	freqPrequa[scorePq] += 1

# print freqPrequa

###Nb d'infos
# nbEntretiens = 0
# for obj in entretiens:
# 	if isinstance(obj, int):
# 		print obj
# 		continue
# 	obj = obj.strip()
# 	if len(obj) > 0:
# 		nbEntretiens +=1

# print 'Entretiens : ',nbEntretiens

# recrutes = df[u"Date Recruté"]
# nbRecrutes = 0
# for obj in recrutes:
# 	obj = obj.strip()
# 	if len(obj) > 0:
# 		nbRecrutes += 1

# print "Recrutés : ", nbRecrutes