import scraperwiki
import lxml.html
import urllib2
import datetime
import json
import string
import random
from BeautifulSoup import BeautifulSoup
import random

base_url = "http://www.allhscodes.com/"
html = scraperwiki.scrape(base_url)
root = lxml.html.fromstring(html)
for count,tr in enumerate(root.cssselect('tr')):
    row = [td.text_content() for td in tr.cssselect('td')]
    if len(row) == 2:
        code = row[0]
        desc = row[1].upper()
        now = datetime.datetime.now()
        data2 = {"tmsp_scraped":str(now), "hs_code":code, "hs_code_description":desc}
        scraperwiki.sqlite.save(unique_keys=["hs_code"], data=data2, table_name = "s_hscode")
        print "Finished "+code+", "+desc
import scraperwiki
import lxml.html
import urllib2
import datetime
import json
import string
import random
from BeautifulSoup import BeautifulSoup
import random

base_url = "http://www.allhscodes.com/"
html = scraperwiki.scrape(base_url)
root = lxml.html.fromstring(html)
for count,tr in enumerate(root.cssselect('tr')):
    row = [td.text_content() for td in tr.cssselect('td')]
    if len(row) == 2:
        code = row[0]
        desc = row[1].upper()
        now = datetime.datetime.now()
        data2 = {"tmsp_scraped":str(now), "hs_code":code, "hs_code_description":desc}
        scraperwiki.sqlite.save(unique_keys=["hs_code"], data=data2, table_name = "s_hscode")
        print "Finished "+code+", "+desc
