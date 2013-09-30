import scraperwiki     
from bs4 import BeautifulSoup
import urllib2
url="http://www.meteoschweiz.admin.ch/web/de/wetter/aktuelles_wetter.par0004.html"

page=urllib2.urlopen(url)

soup = BeautifulSoup(page.read())
#print soup

datum = soup.findAll('p', {'class':'text', 'style':'color:#8B8B8B;'})
#print datum.text

dataset = soup.findAll('div', {'class':'karte_text_hidden'})
for data in dataset:
    data={'Station Id':data['id'],
        'Sonnenscheindauer':data.text}
    scraperwiki.sqlite.save(unique_keys=['Station Id'], data=data)


import scraperwiki     
from bs4 import BeautifulSoup
import urllib2
url="http://www.meteoschweiz.admin.ch/web/de/wetter/aktuelles_wetter.par0004.html"

page=urllib2.urlopen(url)

soup = BeautifulSoup(page.read())
#print soup

datum = soup.findAll('p', {'class':'text', 'style':'color:#8B8B8B;'})
#print datum.text

dataset = soup.findAll('div', {'class':'karte_text_hidden'})
for data in dataset:
    data={'Station Id':data['id'],
        'Sonnenscheindauer':data.text}
    scraperwiki.sqlite.save(unique_keys=['Station Id'], data=data)


