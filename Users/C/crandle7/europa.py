import scraperwiki
import urllib, urlparse, urllib2
import lxml.html
from lxml import etree
import re
import httplib
import socket

scraperwiki.sqlite.save(['URL', "Country"], {"URL":"http://localhost", "Country":"UK"})

########################################
# HTML Fetch Functions
########################################

def MyResolver(host):
    if host == 'ec.europa.eu':
        return '147.67.136.3'
    else:
        return host

class MyHTTPConnection(httplib.HTTPConnection):
    def connect(self):
        self.sock = socket.create_connection((MyResolver(self.host),self.port),self.timeout)

class MyHTTPSConnection(httplib.HTTPSConnection):
    def connect(self):
        sock = socket.create_connection((MyResolver(self.host), self.port), self.timeout)
        self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file)

class MyHTTPHandler(urllib2.HTTPHandler):
    def http_open(self,req):
        return self.do_open(MyHTTPConnection,req)

class MyHTTPSHandler(urllib2.HTTPSHandler):
    def https_open(self,req):
        return self.do_open(MyHTTPSConnection,req)

def scrape(url):
    opener = urllib2.build_opener(MyHTTPHandler,MyHTTPSHandler)
    urllib2.install_opener(opener)

    f = urllib2.urlopen(url)
    data = f.read()
    f.fp._sock.recv = None
    f.close()
    return data


########################################
# Debug / Logging
########################################

def url_count(url):
    c = 0
    try:
        results = scraperwiki.sqlite.select('count(*) as c from swdata where URL="%s"' % url )
        print results
    except Exception:
        raise
    return c


########################################
# Scraping Logic
########################################

def scrapeVacancies(root):
    vacancies = 0
    tables = root.cssselect('table.JResult')
    if tables:
        for table in tables:
            # For each table on the page, get the link from inside it
            links = table.cssselect('a')
            for link in links:
                popupurl = link.attrib.get('onclick')
                if popupurl:
                    vacancies += 1
                    popupurl = urlparse.urljoin("http://ec.europa.eu/eures/eures-searchengine/servlet/", popupurl.split("'")[1])
                    data = {"Country": countryCode, "URL": popupurl}
                    if url_count( popupurl ) > 0:
                        print "vacancies - Duplicate URL *somehow*", popupurl
                    scraperwiki.sqlite.save(["URL", "Country"], data)
                else:
                    print "Failed link: ", etree.tostring(link)
    return vacancies

def scrapeSubsequentPage( countryCode, nextUrl, page ):
    url = url = nextUrl[:-1] + "%d" % page
    print url
    try:
        html = scrape(url)
        root = lxml.html.fromstring(html)
        return scrapeVacancies(root)
    except Exception as e:
        print "Exception: ", e
        print "Possibly lost links on: ", url
        return -1


firstPage = "http://ec.europa.eu/eures/eures-searchengine/servlet/BrowseCountryJVsServlet?lg=EN&isco=%%25&date=01%%2F01%%2F1975&title=&durex=&exp=&serviceUri=browse&qual=&pageSize=99&page=1&country=%s&totalCount=1&multipleRegions=%%25"

def scrapeFirstPage(countryCode):
    url = firstPage % countryCode
    
    nextUrl = url
    pages = 0
    vacancies = 0
    
    try:
        html = scrape(url)
        root = lxml.html.fromstring(html)

        for url in root.cssselect('div.prevNext'):
            relativeNextUrl = url.cssselect('a')[0].attrib.get('href')

        nextUrl = urlparse.urljoin("http://ec.europa.eu/eures/eures-searchengine/servlet/", relativeNextUrl)
        print nextUrl

        # Find claimed number of vacancies and calculate pages
        vacancies = root.cssselect('p.vTall')
        if vacancies:
            num = vacancies[0].text_content()
            numVacancies = int(num[1:-21])
            pages = (numVacancies / 99) + 1

        vacancies = scrapeVacancies(root)
    except Exception as e:
        print "Exception: ", e
        print "Possibly lost links on: ", url

    return {'nextUrl': nextUrl, 'pages': pages, 'vacancies': vacancies }

#All country codes
#["NO", "DE", "MT", "DK", "AT", "FR" ,SE", "LU", "BE", "BG", "CZ", "EE", "GR", "IS", "LV", "LI", "LT", "PL", "SI", "ES", "CH", "FI", "RO", "SK", "UK", "CY", "NL", "HU", "PT", "IR", "IT" ]

countryCodes = [ "FR" ]


for countryCode in countryCodes: 
    scrapeData = scrapeFirstPage(countryCode)
    nextUrl = scrapeData['nextUrl']
    pages = scrapeData['pages']

    for page in range(2, pages + 1):
        vacancies = scrapeSubsequentPage(countryCode, nextUrl, page)
        if vacancies == 0:
            break
