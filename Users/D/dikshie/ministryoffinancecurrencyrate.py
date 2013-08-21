import scraperwiki
from mechanize import Browser
from BeautifulSoup import BeautifulSoup
from lxml import html
import time

mech = Browser()
url = "http://www.depkeu.go.id/ind/Currency/"
page1 = mech.open(url)
html1 = page1.read()
tree = html.fromstring(html1)
epoch_time = time.time()
for tr in tree.cssselect("table[cellpadding='0'] tr.BoardBody"):
    tds = tr.cssselect("td")
    data = { 'id': epoch_time , 'currency-country': tds[2].text_content() , 'currency-rate': tds[3].text_content() , 'deviation': tds[5].text_content()}
    epoch_time=epoch_time+1
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)
    