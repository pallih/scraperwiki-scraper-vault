import scraperwiki, requests, re
from bs4 import BeautifulSoup

url = 'http://www.xfront.com/us_states/'

response = requests.get(url)
bs = BeautifulSoup(response.text)

results = bs.find_all('li')
for item in results:
    title = item.find_all('p')
    name = title[0].get_text().replace('Name: ','')
    capital = title[1].get_text().replace('Capital Name: ','')
    latitude = title[2].get_text().replace('Capital Latitude: ','')
    longitude = title[3].get_text().replace('Capital Longitude: ','')
    scraperwiki.sqlite.save(unique_keys=['name'], data={ 'name' : name, 'capital' : capital, 'latitude' : latitude, 'longitude' : longitude } )import scraperwiki, requests, re
from bs4 import BeautifulSoup

url = 'http://www.xfront.com/us_states/'

response = requests.get(url)
bs = BeautifulSoup(response.text)

results = bs.find_all('li')
for item in results:
    title = item.find_all('p')
    name = title[0].get_text().replace('Name: ','')
    capital = title[1].get_text().replace('Capital Name: ','')
    latitude = title[2].get_text().replace('Capital Latitude: ','')
    longitude = title[3].get_text().replace('Capital Longitude: ','')
    scraperwiki.sqlite.save(unique_keys=['name'], data={ 'name' : name, 'capital' : capital, 'latitude' : latitude, 'longitude' : longitude } )