import pandas as pd
import numpy as np
import datetime as dt
from plot_graph import create_line, create_multiple_lines ,create_group_nps, create_group_sentinel_CV, \
create_group_sentinel_reminder, create_group_level_with_Pup,create_group_level_wout_Pup, create_group, \
create_group_nbconv, create_group_sessions, create_group_nbconv1, create_multiple_bars, create_multiple_perc_lines,\
create_multiple_boxPlot, create_sankey, create_groupTotal


def create_graph(filename, company, debut, fin) : 
	c = company

	hours = ['00:00', '01:00', '02:00','03:00', '04:00', '05:00','06:00', '07:00', '08:00','09:00', '10:00', '11:00',\
	'12:00', '13:00', '14:00','15:00', '16:00', '17:00', '18:00', '19:00', '20:00','21:00', '22:00', '23:00']

	date_debut = debut.replace('/','-')
	date_fin = fin.replace('/','-')

	folderName = filename.replace('.xlsx','')

	# evolution_nbconv_days_df = pd.read_excel(filename, sheetname='evolution #conv by days',columns=['Number of conversations','Dates'])
	# create_line(folderName,pd.to_datetime(evolution_nbconv_days_df['Dates']),evolution_nbconv_days_df['Number of conversations'].values.tolist(),\
	# 	'Evolution of number of conversations '+str(c)+' '+date_debut+' '+date_fin)


	# aph_nbconv_df = pd.read_excel(filename, sheetname='average #conv by hours',columns=['Number of conversations - weekday', 'Number of conversations - weekend','Hours'])
	# create_group_nbconv(folderName,aph_nbconv_df['Number of conversations - weekday'].values.tolist(),\
	# 	aph_nbconv_df['Number of conversations - weekend'].values.tolist(),hours,\
	# 	'Average number of conversations per hour '+str(c)+' '+date_debut+' '+date_fin)


	# apd_nbconv_df = pd.read_excel(filename, sheetname='average #conv by days',columns=['Number of conversations','Days'])
	# create_group_nbconv1(folderName,apd_nbconv_df['Number of conversations'].values.tolist(),apd_nbconv_df['Days'].values.tolist(),\
	# 	'Average number of conversations per day '+str(c)+' '+date_debut+' '+date_fin)


	# evolution_levels_days_df = pd.read_excel(filename, sheetname='evolution levels by days',columns=['PoppedUp','Started', 'level 1', 'level 2', 'level 3', 'level 4','level 5','level 6','level 7','level 8','Exported','Dates'])
	# create_group_level_with_Pup(folderName,evolution_levels_days_df['PoppedUp'],evolution_levels_days_df['Started'].values.tolist(),evolution_levels_days_df['level 1'].values.tolist(),\
	# 	evolution_levels_days_df['level 2'].values.tolist(),evolution_levels_days_df['level 3'].values.tolist(),\
	# 	evolution_levels_days_df['level 4'].values.tolist(),evolution_levels_days_df['level 5'].values.tolist(),\
	# 	evolution_levels_days_df['level 6'].values.tolist(), evolution_levels_days_df['level 7'].values.tolist(),\
	# 	evolution_levels_days_df['level 8'].values.tolist(), evolution_levels_days_df['Exported'].values.tolist(),\
	# 	pd.to_datetime(evolution_levels_days_df['Dates']),'Evolution of completion level '+str(c)+' '+date_debut+' '+date_fin)

	# dataMatrix = {
	# 	'PoppedUp' : evolution_levels_days_df['PoppedUp'],
	# 	'Lvl 7' : evolution_levels_days_df['level 7'] 
	# }
	# create_multiple_lines(folderName,evolution_levels_days_df['Dates'], dataMatrix,
	# 	'Evolution of PoppedUp and Lvl 7 '+str(c)+' '+date_debut+' '+date_fin )

	# create_line(folderName, evolution_levels_days_df['Dates'], evolution_levels_days_df['level 7'],
	# 	'Evolution of Lvl 7 '+str(c)+' '+date_debut+' '+date_fin )

	# create_group_level_wout_Pup(folderName,evolution_levels_days_df['Started'].values.tolist(),evolution_levels_days_df['level 1'].values.tolist(),\
	# 	evolution_levels_days_df['level 2'].values.tolist(),evolution_levels_days_df['level 3'].values.tolist(),\
	# 	evolution_levels_days_df['level 4'].values.tolist(),evolution_levels_days_df['level 5'].values.tolist(),\
	# 	evolution_levels_days_df['level 6'].values.tolist(), evolution_levels_days_df['level 7'].values.tolist(),\
	# 	evolution_levels_days_df['level 8'].values.tolist(), evolution_levels_days_df['Exported'].values.tolist(),\
	# 	pd.to_datetime(evolution_levels_days_df['Dates']),'Evolution of completion level '+str(c)+' '+date_debut+' '+date_fin)


	# aph_levels_df = pd.read_excel(filename, sheetname='average levels by hours',columns=['PoppedUp','Started', 'level 1', 'level 2', 'level 3', 'level 4','level 5','level 6','level 7','level 8','Exported', 'PoppedUp we', 'Started we', 'level 1 we', 'level 2 we', 'level 3 we', 'level 4 we','level 5 we','level 6 we','level 7 we','level 8 we','Exported we','Hours'])
	# create_group_level_with_Pup(folderName,aph_levels_df['PoppedUp'],aph_levels_df['Started'].values.tolist(),aph_levels_df['level 1'].values.tolist(),\
	# 	aph_levels_df['level 2'].values.tolist(),aph_levels_df['level 3'].values.tolist(),\
	# 	aph_levels_df['level 4'].values.tolist(),aph_levels_df['level 5'].values.tolist(),\
	# 	aph_levels_df['level 6'].values.tolist(), aph_levels_df['level 7'].values.tolist(),\
	# 	aph_levels_df['level 8'].values.tolist(), aph_levels_df['Exported'].values.tolist(),\
	# 	hours,'Average completion level per hour durind weekday '+str(c)+' '+date_debut+' '+date_fin)

	# create_group_level_wout_Pup(folderName,aph_levels_df['Started'].values.tolist(),aph_levels_df['level 1'].values.tolist(),\
	# 	aph_levels_df['level 2'].values.tolist(),aph_levels_df['level 3'].values.tolist(),\
	# 	aph_levels_df['level 4'].values.tolist(),aph_levels_df['level 5'].values.tolist(),\
	# 	aph_levels_df['level 6'].values.tolist(), aph_levels_df['level 7'].values.tolist(),\
	# 	aph_levels_df['level 8'].values.tolist(), aph_levels_df['Exported'].values.tolist(),\
	# 	hours,'Average completion level per hour durind weekday '+str(c)+' '+date_debut+' '+date_fin)


	# create_group_level_with_Pup(folderName,aph_levels_df['PoppedUp we'].values.tolist(), aph_levels_df['Started we'].values.tolist(),aph_levels_df['level 1 we'].values.tolist(),\
	# 	aph_levels_df['level 2 we'].values.tolist(),aph_levels_df['level 3 we'].values.tolist(),\
	# 	aph_levels_df['level 4 we'].values.tolist(),aph_levels_df['level 5 we'].values.tolist(),\
	# 	aph_levels_df['level 6 we'].values.tolist(), aph_levels_df['level 7 we'].values.tolist(),\
	# 	aph_levels_df['level 8 we'].values.tolist(), aph_levels_df['Exported we'].values.tolist(),\
	# 	hours,'Average completion level per hour durind weekend '+str(c)+' '+date_debut+' '+date_fin)

	# create_group_level_wout_Pup(folderName,aph_levels_df['Started we'].values.tolist(),aph_levels_df['level 1 we'].values.tolist(),\
	# 	aph_levels_df['level 2 we'].values.tolist(),aph_levels_df['level 3 we'].values.tolist(),\
	# 	aph_levels_df['level 4 we'].values.tolist(),aph_levels_df['level 5 we'].values.tolist(),\
	# 	aph_levels_df['level 6 we'].values.tolist(), aph_levels_df['level 7 we'].values.tolist(),\
	# 	aph_levels_df['level 8 we'].values.tolist(), aph_levels_df['Exported we'].values.tolist(),\
	# 	hours,'Average completion level per hour durind weekend '+str(c)+' '+date_debut+' '+date_fin)


	# apd_levels_df = pd.read_excel(filename, sheetname='average levels by days',columns=['PoppedUp','Started', 'level 1', 'level 2', 'level 3', 'level 4','level 5','level 6','level 7','level 8','Exported','Days'])
	# create_group_level_with_Pup(folderName,apd_levels_df['PoppedUp'].values.tolist(), apd_levels_df['Started'].values.tolist(),apd_levels_df['level 1'].values.tolist(),\
	# 	apd_levels_df['level 2'].values.tolist(),apd_levels_df['level 3'].values.tolist(),\
	# 	apd_levels_df['level 4'].values.tolist(),apd_levels_df['level 5'].values.tolist(),\
	# 	apd_levels_df['level 6'].values.tolist(), apd_levels_df['level 7'].values.tolist(),\
	# 	apd_levels_df['level 8'].values.tolist(), apd_levels_df['Exported'].values.tolist(),\
	# 	apd_levels_df['Days'].values.tolist(),'Average completion level per day '+str(c)+' '+date_debut+' '+date_fin)

	# create_group_level_wout_Pup(folderName,apd_levels_df['Started'].values.tolist(),apd_levels_df['level 1'].values.tolist(),\
	# 	apd_levels_df['level 2'].values.tolist(),apd_levels_df['level 3'].values.tolist(),\
	# 	apd_levels_df['level 4'].values.tolist(),apd_levels_df['level 5'].values.tolist(),\
	# 	apd_levels_df['level 6'].values.tolist(), apd_levels_df['level 7'].values.tolist(),\
	# 	apd_levels_df['level 8'].values.tolist(), apd_levels_df['Exported'].values.tolist(),\
	# 	apd_levels_df['Days'].values.tolist(),'Average completion level per day '+str(c)+' '+date_debut+' '+date_fin)


	# evolution_nps_days_df = pd.read_excel(filename, sheetname='evolution nps by days',columns=['1 star', '2 stars', '3 stars', '4 stars','5 stars','Dates'])
	# create_group_nps(folderName,evolution_nps_days_df['1 star'].values.tolist(),evolution_nps_days_df['2 stars'].values.tolist(),\
	# 	evolution_nps_days_df['3 stars'].values.tolist(), evolution_nps_days_df['4 stars'].values.tolist(),\
	# 	evolution_nps_days_df['5 stars'].values.tolist(),pd.to_datetime(evolution_nps_days_df['Dates']),\
	# 	'Evolution NPS '+str(c)+' '+date_debut+' '+date_fin)


	# aph_nps_df = pd.read_excel(filename, sheetname='average nps by hours',columns=['1 star', '2 stars', '3 stars', '4 stars','5 stars', '1 star we', '2 star we', '3 star we', '4 star we','5 star we','Hours'])
	# create_group_nps(folderName,aph_nps_df['1 star'].values.tolist(),aph_nps_df['2 stars'].values.tolist(),\
	# 	aph_nps_df['3 stars'].values.tolist(),aph_nps_df['4 stars'].values.tolist(),\
	# 	aph_nps_df['5 stars'].values.tolist(),hours,\
	# 	'Average NPS per hour during weekday '+str(c)+' '+date_debut+' '+date_fin)
	# create_group_nps(folderName,aph_nps_df['1 star we'].values.tolist(),aph_nps_df['2 star we'].values.tolist(),\
	# 	aph_nps_df['3 star we'].values.tolist(),aph_nps_df['4 star we'].values.tolist(),\
	# 	aph_nps_df['5 star we'].values.tolist(),hours,\
	# 	'Average NPS per hour during weekend '+str(c)+' '+date_debut+' '+date_fin)

	# apd_nps_df = pd.read_excel(filename, sheetname='average nps by days',columns=['1 star', '2 stars', '3 stars', '4 stars','5 stars','Days'])
	# create_group_nps(folderName,apd_nps_df['1 star'].values.tolist(),apd_nps_df['2 stars'].values.tolist(),\
	# 	apd_nps_df['3 stars'].values.tolist(),apd_nps_df['4 stars'].values.tolist(),\
	# 	apd_nps_df['5 stars'].values.tolist(),apd_nps_df['Days'].values.tolist(),\
	# 	'Average NPS per day '+str(c)+' '+date_debut+' '+date_fin)

	# fake_nps_matrix = {
	# 	'Positive':[0.]*7,
	# 	'Negative':[0.]*7,
	# 	'Total': [0.]*7
	# }
	# j=0
	# for x in apd_nps_df['1 star'].values.tolist():
	# 	fake_nps_matrix['Negative'][j] += x
	# 	fake_nps_matrix['Total'][j] += x
	# 	j+=1
	# j=0
	# for x in apd_nps_df['2 stars'].values.tolist():
	# 	fake_nps_matrix['Negative'][j] += x
	# 	fake_nps_matrix['Total'][j] += x
	# 	j+=1
	# j=0
	# for x in apd_nps_df['4 stars'].values.tolist():
	# 	fake_nps_matrix['Positive'][j] += x
	# 	fake_nps_matrix['Total'][j] += x
	# 	j+=1
	# j=0
	# for x in apd_nps_df['5 stars'].values.tolist():
	# 	fake_nps_matrix['Positive'][j] += x
	# 	fake_nps_matrix['Total'][j] += x
	# 	j+=1

	# for j in range(0,7):
	# 	try:
	# 		fake_nps_matrix['Positive'][j] = (fake_nps_matrix['Positive'][j] / float(fake_nps_matrix['Total'][j]))*100
	# 	except Exception, e:
	# 		fake_nps_matrix['Positive'][j] = 0

	# 	try:
	# 		fake_nps_matrix['Negative'][j] = (fake_nps_matrix['Negative'][j] / float(fake_nps_matrix['Total'][j]))*100
	# 	except Exception, e:
	# 		fake_nps_matrix['Negative'][j] = 0
		
		
	# del fake_nps_matrix['Total']
	# create_multiple_bars(folderName, apd_nps_df['Days'].values.tolist(), fake_nps_matrix,
	# 	'Positives and negatives experiences '+str(c)+' '+date_debut+' '+date_fin, yaxisTitle='%')


	# #####OLD SENTINEL
    
	# evolution_sentinel_days_df = pd.read_excel(filename, sheetname='evolution sentinel by days',columns=['send_cv','opened_cv','upload_cv','export_cv','reminder1', 'reminder2', 'reminder3','returned','recover','Dates'])
	# create_group_sentinel_CV(folderName,evolution_sentinel_days_df['send_cv'].values.tolist(),evolution_sentinel_days_df['opened_cv'].values.tolist(),\
	# 	evolution_sentinel_days_df['upload_cv'].values.tolist(),evolution_sentinel_days_df['export_cv'].values.tolist(),\
	# 	pd.to_datetime(evolution_sentinel_days_df['Dates']),'Evolution sentinel CV '+str(c)+' '+date_debut+' '+date_fin)

	# create_group_sentinel_reminder(folderName,evolution_sentinel_days_df['reminder1'].values.tolist(),evolution_sentinel_days_df['reminder2'].values.tolist(),\
	# 	evolution_sentinel_days_df['reminder3'].values.tolist(), evolution_sentinel_days_df['returned'].values.tolist(),\
	# 	evolution_sentinel_days_df['recover'].values.tolist(), pd.to_datetime(evolution_sentinel_days_df['Dates']),\
	# 	'Evolution sentinel reminder'+str(c)+' '+date_debut+' '+date_fin)


	# aph_sentinel_df = pd.read_excel(filename, sheetname='average sentinel by hours',columns=['send_cv','opened_cv','upload_cv','export_cv','reminder1', 'reminder2', 'reminder3','returned','recover','send_cv we','opened_cv we','upload_cv we','export_cv we','reminder1 we', 'reminder2 we', 'reminder3 we','returned we','recover we','Hours'])
	# create_group_sentinel_CV(folderName,aph_sentinel_df['send_cv'].values.tolist(),aph_sentinel_df['opened_cv'].values.tolist(),\
	# 	aph_sentinel_df['upload_cv'].values.tolist(),aph_sentinel_df['export_cv'].values.tolist(),hours,\
	# 	'Average sentinel CV per hour during weekday '+str(c)+' '+date_debut+' '+date_fin)

	# create_group_sentinel_CV(folderName,aph_sentinel_df['send_cv we'].values.tolist(),aph_sentinel_df['opened_cv we'].values.tolist(),\
	# 	aph_sentinel_df['upload_cv we'].values.tolist(),aph_sentinel_df['export_cv we'].values.tolist(),hours,\
	# 	'Average sentinel CV per hour during weekend '+str(c)+' '+date_debut+' '+date_fin)

	# create_group_sentinel_reminder(folderName,aph_sentinel_df['reminder1'].values.tolist(),aph_sentinel_df['reminder2'].values.tolist(),\
	# 	aph_sentinel_df['reminder3'].values.tolist(), aph_sentinel_df['returned'].values.tolist(),\
	# 	aph_sentinel_df['recover'].values.tolist(), hours,\
	# 	'Average sentinel reminderper hour during weekday '+str(c)+' '+date_debut+' '+date_fin)

	# create_group_sentinel_reminder(folderName,aph_sentinel_df['reminder1 we'].values.tolist(),aph_sentinel_df['reminder2 we'].values.tolist(),\
	# 	aph_sentinel_df['reminder3 we'].values.tolist(), aph_sentinel_df['returned we'].values.tolist(),\
	# 	aph_sentinel_df['recover we'].values.tolist(), hours,\
	# 	'Average sentinel  reminder per hour during weekend '+str(c)+' '+date_debut+' '+date_fin)

	# apd_sentinel_df = pd.read_excel(filename, sheetname='average sentinel by days',columns=['send_cv','opened_cv','upload_cv','export_cv','reminder1', 'reminder2', 'reminder3','returned','recover','Days'])
	# create_group_sentinel_CV(folderName,apd_sentinel_df['send_cv'].values.tolist(),apd_sentinel_df['opened_cv'].values.tolist(),\
	# 	apd_sentinel_df['upload_cv'].values.tolist(),apd_sentinel_df['export_cv'].values.tolist(),\
	# 	apd_sentinel_df['Days'].values.tolist(),'Average sentinel CV per day '+str(c)+' '+date_debut+' '+date_fin)

	# create_group_sentinel_reminder( folderName,apd_sentinel_df['reminder1'].values.tolist(),apd_sentinel_df['reminder2'].values.tolist(),\
	# 	apd_sentinel_df['reminder3'].values.tolist(), apd_sentinel_df['returned'].values.tolist(),\
	# 	apd_sentinel_df['recover'].values.tolist(), apd_sentinel_df['Days'].values.tolist(),\
	# 	'Average sentinel reminder per day '+str(c)+' '+date_debut+' '+date_fin)

	#####OLD SENTINEL END

	##NEW SENTINEL - SANKEY
	# data = {
	# 	"node": {
 #            "pad": 15,
 #            "thickness": 15,
 #            "line": {
 #                "color": "black",
 #                "width": 0.5
 #            },
 #            "label": [
 #                "Started",
 #                "Send Mail",
 #                "Open Mail",
 #                "Send CV",
 #                "Drop"
 #            ],
 #            "color": [
 #                "rgba(31, 119, 180, 0.8)",
 #                "rgba(255, 127, 14, 0.8)",
 #                "rgba(44, 160, 44, 0.8)",
 #                "rgba(214, 39, 40, 0.8)"
 #            ]
 #        },
 #        "link": {
 #            "source": [
 #                1,
 #                1,
 #                2,
 #                2,
 #                3,
 #                3
 #            ],
 #            "target": [
 #            	2,
 #            	5,
 #            	3,
 #            	5,
 #            	4,
 #            	5
 #            ],
 #            "value": [
 #            	60.0,
 #            	40.0,
 #            	80.0,
 #            	20.0,
 #            	50.0,
 #            	50.0
 #            ]
 #        }
 #    }

	# create_sankey(data)



	##new sentinel end

	# levels_df = pd.read_excel(filename, sheetname='levels by device', columns=['Desktop','Mobile'])
	# create_group(folderName,levels_df['Mobile'].values.tolist(),levels_df['Desktop'].values.tolist(),['PoppedUp','Started', 'level 1','level 2','level 3','level 4',\
	# 	'level 5','level 6','level 7', 'level 8', 'Exported'],'Comparison completion level by device '+str(c)+' '+date_debut+' '+date_fin)
	# lvlMobList = levels_df['Mobile'].values.tolist()
	# lvlDeskList = levels_df['Desktop'].values.tolist()
	# res = []
	# for x in range(2,len(lvlDeskList)-1):
	# 	res.append(lvlMobList[x] + lvlDeskList[x])

	# create_groupTotal(folderName,res,['level 1','level 2','level 3','level 4',\
	# 	'level 5','level 6','level 7'], 'Number of completion levels '+str(c)+' '+date_debut+' '+date_fin)


	# nps_df = pd.read_excel(filename, sheetname='nps by device', columns=['Desktop','Mobile'])
	# create_multiple_bars(folderName, ['1 stars','2 stars','3 stars','4 stars','5 stars'], nps_df,
	# 	'Comparison NPS by device '+str(c)+' '+date_debut+' '+date_fin)


	# sentinel_df = pd.read_excel(filename, sheetname='sentinel by device', columns=['Desktop','Mobile'])
	# create_group(folderName,sentinel_df['Mobile'].values.tolist(),levels_df['Desktop'].values.tolist(),\
	# 	['send_cv','opened_cv','upload','export','reminder','returned'],'Comparison sentinel by device '+str(c)+' '+date_debut+' '+date_fin)

	# conv_bysource_df = pd.read_excel(filename, sheetname='#conv by source')
	# dataMatrix = {}
	# for k in conv_bysource_df.keys() :
	# 	if (k != 'Dates') :
	# 		dataMatrix[k] = conv_bysource_df[k]

	# create_multiple_lines(folderName,conv_bysource_df['Dates'], dataMatrix,
	#  	'Evolution of number of conv by source '+str(c)+' '+date_debut+' '+date_fin )

	# lvl7_by_source = pd.read_excel(filename, sheetname='#lvl7 by source')
	# dataMatrix = {}
	# for k in lvl7_by_source.keys() :
	# 	if (k != 'Dates') :
	# 		dataMatrix[k] = lvl7_by_source[k]

	# create_multiple_lines(folderName,lvl7_by_source['Dates'], dataMatrix,
	#  	'Evolution of number of Lvl 7 by source '+str(c)+' '+date_debut+' '+date_fin )


	# apd_nbconv_bysource = pd.read_excel(filename, sheetname = 'average #conv by day by source')
	# create_multiple_bars(folderName, apd_nbconv_bysource['Dates'], apd_nbconv_bysource,
	# 	'Average number of conversations by source'+str(c)+' '+date_debut+' '+date_fin )

	# apd_nblvl7_bysource = pd.read_excel(filename, sheetname = 'average #lvl7 by day by source')
	# create_multiple_bars(folderName, apd_nblvl7_bysource['Dates'], apd_nblvl7_bysource,
	# 	'Average number of lvl7 by source'+str(c)+' '+date_debut+' '+date_fin )

	# apd_nbconv_bydevice = pd.read_excel(filename, sheetname = 'average #conv by day by device')
	# create_multiple_bars(folderName, apd_nbconv_bydevice['Dates'], apd_nbconv_bydevice,
	# 	'Average number of conversations by device'+str(c)+' '+date_debut+' '+date_fin )

	# apd_nblvl7_bydevice = pd.read_excel(filename, sheetname = 'average #lvl7 by day by device')
	# create_multiple_bars(folderName, apd_nblvl7_bydevice['Dates'], apd_nblvl7_bydevice,
	# 	'Average number of Lvl 7 by device'+str(c)+' '+date_debut+' '+date_fin )

	# apd_nbexp_bydevice = pd.read_excel(filename, sheetname = 'average #exp by day by device')
	# create_multiple_bars(folderName, apd_nbexp_bydevice['Dates'], apd_nbexp_bydevice,
	# 	'Average number of Exported by device'+str(c)+' '+date_debut+' '+date_fin )

	# conversionRates = pd.read_excel(filename, sheetname= 'conversion ratios by device')
	# conversionRates = conversionRates[1:8]
	# indexes = conversionRates['indexes']
	# del conversionRates['indexes']
	# create_multiple_lines(folderName, indexes , conversionRates,
	# 	'Conversion Ratio by device'+str(c)+' '+date_debut+' '+date_fin )


	# conversion_by_UA = pd.read_excel(filename, sheetname='conversion ratios by UA')
	# print conversion_by_UA
	# del conversion_by_UA['Exported/Lvl7']
	# del conversion_by_UA['Started/PoppedUp']
	# create_multiple_perc_lines(folderName, conversion_by_UA.columns.values[1:], conversion_by_UA.values,
	# 	'Conversion ratio for major user-agents'+str(c)+' '+date_debut+' '+date_fin )

	conversion_by_source = pd.read_excel(filename, sheetname='conversion ratios by source')
	print conversion_by_source
	del conversion_by_source['Started / PoppedUp']
	create_multiple_perc_lines(folderName, conversion_by_source.columns.values[1:], conversion_by_source.values,
		'Conversion ratio by source '+str(c)+' '+date_debut+' '+date_fin )

	# time_by_level = pd.read_excel(filename,sheetname='time spent on levels ALLDATA')
	# for lvl in time_by_level:
	# 	data = time_by_level[lvl]
	# 	toFill = len(data)
	# 	limit = 2*np.mean(data) - 2*np.min(data)
	# 	data = [ (e/60.) for e in data if e<limit]
	# 	missing = toFill - len(data)
	# 	for x in range(missing):
	# 		data.append(None)
	# 	time_by_level[lvl] = data

	# del time_by_level['Lvl8']

	# create_multiple_boxPlot(folderName, time_by_level,
	# 	'Cumulative Time spent by Levels'+str(c)+' '+date_debut+' '+date_fin )








