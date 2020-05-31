import os.path
import time
from updateArd import updateArdData

def indoorLogging():
	logFileName = str(time.strftime('%Y년%m월%d일',time.localtime(time.time())))
	timestemp = str(time.strftime('%H:%M',time.localtime(time.time())))
	f = open('/home/pi/Desktop/DustDetector/Logs/'+logFileName+'.txt','a')
	indoorDataRaw = updateArdData()
	indoorDataParse = indoorDataRaw.decode().split(',')
	f.write(timestemp+', 미세먼지:'+indoorDataParse[1]+'㎍/㎡, 초미세먼지:'+indoorDataParse[2]+'㎍/㎡, 습도:'+indoorDataParse[5]+'%, 온도:'+indoorDataParse[6]+"℃\n")
	f.close()
