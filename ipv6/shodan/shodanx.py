from shodan import Shodan
from datetime import date
import json

instancesIP = ['2600:1900:41a0:9b2f:0:0:0:0', '2600:1900:40d0:e44c:0:0:0:0', '2600:1901:8160:716:0:0:0:0', '2600:1900:40f0:fce8:0:0:0:0', '2600:1900:4120:d82b:0:0:0:0']
today = date.today()
API_KEY = ''
output_filename = f'shodan-{today}.json'
api = Shodan(API_KEY)
json_list = []

for ip in instancesIP:
	try:
		info = api.host(ip)
		print(info)

		json_list.append(info)

	except Exception as e:
		print ("\nNot found IP: "+ ip + "\n")



json_file = open(output_filename, "a")
json_file.write(json.dumps(json_list))
json_file.close()
