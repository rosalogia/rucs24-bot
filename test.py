import requests
import json


requestURL = "https://sis.rutgers.edu/soc/api/openSections.gzip?year=2020&term=9&campus=NB"

res = requests.get(requestURL)

x = json.loads(res.text)

print(len(x))