import requests
from bs4 import BeautifulSoup
import pandas
import time

nowDate = time.strftime('%Y%m%d',time.localtime(time.time()))
nowHour = time.strftime('%H',time.localtime(time.time()))
nowMin = time.strftime('%M',time.localtime(time.time()))
x = '60'
y = '127'
key='your key'

if(int(nowMin)<41):
	nowHour=int(nowHour)-1
	nowTime = str(nowHour)+str(nowHour)

url='http://apis.data.go.kr/1360000/VilageFcstInfoService/getUltraSrtNcst?serviceKey='+key+'&numOfRows=10&pageNo=1&base_date='+nowDate+'&base_time='+nowTime+'&nx='+x+'&ny='+y

def updateOutdoorWeather():
	response = requests.get(url)
	soup=BeautifulSoup(response.text,"html.parser")
	
	recvDate = soup.findAll('basedate')[0]
	recvTime = soup.findAll('basetime')[0]
	rainValue = soup.findAll('obsrvalue')[2]
	tempValue = soup.findAll('obsrvalue')[3]
	
	a = recvDate.text
	b=recvTime.text
	c=rainValue.text
	d=tempValue.text
	
	outdoorWeatherData = a+'/'+b+','+c+','+d
	
	print(outdoorWeatherData)
	return(outdoorWeatherData)
