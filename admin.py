from requests import get
from time import sleep
url = ''
prerespond = ""


while True:
	code = input("code-->")
	req = get(url+f'/admin?code={code}')
	ssda = True
	while ssda:
		if prerespond != get(url+f'/gmeres').text:
			res = get(url+f'/gmeres')
			print(res.text)
			prerespond = res.text
			ssda = False
		else:
			sleep(2.7)
		
