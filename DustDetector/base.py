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
	return 0
	
def updateData():
	indoorDataRaw = updateArdData()
	outdoorDataRaw = updateAirKRData()
	indoorDataParse = indoorDataRaw.decode().split(',')
		
	indoorDustShow.configure(text = "미세먼지 : "+indoorDataParse[3]+"㎍/㎡")
	indoorFineDustShow.configure(text = "초미세먼지 : "+indoorDataParse[4]+"㎍/㎍")
	indoorHumidShow.configure(text = "습도 : " + indoorDataParse[5] + "%")
	indoorTempShow.configure(text = "온도 : " + indoorDataParse[6] + "℃")
	
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
		indoorDustImg.config(image = indoorDustImg.img, bg='#404040')	
	elif(indoorDustTotalGrade==2):
		indoorDustImg.img=PhotoImage(file = 'normal.gif')
		indoorDustImg.config(image = indoorDustImg.img, bg='#404040')	
	elif(indoorDustTotalGrade==3):
		indoorDustImg.img=PhotoImage(file = 'bad.gif')
		indoorDustImg.config(image = indoorDustImg.img,bg='#404040')	
	elif(indoorDustToatalGrade==4):
		indoorDustImg.img=PhotoImage(file = 'worst.gif')
		indoorDustImg.config(image = indoorDustImg.img,bg='#404040')	
	else:
		indoorDustImg.img=PhotoImage(file = 'hmm.gif')
		indoorDustImg.config(image = indoorDustImg.img,bg='#404040')
	outdoorDustShow.configure(text = outdoorDataRaw)
	
def showAll():
	indoorDustImg.place(x=220,y=210)
	indoorDustShow.place(x=35, y=320)
	indoorFineDustShow.place(x=35, y=350)
	
	indoorHumidImg.place(x=30,y=380)
	indoorHumidShow.place(x=65, y=385)
	
	indoorTempImg.place(x=30,y=420)
	indoorTempShow.place(x=65, y=425)
	
	outdoorDustImg.place(x=620,y=210)
	outdoorDustShow.place(x=435, y=320)
	outdoorFineDustShow.place(x=435,y=350)
	
	outdoorHumidImg.place(x=430,y=380)
	outdoorHumidShow.place(x=465, y=385)
	
	outdoorTempImg.place(x=430,y=420)
	outdoorTempShow.place(x=465, y=425)

def showIndoor():
	indoorDustImg.place(x=360,y=200)
	indoorDustShow.place(x=80, y=365)
	indoorFineDustShow.place(x=80, y=425)
	
	indoorHumidImg.place(x=450,y=360)
	indoorHumidShow.place(x=485, y=365)
	
	indoorTempImg.place(x=450,y=420)
	indoorTempShow.place(x=485, y=425)
	
	outdoorDustImg.place_forget()
	outdoorDustShow.place_forget()
	outdoorFineDustShow.place_forget()
	
	outdoorHumidImg.place_forget()
	outdoorHumidShow.place_forget()
	
	outdoorTempImg.place_forget()
	outdoorTempShow.place_forget()

def showOutdoor():
	indoorDustImg.place_forget()
	indoorDustShow.place_forget()
	indoorFineDustShow.place_forget()
	
	indoorHumidImg.place_forget()
	indoorHumidShow.place_forget()
	
	indoorTempImg.place_forget()
	indoorTempShow.place_forget()
	
	outdoorDustImg.place(x=360,y=200)
	outdoorDustShow.place(x=80, y=365)
	outdoorFineDustShow.place(x=80,y=425)
	
	outdoorHumidImg.place(x=450,y=360)
	outdoorHumidShow.place(x=485, y=365)
	
	outdoorTempImg.place(x=450,y=420)
	outdoorTempShow.place(x=485, y=425)

def timeUpdate():
	timeShow.configure(text = time.strftime('%Y/%m/%d %a %p %I:%M;%S',time.localtime(time.time())))
	timeShow.pack(side="top",anchor="e")
	updateData()
	threading.Timer(1,timeUpdate).start()

