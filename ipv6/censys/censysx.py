from censys.search import CensysHosts
from datetime import date
import json

API_ID = ''
API_SECRET = ''
api = CensysHosts(API_ID, API_SECRET)

json_list = []
today = date.today()
output_filename = f'censys-{today}.json'

instancesIP = ['2600:1900:41a0:9b2f:0:0:0:0', '2600:1900:40d0:e44c:0:0:0:0', '2600:1901:8160:716:0:0:0:0', '2600:1900:40f0:fce8:0:0:0:0', '2600:1900:4120:d82b:0:0:0:0']

for ip in instancesIP:
      result = api.view(ip)
      json_list.append(result)
      print(result)

json_file = open(output_filename, "a")
json_file.write(json.dumps(json_list))
json_file.close()
