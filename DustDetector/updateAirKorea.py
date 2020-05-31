import requests
from bs4 import BeautifulSoup
import pandas
M='&stationName=성북구&dataTerm=month&pageNo=1&numOfRows=10'
key='your key'
url='http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty?'+M+'&ServiceKey='+key+'&ver=1.3'



def updateAirKRData():
	response = requests.get(url)
	soup=BeautifulSoup(response.text,"html.parser")
	ItemList=soup.findAll('items')
	for item in ItemList:
		a=item.find('datatime').text
		b=item.find('pm10value').text
		c=item.find('pm25value').text
		d=item.find('pm10grade').text
		e=item.find('pm25grade').text
	AirKRData = a+','+b+','+c+','+d+','+e
	print(AirKRData)
	return(AirKRData)
