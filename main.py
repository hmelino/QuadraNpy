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
	
class Item:
	
	def strToNum(n):
		if n:
			return float(re.sub('[£,", ]','',n))
		else:
			return 0
	
	def __init__(self,list):
		self.name=list[4]
		self.server=list[6]
		self.amount=list[7]
		self.tPrice=Item.strToNum(list[8])
		self.service=Item.strToNum(list[10])
	
def addItem(l):
	item=Item()
	item.name=l[4]
	item.server=l[6]
	item.amount=l[7]
	item.tPrice=convertToNum(l[8])
	item.service=convertToNum(l[10])
	return item
	
def createBill():
	bill=Bill()
	bill.loc=None
	bill.total=0
	bill.service=0
	bill.date=None
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
			item=Item(w)
			db[billId].total+=float(item.tPrice)
			db[billId].service+=updateService(item)
			db[billId].items.append(item)
		elif billId == "CheckItemID":
				pass
		else:
			db[billId]=createBill()
			db[billId].loc=w[1]
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



def parsePaymentData(month,sD):
	newID=[]
	e=codecs.open("Reports/PaymentData"+str(month)+".csv","r",encoding="utf-8").readlines()
	for n in range(1,len(e)):
		pay=e[n].split('"')
		if "\r\n" in pay:
			# needs to get rid of this line before it gets here , for timebeing fix
			pass
		else:
			info=pay[0].split(",")
			billID=createBillID(sD,info,newID)
			if billID:
				parseDate(info,billID,sD)
				if str(billID) in sD:
					paymentType(info,pay,billID,sD)
					tableNum(info,pay,billID,sD)
				else:
					pass
					#add function to handle not processed billID
			else:
				billID=info[2]
				db[billID]=createBill()
	return sD

	
y=parsePaymentData(11,db)
		
pickle.dump(y,open('db.pickle','wb'))

newestDate=datetime.datetime(2019,11,26)
