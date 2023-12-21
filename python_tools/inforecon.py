import sys
import requests

if len(sys.argv) < 2:
	print (f"Usage: {sys.argv[0]} <url>")
	sys.exit(0)
#req=requests.get(f"http://{sys.argv[1]}")
#print(f'Response headers:\n{req.headers}')

import socket

gethostby = socket.gethostbyname(sys.argv[1])
print(f'\nIP address of {sys.argv[1]} : {gethostby}')

#ipinfo.io

req=requests.get(f'https://ipinfo.io/{gethostby}/json')
print(f'\nIP Info: City : {req.json()["city"]}')
import json
js=json.loads(req.text)
print(f'\nIP Info: Country : {js["loc"]}')