import scraperwiki
import urllib, urlparse, urllib2
import lxml.html
from lxml import etree
import re
import httplib
import socket

scraperwiki.sqlite.save(['URL', "Country"], {"URL":"http://localhost", "Country":"UK"})

########################################
# HTML Fetch Functions
########################################

def MyResolver(host):
    if host == 'ec.europa.eu':
        return '147.67.136.3'
    else:
        return host

class MyHTTPConnection(httplib.HTTPConnection):
    def connect(self):
        self.sock = socket.create_connection((MyResolver(self.host),self.port),self.timeout)

class MyHTTPSConnection(httplib.HTTPSConnection):
    def connect(self):
        sock = socket.create_connection((MyResolver(self.host), self.port), self.timeout)
        self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file)

class MyHTTPHandler(urllib2.HTTPHandler):
    def http_open(self,req):
        return self.do_open(MyHTTPConnection,req)

class MyHTTPSHandler(urllib2.HTTPSHandler):
    def https_open(self,req):
        return self.do_open(MyHTTPSConnection,req)

def scrape(url):
    opener = urllib2.build_opener(MyHTTPHandler,MyHTTPSHandler)
    urllib2.install_opener(opener)

    f = urllib2.urlopen(url)
    data = f.read()
    f.fp._sock.recv = None
    f.close()
    return data


########################################
# Debug / Logging
########################################

def url_count(url):
    c = 0
    try:
        results = scraperwiki.sqlite.select('count(*) as c from swdata where URL="%s"' % url )
        print results
    except Exception:
        raise
    return c


########################################
# Scraping Logic
########################################

def scrapeVacancies(root):
    vacancies = 0
    tables = root.cssselect('table.JResult')
    if tables:
        for table in tables:
            # For each table on the page, get the link from inside it
            links = table.cssselect('a')
            for link in links:
                popupurl = link.attrib.get('onclick')
                if popupurl:
                    vacancies += 1
                    popupurl = urlparse.urljoin("http://ec.europa.eu/eures/eures-searchengine/servlet/", popupurl.split("'")[1])
                    data = {"Country": countryCode, "URL": popupurl}
                    if url_count( popupurl ) > 0:
                        print "vacancies - Duplicate URL *somehow*", popupurl
                    scraperwiki.sqlite.save(["URL", "Country"], data)
                else:
                    print "Failed link: ", etree.tostring(link)
    return vacancies

def scrapeSubsequentPage( countryCode, nextUrl, page ):
    url = url = nextUrl[:-1] + "%d" % page
    print url
    try:
        html = scrape(url)
        root = lxml.html.fromstring(html)
        return scrapeVacancies(root)
    except Exception as e:
        print "Exception: ", e
        print "Possibly lost links on: ", url
        return -1


firstPage = "http://ec.europa.eu/eures/eures-searchengine/servlet/BrowseCountryJVsServlet?lg=EN&isco=%%25&date=01%%2F01%%2F1975&title=&durex=&exp=&serviceUri=browse&qual=&pageSize=99&page=1&country=%s&totalCount=1&multipleRegions=%%25"

def scrapeFirstPage(countryCode):
    url = firstPage % countryCode
    
    nextUrl = url
    pages = 0
    vacancies = 0
    
    try:
        html = scrape(url)
        root = lxml.html.fromstring(html)

        for url in root.cssselect('div.prevNext'):
            relativeNextUrl = url.cssselect('a')[0].attrib.get('href')

        nextUrl = urlparse.urljoin("http://ec.europa.eu/eures/eures-searchengine/servlet/", relativeNextUrl)
        print nextUrl

        # Find claimed number of vacancies and calculate pages
        vacancies = root.cssselect('p.vTall')
        if vacancies:
            num = vacancies[0].text_content()
            numVacancies = int(num[1:-21])
            pages = (numVacancies / 99) + 1

        vacancies = scrapeVacancies(root)
    except Exception as e:
        print "Exception: ", e
        print "Possibly lost links on: ", url

    return {'nextUrl': nextUrl, 'pages': pages, 'vacancies': vacancies }

#All country codes
#["NO", "DE", "MT", "DK", "AT", "FR" ,SE", "LU", "BE", "BG", "CZ", "EE", "GR", "IS", "LV", "LI", "LT", "PL", "SI", "ES", "CH", "FI", "RO", "SK", "UK", "CY", "NL", "HU", "PT", "IR", "IT" ]

countryCodes = [ "FR" ]


for countryCode in countryCodes: 
    scrapeData = scrapeFirstPage(countryCode)
    nextUrl = scrapeData['nextUrl']
    pages = scrapeData['pages']

    for page in range(2, pages + 1):
        vacancies = scrapeSubsequentPage(countryCode, nextUrl, page)
        if vacancies == 0:
            break
