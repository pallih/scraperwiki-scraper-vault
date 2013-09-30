import scraperwiki

# Blank Python

#scraperwiki.sqlite.save(data={'value':"raw £ sign"}, unique_keys=['value'])
#scraperwiki.sqlite.save(data={'value':u"uni aq sign fix? \u1234\u00e1\u00a3 $£$"}, unique_keys=['value'])

#print repr(u'£')#
#
#print repr('£')

import requests
import re
import lxml.html
url = 'http://www2.comune.rovereto.tn.it/iride/extra/determina_dettaglio/529749'
h = requests.get(url)
v= re.findall("DIRIGENTE ATTIVIT.{0,10} SOCIALI", h.text)
print '1', repr(v),v[0]
hh = scraperwiki.scrape(url)
v= re.findall("DIRIGENTE ATTIVIT.{0,10} SOCIALI", hh)
print '2', repr(v),v[0]



r = lxml.html.fromstring(h.text)
v= r.xpath('//*[contains(text(), "DIRIGENTE")]/text()')[0]
print repr(v)
scraperwiki.sqlite.save(data={'value':0, 'payload':v}, unique_keys=['value'])import scraperwiki

# Blank Python

#scraperwiki.sqlite.save(data={'value':"raw £ sign"}, unique_keys=['value'])
#scraperwiki.sqlite.save(data={'value':u"uni aq sign fix? \u1234\u00e1\u00a3 $£$"}, unique_keys=['value'])

#print repr(u'£')#
#
#print repr('£')

import requests
import re
import lxml.html
url = 'http://www2.comune.rovereto.tn.it/iride/extra/determina_dettaglio/529749'
h = requests.get(url)
v= re.findall("DIRIGENTE ATTIVIT.{0,10} SOCIALI", h.text)
print '1', repr(v),v[0]
hh = scraperwiki.scrape(url)
v= re.findall("DIRIGENTE ATTIVIT.{0,10} SOCIALI", hh)
print '2', repr(v),v[0]



r = lxml.html.fromstring(h.text)
v= r.xpath('//*[contains(text(), "DIRIGENTE")]/text()')[0]
print repr(v)
scraperwiki.sqlite.save(data={'value':0, 'payload':v}, unique_keys=['value'])