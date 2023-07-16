from requests import get
from time import sleep
url = ''
prerespond = ""

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
		
