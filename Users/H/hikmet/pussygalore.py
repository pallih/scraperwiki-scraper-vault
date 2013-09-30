import scraperwiki, requests, re
from bs4 import BeautifulSoup

url = 'http://www.amazon.de/s/ref=nb_sb_noss_2?__mk_de_DE=%C5M%C5Z%D5%D1&url=search-alias%3Daps&field-keywords='
query = 'shisha'

response = requests.get(url + query)
bs = BeautifulSoup(response.text)

results = bs.find_all(id=re.compile('result_[\d]+'))
parsed_content = []
for item in results:
    title = item.find('div', 'productTitle').get_text()
    details_link = item.find('div', 'productImage').a['href']
    details_soup = BeautifulSoup(requests.get(details_link).text)
    description_element = details_soup.find('div', 'productDescriptionWrapper')    
    if description_element:
        description = description_element.get_text()
    else:
        description = 'No description avalable.'
    parsed_content.append((title, description, details_link))

scraperwiki.sqlite.save(unique_keys=['produce'], data={ 'produce' : parsed_content } )import scraperwiki, requests, re
from bs4 import BeautifulSoup

url = 'http://www.amazon.de/s/ref=nb_sb_noss_2?__mk_de_DE=%C5M%C5Z%D5%D1&url=search-alias%3Daps&field-keywords='
query = 'shisha'

response = requests.get(url + query)
bs = BeautifulSoup(response.text)

results = bs.find_all(id=re.compile('result_[\d]+'))
parsed_content = []
for item in results:
    title = item.find('div', 'productTitle').get_text()
    details_link = item.find('div', 'productImage').a['href']
    details_soup = BeautifulSoup(requests.get(details_link).text)
    description_element = details_soup.find('div', 'productDescriptionWrapper')    
    if description_element:
        description = description_element.get_text()
    else:
        description = 'No description avalable.'
    parsed_content.append((title, description, details_link))

scraperwiki.sqlite.save(unique_keys=['produce'], data={ 'produce' : parsed_content } )