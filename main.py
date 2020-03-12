class Sales:
	import codecs as __codecs
	import csv as __csv
	import re as re
	import datetime
	import time
	import difflib
	from QuadraNpy._graphFunc import getLabelsX
	from matplotlib import pyplot as __plt
	from QuadraNpy.style import ownStyle
	
	
	db={}
	oldestDay=None
	newestDay=None
	itemsList=None
	dataRange=None
	graphObject=__plt
	labelsX=None
	itemSoldCount=0
	
	class Payment:
		def updateOldestNewestDay(self,date):
			if Sales.oldestDay == None:
				Sales.oldestDay=date
				Sales.newestDay=date
				
			if date < Sales.oldestDay:
				Sales.oldestDay=date
			if date > Sales.newestDay:
				Sales.newestDay=date

		def __init__(self,l,db):
			billId=l[1]
			self.pay=float(Sales.re.sub(",","",l[12]))
			self.type=l[9]
			self.service=0
			if l[11]:
					self.service=float(Sales.re.sub(",","",l[11]))	
			self.netPay=self.pay-self.service

			if billId not in Sales.db:
			#create bill if doesnt exist yet
				print(f'new exntry {billId}')
				Sales.db[billId]=Sales.Billy(billId)
			
			date=Sales.datetime.datetime.strptime(l[6],'%d %b %Y %H:%M:%S')
			self.updateOldestNewestDay(date)
			Sales.db[billId].date=date
			Sales.db[billId].serviceTotal+=self.service
			Sales.db[billId].loc=l[5]
			
	class Deposit:
		def __init__(self,row):
			self.pay=float(Sales.re.sub(",","",row[12]))
			self.name=row[16]

	
	class Billy():
		def __init__(self,billID):
			self.ID=billID
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
			
	def loadFolder(self,path):
		import os
		directory=os.fsencode(path)
		files = [str(f).split("'")[1] for f in os.listdir(directory)]
		for f in files:
			fullPath=f'{path}/{f}'
			with open(fullPath,'r') as file:
				#Assign correct file to its processing function Sales/Payment reports
				data=file.readlines()[0].split(',')
				if data[4] == 'PaymentName':
					self.paymentData(fullPath)
				elif data[4] == 'Description':
					self.salesData(fullPath)
				else:
					print(f'Unrecognised file {f}')
				print(f'Loaded {f}')
		
	def addSalesNPayments(self,mmYY:str): 
		Sales.salesData("Reports/SalesDetailed"+mmYY)
		Sales.paymentData("Reports/PaymentData"+mmYY)
		print(f"Data range is from {Sales.oldestDay} to {Sales.newestDay}")
	
	def salesData(self,path):
		count=0
		raw=Sales.__codecs.open(path,"r",encoding='utf-8').readlines()
		data=[Sales.__breakCSV__(l)[1:9] for l in raw[1:]]
		
		for row in data:
			if row:
				billID=row[4]
				if billID not in Sales.db:
					Sales.db[billID]=Sales.Billy(billID)
				
				Sales.db[billID].items.append(Sales.Item(row))
				Sales.itemSoldCount+=1
				
	def paymentData(self,paymentsPath):
		def addDeposit(billID,line):
			deposit=line
			print(line)

		raw=self.__codecs.open(paymentsPath,"r",encoding="utf-8").readlines()
		data=[Sales.__breakCSV__(l)[2:] for l in raw][1:]
		for row in data:
			if row:
			# protection against empty rows in report
				billID=row[1]
				transType=row[2]
				if billID in Sales.db:
				#if transaction exists
					if transType == 'Payment':
						Sales.db[billID].payments.append(Sales.Payment(row,Sales.db))
					elif transType == 'DepositRedeemed':
						Sales.db[billID].deposits.append(Sales.Deposit(row))
				else:
					Sales.db[billID]=Sales.Billy(billID)
					if transType == 'Payment':
						Sales.db[billID].payments.append(Sales.Payment(row,Sales.db))
					elif transType == 'DepositRedeemed':
						#Sales.db[billID]=self.Billy(billID)
						Sales.db[billID].deposits.append(Sales.Deposit(row))

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
