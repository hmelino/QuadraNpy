j20=[0,0,24.669999999999995, 72.47, 66.63999999999999, 135.26, 15.44, 39.260000000000005,0, 61.77000000000001, 67.02, 74.6, 89.28999999999996, 23.4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
j19=[0,0,0,62.48999999999999, 41.779999999999994, 94.97000000000001, 92.16000000000001, 32.05, 16.869999999999997, 21.3, 36.03, 51.010000000000005, 117.58999999999997, 287.06999999999994, 73.23, 34.73, 27.14, 30.369999999999997, 59.39, 87.63999999999999, 232.18999999999997, 237.32999999999998, 64.99000000000001, 30.46, 48.220000000000006, 87.81, 63.56, 184.33000000000004, 75.86999999999999, 55.27, 42.34, 33.93, 48.160000000000004]

import numpy as np
import matplotlib.pyplot as plt
j2020=np.array(j20)
j2019=np.array(j19)

ind = np.arange(len(j2019)) 

width = 0.3
plt.bar(ind, j2019, width, label='2019',color="LightSalmon")
plt.bar(ind+width , j2020, width,label='2020', color="OrangeRed")


plt.ylabel('Service Charge')
plt.xlabel('Days in week')
plt.title('Service charge in Lounge from bills closed before 5PM in Jan')
#plt.grid(True)

days=['M','T',"W","T","F","S","S","M","T","W","T","F","S","S","M","T","W","T","F","S","S","M","T","W","T","F","S","S","M","T","W","T","F","S","S","M","T"]


plt.xticks(ind+width/1.2,days)
plt.legend(loc='best')
ax=plt.subplot()
#ax.axvspan(4.7,7.7, alpha=0.2, color='Blue')
#ax.axvspan(10,11.7, alpha=0.2, color='Blue')
#ax.axvspan(17,18.4, alpha=0.2, color='Blue')
#ax.axvspan(24,25.4, alpha=0.2, color='Blue')

plt.show()
#plt.plot(chartValues)

print('yh')
	
