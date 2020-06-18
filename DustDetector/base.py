from tkinter import *
from tkinter import ttk
import tkinter.font
import threading
import time
from updateArd import updateArdData
from updateAirKorea import updateAirKRData
from updateWeatherData import updateOutdoorWeather
from logger import indoorLogging
from logUploader import uploadLog
import os
import RPi.GPIO as GPIO
import pygame

win=Tk()
pygame.init()
audio = pygame.mixer.Sound("/home/pi/Desktop/DustDetector/refresh.wav")
soundEnabled = True
pushsw=17
indoorDustTotalGrade=0

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pushsw,GPIO.IN,GPIO.PUD_UP)

def exitProgram():
	print("Entering Maintenance Mode!")
	win.quit()
	return 0
	
def turnOff():
	print("Turning Off System. Good Bye!")
	win.quit()
	os.system("sudo shutdown -h now")
	return 0

def soundToggle():
	global soundEnabled
	if(soundEnabled==True):
		soundEnabled = not soundEnabled
		soundButton.configure(text = "음소거")
	elif(soundEnabled==False):
		soundEnabled = not soundEnabled
		soundButton.configure(text="음성안내")

def updateIndoorData():
	indoorDataRaw = updateArdData()
	indoorDataParse = indoorDataRaw.decode().split(',')
		
	indoorDustShow.configure(text = "실내 PM10 : "+indoorDataParse[1]+"㎍/㎡")
	indoorFineDustShow.configure(text = "실내 PM2.5 : "+indoorDataParse[2]+"㎍/㎍")
	indoorHumidShow.configure(text = "실내습도 : " + indoorDataParse[5] + "%")
	indoorTempShow.configure(text = "실내온도 : " + indoorDataParse[6] + "℃")
	
	if(int(indoorDataParse[1])<16):
		indoorPM2Grade = 1
	elif(int(indoorDataParse[1])<51):
		indoorPM2Grade = 2
	elif(int(indoorDataParse[1])<101):
		indoorPM2Grade = 3
	else:
		indoorPM2Grade = 4
	
	if(int(indoorDataParse[2])<31):
		indoorPM10Grade = 1
	elif(int(indoorDataParse[2])<82):
		indoorPM10Grade = 2
	elif(int(indoorDataParse[2])<151):
		indoorPM10Grade = 3
	else:
		indoorPM10Grade = 4
	global indoorDustTotalGrade
	indoorDustTotalGrade = max(indoorPM2Grade,indoorPM10Grade)

	if(indoorDustTotalGrade==1):
		indoorDustImg.img=PhotoImage(file = '/home/pi/Desktop/DustDetector/good.gif')
		indoorDustImg.config(image = indoorDustImg.img, bg='#404040')	
		audio = pygame.mixer.Sound("/home/pi/Desktop/DustDetector/normal.wav")
	elif(indoorDustTotalGrade==2):
		indoorDustImg.img=PhotoImage(file = '/home/pi/Desktop/DustDetector/normal.gif')
		indoorDustImg.config(image = indoorDustImg.img, bg='#404040')	
		audio = pygame.mixer.Sound("/home/pi/Desktop/DustDetector/normal.wav")
	elif(indoorDustTotalGrade==3):
		indoorDustImg.img=PhotoImage(file = '/home/pi/Desktop/DustDetector/bad.gif')
		indoorDustImg.config(image = indoorDustImg.img,bg='#404040')	
		audio = pygame.mixer.Sound("/home/pi/Desktop/DustDetector/bad.wav")
	elif(indoorDustTotalGrade==4):
		indoorDustImg.img=PhotoImage(file = '/home/pi/Desktop/DustDetector/worst.gif')
		indoorDustImg.config(image = indoorDustImg.img,bg='#404040')	
		audio = pygame.mixer.Sound("/home/pi/Desktop/DustDetector/worst.wav")
	else:
		indoorDustImg.img=PhotoImage(file = '/home/pi/Desktop/DustDetector/hmm.gif')
		indoorDustImg.config(image = indoorDustImg.img,bg='#404040')
	indoorLogging()
	
