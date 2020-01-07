import codecs
import pickle
import re
import datetime

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
class Bill():
	items=[]
	
class Item():
	pass

def convertToNum(n):
	if n:
		return float(re.sub('[£,", ]','',n))
	else:
			return 0
	
def addItem(l):
	item=Item()
	item.name=l[4]
	item.server=l[6]
	item.amount=l[7]
	item.tPrice=convertToNum(l[8])
	item.service=convertToNum(l[10])
	return item
	
def createBill(l):
	bill=Bill()
	bill.loc=l[1]
	bill.total=0
	bill.service=0
	return bill
	
	
def updateService(item):
	return float(item.service)

def updateTotal(item):
	try:
		return float(item.total)
	except :
		print(item.total)
	

def parseSalesData(month):
	e=codecs.open("Reports/SalesDetailed"+str(month)+".csv","r",encoding='utf-8').readlines()
	db={}
	for n in range(len(e)-1):
		w=e[n].split(",")
		billId=w[5]
		if billId in db:
			item=addItem(w)
			db[billId].total+=float(item.tPrice)
			db[billId].service+=updateService(item)
			db[billId].items.append(item)
		elif billId == "CheckItemID":
				pass
		else:
			db[billId]=createBill(w)
	pickle.dump(db,open("db.pickle","wb"))
	return db



e=codecs.open("Reports/PaymentData11.csv","r",encoding='utf-8').readlines()
db=parseSalesData(11)
del e

def paymentType(info,pay,billID,sD):
	pType=info[4]
	if pType == 'DepositRedeemed':
		#to handle differences in report
		if len(pay)==1:
			sD[billID].deposit=convertToNum(info[14])
		else:
			sD[billID].deposit=convertToNum(pay[3])
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

def parsePaymentData(month,sD):
	e=codecs.open("Reports/PaymentData"+str(month)+".csv","r",encoding="utf-8").readlines()
	for n in range(len(e)-1):
		pay=e[n].split('"')
		info=pay[0].split(",")
		billID=info[2]
		if str(billID) in sD:
			parseDate(info,billID,sD)
			paymentType(info,pay,billID,sD)
			tableNum(info,pay,billID,sD)
		else:
			pass
			#add function to handle not processed billID
	return sD

	
y=parsePaymentData(11,db)
		
	
