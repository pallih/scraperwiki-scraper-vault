import scraperwiki
from urllib2 import urlopen
from lxml.html import fromstring, tostring
from scraperwiki.sqlite import save
#import json

COLUMN_NAMES = [
    'name', 'price','city'
]
PHONE_NAMES = [
    'Iphone', 'Samsung','Motorola','Blackberry'
]

    


# download the page 
url = 'http://sfbay.craigslist.org/moa/'
raw = urlopen(url).read()
# j'obtient l'objet html
html = fromstring(raw)
#selectionne les colonnes de type <p class='row'> et récupère une liste
rows = html.cssselect('p.row')


for row in rows:
    name = row.cssselect('a')[0].text_content()
    price = row.cssselect('.itempp')[0].text_content()
    city = row.cssselect('.itempn')[0].text_content()
    #print city
    #print row_data
    for phone_name in PHONE_NAMES:
        if(name.upper().find(phone_name.upper())>=0):
            name = phone_name
    row_data = {'city': city, 'price': price, 'name': name}
    save([],row_data)
    