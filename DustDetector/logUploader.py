import time
from updateArd import updateArdData
import requests
import socket

url='http://192.168.0.22/getLog.php'

def uploadLog():
	logFileName = str(time.strftime('%Y.%m.%d',time.localtime(time.time())))
	f = open('/home/pi/Desktop/DustDetector/Logs/'+logFileName+'.txt','rb')
	upload = {'userfile':f}
	res = requests.post(url,files = upload)

	print("Reply code : ",res.status_code)
	f.close()
