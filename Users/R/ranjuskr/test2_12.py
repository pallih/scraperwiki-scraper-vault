import scraperwiki
from lxml.html import parse, open_in_browser
import time
#import string

doc = parse('http://www.hotairac.com/Products.html').getroot()
doc.make_links_absolute()
for a in doc.cssselect('tr a'):
    print 'found "%s" link to href "%s"' % (a.text, a.get('href'))
    Section = ""
    #add a time stamp
    t=time.time()
    #write data in table androidmkt
    data = {
               'timestamp': t,
               'Section': Section,
               'Txt': a.text,               
               'urlid': a.get('href')
            }

    scraperwiki.sqlite.save(unique_keys=["timestamp"], data=data, table_name="Productshtml")

import scraperwiki
from lxml.html import parse, open_in_browser
import time
#import string

doc = parse('http://www.hotairac.com/Products.html').getroot()
doc.make_links_absolute()
for a in doc.cssselect('tr a'):
    print 'found "%s" link to href "%s"' % (a.text, a.get('href'))
    Section = ""
    #add a time stamp
    t=time.time()
    #write data in table androidmkt
    data = {
               'timestamp': t,
               'Section': Section,
               'Txt': a.text,               
               'urlid': a.get('href')
            }

    scraperwiki.sqlite.save(unique_keys=["timestamp"], data=data, table_name="Productshtml")

