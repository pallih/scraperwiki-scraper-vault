import StringIO
import scraperwiki
import urllib2
import string
import lxml.etree
import lxml.html
import lxml.cssselect
from bs4 import BeautifulSoup

try:
    scraperwiki.sqlite.execute("create table regions(name text, link text)")
    
except:
    print "Table probably already exists."