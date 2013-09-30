import mechanize 
import urllib2
import scraperwiki
import lxml.html
import string
import re

from htmlentitydefs import name2codepoint
def htmlentitydecode(s):
    return re.sub('&(%s);' % '|'.join(name2codepoint), 
            lambda m: unichr(name2codepoint[m.group(1)]), s)

EtbUrl = "http://www.lefigaro.fr/resultats-bac/academie-poitiers/deux-sevres/0790080h-bressuire-lycee-saint-joseph/"

pagestart = 0
pagestep = 100
page = 0
pagemax = 999999

br = mechanize.Browser()
s = br.open(EtbUrl)

html = lxml.html.fromstring(s.read())
EtbTableArea = html.cssselect('table.exa12-diplst')[0] 

i = 0
uniquekey = 0

for tr in EtbTableArea.cssselect("tr"):
    i = i + 1
    if i > 1 :
        tds = tr.cssselect("td")
        if len(tds) > 1 :
            uniquekey = uniquekey + 1
            print str(uniquekey) + lxml.html.tostring(tds[0])import mechanize 
import urllib2
import scraperwiki
import lxml.html
import string
import re

from htmlentitydefs import name2codepoint
def htmlentitydecode(s):
    return re.sub('&(%s);' % '|'.join(name2codepoint), 
            lambda m: unichr(name2codepoint[m.group(1)]), s)

EtbUrl = "http://www.lefigaro.fr/resultats-bac/academie-poitiers/deux-sevres/0790080h-bressuire-lycee-saint-joseph/"

pagestart = 0
pagestep = 100
page = 0
pagemax = 999999

br = mechanize.Browser()
s = br.open(EtbUrl)

html = lxml.html.fromstring(s.read())
EtbTableArea = html.cssselect('table.exa12-diplst')[0] 

i = 0
uniquekey = 0

for tr in EtbTableArea.cssselect("tr"):
    i = i + 1
    if i > 1 :
        tds = tr.cssselect("td")
        if len(tds) > 1 :
            uniquekey = uniquekey + 1
            print str(uniquekey) + lxml.html.tostring(tds[0])