def updateOutdoorDustData():
		outdoorDataRaw = updateAirKRData()
		outdoorDataParse = outdoorDataRaw.split(',')
		outdoorDustShow.configure(text = "실외 PM10 : "+outdoorDataParse[1]+"㎍/㎡")
		outdoorFineDustShow.configure(text = "실외 PM2.5 : "+outdoorDataParse[2]+"㎍/㎍")
		
		outdoorDustTotalGrade = max(outdoorDataParse[3],outdoorDataParse[4])
		if(outdoorDustTotalGrade=='1'):
			outdoorDustImg.img=PhotoImage(file = '/home/pi/Desktop/DustDetector/good.gif')
			outdoorDustImg.config(image = outdoorDustImg.img, bg='#404040')	
		elif(outdoorDustTotalGrade=='2'):
			outdoorDustImg.img=PhotoImage(file = '/home/pi/Desktop/DustDetector/normal.gif')
			outdoorDustImg.config(image = outdoorDustImg.img, bg='#404040')	
		elif(outdoorDustTotalGrade=='3'):
			outdoorDustImg.img=PhotoImage(file = '/home/pi/Desktop/DustDetector/bad.gif')
			outdoorDustImg.config(image = outdoorDustImg.img,bg='#404040')	
		elif(outdoorDustTotalGrade=='4'):
			outdoorDustImg.img=PhotoImage(file = '/home/pi/Desktop/DustDetector/worst.gif')
			outdoorDustImg.config(image = outdoorDustImg.img,bg='#404040')	
		else:
			outdoorDustImg.img=PhotoImage(file = '/home/pi/Desktop/DustDetector/hmm.gif')
			outdoorDustImg.config(image = outdoorDustImg.img,bg='#404040')

def updateOutdoorWeatherData():
	outdoorWeatherDataRaw = updateOutdoorWeather()
	outdoorWeatherDataParse = outdoorWeatherDataRaw.split(',')
	outdoorHumidShow.configure(text = "강수량 : " + outdoorWeatherDataParse[1] + "mm")
	outdoorTempShow.configure(text = "실외온도 : " + outdoorWeatherDataParse[2] + "℃")
	
def showAll():
	indoorDustImg.place(x=85,y=75)
	indoorDustShow.place(x=30, y=285)
	indoorFineDustShow.place(x=30, y=330)
	
	indoorHumidImg.place(x=30,y=380)
	indoorHumidShow.place(x=65, y=380)
	
	indoorTempImg.place(x=30,y=430)
	indoorTempShow.place(x=65, y=430)
	
	outdoorDustImg.place(x=430,y=75)
	outdoorDustShow.place(x=380, y=285)
	outdoorFineDustShow.place(x=380,y=330)
	
	outdoorHumidImg.place(x=380,y=380)
	outdoorHumidShow.place(x=410, y=380)
	
	outdoorTempImg.place(x=380,y=430)
	outdoorTempShow.place(x=410, y=430)

def showIndoor():
	indoorDustImg.place(x=300,y=120)
	indoorDustShow.place(x=50, y=360)
	indoorFineDustShow.place(x=50, y=420)
	
	indoorHumidImg.place(x=380,y=360)
	indoorHumidShow.place(x=415, y=360)
	
	indoorTempImg.place(x=380,y=420)
	indoorTempShow.place(x=415, y=420)
	
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
	
	outdoorDustImg.place(x=300,y=120)
	outdoorDustShow.place(x=50, y=360)
	outdoorFineDustShow.place(x=50,y=420)
	
	outdoorHumidImg.place(x=380,y=360)
	outdoorHumidShow.place(x=415, y=360)
	
	outdoorTempImg.place(x=380,y=420)
	outdoorTempShow.place(x=415, y=420)

def timeUpdate():
	timeShow.configure(text = time.strftime('%Y/%m/%d %a %p %I:%M:%S',time.localtime(time.time())))
	timeShow.pack(side="top",anchor="e")
	nowHour = time.strftime('%H', time.localtime(time.time()))
	nowMin = time.strftime('%M', time.localtime(time.time()))
	nowSec = time.strftime('%S', time.localtime(time.time()))
	
	if(nowSec=='00'):
		updateIndoorData()
		#uploadLog()
	if(nowMin=='00' and nowSec=='00'):
		updateOutdoorDustData()
		if(soundEnabled==True):
			if(indoorDustTotalGrade==1):
				audio = pygame.mixer.Sound("/home/pi/Desktop/DustDetector/good.wav")
				audio.play()
			elif(indoorDustTotalGrade==2):
				audio = pygame.mixer.Sound("/home/pi/Desktop/DustDetector/normal.wav")
				audio.play()
			elif(indoorDustTotalGrade==3):
				audio = pygame.mixer.Sound("/home/pi/Desktop/DustDetector/bad.wav")
				audio.play()
			else:
				audio = pygame.mixer.Sound("/home/pi/Desktop/DustDetector/worst.wav")
				audio.play()
	if(nowMin=='45' and nowSec=='00'):
		updateOutdoorWeatherData()
	if GPIO.input(pushsw)==0:
		exitProgram()
		
	threading.Timer(1,timeUpdate).start()

def noticeUpdate():
	noticeShow.pack(side="top", fill="x")
	
