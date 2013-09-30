import scraperwiki
from urllib2 import urlopen
from lxml.html import fromstring, tostring
from scraperwiki.sqlite import save
#import json

# download the page 
url = 'http://www.leboncoin.fr/telephonie/offres/ile_de_france/'
raw = urlopen(url).read()
# j'obtient l'objet html
html = fromstring(raw)
#selectionne les colonnes de type <p class='row'> et récupère une liste
rows = html.cssselect('.lbc')

print rows
for row in rows:
    print row
    name = row.cssselect('.title')[0].text_content()
    print name
import scraperwiki
from urllib2 import urlopen
from lxml.html import fromstring, tostring
from scraperwiki.sqlite import save
#import json

# download the page 
url = 'http://www.leboncoin.fr/telephonie/offres/ile_de_france/'
raw = urlopen(url).read()
# j'obtient l'objet html
html = fromstring(raw)
#selectionne les colonnes de type <p class='row'> et récupère une liste
rows = html.cssselect('.lbc')

print rows
for row in rows:
    print row
    name = row.cssselect('.title')[0].text_content()
    print name
