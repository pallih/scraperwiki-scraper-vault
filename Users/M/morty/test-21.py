import scraperwiki
print "Testing"

scraperwiki.sqlite.save(['name'], {'name': 'Tom'})
scraperwiki.sqlite.save(['name'], {'name': 'Dick'})
scraperwiki.sqlite.save(['name'], {'name': 'Harry'})
scraperwiki.sqlite.save(['name'], {'name': u'12\u304234\u3042'})

import urllib, urllib2

proxy = urllib2.ProxyHandler({'http': 'http://178.18.115.73/'})
opener = urllib2.build_opener(proxy)
urllib2.install_opener(opener)
print urllib2.urlopen('http://rsk.is/fyrirtaekjaskra/thjonusta/nyskra/').read()
import scraperwiki
print "Testing"

scraperwiki.sqlite.save(['name'], {'name': 'Tom'})
scraperwiki.sqlite.save(['name'], {'name': 'Dick'})
scraperwiki.sqlite.save(['name'], {'name': 'Harry'})
scraperwiki.sqlite.save(['name'], {'name': u'12\u304234\u3042'})

import urllib, urllib2

proxy = urllib2.ProxyHandler({'http': 'http://178.18.115.73/'})
opener = urllib2.build_opener(proxy)
urllib2.install_opener(opener)
print urllib2.urlopen('http://rsk.is/fyrirtaekjaskra/thjonusta/nyskra/').read()
