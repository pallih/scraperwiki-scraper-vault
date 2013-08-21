import scraperwiki
from urllib2 import urlopen
from lxml.html import fromstring, tostring
from scraperwiki.sqlite import save
#import json

COLUMN_NAMES = [
    'name', 'price','city'
]
CAR_NAMES = [
    'Toyota', 'Honda','Chevy','Audi','Bmw','Mercedes','Dodge',
]

    


# download the page 
url = 'http://miami.craigslist.org/cto/'
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
    for car_name in CAR_NAMES:
        if(name.upper().find(car_name.upper())>=0):
            name = car_name
    row_data = {'city': city, 'price': price, 'name': name}
    save([],row_data)
    