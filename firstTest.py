import serial
from tkinter import *
from tkinter import ttk
import threading
import time

#UART용 시리얼 포트
#ard = serial.Serial(port='/dev/ttyS0')
#USB용 시리얼 포트
ard = serial.Serial(port='/dev/ttyUSB0')

win=Tk()

def updateData():
	if ard.readable():
		airHT = ard.readline()
		print(airHT)
	dustShow.configure(text = airHT)
	threading.Timer(3,updateData).start()

def exitProgram():
	print("User Aborted Program")
	win.quit()
	
win.title("My First GUI")
win.geometry("800x600")

exitButton = Button(win, text="Abort",command=exitProgram,height=4,width=12)
exitButton.pack(side = BOTTOM)

ledButton = Button(win,text="Update",command=updateData,height=4,width=12)
ledButton.pack()

dustShow = Label(win, text='Default Text')
dustShow.pack()

updateData();


mainloop()
