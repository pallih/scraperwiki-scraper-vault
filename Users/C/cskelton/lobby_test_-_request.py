import scraperwiki
import requests

# Tests Requests library on another site -- successfully

s = requests.get('http://vancouversun.com/')

print s.text

# Chokes on registry site, similar SSL errors

r = requests.get('https://eservice.pssg.gov.bc.ca/LRA/', verify=False)

print r.content


