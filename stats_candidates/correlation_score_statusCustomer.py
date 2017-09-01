# -*- coding: utf-8 -*-
from pymongo import MongoClient
import pandas as pd
from bson.objectid import ObjectId
import json
from datetime import timedelta, datetime, date
from pprint import pprint

### MongoDB
# client = MongoClient()
# db = client.app64723109

# candidates = db['candidates']
# conversations = db['conversations']
# messages = db['messages']
# sessions = db['sessions']


##open Eolia file
df = pd.read_excel('SuiviCandidatures - 07 01 17 to 08 31 17.xlsx')

print df.columns
print df.columns.values

##