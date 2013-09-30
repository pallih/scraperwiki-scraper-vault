import scraperwiki
import httplib, ssl, urllib2, socket
import datetime
import calendar
from BeautifulSoup import BeautifulSoup


# custom HTTPS opener, supporting SSLv3.
# from: http://bugs.python.org/issue11220
class HTTPSConnectionV3(httplib.HTTPSConnection):
    def __init__(self, *args, **kwargs):
        httplib.HTTPSConnection.__init__(self, *args, **kwargs)
        
    def connect(self):
        sock = socket.create_connection((self.host, self.port), self.timeout)
        if self._tunnel_host:
            self.sock = sock
            self._tunnel()
        try:
            self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_SSLv3)
        except ssl.SSLError, e:
            print("Trying SSLv3.")
            self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_SSLv23)
            
class HTTPSHandlerV3(urllib2.HTTPSHandler):
    def https_open(self, req):
        return self.do_open(HTTPSConnectionV3, req)

urllib2.install_opener(urllib2.build_opener(HTTPSHandlerV3()))


# https://eservice.pssg.gov.bc.ca/LRA/reporting/public/newregistrations.do?method=get&registrationRole=all&startDate=01%2F01%2F2012&endDate=05%2F15%2F2012
# https://eservice.pssg.gov.bc.ca/LRA/reporting/public/newregistrations.do;jsessionid=75ceeb71f904ea2634f65b035b2232868cb1ed71d0e5a608b512f00177c61b69.e34PaxaNah0Pe34LchaRbNuSe0?method=get&registrationRole=all&startDate=01%2F01%2F2012&endDate=05%2F15%2F2012

theMonth = datetime.date.today().month
if theMonth < 10:
    theMonth = str("0"+str(theMonth ))
theDay = datetime.date.today().day
if theDay < 10:
    theDay = str("0"+str(theDay))


# page = urllib2.urlopen("https://eservice.pssg.gov.bc.ca/LRA/reporting/public/newregistrations.do;jsessionid=75ceeb71f904ea2634f65b035b2232868cb1ed71d0e5a608b512f00177c61b69.e34PaxaNah0Pe34LchaRbNuSe0?method=get&registrationRole=all&startDate=" + str(theMonth) + "%2F" + str(theDay) + "%2F" + str(datetime.date.today().year) + "&endDate=" + str(theMonth) + "%2F" + str(theDay) + "%2F" + str(datetime.date.today().year))

# print "https://eservice.pssg.gov.bc.ca/LRA/reporting/public/newregistrations.do?method=get&registrationRole=all&startDate=" + str(theMonth) + "%2F" + str(14) + "%2F" + str(datetime.date.today().year) + "&endDate=" + str(theMonth) + "%2F" + str(14) + "%2F" + str(datetime.date.today().year)

url = "https://eservice.pssg.gov.bc.ca/LRA/reporting/public/newregistrations.do;jsessionid=75ceeb71f904ea2634f65b035b2232868cb1ed71d0e5a608b512f00177c61b69.e34PaxaNah0Pe34LchaRbNuSe0?method=get&registrationRole=all&startDate=" + str(theMonth) + "%2F" + str(14) + "%2F" + str(datetime.date.today().year) + "&endDate=" + str(theMonth) + "%2F" + str(14) + "%2F" + str(datetime.date.today().year)
# trying the link Marc sent via email:
url = "https://eservice.pssg.gov.bc.ca/LRA/reporting/public/newregistrations.do?method=get&registrationRole=all&startDate=05%2F14%2F2012&endDate=05%2F14%2F2012"
print 'url = ', url

page = urllib2.urlopen(url)
print 'page = ', page.read()

soup = BeautifulSoup(page)
print 'soup = ', soup

resultsTable = soup.findAll("table", { "class" : "results" })
print 'resultsTable = ', resultsTable








import scraperwiki
import httplib, ssl, urllib2, socket
import datetime
import calendar
from BeautifulSoup import BeautifulSoup


# custom HTTPS opener, supporting SSLv3.
# from: http://bugs.python.org/issue11220
class HTTPSConnectionV3(httplib.HTTPSConnection):
    def __init__(self, *args, **kwargs):
        httplib.HTTPSConnection.__init__(self, *args, **kwargs)
        
    def connect(self):
        sock = socket.create_connection((self.host, self.port), self.timeout)
        if self._tunnel_host:
            self.sock = sock
            self._tunnel()
        try:
            self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_SSLv3)
        except ssl.SSLError, e:
            print("Trying SSLv3.")
            self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_SSLv23)
            
class HTTPSHandlerV3(urllib2.HTTPSHandler):
    def https_open(self, req):
        return self.do_open(HTTPSConnectionV3, req)

urllib2.install_opener(urllib2.build_opener(HTTPSHandlerV3()))


