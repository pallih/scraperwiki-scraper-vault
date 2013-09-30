import scraperwiki
from urllib2 import urlopen
from lxml.html import fromstring, tostring
from scraperwiki.sqlite import save
import re

non_decimal = re.compile(r'[^\d,]+')
TOTAL_NUMBER_OF_PAGES = 680

for page_number in range(1,TOTAL_NUMBER_OF_PAGES):
    document = urlopen('http://www.swoggi.fr/fr-fr/encheres-terminees.aspx?status=4&page=1'+ str(page_number))
    raw = document.read()
    html = fromstring(raw)
    rows = html.cssselect('.a_box')
    for row in rows:
            divs = row.cssselect('div')#.cssselect('a')[0]
            name = divs[2].cssselect('a')[0].text_content()
            prices = row.cssselect('.f12')
            auction_price = non_decimal.sub('',prices[0].text_content())
            real_price = non_decimal.sub('', prices[1].text_content())
            row_data = {'name': name, 'auction_price': auction_price, 'real_price': real_price}
            #print auction_price, real_price
            save([],row_data)import scraperwiki
from urllib2 import urlopen
from lxml.html import fromstring, tostring
from scraperwiki.sqlite import save
import re

non_decimal = re.compile(r'[^\d,]+')
TOTAL_NUMBER_OF_PAGES = 680

for page_number in range(1,TOTAL_NUMBER_OF_PAGES):
    document = urlopen('http://www.swoggi.fr/fr-fr/encheres-terminees.aspx?status=4&page=1'+ str(page_number))
    raw = document.read()
    html = fromstring(raw)
    rows = html.cssselect('.a_box')
    for row in rows:
            divs = row.cssselect('div')#.cssselect('a')[0]
            name = divs[2].cssselect('a')[0].text_content()
            prices = row.cssselect('.f12')
            auction_price = non_decimal.sub('',prices[0].text_content())
            real_price = non_decimal.sub('', prices[1].text_content())
            row_data = {'name': name, 'auction_price': auction_price, 'real_price': real_price}
            #print auction_price, real_price
            save([],row_data)