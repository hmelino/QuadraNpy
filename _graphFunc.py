
def getLabelsX(dates):
	import numpy as np
	import datetime
	
	def getRightDate(i):
		#parse string date based on index number
		indexN=int((daysRange*percent)*i)
		date=dates[indexN]
		return datetime.datetime.strftime(date,dFormat)
	
	def dateFormat():
		period=(max(dates)-min(dates)).days
		if daysRange<32:
			return "%d/%m"
		return "%m/%Y"
		
	howManyTicks=6
	percent=int(100/6)/100
	daysRange=len(dates)
	dFormat=dateFormat()
	
	labelsX = [getRightDate(i) for i in range(howManyTicks+1)]
	return labelsX
