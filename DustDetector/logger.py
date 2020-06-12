import os.path
import time
from updateArd import updateArdData

def indoorLogging():
	logFileName = str(time.strftime('%Y-%-m-%-d',time.localtime(time.time())))
	timestemp = str(time.strftime('%H:%M',time.localtime(time.time())))
	f = open('/home/pi/Desktop/DustDetector/Logs/'+logFileName+'.txt','a')
	indoorDataRaw = updateArdData()
	indoorDataParse = indoorDataRaw.decode().split(',')
	f.write(timestemp+', PM10: '+indoorDataParse[1]+'ug/m^3, PM2.5: '+indoorDataParse[2]+'ug/m^3, Humid: '+indoorDataParse[5]+'%, temp: '+indoorDataParse[6]+"C\n")
	f.close()
indoorLogging()
