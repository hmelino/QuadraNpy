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
	from _graphFunc import getLabelsX
	from matplotlib import pyplot as plt
	
	db={}
	oldestDay=None
	newestDay=None
	itemsList=None
	dataRange=None
	graphObject=plt
	labelsX=None
	
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
		
	def addSalesNPayments(self,mmYY:str): 
		Sales.salesData(self,"Reports/SalesDetailed"+mmYY)
		Sales.paymentData(self,"Reports/PaymentData"+mmYY)
		print(f"Data range is from {Sales.oldestDay} to {Sales.newestDay}")
	
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
				count+=1
		print(f"Added {count} items")
				
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
		print(f"Added {count} payments")
		Sales.dataRange=(Sales.newestDay-Sales.oldestDay).days
						
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
	def findTotal(self,searchedItem,fromDate=None,toDate=None):
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
		datesNValues={}
		totalCount=0
		for t in Sales.db:
			if Sales.db[t].date:
				date=Sales.db[t].date.date()
				if date>=fromDate.date() and date<=toDate.date():
					if date not in datesNValues:
						datesNValues[date]=0
					for i in range(len(Sales.db[t].items)):
						if searchedItem in Sales.db[t].items[i].name:
							datesNValues[date]+=1
							totalCount+=1
		dates=[d for d in datesNValues.keys()]
		dates.sort()
		values=[datesNValues[v] for v in dates]
		finish=Sales.time.time()-start
		print(finish)
		print(f"Total sold {totalCount} of {searchedItem}")
		
		if Sales.labelsX is None:
			print("yh")
			Sales.labelsX=Sales.getLabelsX(dates)
			fig = Sales.graphObject.figure()
			ax = fig.add_subplot(1, 1, 1)
			ax.set_xticklabels(labels=Sales.labelsX)
		Sales.graphObject.plot(values,label=searchedItem)
		Sales.graphObject.legend()
		Sales.graphObject.show()
		
report = Sales()
report.salesData("Reports/SalesDetailed0119")
report.paymentData("Reports/PaymentData0119")
report.findTotal("Cappucino")
