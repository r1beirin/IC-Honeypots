from censys.search import CensysHosts
from datetime import date
import json

API_ID = ''
API_SECRET = ''
api = CensysHosts(API_ID, API_SECRET)

json_list = []
today = date.today()
output_filename = f'censys-{today}.json'

# asia-east2-instance-02 		2600:1900:41a0:138:0:0:0:0
# europe-west3-instance-02 	2600:1900:40d0:7bc2:0:0:0:0
# me-west1-instance-02 		2600:1901:8160:d0:0:0:0:0
# southamerica-east1-instance-02	2600:1900:40f0:f9f2:0:0:0:0
# us-west2-instance-02 		2600:1900:4120:ecf8:0:0:0:0
instancesIP = ['2600:1900:41a0:138:0:0:0:0', '2600:1900:40d0:7bc2:0:0:0:0', '2600:1901:8160:d0:0:0:0:0', '2600:1900:40f0:f9f2:0:0:0:0', '2600:1900:4120:ecf8:0:0:0:0']

for ip in instancesIP():
      result = api.view(ip)
      json_list.append(result)
      print(result)

json_file = open(output_filename, "a")
json_file.write(json.dumps(json_list))
json_file.close()