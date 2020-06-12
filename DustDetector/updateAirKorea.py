import requests
from bs4 import BeautifulSoup
import pandas
stationName = '성북구'
M='&stationName='+stationName+'&dataTerm=month&pageNo=1&numOfRows=10'
key='vxzcqtYtji%2BOm9SAYjToHIidQDa3U%2Fc9QVLcxD2iEpILXVjyvsrGR15rFBrBv7yJVkxK8XitTLjw7HoJhyxDOA%3D%3D'
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
