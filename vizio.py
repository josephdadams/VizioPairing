#!/usr/bin/python3

# File name: vizio.py
# Version: 1.0.0
# Author: Joseph Adams
# Email: josephdadams@gmail.com
# Date created: 1/10/2023
# Date last modified: 1/10/2023

from requests.adapters import HTTPAdapter
from urllib3 import PoolManager
import requests
import ssl
import json
import sys

class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)


s = requests.session()
s.mount('https://', MyAdapter())

port = '9000'

tv_ip = input('What is the TV IP Address? ')

port = input('What port? Newer TV\'s use 7345, older ones use 9000: ') or '7345'

if tv_ip != '':
	try:
		r = s.put(url=f'https://{tv_ip}:{port}/pairing/start',
				json={"DEVICE_ID": "python-app",
						"DEVICE_NAME": "Python App"},
				headers={'Content-Type': 'application/json'},
				verify=False)

		#print(r.content)
	except Exception as e:
		print(e)
		print('Is the TV online? Maybe try the other port number?')
		sys.exit(1)

	try:
		contentRequest = json.loads(r.content)

		if contentRequest['STATUS']['RESULT'] == 'SUCCESS':
			token = contentRequest['ITEM']['PAIRING_REQ_TOKEN']
			print('Pairing Req Token is: ' + str(token))

			print('What is the 4-Digit PIN on the TV?')
			pin = input('PIN: ')

			s = requests.session()
			s.mount('https://', MyAdapter())

			r = s.put(url=f'https://{tv_ip}:{port}/pairing/pair',
				json={"DEVICE_ID": "python-app",
						"CHALLENGE_TYPE": 1,
						"RESPONSE_VALUE": pin,
						"PAIRING_REQ_TOKEN": token},
				headers={'Content-Type': 'application/json'},
				verify=False)
			
			contentPair = json.loads(r.content)

			if contentPair['STATUS']['RESULT'] == 'SUCCESS':
				print('The Auth Token is: ' + contentPair['ITEM']['AUTH_TOKEN'])
			else:
				print('Error: See below:')
				print(contentPair['STATUS']['RESULT'])
		elif contentRequest['STATUS']['RESULT'] == 'BLOCKED':
				print('Operation blocked. Is the TV already showing a PIN code? Wait until it goes away, and then try again.')
		else:
			print('Error')
	except Exception as e:
		print(e)
		print('Exiting due to error.')
		sys.exit(1)
else:
	print('TV IP was blank. Try again.')
	sys.exit(0)