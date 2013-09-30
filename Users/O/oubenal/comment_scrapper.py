import scraperwiki
import urllib2 
from unidecode import unidecode
from lxml.html import fromstring

# Blank Python


def scrape_table(url):
    download = urllib2.urlopen(url)
    raw = download.read()
    print unidecode(raw) #.encode('ISO-8859-1') #decode('utf-8')
    html = fromstring(raw)
    comments = html.cssselect("ol.commentlist li")
    
    print [c.text_content().strip().replace('\t', '') for c in comments][0]

scrape_table("http://www.demainonline.com/2012/06/21/pov-con-est-aussi-un-chaud-lapin/")import scraperwiki
import urllib2 
from unidecode import unidecode
from lxml.html import fromstring

# Blank Python


def scrape_table(url):
    download = urllib2.urlopen(url)
    raw = download.read()
    print unidecode(raw) #.encode('ISO-8859-1') #decode('utf-8')
    html = fromstring(raw)
    comments = html.cssselect("ol.commentlist li")
    
    print [c.text_content().strip().replace('\t', '') for c in comments][0]

scrape_table("http://www.demainonline.com/2012/06/21/pov-con-est-aussi-un-chaud-lapin/")