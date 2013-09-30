import time
from twisted.web.client import getPage
from twisted.internet import reactor
import scraperwiki

print "beginning"


urls = 8 * ['http://www.google.com', "http://yahoo.com", "http://aol.com", "http://microsoft.com", "http://amazon.com"]
count = len(urls)

#################
# Testing non-blocking, async twisted page fetch
#################
def print_and_stop(output):
    #print output
    global count
    print "downloaded"
    print count
    count -= 1
    if not count and reactor.running :
        reactor.stop()

t = time.time()
for url in urls:
    print 'fetching', url
    d = getPage(url)
    d.addCallback(print_and_stop)
#    if not reactor.running:

reactor.run()
print time.time() - t

#################
# Testing blocking, single threaded scraperwiki page fetch
#################
t = time.time()
for url in urls:
    continue
    scraperwiki.scrape(url)
print time.time() - timport time
from twisted.web.client import getPage
from twisted.internet import reactor
import scraperwiki

print "beginning"


urls = 8 * ['http://www.google.com', "http://yahoo.com", "http://aol.com", "http://microsoft.com", "http://amazon.com"]
count = len(urls)

#################
# Testing non-blocking, async twisted page fetch
#################
def print_and_stop(output):
    #print output
    global count
    print "downloaded"
    print count
    count -= 1
    if not count and reactor.running :
        reactor.stop()

t = time.time()
for url in urls:
    print 'fetching', url
    d = getPage(url)
    d.addCallback(print_and_stop)
#    if not reactor.running:

reactor.run()
print time.time() - t

#################
# Testing blocking, single threaded scraperwiki page fetch
#################
t = time.time()
for url in urls:
    continue
    scraperwiki.scrape(url)
print time.time() - t