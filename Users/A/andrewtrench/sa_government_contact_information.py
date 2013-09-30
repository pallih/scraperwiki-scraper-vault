import scraperwiki
import BeautifulSoup
import mechanize
import cookielib
import lxml.html

#scrape South African government official contact information

url = 'http://www.gcis.gov.za/gcis/directory.jsp?dir=6&cat=27&org=2254&ref=cat'

html = scraperwiki.scrape(url)

root = lxml.html.fromstring(html)
for tr in root.cssselect("div[class='tableinfo']"): 
    tds = tr.cssselect("td")

    print tds[0].text_content()

#    data = { 'address' : tds[0].text_content(), 'more data' : int(tds[4].text_content()) }
 #   print data



import scraperwiki
import BeautifulSoup
import mechanize
import cookielib
import lxml.html

#scrape South African government official contact information

url = 'http://www.gcis.gov.za/gcis/directory.jsp?dir=6&cat=27&org=2254&ref=cat'

html = scraperwiki.scrape(url)

root = lxml.html.fromstring(html)
for tr in root.cssselect("div[class='tableinfo']"): 
    tds = tr.cssselect("td")

    print tds[0].text_content()

#    data = { 'address' : tds[0].text_content(), 'more data' : int(tds[4].text_content()) }
 #   print data



