import pandas as pd 
from datetime import timedelta, datetime, date
from produce_stats import nps_by_time, count_conversations, count_level_reached, sentinel_level,\
time_by_session,which_return,conv_by_browser,return_with_new_conv, ids_conv, convs_by_source, lvl7_by_source, convs_by_device, lvl7_by_device
from produce_stats_by_period import evolution_by_period, average_periode_hours, average_periode_days 

def create_xlsx(debut,fin,company) : 
	date_debut = debut.replace('/','-')
	date_fin = fin.replace('/','-')

	if isinstance(debut, date) is False : 
		debut = datetime.strptime(debut, '%d/%m/%Y')

	if isinstance(fin, date) is False: 
		fin = datetime.strptime(fin, '%d/%m/%Y')

	writer = pd.ExcelWriter(str(company)+'_'+str(date_debut)+'_'+str(date_fin)+'.xlsx',float_format = int)

	evolution_nbconv_hours = evolution_by_period(debut,fin,count_conversations,company,'hours')
	evolution_nbconv_days = evolution_by_period(debut,fin,count_conversations,company)
	aph_nbconv = average_periode_hours(evolution_nbconv_hours)
	apd_nbconv = average_periode_days(evolution_nbconv_days)

	evolution_nbconv_hours_df = pd.DataFrame(evolution_nbconv_hours,columns=['Number of conversations','Dates','Hours'])
	evolution_nbconv_hours_df.to_excel(writer,sheet_name='evolution #conv by hours',index = False)

	evolution_nbconv_days_df = pd.DataFrame(evolution_nbconv_days,columns=['Number of conversations','Dates'])
	evolution_nbconv_days_df.to_excel(writer,sheet_name='evolution #conv by days',index = False)

	aph_nbconv_df = pd.DataFrame(aph_nbconv,columns=['Number of conversations - weekday', 'Number of conversations - weekend','Hours'])
	aph_nbconv_df.to_excel(writer,sheet_name='average #conv by hours',index = False)

	apd_nbconv_df = pd.DataFrame(apd_nbconv,columns=['Number of conversations','Days'])
	apd_nbconv_df.to_excel(writer,sheet_name='average #conv by days',index = False)

	print '1/10'

	evolution_conv_bysource = evolution_by_period(debut, fin, convs_by_source, company)
	evolution_conv_bysource, sources_conv = formalize_data(evolution_conv_bysource)
	sources_conv.append('Dates')
	evolution_conv_bysource_df = pd.DataFrame(evolution_conv_bysource, columns = sources_conv)
	evolution_conv_bysource_df.to_excel(writer, sheet_name='#conv by source', index= False)

	evolution_lvl7_bysource = evolution_by_period(debut, fin, lvl7_by_source, company)
	evolution_lvl7_bysource, sources_lvl7 = formalize_data(evolution_lvl7_bysource)
	sources_lvl7.append('Dates')
	evolution_lvl7_bysource_df = pd.DataFrame(evolution_lvl7_bysource, columns = sources_lvl7)
	evolution_lvl7_bysource_df.to_excel(writer, sheet_name='#lvl7 by source', index=False)

	aph_conv_by_source = average_periode_days(evolution_conv_bysource)
	aph_conv_by_source_df = pd.DataFrame(aph_conv_by_source, columns = sources_conv)
	aph_conv_by_source_df.to_excel(writer, sheet_name='average #conv by day by source', index = False)

	aph_lvl7_by_source = average_periode_days(evolution_lvl7_bysource)
	aph_lvl7_by_source_df = pd.DataFrame(aph_lvl7_by_source, columns = sources_lvl7)
	aph_lvl7_by_source_df.to_excel(writer, sheet_name='average #lvl7 by day by source', index = False)


	evolution_conv_bydevice = evolution_by_period(debut, fin, convs_by_device, company)
	evolution_conv_bydevice, devices = formalize_data(evolution_conv_bydevice)
	devices.append('Dates')
	evolution_conv_bydevice_df = pd.DataFrame(evolution_conv_bydevice, columns = devices)
	evolution_conv_bydevice_df.to_excel(writer, sheet_name='#conv by day dy device', index = False)

	apd_conv_by_device = average_periode_days(evolution_conv_bydevice)
	apd_conv_by_device_df = pd.DataFrame(apd_conv_by_device, columns = devices)
	apd_conv_by_device_df.to_excel(writer, sheet_name='average #conv by day by device')


	evolution_lvl7_bydevice = evolution_by_period(debut, fin, lvl7_by_device, company)
	evolution_lvl7_bydevice, devicesLvl7 = formalize_data(evolution_lvl7_bydevice)
	devicesLvl7.append('Dates')
	evolution_lvl7_bydevice_df = pd.DataFrame(evolution_lvl7_bydevice, columns = devices)
	evolution_lvl7_bydevice_df.to_excel(writer, sheet_name='#lvl7 by day dy device', index = False)

	apd_lvl7_by_device = average_periode_days(evolution_lvl7_bydevice)
	apd_lvl7_by_device_df = pd.DataFrame(apd_lvl7_by_device, columns = devicesLvl7)
	apd_lvl7_by_device_df.to_excel(writer, sheet_name='average #lvl7 by day by device')


	evolution_levels_hours = evolution_by_period(debut,fin,count_level_reached,company,'hours')
	evolution_levels_days = evolution_by_period(debut,fin,count_level_reached,company)
	aph_levels = average_periode_hours(evolution_levels_hours)
	apd_levels = average_periode_days(evolution_levels_days)

	evolution_levels_hours_df = pd.DataFrame(evolution_levels_hours,columns=['PoppedUp','Started', 'level 1', 'level 2', 'level 3', 'level 4','level 5','level 6','level 7','level 8','Exported','Dates','Hours'])
	evolution_levels_hours_df.to_excel(writer,sheet_name='evolution levels by hours',index = False)

	evolution_levels_days_df = pd.DataFrame(evolution_levels_days,columns=['PoppedUp','Started', 'level 1', 'level 2', 'level 3', 'level 4','level 5','level 6','level 7','level 8','Exported','Dates'])
	evolution_levels_days_df.to_excel(writer,sheet_name='evolution levels by days',index = False)

	aph_levels_df = pd.DataFrame(aph_levels,columns=['PoppedUp','Started', 'level 1', 'level 2', 'level 3', 'level 4','level 5','level 6','level 7','level 8','Exported','PoppedUp we', 'Started we', 'level 1 we', 'level 2 we', 'level 3 we', 'level 4 we','level 5 we','level 6 we','level 7 we','level 8 we','Exported we','Hours'])
	aph_levels_df.to_excel(writer,sheet_name='average levels by hours',index = False)

	apd_levels_df = pd.DataFrame(apd_levels,columns=['PoppedUp','Started', 'level 1', 'level 2', 'level 3', 'level 4','level 5','level 6','level 7','level 8','Exported','Days'])
	apd_levels_df.to_excel(writer,sheet_name='average levels by days',index = False)

	print '2/10'

	evolution_nps_hours = evolution_by_period(debut,fin,nps_by_time,company,'hours')
	evolution_nps_days = evolution_by_period(debut,fin,nps_by_time,company)
	aph_nps = average_periode_hours(evolution_nps_hours)
	apd_nps = average_periode_days(evolution_nps_days)

	evolution_nps_hours_df = pd.DataFrame(evolution_nps_hours,columns=['1 star', '2 stars', '3 stars', '4 stars','5 stars','Dates','Hours'])
	evolution_nps_hours_df.to_excel(writer,sheet_name='evolution nps by hours',index = False)

	evolution_nps_days_df = pd.DataFrame(evolution_nps_days,columns=['1 star', '2 stars', '3 stars', '4 stars','5 stars','Dates'])
	evolution_nps_days_df.to_excel(writer,sheet_name='evolution nps by days',index = False)

	aph_nps_df = pd.DataFrame(aph_nps,columns=['1 star', '2 stars', '3 stars', '4 stars','5 stars', '1 star we', '2 star we', '3 star we', '4 star we','5 star we','Hours'])
	aph_nps_df.to_excel(writer,sheet_name='average nps by hours',index = False)

	apd_nps_df = pd.DataFrame(apd_nps,columns=['1 star', '2 stars', '3 stars', '4 stars','5 stars','Days'])
	apd_nps_df.to_excel(writer,sheet_name='average nps by days',index = False)

	print '3/10'

	evolution_sentinel_hours = evolution_by_period(debut,fin,sentinel_level,company,'hours')
	evolution_sentinel_days = evolution_by_period(debut,fin,sentinel_level,company)
	aph_sentinel= average_periode_hours(evolution_sentinel_hours)
	apd_sentinel = average_periode_days(evolution_sentinel_days)

	evolution_sentinel_hours_df = pd.DataFrame(evolution_sentinel_hours,columns=['send_cv','opened_cv','upload_cv','export_cv','reminder1', 'reminder2', 'reminder3','returned','recover','Dates','Hours'])
	evolution_sentinel_hours_df.to_excel(writer,sheet_name='evolution sentinel by hours',index = False)

	evolution_sentinel_days_df = pd.DataFrame(evolution_sentinel_days,columns=['send_cv','opened_cv','upload_cv','export_cv','reminder1', 'reminder2', 'reminder3','returned','recover','Dates'])
	evolution_sentinel_days_df.to_excel(writer,sheet_name='evolution sentinel by days',index = False)

	aph_sentinel_df = pd.DataFrame(aph_sentinel,columns=['send_cv','opened_cv','upload_cv','export_cv','reminder1', 'reminder2', 'reminder3','returned','recover','send_cv we','opened_cv we','upload_cv we','export_cv we','reminder1 we', 'reminder2 we', 'reminder3 we','returned we','recover we','Hours'])
	aph_sentinel_df.to_excel(writer,sheet_name='average sentinel by hours',index = False)

	apd_sentinel_df = pd.DataFrame(apd_sentinel,columns=['send_cv','opened_cv','upload_cv','export_cv','reminder1', 'reminder2', 'reminder3','returned','recover','Days'])
	apd_sentinel_df.to_excel(writer,sheet_name='average sentinel by days',index = False)

	print '4/10'

	evolution_sessions_hours = evolution_by_period(debut,fin,time_by_session,company,'hours')
	evolution_sessions_days = evolution_by_period(debut,fin,time_by_session,company)
	aph_sessions = average_periode_hours(evolution_sessions_hours)
	apd_sessions = average_periode_days(evolution_sessions_days)

	evolution_sessions_hours_df = pd.DataFrame(evolution_sessions_hours,columns=['duration','welcomingQuestion', 'whyMcDonalds', 'satisfactionQuestion', 'satisfactionQuestionReply', 'unhappyClientQuestionReply','Dates','Hours'])
	evolution_sessions_hours_df.to_excel(writer,sheet_name='evolution sessions by hours',index = False)

	evolution_sessions_days_df = pd.DataFrame(evolution_sessions_days,columns=['duration','welcomingQuestion', 'whyMcDonalds', 'satisfactionQuestion', 'satisfactionQuestionReply', 'unhappyClientQuestionReply','Dates'])
	evolution_sessions_days_df.to_excel(writer,sheet_name='evolution sessions by days',index = False)

	aph_sessions_df = pd.DataFrame(aph_sessions,columns=['duration','welcomingQuestion', 'whyMcDonalds', 'satisfactionQuestion', 'satisfactionQuestionReply', 'unhappyClientQuestionReply', 'duration we','welcomingQuestion we', 'whyMcDonalds we', 'satisfactionQuestion we', 'satisfactionQuestionReply we', 'unhappyClientQuestionReply we','Hours'])
	aph_sessions_df.to_excel(writer,sheet_name='average sessions by hours',index = False)

	apd_sessions_df = pd.DataFrame(apd_sessions,columns=['duration','welcomingQuestion', 'whyMcDonalds', 'satisfactionQuestion', 'satisfactionQuestionReply', 'unhappyClientQuestionReply','Days'])
	apd_sessions_df.to_excel(writer,sheet_name='average sessions by days',index = False)

	print '5/10'

	id_conv, ids_company,level = ids_conv(debut,fin, company)

	levels,nps,sentinel = conv_by_browser(id_conv, ids_company, level,debut,fin)

	levels_df = pd.DataFrame.from_dict(levels)
	levels_df = levels_df.set_index('indexes')
	levels_df.to_excel(writer,sheet_name='levels by device')

	conversionRates = {}
	for k in levels:
		conversionRates[k] = []
		if (k == 'indexes') :
			for i in xrange(len(levels[k])-2) :
				tmp = levels[k][i+1]+'/'+levels[k][i]
				conversionRates[k].append(tmp)
		else :
			for i in xrange(len(levels[k])-2) :
				tmp = float(levels[k][i+1]) / float(levels[k][i])
				tmp = min(tmp*100, 100)
				conversionRates[k].append(tmp)

	conversionRates_df = pd.DataFrame.from_dict(conversionRates)
	conversionRates_df = conversionRates_df.set_index('indexes')
	conversionRates_df.to_excel(writer, sheet_name='conversion ratios by device')

	print '6/10'

	nps_df = pd.DataFrame.from_dict(nps)
	nps_df = nps_df.set_index('indexes')
	nps_df.to_excel(writer,sheet_name='nps by device')

	print '7/10'


	sentinel_df = pd.DataFrame.from_dict(sentinel)
	sentinel_df = sentinel_df.set_index('indexes')
	sentinel_df.to_excel(writer,sheet_name='sentinel by device')

	print '8/10'

	returns_df = pd.DataFrame(which_return(id_conv, ids_company, level,debut,fin), index = ['Return at J+0','Return at J+1','Return at J+2','Return at J+3'], columns = ['return at level3','return at level4','return at level5','return at level6','return at level7','return at level8'])
	returns_df.to_excel(writer,sheet_name = 'return level')


	print '9/10'

	candidate_returns_df = pd.DataFrame(return_with_new_conv(id_conv, ids_company, level, debut,fin), index = ['nb_candidates_return', 'nb_candidates_unique', 'nb_candidates_total'],columns = ['Number'])
	candidate_returns_df.to_excel(writer,sheet_name = 'candidates returns')

	writer.save()

	print '10/10'

def formalize_data(matrix) :
	dates = []
	sources = []
	resMatrix = {}
	for line in matrix :
		tempLine = {};
		for obj in line :
			if isinstance(obj, dict):
				sources.append(obj.get('_id'))
				tempLine[obj.get('_id')] = obj.get('value');
			elif isinstance(obj, date):
				dates.append(obj)
				resMatrix[obj] = tempLine
	unique_sources = []
	[unique_sources.append(item) for item in sources if item not in unique_sources]

	finalResult = []
	#new that we got the sources list, formalize the matrix
	for day in dates :
		lineRes = []
		for src in unique_sources :
			if src in resMatrix[day] :
				lineRes.append(resMatrix[day][src])
			else :
				lineRes.append(0)
		lineRes.append(day)
		finalResult.append(lineRes)
	return finalResult, unique_sources
