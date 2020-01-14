import pickle
from main import Billy
import datetime
import matplotlib.pyplot as plt
import collections
import numpy as np
db=pickle.load(open("db.pickle","rb"))

service=0
month={}
for t in db:
	if db[t].date:
		if db[t].loc in ['009','010']:
			day=db[t].date.date()
			if db[t].date.hour < 17:
				if db[t].date.isoweekday() in [1,2,3,4,5,6,7]:
					
					if day in month:
						month[day]+=db[t].serviceTotal
					else:
						month[day]=db[t].serviceTotal
					service+=db[t].serviceTotal
					
	elif db[t].date and db[t].date.isoweekday() in range(6,8):
		if db[t].date.hour < 18:
			if db[t].loc in ['009','010']:
				day=db[t].date.date()
				if not day in month:
					month[day]=0

days=sorted(month.keys())
daysLegendArr=[d.strftime("%a")[0] for d in days]
chartValues=[month[d] for d in days]
	

print(f'Total service for weekday before 5PM in lounge is {service}')
print(chartValues)
print('yh')


