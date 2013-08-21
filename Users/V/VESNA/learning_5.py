import scraperwiki

URL = "http://www.parlament.rs/national-assembly/composition/members-of-parliament/current-convocation.487.html"
PREFIX = "http://www.parlament.rs/"

# Teach it read data from the web:
import requests
# Grab the page from the web: 
response = requests.get(URL)

# Teach it how to interpret HTML web pages:
from lxml import html 

# Convert the HTML to "document object model": 
document = html.document_fromstring(response.content)

# Asking it: Where are your tables? 
table = document.find('.//table') 

print len(table.findall('.//tr'))

# For each row: 
for row in table.findall('.//tr'):
    link = row.find('./td//a')
    if link is None:
        continue
    url = PREFIX + link.get('href')
    response = requests.get(url)
    mp_document = html.document_fromstring(response.content)

    name = mp_document.find('.//h2').xpath("string()")
    place = mp_document.findall('.//p')[7].text

    print [name, place]

    data = {'name': name, 'place': place}
    scraperwiki.sqlite.save(unique_keys=['name'], data=data)