# https://eservice.pssg.gov.bc.ca/LRA/reporting/public/newregistrations.do?method=get&registrationRole=all&startDate=01%2F01%2F2012&endDate=05%2F15%2F2012
# https://eservice.pssg.gov.bc.ca/LRA/reporting/public/newregistrations.do;jsessionid=75ceeb71f904ea2634f65b035b2232868cb1ed71d0e5a608b512f00177c61b69.e34PaxaNah0Pe34LchaRbNuSe0?method=get&registrationRole=all&startDate=01%2F01%2F2012&endDate=05%2F15%2F2012

theMonth = datetime.date.today().month
if theMonth < 10:
    theMonth = str("0"+str(theMonth ))
theDay = datetime.date.today().day
if theDay < 10:
    theDay = str("0"+str(theDay))


# page = urllib2.urlopen("https://eservice.pssg.gov.bc.ca/LRA/reporting/public/newregistrations.do;jsessionid=75ceeb71f904ea2634f65b035b2232868cb1ed71d0e5a608b512f00177c61b69.e34PaxaNah0Pe34LchaRbNuSe0?method=get&registrationRole=all&startDate=" + str(theMonth) + "%2F" + str(theDay) + "%2F" + str(datetime.date.today().year) + "&endDate=" + str(theMonth) + "%2F" + str(theDay) + "%2F" + str(datetime.date.today().year))

# print "https://eservice.pssg.gov.bc.ca/LRA/reporting/public/newregistrations.do?method=get&registrationRole=all&startDate=" + str(theMonth) + "%2F" + str(14) + "%2F" + str(datetime.date.today().year) + "&endDate=" + str(theMonth) + "%2F" + str(14) + "%2F" + str(datetime.date.today().year)

url = "https://eservice.pssg.gov.bc.ca/LRA/reporting/public/newregistrations.do;jsessionid=75ceeb71f904ea2634f65b035b2232868cb1ed71d0e5a608b512f00177c61b69.e34PaxaNah0Pe34LchaRbNuSe0?method=get&registrationRole=all&startDate=" + str(theMonth) + "%2F" + str(14) + "%2F" + str(datetime.date.today().year) + "&endDate=" + str(theMonth) + "%2F" + str(14) + "%2F" + str(datetime.date.today().year)
# trying the link Marc sent via email:
url = "https://eservice.pssg.gov.bc.ca/LRA/reporting/public/newregistrations.do?method=get&registrationRole=all&startDate=05%2F14%2F2012&endDate=05%2F14%2F2012"
print 'url = ', url

page = urllib2.urlopen(url)
print 'page = ', page.read()

soup = BeautifulSoup(page)
print 'soup = ', soup

resultsTable = soup.findAll("table", { "class" : "results" })
print 'resultsTable = ', resultsTable








import scraperwiki
import httplib, ssl, urllib2, socket
import datetime
import calendar
from BeautifulSoup import BeautifulSoup


# custom HTTPS opener, supporting SSLv3.
# from: http://bugs.python.org/issue11220
class HTTPSConnectionV3(httplib.HTTPSConnection):
    def __init__(self, *args, **kwargs):
        httplib.HTTPSConnection.__init__(self, *args, **kwargs)
        
    def connect(self):
        sock = socket.create_connection((self.host, self.port), self.timeout)
        if self._tunnel_host:
            self.sock = sock
            self._tunnel()
        try:
            self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_SSLv3)
        except ssl.SSLError, e:
            print("Trying SSLv3.")
            self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_SSLv23)
            
class HTTPSHandlerV3(urllib2.HTTPSHandler):
    def https_open(self, req):
        return self.do_open(HTTPSConnectionV3, req)

urllib2.install_opener(urllib2.build_opener(HTTPSHandlerV3()))


# https://eservice.pssg.gov.bc.ca/LRA/reporting/public/newregistrations.do?method=get&registrationRole=all&startDate=01%2F01%2F2012&endDate=05%2F15%2F2012
# https://eservice.pssg.gov.bc.ca/LRA/reporting/public/newregistrations.do;jsessionid=75ceeb71f904ea2634f65b035b2232868cb1ed71d0e5a608b512f00177c61b69.e34PaxaNah0Pe34LchaRbNuSe0?method=get&registrationRole=all&startDate=01%2F01%2F2012&endDate=05%2F15%2F2012

theMonth = datetime.date.today().month
if theMonth < 10:
    theMonth = str("0"+str(theMonth ))
theDay = datetime.date.today().day
if theDay < 10:
    theDay = str("0"+str(theDay))


# page = urllib2.urlopen("https://eservice.pssg.gov.bc.ca/LRA/reporting/public/newregistrations.do;jsessionid=75ceeb71f904ea2634f65b035b2232868cb1ed71d0e5a608b512f00177c61b69.e34PaxaNah0Pe34LchaRbNuSe0?method=get&registrationRole=all&startDate=" + str(theMonth) + "%2F" + str(theDay) + "%2F" + str(datetime.date.today().year) + "&endDate=" + str(theMonth) + "%2F" + str(theDay) + "%2F" + str(datetime.date.today().year))

