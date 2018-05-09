# -*- coding: utf-8 -*-
from pymongo import MongoClient
import pandas as pd
from bson.objectid import ObjectId
from bson.code import Code
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
companies = db['companies']

status_mapper = Code("""
		function () {
			emit(this.candidateStatus,1);
		}
	""")

status_reducer = Code("""
		function (key, value) {
			var total = 0;
          	for (var i = 0; i < value.length; i++) {
        	    total += value[i];
        	}
            return parseInt(total);
		}
	""")

def count_status(queryToAdd):
	allComp = companies.find({});
	status_headers = set();
	final_res = [];
	companyNames = [];

	for company in allComp :
		print '=>',company['name']
		tmp_query = {'company': company['_id'], 'score':{'$gte':7}}
		tmp_query.update(queryToAdd)
		comp_query = {'company': company['_id']}
		comp_query.update(queryToAdd)

		tmp_res = {};
		tmp_res['company'] = company['name'];
		tmp_res['count_Conv'] = conversations.count(comp_query)
		tmp_res['displayed_conv'] = conversations.count(tmp_query)
		companyNames.append(company['name'])

		results = conversations.map_reduce(status_mapper, status_reducer, "my_res", query = tmp_query )
		for res in results.find():
			status_headers.add(res['_id'])
			tmp_res[res['_id']] = res['value']

		final_res.append(tmp_res)
	status_headers = list(status_headers);
	status_headers.insert(0,'displayed_conv')
	status_headers.insert(0,'count_Conv')
	

	final_df = pd.DataFrame(final_res, index=companyNames, columns=status_headers)
	final_df.index.name = 'Company';

	return final_df



writer = pd.ExcelWriter('candidates_status.xlsx')
#total
total_numbers = count_status({});
total_numbers.to_excel(writer, sheet_name= 'Total numbers')
print 'Total'
#june
debut = datetime.strptime('01/06/2017', '%d/%m/%Y')
fin = datetime.strptime('01/07/2017', '%d/%m/%Y')
july_numbers = count_status({'meta.createdOn': {'$lt': fin , '$gte': debut}})
july_numbers.to_excel(writer, sheet_name= 'June')
print 'June'
#july
debut = datetime.strptime('01/07/2017', '%d/%m/%Y')
fin = datetime.strptime('01/08/2017', '%d/%m/%Y')
july_numbers = count_status({'meta.createdOn': {'$lt': fin , '$gte': debut}})
july_numbers.to_excel(writer, sheet_name= 'July')
print 'July'
#august
debut = datetime.strptime('01/08/2017', '%d/%m/%Y')
fin = datetime.strptime('01/09/2017', '%d/%m/%Y')
month_numbers = count_status({'meta.createdOn': {'$lt': fin , '$gte': debut}})
month_numbers.to_excel(writer, sheet_name= 'August')
print 'August'
#september
debut = datetime.strptime('01/09/2017', '%d/%m/%Y')
fin = datetime.strptime('01/10/2017', '%d/%m/%Y')
month_numbers = count_status({'meta.createdOn': {'$lt': fin , '$gte': debut}})
month_numbers.to_excel(writer, sheet_name= 'September')
print 'September'
#October
debut = datetime.strptime('01/10/2017', '%d/%m/%Y')
fin = datetime.strptime('01/11/2017', '%d/%m/%Y')
month_numbers = count_status({'meta.createdOn': {'$lt': fin , '$gte': debut}})
month_numbers.to_excel(writer, sheet_name= 'October')
print 'October'

writer.save()

