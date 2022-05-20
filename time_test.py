import datetime
import json

with open('forcast.json','r') as infile:
	data = json.load(infile)

all_days = {}
for each_date in data['list']:
	this_date = each_date['dt']
	millseconds = this_date
	this_date = datetime.datetime.fromtimestamp(millseconds)

	if not this_date.date() in all_days:
		all_days[this_date.date()] = [each_date]
	else:
		these_days = all_days[this_date.date()]
		these_days.append(each_date)
		all_days[this_date.date()] = these_days

forcast_data = {}
for each_date in all_days:
	max_temp = -50
	min_temp = 100
	descriptions = {}
	# print('**',each_date)

	for each_forcast in all_days[each_date]:
		# print(each_forcast)
		if float(each_forcast['main']['temp_max']) > max_temp:
			max_temp = float(each_forcast['main']['temp'])

		if float(each_forcast['main']['temp_min']) < min_temp:
			min_temp = float(each_forcast['main']['temp'])

	# 	this_time = datetime.datetime.fromtimestamp(each_forcast['dt']).time()
	# 	for each_weather in each_forcast['weather']:
	# 		print(each_weather)
	# 	descriptions[this_time] = each_forcast['weather'][0]['description']
	# print()
	# print(descriptions)
	#
	# morning = datetime.datetime()
	# for each_description in descriptions:
	#


	print(f"Max temp for {each_date} is {max_temp} and the min is {min_temp}")



