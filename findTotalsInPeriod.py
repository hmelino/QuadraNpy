import pickle
import datetime
from main import Billy,Item,Payment,Deposit
import time 
from matplotlib import pyplot as plt
import difflib

#hotDrinks=['Cappuccino','Latte','Espresso','Double Espresso','Americano','Flat White','Mocha','Macchiato','Double Macchiato','Hot Chocolate','Earl Grey','English Breakfast','Camomile Tea','Peppermint','Green Tea','Fresh Mint Tea']
print("Loading dataset...")
start=time.time()
db=pickle.load(open("db.pickle","rb"))
print(time.time()-start)

def createM


def findAllItems(db=db):
	print("Getting Items List")
	items=[]
	start=time.time()
	for t in db:
			for i in range(len(db[t].items)):
				items.append(db[t].items[i].name)
	del db
	uniqueItems=list(dict.fromkeys(items))
	finish=time.time()-start
	uniqueItems.sort()
	print(finish)
	return uniqueItems
	
items=findAllItems()
print("Type: \nfindTotalsForAYear(item,*fromDate,*toDate)\n -for sales graph\nmostSellingItems(howMany)\n -most sold items")

def findTotalsForAYear(searchedItem,db=db,items=items,fromDate='01.01.2019',toDate='01.01.2020'):
	searchedItem=difflib.get_close_matches(searchedItem,items)[0]
	print(f"Searching for {searchedItem}")
	start=time.time()
	fromD=datetime.datetime.strptime(fromDate,'%d.%m.%Y').date()
	toD=datetime.datetime.strptime(toDate,'%d.%m.%Y').date()
	dates={}
	totalCount=0
	for t in db:
		if db[t].date:
			date=db[t].date.date()
			if date>fromD and date<toD:
				if date not in dates:
					dates[date]=0
				o=db[t]
				for i in range(len(db[t].items)):
					if searchedItem in db[t].items[i].name:
						dates[date]+=1
						totalCount+=1
	del db
	sortedDates=sorted(dates,key=lambda x:x)
	datesList=[dates[v] for v in sortedDates]
	plt.plot(datesList)
	finish=time.time()-start
	print(finish)
	print(f"Total sold {totalCount} of {searchedItem}")
	#new Stuff
	
	
	import numpy as np
	fig=plt.figure()
	plt.plot(datesList)
	ax = fig.add_subplot(1, 1, 1)
	dataRange=(toD-fromD).days
	print(dataRange)
	howOften=6
	midPoints=int(dataRange/howOften)
	major_ticks = np.arange(0, dataRange, midPoints)
	ax.set_xticks(major_ticks)
	labelsis=["Oct 18","Dec 18","Feb 19","Apr 19","Jun 19","Aug 19","Oct 19","Dec 19","Feb 20"]
	ax.set_xticklabels(labels=labelsis)
	
	#endOfNewStuff
	
	
	
	
	
	
	plt.show()
	
def mostSellingItems(howMany,db=db,fromDate='01.01.2019',toDate='01.01.2020'):
	fromD=datetime.datetime.strptime(fromDate,'%d.%m.%Y').date()
	toD=datetime.datetime.strptime(toDate,'%d.%m.%Y').date()
	print("Creating list of most sold items")
	start=time.time()
	sales={}
	for t in db:
		for i in range(len(db[t].items)):
			name=db[t].items[i].name
			if name in sales:
				sales[name]+=1
			else:
				sales[name]=1
	print(time.time()-start)
	salesN=sorted(sales.items(),key=lambda x:x[1],reverse=True)
	print(f"Top {howMany} sold items")
	lSales=list(salesN)
	for i in range(0,howMany):
		print(f" {lSales[i][1]} of {lSales[i][0]} ")
	del db
	
	
