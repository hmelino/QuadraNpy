import pickle
from main import Billy
import datetime
import matplotlib.pyplot as plt
import collections
import numpy as np
db=pickle.load(open("db.pickle","rb"))
t20=pickle.load(open("chartValues.pickle","rb"))
t2020=np.array(t20)

service=0
month={}
for t in db:
	
	object=db[t]
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

import numpy as np
N = 1
men_means = (20, 35, 30, 35, 27)
#women_means = (25, 32, 34, 20, 25)

ind = np.arange(len(chartValues)) 

width = 0.35
ncv=np.array(chartValues)
plt.bar(ind, ncv, width, label='Service')
plt.bar(ind+width , t2020, width,label='Women', color="green")


plt.ylabel('Scores')
plt.title('Service charge in Lounge from bills closed before 5PM Jan 2019')

plt.xticks(ind+width/2,daysLegendArr)
plt.legend(loc='best')
ax=plt.subplot()
ax.axvspan(3,4.4, alpha=0.4, color='red')
ax.axvspan(10,11.4, alpha=0.4, color='red')
ax.axvspan(17,18.4, alpha=0.4, color='red')
ax.axvspan(24,25.4, alpha=0.4, color='red')

plt.show()
#plt.plot(chartValues)

plt.show()
	

print(f'Total service for weekday before 5PM in lounge is {service}')


"""
weekends for Jan 19
ax.axvspan(3,4.4, alpha=0.4, color='red')
ax.axvspan(10,11.4, alpha=0.4, color='red')
ax.axvspan(17,18.4, alpha=0.4, color='red')
ax.axvspan(24,25.4, alpha=0.4, color='red')
"""
#pickle.dump(chartValues,open("chartValues.pickle","wb"))
