import serial

#UART용 시리얼 포트
ard = serial.Serial(port='/dev/ttyS0')
#USB용 시리얼 포트
#ard = serial.Serial(port='/dev/ttyUSB0')

def updateArdData():
	if ard.readable():
		ardData = ard.readline()
		print(ardData)
		return(ardData)
	else:
		print("Arduino Connection Error!")

updateArdData()
