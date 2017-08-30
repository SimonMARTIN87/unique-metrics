from datetime import timedelta, datetime, date
import numpy as np
from produce_stats import ids_conv, nps_by_time, count_conversations, count_level_reached, sentinel_level, time_by_session

def evolution_by_period(start, end,function,company,period=None) :
	if isinstance(start, date) is False : 
		start = datetime.strptime(start, '%d/%m/%Y')

	if isinstance(end, date) is False: 
		end = datetime.strptime(end, '%d/%m/%Y')

	## calculate number of periods
	delta = timedelta(days=1)
	nb_periods = (end - start).days//delta.days

	if period == 'hours' :
		delta = timedelta(hours= 1)
		nb_periods = 24*3600*(end - start).days//delta.seconds

	timeline = []
	percentages= []

	for i in range(nb_periods) :
		temp = start + delta
		id_conv, ids_company,levels = ids_conv(start,temp,company)
		element = function(id_conv, ids_company,levels,start,end)

		print function, start, 'OK'
		
		if isinstance(element,int) : 
			percentages.append([element])
			timeline.append(start)

		else :
			percentages.append(element)
			timeline.append(start)
		
		start = temp

	percentages_with_time = list(percentages)
	for i in range(len(percentages_with_time)) :
		if period == 'hours' : 
			percentages_with_time[i] += [timeline[i],timeline[i].time()]
		else :
			percentages_with_time[i].append(timeline[i])

	return percentages_with_time


def average_periode_hours(evolution) :
	elements_hours = evolution

	### hours
	average_hours_weekday = []
	average_hours_weekend = []
	average_hours = []
	for i in range(24) :
		temp_weekday = [x[:-2] for x in elements_hours if (x[-1] == elements_hours[i][-1] and x[-2].weekday() in [0,1,2,3,4])]
		nb_days_weekday = len(temp_weekday)
		average_weekday = [0]*len(elements_hours[i][:-2])

		temp_weekend = [x[:-2] for x in elements_hours if (x[-1] == elements_hours[i][-1] and x[-2].weekday() in [5,6])]
		nb_days_weekend = len(temp_weekend)
		average_weekend = [0]*len(elements_hours[i][:-2])

		for t in temp_weekday :
			average_weekday = np.add(average_weekday,t)

		for t in temp_weekend :
			average_weekend = np.add(average_weekend,t)

		average_weekday = average_weekday/5
		average_weekend = average_weekend/2
		average_hours.append(average_weekday.tolist() + average_weekend.tolist() + [str(i)])

	return average_hours

def average_periode_days(evolution) :
	elements = evolution
	### days
	average_days = []
	days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
	for i in range(7) :
		temp = [x[:-1] for x in elements if x[-1].weekday()==elements[i][-1].weekday()]
		nb_days = len(temp)
		average = [0]*len(elements[i][:-1])
		for t in temp :
			average = np.add(average,t)
		
		average = average/(nb_days + 1e-17)
	
		average_days.append(average.tolist() + [days[i]])


	return average_days

