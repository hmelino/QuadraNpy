def plotGraph(datesNValues):
	from matplotlib import pyplot as plt
	import numpy as np
	import datetime
	
	def getRightDate(i):
				#parse string date based on index number
				indexN=int((daysRange*percent)*i)
				date=datesList[indexN]
				return datetime.datetime.strftime(date,dFormat)
	
	def dateFormat():
		period=(newestDay-oldestDay).days
		if daysRange<32:
			return "%d/%m"
		return "%m/%Y"
		
	datesList=[d for d in datesNValues.keys()]
	datesList.sort()
	
	fig=plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	daysRange=len(datesNValues)
	howManyTicks=6
	percent=int(100/6)/100
	oldestDay=min(datesNValues)
	newestDay=max(datesNValues)

	dFormat=dateFormat()
	"""
			def getRightDate(i):
				#parse string date based on index number of all dates list
				indexN=int((daysRange*percent)*i)
				date=datesList[indexN]
				return Sales.datetime.datetime.strftime(date,dFormat)
				"""
			
	valuesList=[datesNValues[d] for d in datesList]
	plt.plot(valuesList)
	howOften=(daysRange/4.9)-1
			
	midPoints=int(daysRange/howOften)
	major_ticks = np.arange(0, daysRange, midPoints)
	ax.set_xticks(major_ticks)
			
	labelsX=[getRightDate(i) for i in range(howManyTicks+1)]
			
	ax.set_xticklabels(labels=labelsX)
	plt.show()
