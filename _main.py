class Sales:
	import codecs as __codecs
	import csv as __csv
	import re as re
	import datetime
	import time
	import difflib
	from _graphFunc import getLabelsX
	from matplotlib import pyplot as __plt
	from style import ownStyle
	
	db={}
	oldestDay=None
	newestDay=None
	itemsList=None
	dataRange=None
	graphObject=__plt
	labelsX=None
	itemSoldCount=0
	
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
		e=Sales.__codecs.open(path+".csv","r",encoding='utf-8').readlines()
		
		data=[Sales.__breakCSV__(l)[1:9] for l in e[1:]]
		
		for l in data:
			if l:
				b=Sales.Billy(l)
				if not b.ID in Sales.db:
					Sales.db[b.ID]=b
				Sales.db[b.ID].items.append(Sales.Item(l))
				Sales.itemSoldCount+=1
				
	def paymentData(self,paymentsPath):
		raw=self.__codecs.open(paymentsPath+".csv","r",encoding="utf-8").readlines()
		data=[Sales.__breakCSV__(l)[2:] for l in raw]
		for line in data:
			if line:
				if line[1] in Sales.db:
					if line[2] == 'Payment':
						Sales.db[line[1]].payments.append(Sales.Payment(line,Sales.db))
					elif line[2] == 'DepositRedeemed':
						Sales.db[line[1]].deposits.append(Sales.Deposit(line))
		Sales.dataRange=(Sales.newestDay-Sales.oldestDay).days
						
	def __breakCSV__(text):
		return ['{}'.format(x) for x in list(Sales.__csv.reader([text], delimiter=','))[0]]
		
	def loadWholeYear(self,YY):
		if type(YY) is int:
			YY=str(YY)
		for m in range(1,13):
			month=f"{m:02d}"
			Sales.salesData(self,"Reports/SalesDetailed"+month+YY)
			Sales.paymentData(self,"Reports/PaymentData"+month+YY)
			print(month)
		
	def saveDB(self):
		import pickle
		pickle.dump(Sales.db,open("savedDB.pickle","wb"))
		
	def loadDB(self):
		import pickle
		Sales.db=pickle.load(open("savedDB.pickle","rb"))
		
			
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
		print(f"Searching for {searchedItem}.")
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
		
		Sales.ownStyle(Sales.graphObject)
		if Sales.labelsX is None:
			Sales.labelsX=Sales.getLabelsX(dates)
			fig = Sales.graphObject.figure()
			ax = fig.add_subplot(1, 1, 1)
			ax.set_xticklabels(labels=Sales.labelsX)

		Sales.graphObject.grid(which='minor', linestyle=':', linewidth='0.5', color='#9E807E')
		Sales.graphObject.grid(which='major', linestyle=':', linewidth='0.5', color='#9E807E')
		Sales.graphObject.plot(values,label=searchedItem)
		Sales.graphObject.legend()
		Sales.graphObject.show()
		
o=Sales()
o.loadDB()
o.findTotal("Dash Tonic")
