import serial
from tkinter import *
from tkinter import ttk
import threading
import time
from updateArd import updateArdData
from updateAirKorea import updateAirKRData

win=Tk()


def exitProgram():
	print("User Aborted Program")
	win.quit()
	
def updateData():
	indoorDataRaw = updateArdData()
	outdoorDataRaw = updateAirKRData()
	indoorDataParse = indoorDataRaw.decode().split(',')
	indoorDustData = "PM 2.5 GRIMM : "+indoorDataParse[1] + ", PM 10 GRIMM : " + indoorDataParse[2]
	indoorTHData = "Humid : " + indoorDataParse[5] +"%, Temp : "+indoorDataParse[6]+"C"
	indoorDustShow.configure(text = indoorDustData)
	indoorTHShow.configure(text = indoorTHData)
	
	if(int(indoorDataParse[1])<16):
		indoorPM2Grade = 1
	elif(int(indoorDataParse[1])<51):
		indoorPM2Grade = 2
	elif(int(indoorDataParse[1])<101):
		indoorPM2Grade = 3
	else:
		indoorPM2Grade = 4
	
	if(int(indoorDataParse[2])<16):
		indoorPM10Grade = 1
	elif(int(indoorDataParse[2])<51):
		indoorPM10Grade = 2
	elif(int(indoorDataParse[2])<101):
		indoorPM10Grade = 3
	else:
		indoorPM10Grade = 4
	
	indoorDustTotalGrade = max(indoorPM2Grade,indoorPM10Grade)
	print(indoorDustTotalGrade)

	if(indoorDustTotalGrade==1):
		indoorDustImg.img=PhotoImage(file = 'good.gif')
		indoorDustImg.config(image = indoorDustImg.img)	
	elif(indoorDustTotalGrade==2):
		indoorDustImg.img=PhotoImage(file = 'normal.gif')
		indoorDustImg.config(image = indoorDustImg.img)	
	elif(indoorDustTotalGrade==3):
		indoorDustImg.img=PhotoImage(file = 'bad.gif')
		indoorDustImg.config(image = indoorDustImg.img)	
	elif(indoorDustToatalGrade==4):
		indoorDustImg.img=PhotoImage(file = 'worst.gif')
		indoorDustImg.config(image = indoorDustImg.img)	
	else:
		indoorDustImg.img=PhotoImage(file = 'hmm.gif')
		indoorDustImg.config(image = indoorDustImg.img)	
	
	outdoorDustShow.configure(text = outdoorDataRaw)
	threading.Timer(1,updateData).start()
	
def showAll():
	indoorDustImg.place(x=130,y=100)
	indoorDustShow.place(x=50, y=200)
	indoorTHShow.place(x=75, y=230)
	outdoorDustImg.place(x=500,y=100)
	outdoorDustShow.place(x=450, y=200)
	outdoorTHShow.place(x=490, y=230)

def showIndoor():
	indoorDustImg.place(x=330,y=100)
	indoorDustShow.place(x=250, y=200)
	indoorTHShow.place(x=275, y=230)
	outdoorDustImg.place_forget()
	outdoorDustShow.place_forget()
	outdoorTHShow.place_forget()

def showOutdoor():
	indoorDustImg.place_forget()
	indoorDustShow.place_forget()
	indoorTHShow.place_forget()
	outdoorDustImg.place(x=330,y=100)
	outdoorDustShow.place(x=250, y=200)
	outdoorTHShow.place(x=290, y=230)
	

def noticeUpdate():
	noticeShow.pack(side="top", fill="x")
	
win.title("My First GUI")
win.geometry("800x480")

showAllButton = Button(win, text="모두 보기", command = showAll,height = 1, width = 10)
showAllButton.place(x=5, y=400)

showIndoorButton = Button(win, text="실내 보기", command = showIndoor,height = 1, width = 10)
showIndoorButton.place(x=110, y=400)

showIndoorButton = Button(win, text="실외 보기", command = showOutdoor,height = 1, width = 10)
showIndoorButton.place(x=215, y=400)

exitButton = Button(win, text="종료",command=exitProgram,height=1,width=10)
exitButton.place(x=690, y = 400)

indoorDustShow = Label(win, text='Outdoor Dust Data Here')
indoorDustImg = Label(win)
indoorDustImg.img=PhotoImage(file = 'hmm.gif')
indoorDustImg.config(image = indoorDustImg.img)

outdoorDustShow = Label(win, text='Outdoor Dust Data Here')
outdoorDustImg = Label(win)
outdoorDustImg.img=PhotoImage(file = 'hmm.gif')
outdoorDustImg.config(image = outdoorDustImg.img)

indoorTHShow = Label(win, text='Indoor Humid Temp & Data here')
outdoorTHShow = Label(win, text='Outdoor Humid & Temp Here')
noticeShow = Label(win, text = 'Noooooooootice Shooooooows Heeeeeeere!')

updateData()
showAll()
noticeUpdate()

mainloop()