win.title("먼지안심")
win.geometry("800x480")
win.attributes("-fullscreen",False)
win.configure(bg='#404040')

font = tkinter.font.Font(size=20)
font2 = tkinter.font.Font(size=15)

showAllButtonImg = PhotoImage(file='/home/pi/Desktop/DustDetector/all.gif')
showAllButton = Button(win, image=showAllButtonImg, command = showAll, bg='#404040', highlightthickness=0, bd=0)
showAllButton.place(x=700, y=60)

showIndoorButtonImg = PhotoImage(file='/home/pi/Desktop/DustDetector/indoor.gif')
showIndoorButton = Button(win, image=showIndoorButtonImg, command = showIndoor, bg='#404040', highlightthickness=0, bd=0)
showIndoorButton.place(x=700, y=170)

showOutdoorButtonImg = PhotoImage(file='/home/pi/Desktop/DustDetector/outdoor.gif')
showOutdoorButton = Button(win, image=showOutdoorButtonImg, command = showOutdoor, bg='#404040', highlightthickness=0, bd=0)
showOutdoorButton.place(x=700, y=280)

exitButton = Button(win, text="종료",command=turnOff,height=1,width=5, bg='#404040', fg='#FFFFFF', highlightthickness=0)
exitButton.place(x=720, y = 440)
maintButton = Button(win,text="정비모드",command=exitProgram,height=1,width=5,bg='#404040',fg='#FFFFFF',highlightthickness=0)
maintButton.place(x=5,y=50)
soundButton = Button(win,text="음성안내",command=soundToggle,height=1,width=5,bg='#404040',fg='#FFFFFF',highlightthickness=0)
soundButton.place(x=5,y=70)

indoorDustShow = Label(win, text='내부 미세먼지 정보', font=font)
indoorDustShow.configure(bg='#404040',fg='#FFFFFF')
indoorFineDustShow = Label(win, text='내부 초미세먼지 정보', font=font)
indoorFineDustShow.configure(bg='#404040',fg='#FFFFFF')
indoorDustImg = Label(win)
indoorDustImg.img=PhotoImage(file = '/home/pi/Desktop/DustDetector/hmm.gif')
indoorDustImg.config(image = indoorDustImg.img)

outdoorDustShow = Label(win, text='외부 미세먼지 정보', font=font)
outdoorDustShow.configure(bg='#404040',fg='#FFFFFF')
outdoorFineDustShow = Label(win, text='외부 초미세먼지 정보', font=font)
outdoorFineDustShow.configure(bg='#404040',fg='#FFFFFF')
outdoorDustImg = Label(win)
outdoorDustImg.img=PhotoImage(file = '/home/pi/Desktop/DustDetector/hmm.gif')
outdoorDustImg.config(image = outdoorDustImg.img)

indoorHumidImg = Label(win)
indoorHumidImg.img = PhotoImage(file='/home/pi/Desktop/DustDetector/humid.gif')
indoorHumidImg.config(image=indoorHumidImg.img, bg='#404040')
indoorHumidShow = Label(win, text='내부 습도', font=font)
indoorHumidShow.configure(bg='#404040', fg='#FFFFFF')

indoorTempImg = Label(win)
indoorTempImg.img = PhotoImage(file='/home/pi/Desktop/DustDetector/temp.gif')
indoorTempImg.config(image=indoorTempImg.img, bg='#404040')
indoorTempShow = Label(win, text='내부 온도', font=font)
indoorTempShow.configure(bg='#404040', fg='#FFFFFF')

outdoorHumidImg = Label(win)
outdoorHumidImg.img = PhotoImage(file='/home/pi/Desktop/DustDetector/humid.gif')
outdoorHumidImg.config(image=outdoorHumidImg.img, bg='#404040')
outdoorHumidShow = Label(win, text='외부 습도', font=font)
outdoorHumidShow.configure(bg='#404040', fg='#FFFFFF')

outdoorTempImg = Label(win)
outdoorTempImg.img = PhotoImage(file='/home/pi/Desktop/DustDetector/temp.gif')
outdoorTempImg.config(image=outdoorTempImg.img, bg='#404040')
outdoorTempShow = Label(win, text='외부 온도', font=font)
outdoorTempShow.configure(bg='#404040', fg='#FFFFFF')

timeShow = Label(win, text = '날짜 및 시간')
timeShow.configure(bg='#404040', fg='#FFFFFF', font=font2)
noticeShow = Label(win, text = '공지사항은 여기에 표시됩니다!', font=font2)
noticeShow.configure(bg='#404040', fg='#FFFFFF')
	
updateIndoorData()
showAll()
timeUpdate()
noticeUpdate()
updateOutdoorDustData()
updateOutdoorWeatherData()
#uploadLog()

mainloop()
