import scraperwiki
import urllib2
from bs4 import BeautifulSoup
import re

"""
#StarBazaar
chain1 = "StarBazaar"
url_base ="https://www.starbazaarindia.com/"
city = ["sl_ahmedabad.html", "sl_aurangabad.html", "sl_bengaluru.html", "sl_chennai.html",
        "sl_kolhapur.html", "sl_mumbai.html", "sl_pune.html", "sl_surat.html"]

def get_page(url,city):
    content = None
    try:
        content = urllib2.urlopen(url+city).read()
        return content
    except urllib2.URLError:
        return content

def extract_main (page):
    soup = BeautifulSoup(page)
    content = soup.find_all('div', attrs={'class' : 'address-cont-box', 'class':'address-cont'})
    return content

contentAll = []
for i in range (1,len(city)):
    contentAll.append(extract_main(get_page(url_base,city[i])))
    ##scraperwiki.sqlite.save(unique_keys=["id"], data={"id":i,"chain": chain, "url": url_base+city[i], "content":extract_main(get_page(url_base,city[i]))})

data = scraperwiki.sqlite.select(
    '''* FROM swdata ORDER BY id '''
)

print data 

print contentAll
"""

#Reliance
chain2 = "Reliance"
url_base2 ="http://storelocator.ril.com/getAllStores.aspx?flag=false&Searchformat=All&distance=500&latitude=%s&longitude=%s"
lat = "26.9124165"
lon = "75.78728790000002"
url_full= url_base2 %(lat,lon)

def get_page_ajax(url,lat,lon):
    content = None
    try:
        content = urllib2.urlopen(url_full).read()
        return content
    except urllib2.URLError:
        return content

store_details = (each i in get_page_ajax(url_base2, lat, lon).split('$')).split('^')


print url_full
print store_details
    