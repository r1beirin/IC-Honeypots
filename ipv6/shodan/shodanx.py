from shodan import Shodan
from datetime import date
import json

#instancesIP = getIp()
# asia-east2-instance-02 		2600:1900:41a0:138:0:0:0:0
# europe-west3-instance-02 	2600:1900:40d0:7bc2:0:0:0:0
# me-west1-instance-02 		2600:1901:8160:d0:0:0:0:0
# southamerica-east1-instance-02	2600:1900:40f0:f9f2:0:0:0:0
# us-west2-instance-02 		2600:1900:4120:ecf8:0:0:0:0
instancesIP = ['2600:1900:41a0:138:0:0:0:0', '2600:1900:40d0:7bc2:0:0:0:0', '2600:1901:8160:d0:0:0:0:0', '2600:1900:40f0:f9f2:0:0:0:0', '2600:1900:4120:ecf8:0:0:0:0']
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