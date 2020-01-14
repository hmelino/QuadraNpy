import pickle
from main import Billy
db=pickle.load(open("db.pickle","rb"))


c=0
for t in db:
	
	list=db[t]
	netPay=0
	deposits=0
	for p in range(len(db[t].payments)):
		netPay+=db[t].payments[p].netPay
	if db[t].deposits:
		for d in range(len(db[t].deposits)):
			deposits+=db[t].deposits[d].pay
	if (netPay+deposits)-db[t].total>1:
		
		print(db[t].ID)
		print(f"{netPay+deposits} | {db[t].total}")
		c+=1
print(f"Total count is {c}")
