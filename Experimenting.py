import codecs
import csv
import re
from sys import getsizeof
import time

def breakCSV(text):
		return ['{}'.format(x) for x in list(csv.reader([text], delimiter=','))[0]]

def loadNProcessSalesFile(month:str):
	e=codecs.open(f"Reports/SalesDetailed{month}.csv","r",encoding='utf-8').readlines()
	db= (Item(breakCSV(s)[1:9]) for s in e[1:] if breakCSV(s))
	return db
	"""
	for i in db:
		item=Item(i)
		if item.billID in:
	return {i[4]:Item(i) for i in db[1:] if i}
	"""

def loadNProcessPaymentFile(month:str):
	e=codecs.open(f"Reports/PaymentData{month}.csv","r",encoding='utf-8').readlines()
	payData = [breakCSV(s)[2:] for s in e]
	return payData
	for payment in range(1,len(payData)):
		print(payData[payment].billID)
		
class Payment():
	def __init__(self,list):
		self.billID=list[0]
		self.checkID=list[1]
		self.pName=list[2]
		self.table=list[3]
		self
		
		
class Item:
	def turnToNum(n):
		if 'ItemsTotal' in n:
			return 0
		if n:
			q=n[1:]
			return float(re.sub(',','',q))
	
	def __init__(self,list):
		self.loc=list[0]
		self.name=list[3]
		self.billID=list[4]
		self.user=list[5]
		self.payments=[]
		self.date=None
		self.amount=list[6]
		self.priceT=Item.turnToNum(list[7])
		if self.priceT:
			self.service=round(self.priceT*0.11111,2)
			self.price=self.priceT-self.service
start=time.time()
data=loadNProcessSalesFile("11")
print(time.time()-start)
data2=loadNProcessPaymentFile("11")
data3=[t for t in data2]