def noticeUpdate():
	noticeShow.pack(side="top", fill="x")
	
win.title("My First GUI")
win.geometry("800x480")
win.attributes("-fullscreen",True)
win.configure(bg='#404040')

showAllButtonImg = PhotoImage(file='all.gif')
showAllButton = Button(win, image=showAllButtonImg, command = showAll, bg='#404040', highlightthickness=0, bd=0)
showAllButton.place(x=120, y=70)

showIndoorButtonImg = PhotoImage(file='indoor.gif')
showIndoorButton = Button(win, image=showIndoorButtonImg, command = showIndoor, bg='#404040', highlightthickness=0, bd=0)
showIndoorButton.place(x=360, y=70)

showOutdoorButtonImg = PhotoImage(file='outdoor.gif')
showOutdoorButton = Button(win, image=showOutdoorButtonImg, command = showOutdoor, bg='#404040', highlightthickness=0, bd=0)
showOutdoorButton.place(x=600, y=70)

exitButton = Button(win, text="종료",command=exitProgram,height=1,width=5, bg='#404040', fg='#FFFFFF', highlightthickness=0)
exitButton.place(x=720, y = 440)

indoorDustShow = Label(win, text='내부 미세먼지 정보')
indoorDustShow.configure(bg='#404040',fg='#FFFFFF')
indoorFineDustShow = Label(win, text='내부 초미세먼지 정보')
indoorFineDustShow.configure(bg='#404040',fg='#FFFFFF')
indoorDustImg = Label(win)
indoorDustImg.img=PhotoImage(file = 'hmm.gif')
indoorDustImg.config(image = indoorDustImg.img)

outdoorDustShow = Label(win, text='외부 미세먼지 정보')
outdoorDustShow.configure(bg='#404040',fg='#FFFFFF')
outdoorFineDustShow = Label(win, text='외부 초미세먼지 정보')
outdoorFineDustShow.configure(bg='#404040',fg='#FFFFFF')
outdoorDustImg = Label(win)
outdoorDustImg.img=PhotoImage(file = 'hmm.gif')
outdoorDustImg.config(image = outdoorDustImg.img)

indoorHumidImg = Label(win)
indoorHumidImg.img = PhotoImage(file='humid.gif')
indoorHumidImg.config(image=indoorHumidImg.img, bg='#404040')
indoorHumidShow = Label(win, text='내부 습도')
indoorHumidShow.configure(bg='#404040', fg='#FFFFFF')

indoorTempImg = Label(win)
indoorTempImg.img = PhotoImage(file='temp.gif')
indoorTempImg.config(image=indoorTempImg.img, bg='#404040')
indoorTempShow = Label(win, text='내부 온도')
indoorTempShow.configure(bg='#404040', fg='#FFFFFF')

outdoorHumidImg = Label(win)
outdoorHumidImg.img = PhotoImage(file='humid.gif')
outdoorHumidImg.config(image=outdoorHumidImg.img, bg='#404040')
outdoorHumidShow = Label(win, text='외부 습도')
outdoorHumidShow.configure(bg='#404040', fg='#FFFFFF')

outdoorTempImg = Label(win)
outdoorTempImg.img = PhotoImage(file='temp.gif')
outdoorTempImg.config(image=outdoorTempImg.img, bg='#404040')
outdoorTempShow = Label(win, text='외부 온도')
outdoorTempShow.configure(bg='#404040', fg='#FFFFFF')

timeShow = Label(win, text = '날짜 및 시간')
timeShow.configure(bg='#404040', fg='#FFFFFF')
noticeShow = Label(win, text = '공지사항은 여기에 표시됩니다!')
noticeShow.configure(bg='#404040', fg='#FFFFFF')

updateData()
showAll()
timeUpdate()
noticeUpdate()

mainloop()
