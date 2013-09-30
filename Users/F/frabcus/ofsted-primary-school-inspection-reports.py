import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re

for i in range(10):
    print "hello", i*i

def get_one_page(offset):
    url = 'http://www.ofsted.gov.uk/oxfind/name/(%s)/0/(type)/4096/(length)/10' % (offset,)
    root = lxml.html.parse(url).getroot()

    # place your cssselection case here and extract the values
    for tr in root.cssselect('div#contentHome table.list tr'):
        rec = {} 
        rec['school_type'] = tr[1].text

        
        print list(tr), lxml.etree.tostring(tr)
        
get_one_page(0)
import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re

for i in range(10):
    print "hello", i*i

def get_one_page(offset):
    url = 'http://www.ofsted.gov.uk/oxfind/name/(%s)/0/(type)/4096/(length)/10' % (offset,)
    root = lxml.html.parse(url).getroot()

    # place your cssselection case here and extract the values
    for tr in root.cssselect('div#contentHome table.list tr'):
        rec = {} 
        rec['school_type'] = tr[1].text

        
        print list(tr), lxml.etree.tostring(tr)
        
get_one_page(0)
