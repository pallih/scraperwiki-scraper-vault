import scraperwiki
from lxml.html import parse, fromstring
import urllib, datetime, hashlib

base_url = "http://www.camara.sp.gov.br/"

def getPauta(url, title):
    soap = parse(urllib.urlopen(base_url + url)).getroot()
    print_url = soap.cssselect(".contentpaneopen a[title='Imprimir']")[0].get('href')
    print_html = urllib.urlopen(base_url + print_url).read()
    print_soap = fromstring(print_html)
    data = { "raw_html" : print_html,
             "raw_text" : print_soap.text_content(),
             "url" : base_url + url,
             "title" : title.strip(),
             "timestamp" : datetime.datetime.now(),
             "id" : hashlib.md5(print_soap.text_content().encode("iso-8859-1")).hexdigest()
            }
    scraperwiki.sqlite.save(["id"], data)
    

# Rock and roll!
url = "/index.php?option=com_content&view=category&id=19&Itemid=35"
soap = parse(urllib.urlopen(base_url + url)).getroot()

links = soap.cssselect(".sectiontableentry2 a")
for link in links:
    getPauta(link.get('href'), link.text)

