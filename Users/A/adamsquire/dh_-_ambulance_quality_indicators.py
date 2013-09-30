import scraperwiki
import lxml.html
import datetime
from time import strptime

html = scraperwiki.scrape("http://transparency.dh.gov.uk/2012/06/19/ambqidownloads/") 

root = lxml.html.fromstring(html) 
data = []

for el in root.cssselect('div.entry-content a'):
    if 'xls' in el.attrib['href']:
        d = el.text
        dc = d.replace('Download ','')
        domain_value = dc[0:dc.find('2')-1]
        financial_year = dc[len(domain_value):len(domain_value)+8]
        month_value = dc[len(domain_value)+8:dc.find('(')-1]
        data.append({'link': el.attrib['href'],'description': d, 'timestamp': datetime.datetime.now(),'month_value':month_value.strip(),'financial_year':financial_year.strip(),'domain':domain_value.strip(),'month_number':strptime(month_value.strip(), '%B').tm_mon})

for link in data:
     scraperwiki.sqlite.save(unique_keys=['link'], data=link)
import scraperwiki
import lxml.html
import datetime
from time import strptime

html = scraperwiki.scrape("http://transparency.dh.gov.uk/2012/06/19/ambqidownloads/") 

root = lxml.html.fromstring(html) 
data = []

for el in root.cssselect('div.entry-content a'):
    if 'xls' in el.attrib['href']:
        d = el.text
        dc = d.replace('Download ','')
        domain_value = dc[0:dc.find('2')-1]
        financial_year = dc[len(domain_value):len(domain_value)+8]
        month_value = dc[len(domain_value)+8:dc.find('(')-1]
        data.append({'link': el.attrib['href'],'description': d, 'timestamp': datetime.datetime.now(),'month_value':month_value.strip(),'financial_year':financial_year.strip(),'domain':domain_value.strip(),'month_number':strptime(month_value.strip(), '%B').tm_mon})

for link in data:
     scraperwiki.sqlite.save(unique_keys=['link'], data=link)
