import urllib2
import httplib
import socket
import lxml.html
import scraperwiki
import time


def MyResolver(host):
    if host == 'clinicaltrials.gov':
        return '130.14.81.50' # Google IP
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

scraperwiki.sqlite.attach('clinical_trials_links','links')

def parse_trial(code, page):
    trial = {}
    print '+Parsing trial'
    d = { 'code': code }
    for table in page.cssselect('table.data_table'):
        for row in table.cssselect('tr')[1:]:
            label = row[0].text_content().replace(' ICMJE ', '')
            if label.startswith('Contact'):
                continue
            if not label or label.startswith('Data element required by the International Committee of') or len(row) == 1:
                continue
            value = lxml.html.tostring(row[1])
            if value.startswith('<td class="missing_color">'):
                value = ""
            else:
                value = value.replace('<td class="body3" valign="top">', "")
                value = value.replace('</td>', "")
                value = value.replace('&#13;', '')
            label = label.replace(' * ', '')
            label = label.replace(':', '')
            if '(' in label: 
                continue
            d[label.encode('ascii', 'ignore')] = value
    scraperwiki.sqlite.save( ['code'], d, table_name='trials', verbose=0)
                

last = scraperwiki.sqlite.get_var('last', '');
results = scraperwiki.sqlite.select('code,link from links.search_page_links where code > "' + last + '" order by code  limit 2000')
for d in results:
    code = d['code']
    link = d['link']
    html = scrape(link)
    parse_trial( code, lxml.html.fromstring( html ) )   
    scraperwiki.sqlite.save_var('last', code);
    time.sleep(1)
import urllib2
import httplib
import socket
import lxml.html
import scraperwiki
import time


def MyResolver(host):
    if host == 'clinicaltrials.gov':
        return '130.14.81.50' # Google IP
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

scraperwiki.sqlite.attach('clinical_trials_links','links')

def parse_trial(code, page):
    trial = {}
    print '+Parsing trial'
    d = { 'code': code }
    for table in page.cssselect('table.data_table'):
        for row in table.cssselect('tr')[1:]:
            label = row[0].text_content().replace(' ICMJE ', '')
            if label.startswith('Contact'):
                continue
            if not label or label.startswith('Data element required by the International Committee of') or len(row) == 1:
                continue
            value = lxml.html.tostring(row[1])
            if value.startswith('<td class="missing_color">'):
                value = ""
            else:
                value = value.replace('<td class="body3" valign="top">', "")
                value = value.replace('</td>', "")
                value = value.replace('&#13;', '')
            label = label.replace(' * ', '')
            label = label.replace(':', '')
            if '(' in label: 
                continue
            d[label.encode('ascii', 'ignore')] = value
    scraperwiki.sqlite.save( ['code'], d, table_name='trials', verbose=0)
                

last = scraperwiki.sqlite.get_var('last', '');
results = scraperwiki.sqlite.select('code,link from links.search_page_links where code > "' + last + '" order by code  limit 2000')
for d in results:
    code = d['code']
    link = d['link']
    html = scrape(link)
    parse_trial( code, lxml.html.fromstring( html ) )   
    scraperwiki.sqlite.save_var('last', code);
    time.sleep(1)
