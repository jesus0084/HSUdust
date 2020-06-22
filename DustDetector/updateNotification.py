import requests

def getNotification():
	url = 'http://192.168.0.22/Annc/notification.txt'
	notiResponse = requests.get(url)
	return notiResponse.text
