import requests
import json

URL = "http://127.0.0.1:3000/"
data = {"mode": "cluster", "command": "list"}
headers = {"Content-type": "application/json", "Accept": "application/json"}
r = requests.post(URL, data=json.dumps(data), headers=headers)
# r = requests.get(URL)
print(r.content)
