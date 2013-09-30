import scraperwiki
import lxml.html
import urlparse
params={'q_CityLOV':'OAKLAND',
        'q_LTLOV':'01',
        'RPTYPE':'p_OffSale',
        'SUBMIT1':'Continue'}
url = 'http://www.abc.ca.gov/datport/AHCityRep.asp'

html = scraperwiki.scrape(url,params)
root = lxml.html.fromstring(html)

for tr in root.cssselect("table[class='wikitable'] tr"):
    tds = tr.cssselect("td")
    if len(tds)>1:
        data = {'ID' : tds[0].text_content(),'License Number' : tds[1].text_content(),'Status' : tds[2].text_content(),'License Type' : tds[3],'Original Issue Date' : tds[4],'Expiration Date' : tds[5],'Primary Owner and Address' : tds[6],'Business Name' : tds[7],'Mailing Address' : tds[8],'Geo Code' : tds[9]}
        print data
        #scraperwiki.sqlite.save(unique_keys=['Name'], data=data)
import scraperwiki
import lxml.html
import urlparse
params={'q_CityLOV':'OAKLAND',
        'q_LTLOV':'01',
        'RPTYPE':'p_OffSale',
        'SUBMIT1':'Continue'}
url = 'http://www.abc.ca.gov/datport/AHCityRep.asp'

html = scraperwiki.scrape(url,params)
root = lxml.html.fromstring(html)

for tr in root.cssselect("table[class='wikitable'] tr"):
    tds = tr.cssselect("td")
    if len(tds)>1:
        data = {'ID' : tds[0].text_content(),'License Number' : tds[1].text_content(),'Status' : tds[2].text_content(),'License Type' : tds[3],'Original Issue Date' : tds[4],'Expiration Date' : tds[5],'Primary Owner and Address' : tds[6],'Business Name' : tds[7],'Mailing Address' : tds[8],'Geo Code' : tds[9]}
        print data
        #scraperwiki.sqlite.save(unique_keys=['Name'], data=data)
