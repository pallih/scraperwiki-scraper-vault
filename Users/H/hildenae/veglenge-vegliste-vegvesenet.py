#Scraperwiki som hentar veglengder frå veglistene til vegvesenet
#Av Gnonthgol

import scraperwiki
import urllib2
import lxml.etree
import re
utils=scraperwiki.swimport('hildenae_utils') # for caching + pretty-print

res = {}

#Henta frå http://www.vegvesen.no/Kjoretoy/Yrkestransport/Veglister+og+dispensasjoner/Veglister+2012
url = "http://www.vegvesen.no/_attachment/314828/binary/553942"

xmldata = utils.findInCache(url)
if xmldata is None:
    pdfdata = urllib2.urlopen(url).read()
    xmldata = scraperwiki.pdftoxml(pdfdata)
    utils.putInCache(url, xmldata)

root = lxml.etree.fromstring(xmldata)
pages = list(root)

for page in pages:
    ref = None
    for el in list(page):
        if el.tag == "text" and el.text:
            if el.text.find('FV ') == 0 or el.text.find('KV ') == 0:
                ref = el.text.strip(" *")
            if ref and re.match("(\d*,\d{3})", el.text):
                if not res.has_key(ref):
                    res[ref] = 0
                val = float(re.match("(\d*,\d{3})", el.text).groups()[0].replace(",", "."))
                res[ref] = res[ref] + val
                ref = None

for ref in res:
    print ref, res[ref]