# print "https://eservice.pssg.gov.bc.ca/LRA/reporting/public/newregistrations.do?method=get&registrationRole=all&startDate=" + str(theMonth) + "%2F" + str(14) + "%2F" + str(datetime.date.today().year) + "&endDate=" + str(theMonth) + "%2F" + str(14) + "%2F" + str(datetime.date.today().year)

url = "https://eservice.pssg.gov.bc.ca/LRA/reporting/public/newregistrations.do;jsessionid=75ceeb71f904ea2634f65b035b2232868cb1ed71d0e5a608b512f00177c61b69.e34PaxaNah0Pe34LchaRbNuSe0?method=get&registrationRole=all&startDate=" + str(theMonth) + "%2F" + str(14) + "%2F" + str(datetime.date.today().year) + "&endDate=" + str(theMonth) + "%2F" + str(14) + "%2F" + str(datetime.date.today().year)
# trying the link Marc sent via email:
url = "https://eservice.pssg.gov.bc.ca/LRA/reporting/public/newregistrations.do?method=get&registrationRole=all&startDate=05%2F14%2F2012&endDate=05%2F14%2F2012"
print 'url = ', url

page = urllib2.urlopen(url)
print 'page = ', page.read()

soup = BeautifulSoup(page)
print 'soup = ', soup

resultsTable = soup.findAll("table", { "class" : "results" })
print 'resultsTable = ', resultsTable








import scraperwiki
import httplib, ssl, urllib2, socket
import datetime
import calendar
from BeautifulSoup import BeautifulSoup


# custom HTTPS opener, supporting SSLv3.
# from: http://bugs.python.org/issue11220
class HTTPSConnectionV3(httplib.HTTPSConnection):
    def __init__(self, *args, **kwargs):
        httplib.HTTPSConnection.__init__(self, *args, **kwargs)
        
    def connect(self):
        sock = socket.create_connection((self.host, self.port), self.timeout)
        if self._tunnel_host:
            self.sock = sock
            self._tunnel()
        try:
            self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_SSLv3)
        except ssl.SSLError, e:
            print("Trying SSLv3.")
            self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_SSLv23)
            
class HTTPSHandlerV3(urllib2.HTTPSHandler):
    def https_open(self, req):
        return self.do_open(HTTPSConnectionV3, req)

urllib2.install_opener(urllib2.build_opener(HTTPSHandlerV3()))


# https://eservice.pssg.gov.bc.ca/LRA/reporting/public/newregistrations.do?method=get&registrationRole=all&startDate=01%2F01%2F2012&endDate=05%2F15%2F2012
# https://eservice.pssg.gov.bc.ca/LRA/reporting/public/newregistrations.do;jsessionid=75ceeb71f904ea2634f65b035b2232868cb1ed71d0e5a608b512f00177c61b69.e34PaxaNah0Pe34LchaRbNuSe0?method=get&registrationRole=all&startDate=01%2F01%2F2012&endDate=05%2F15%2F2012

theMonth = datetime.date.today().month
if theMonth < 10:
    theMonth = str("0"+str(theMonth ))
theDay = datetime.date.today().day
if theDay < 10:
    theDay = str("0"+str(theDay))


# page = urllib2.urlopen("https://eservice.pssg.gov.bc.ca/LRA/reporting/public/newregistrations.do;jsessionid=75ceeb71f904ea2634f65b035b2232868cb1ed71d0e5a608b512f00177c61b69.e34PaxaNah0Pe34LchaRbNuSe0?method=get&registrationRole=all&startDate=" + str(theMonth) + "%2F" + str(theDay) + "%2F" + str(datetime.date.today().year) + "&endDate=" + str(theMonth) + "%2F" + str(theDay) + "%2F" + str(datetime.date.today().year))

# print "https://eservice.pssg.gov.bc.ca/LRA/reporting/public/newregistrations.do?method=get&registrationRole=all&startDate=" + str(theMonth) + "%2F" + str(14) + "%2F" + str(datetime.date.today().year) + "&endDate=" + str(theMonth) + "%2F" + str(14) + "%2F" + str(datetime.date.today().year)

url = "https://eservice.pssg.gov.bc.ca/LRA/reporting/public/newregistrations.do;jsessionid=75ceeb71f904ea2634f65b035b2232868cb1ed71d0e5a608b512f00177c61b69.e34PaxaNah0Pe34LchaRbNuSe0?method=get&registrationRole=all&startDate=" + str(theMonth) + "%2F" + str(14) + "%2F" + str(datetime.date.today().year) + "&endDate=" + str(theMonth) + "%2F" + str(14) + "%2F" + str(datetime.date.today().year)
# trying the link Marc sent via email:
url = "https://eservice.pssg.gov.bc.ca/LRA/reporting/public/newregistrations.do?method=get&registrationRole=all&startDate=05%2F14%2F2012&endDate=05%2F14%2F2012"
print 'url = ', url

page = urllib2.urlopen(url)
print 'page = ', page.read()

soup = BeautifulSoup(page)
print 'soup = ', soup

resultsTable = soup.findAll("table", { "class" : "results" })
print 'resultsTable = ', resultsTable








