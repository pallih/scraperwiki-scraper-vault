import json
import requests

response = requests.get('http://statementdog.com/finance/Analysis3.php?stockid=%s&type=0&startyear=2007&startquarter=1&endyear=%d&endquarter=4&func=0')
info = json.loads(response.text)
print infoimport json
import requests

response = requests.get('http://statementdog.com/finance/Analysis3.php?stockid=%s&type=0&startyear=2007&startquarter=1&endyear=%d&endquarter=4&func=0')
info = json.loads(response.text)
print info