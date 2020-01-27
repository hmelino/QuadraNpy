"""
to change
- remove csv from absolute path ? 
"""
class Sales:
	import codecs
	import csv
	import re
	import datetime
	import time
	import difflib
	
	
	db={}
	oldestDay=None
	newestDay=None
	itemsList=None
	
	class Payment:
		def __init__(self,l,db):
			self.pay=float(Sales.re.sub(",","",l[12]))
			self.type=l[9]
			if l[11]:
				self.service=float(Sales.re.sub(",","",l[11]))
			else:
				self.service=0
			self.netPay=self.pay-self.service
			Sales.db[l[1]].serviceTotal+=self.service
			date=Sales.datetime.datetime.strptime(l[6],'%d %b %Y %H:%M:%S')
			if Sales.oldestDay == None:
				Sales.oldestDay=date
				Sales.newestDay=date
			if date < Sales.oldestDay:
				Sales.oldestDay=date
			if date > Sales.newestDay:
				Sales.newestDay=date
				
				
			Sales.db[l[1]].date=date
			Sales.db[l[1]].loc=l[5]
	
	class Deposit:
		def __init__(self,l):
			self.pay=float(Sales.re.sub(",","",l[12]))
	
	class Billy():
		def __init__(self,list):
			self.ID=list[4]
			self.totalNet=0
			self.total=0
			self.serviceTotal=0
			self.loc=None
			self.date=None
			self.items=[]
			self.payments=[]
			self.deposits=[]
			
	class Item:
		def strToNum(self,n):
			if n:
				return float(Sales.re.sub('[£,", ]','',n))
			else:
				return 0
				
		def __init__(self,list):
			self.name=list[3]
			self.server=list[5]
			self.amount=list[6]
			if list[7]=='(£0.01)'or list[7]=='(£0.02)':
				self.tPrice=0.0
			else:
				try:
					self.tPrice=self.strToNum(list[7])
				except IndexError:
					self.tPrice=self.strToNum((list[9]))
			Sales.db[list[4]].total+=self.tPrice
	
	def __init__ (self):
		pass
		
	def salesData(self,path):
		count=0
		e=Sales.codecs.open(path+".csv","r",encoding='utf-8').readlines()
		data=[Sales.__breakCSV__(l)[1:9] for l in e[1:]]
		
		for l in data:
			if l:
				b=Sales.Billy(l)
				if not b.ID in Sales.db:
					Sales.db[b.ID]=b
				Sales.db[b.ID].items.append(Sales.Item(l))
		print(f"Added {count} entries")
				
	def paymentData(self,paymentsPath):
		count=0
		raw=self.codecs.open(paymentsPath+".csv","r",encoding="utf-8").readlines()
		data=[Sales.__breakCSV__(l)[2:] for l in raw]
		for line in data:
			if line:
				if line[1] in Sales.db:
					if line[2] == 'Payment':
						count+=1
						Sales.db[line[1]].payments.append(Sales.Payment(line,Sales.db))
					elif line[2] == 'DepositRedeemed':
						count+=1
						Sales.db[line[1]].deposits.append(Sales.Deposit(line))
		print(f"Added {count} entries")
						
	def __breakCSV__(text):
		return ['{}'.format(x) for x in list(Sales.csv.reader([text], delimiter=','))[0]]
		
	def getItemsList(db=db):
		print("Getting Items List")
		items=[]
		start=Sales.time.time()
		for t in Sales.db:
				for i in range(len(Sales.db[t].items)):
					items.append(Sales.db[t].items[i].name)
		uniqueItems=list(dict.fromkeys(items))
		finish=Sales.time.time()-start
		uniqueItems.sort()
		print(finish)
		Sales.itemsList = uniqueItems
		return uniqueItems
		
	def findTotalsForAYear(self,searchedItem,fromDate=None,toDate=None):
		if Sales.itemsList is None:
			Sales.getItemsList()
		if fromDate is None:
			fromDate=Sales.oldestDay
		else:
			fromDate=Sales.datetime.datetime.strptime(fromDate,'%d.%m.%Y').date()
			
		
		if toDate is None:
			toDate=Sales.newestDay
		else:
			toDate=Sales.datetime.datetime.strptime(toDate,'%d.%m.%Y').date()
		
		searchedItem=Sales.difflib.get_close_matches(searchedItem,Sales.itemsList)[0]
		print(f"Searching for {searchedItem} ?")
		start=Sales.time.time()
		dates={}
		totalCount=0
		for t in Sales.db:
			if Sales.db[t].date:
				date=Sales.db[t].date.date()
				if date>=fromDate.date() and date<=toDate.date():
					if date not in dates:
						dates[date]=0
					for i in range(len(Sales.db[t].items)):
						if searchedItem in Sales.db[t].items[i].name:
							dates[date]+=1
							totalCount+=1

		sortedDates=sorted(dates,key=lambda x:x)
		datesList=[dates[v] for v in sortedDates]
		from matplotlib import pyplot as plt
		plt.plot(datesList)
		finish=Sales.time.time()-start
		print(finish)
		print(f"Total sold {totalCount} of {searchedItem}")
		
		#new Stuff
		
		import numpy as np
		fig=plt.figure()
		plt.plot(datesList)
		ax = fig.add_subplot(1, 1, 1)
		dataRange=(toDate-fromDate).days
		print(dataRange)
		howOften=(dataRange/4.9)
		midPoints=int(dataRange/howOften)
		major_ticks = np.arange(0, dataRange, midPoints)
		ax.set_xticks(major_ticks)
		
		labelsis=["Oct 18","Dec 18","Feb 19","Apr 19","Jun 19","Aug 19","Oct 19","Dec 19","Feb 20"]
		29
		#labelsis=[Sales.datetime.datetime.strftime((fromDate+Sales.datetime.timedelta(v)),"%d-%m") for v in range(dataRange/6)]
		ax.set_xticklabels(labels=labelsis)
		plt.show()
	
		
		
							
						
report = Sales()
report.salesData("Reports/SalesDetailed0119")
report.paymentData("Reports/PaymentData0119")
w=report.getItemsList()
report.findTotalsForAYear("Cappucino")
