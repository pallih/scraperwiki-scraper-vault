from string import ascii_lowercase
import urllib2
import re
import scraperwiki
import lxml.html           
import urlparse


def get_html(url):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2'
    headers = {
        'User-Agent': user_agent,
        'Accept': '*/*',
    }
    request = urllib2.Request(url, headers=headers)
    try:
        return urllib2.urlopen(request).read()
    except IOError, e:
        if hasattr(e, 'reason'):
            print "We failed to reach a server."
            print "Reason: ", e.reason
        elif hasattr(e, 'code'):
            print "The server couldn't fulfill the request."
            print "Error code: ", e.code
        return None

def morosos_list(root):
    rows = root.cssselect("tr")
    for row in rows:
        dato = row.cssselect(".TDtabla")
        if len(dato)==7:
            record = {}
            record['Pdo_pda'] = dato[0].text
            record['Cuit'] = dato[1].text
            record['Razon_social_Titular'] = dato[2].text
            record['Deuda_total'] = dato[3].text
            record['Localidad'] = dato[4].text
            record['Estado_de_la_deuda'] = dato[5].text
            record['Titulo_ejecutivo'] = dato[6].text
            scraperwiki.sqlite.save(unique_keys=['Pdo_pda'], data=record)


base_url = "http://www.arba.gov.ar"
for begin in range(1,329):
    starting_url = urlparse.urljoin(base_url, '/DeudoresCountries/DeudoresCountries.asp?imp=&pagina=%s' % begin)
    print starting_url
    html = get_html(starting_url)
    if html:
         root = lxml.html.fromstring(html) 
         morosos_list(root)
from string import ascii_lowercase
import urllib2
import re
import scraperwiki
import lxml.html           
import urlparse


def get_html(url):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2'
    headers = {
        'User-Agent': user_agent,
        'Accept': '*/*',
    }
    request = urllib2.Request(url, headers=headers)
    try:
        return urllib2.urlopen(request).read()
    except IOError, e:
        if hasattr(e, 'reason'):
            print "We failed to reach a server."
            print "Reason: ", e.reason
        elif hasattr(e, 'code'):
            print "The server couldn't fulfill the request."
            print "Error code: ", e.code
        return None

def morosos_list(root):
    rows = root.cssselect("tr")
    for row in rows:
        dato = row.cssselect(".TDtabla")
        if len(dato)==7:
            record = {}
            record['Pdo_pda'] = dato[0].text
            record['Cuit'] = dato[1].text
            record['Razon_social_Titular'] = dato[2].text
            record['Deuda_total'] = dato[3].text
            record['Localidad'] = dato[4].text
            record['Estado_de_la_deuda'] = dato[5].text
            record['Titulo_ejecutivo'] = dato[6].text
            scraperwiki.sqlite.save(unique_keys=['Pdo_pda'], data=record)


base_url = "http://www.arba.gov.ar"
for begin in range(1,329):
    starting_url = urlparse.urljoin(base_url, '/DeudoresCountries/DeudoresCountries.asp?imp=&pagina=%s' % begin)
    print starting_url
    html = get_html(starting_url)
    if html:
         root = lxml.html.fromstring(html) 
         morosos_list(root)
