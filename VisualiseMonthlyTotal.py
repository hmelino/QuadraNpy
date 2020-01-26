import pickle
import matplotlib.pyplot as plt
from main import Billy
db=pickle.load(open("db.pickle","rb"))

dates={}
for key in db.keys():
	if db[key].date:
		date=db[key].date.date()
		if date not in dates:
			dates[date]=0
			
for t in db:
	if db[t].date:
		total=db[t].total
		dates[db[t].date.date()]+=total

sortedKeys=sorted(dates,key=lambda x:x)
results=[dates[f] for f in sortedKeys]
plt.plot(results)
plt.show()
