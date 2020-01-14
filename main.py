import codecs
import pickle
import re
import datetime
import csv
pMonth="0120"

def breakCSV(text):
		return ['{}'.format(x) for x in list(csv.reader([text], delimiter=','))[0]]

def sumTotalOfDb():
	max=0
	for w in db:
		if db[w].total > max:
			total=db[w].total
	return max

class Transaction():
	def __init__(self,loc,name,server,amount,priceTotal,service):
		self.loc=loc
		self.name=name
		self.server=server
		self.amount=amount
		self.priceTotal=priceTotal
		self.service=service
		
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
	def strToNum(n):
		if n:
			return float(re.sub('[£,", ]','',n))
		else:
			return 0
	
	def __init__(self,list,db):
		self.name=list[3]
		self.server=list[5]
		self.amount=list[6]
		try:
			self.tPrice=Item.strToNum(list[7])
		except:
			self.tPrice=Item.strToNum((list[9]))
		db[list[4]].total+=self.tPrice

def parseSalesData(month):
	e=codecs.open("Reports/SalesDetailed"+str(month)+".csv","r",encoding='utf-8').readlines()
	data=[breakCSV(l)[1:9] for l in e[1:]]
	db={}
	
	for l in data:
		if l:
			b=Billy(l)
			if not b.ID in db:
				db[b.ID]=b
			db[b.ID].items.append(Item(l,db))
	pickle.dump(db,open("db.pickle","wb"))
	return db


db=parseSalesData(pMonth)

def paymentType(info,pay,billID,sD):
	pType=info[4]
	if pType == 'DepositRedeemed':
		#to handle differences in report
		if len(pay)==1:
			sD[billID].deposit=Item.strToNum(info[14])
		else:
			sD[billID].deposit=Item.strToNum(pay[3])
	elif pType == 'Payment':
		pCategory=info[10]
		sD[billID].payType=pCategory
		if pCategory=='Credit Card':
			sD[billID].cardType=info[11]


def tableNum(info,pay,billID,sD):
	try:
		sD[billID].table=pay[5]
	except IndexError:
		if info[5]:
			sD[billID].table=info[5]
		
def parseDate(info,billID,sD):
	sD[billID].date=datetime.datetime.strptime(info[8],'%d %b %Y %H:%M:%S')

def createBillID(sD,info,newID):
	if info[2] in sD:
		return info[2]
	elif info[3] in sD:
		return info[3]
	else:
		newID.append(info)
		
class Payment:
	def __init__(self,l,db):
		self.pay=float(re.sub(",","",l[12]))
		self.type=l[9]
		self.service=float(re.sub(",","",l[11]))
		self.netPay=self.pay-self.service
		db[l[1]].serviceTotal+=self.service
		db[l[1]].date=datetime.datetime.strptime(l[6],'%d %b %Y %H:%M:%S')
		db[l[1]].loc=l[5]
		
		
		
class Deposit:
	def __init__(self,l):
		self.pay=float(re.sub(",","",l[12]))

def trackTransaction(i,billID):
	
	"""For dubugging"""
	l=[]
	if i:
		if billID == i[1]:
			print(i)
			l.append(i)
		

def parsePaymentData(month,db):
	newID=[]
	e=codecs.open("Reports/PaymentData"+str(month)+".csv","r",encoding="utf-8").readlines()
	data=[breakCSV(l)[2:] for l in e]
	for n in data:
		if n:
			#if n[1]=='1483618':
				#print(n)
			#print(n)
			if n[1] in db:
				if n[2] == 'Payment':
					db[n[1]].payments.append(Payment(n,db))
				elif n[2] == 'DepositRedeemed':
					db[n[1]].deposits.append(Deposit(n))
	return db

	
db=parsePaymentData(pMonth,db)

def fixOnlyDepositBill():
	for p in db:
		if len(db[p].payments)==0:
			print("yh")
			if db[p].deposits:
				print(p)
				db[p].serviceTotal=db[p].total*0.125
		
pickle.dump(db,open('db.pickle','wb'))





