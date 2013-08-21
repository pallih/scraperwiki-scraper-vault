import scraperwiki
import sys, urllib2, urlparse, string
from BeautifulSoup import BeautifulSoup
from time import gmtime, strftime
print "start time ",strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()),"nnn"
try:
    root = sys.argv[1]
except IndexError:
    print "  Usage: ./crawler.py link"
    print "  Example: ./crawler.py http://blah.com/"
exit()
linkz = []
crawled = []
errorz = []
imgz = []
parsedRoot = urlparse.urlparse(root)
if parsedRoot.port == 80:
    hostRoot = parsedRoot.netloc[:-3]
else:
    hostRoot = parsedRoot.netloc
linkz.append(root)
print '<?xml version="1.0" encoding="UTF-8"?>n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">n'
for l in linkz:
    try:
        src = urllib2.urlopen(l).read()
        bs = BeautifulSoup(src)
        for j in bs.findAll('a', {'href':True}):
            try:
                absUrl = urlparse.urljoin(l, j['href'])
                parsedUrl = urlparse.urlparse(absUrl)
                if parsedUrl.port == 80:
                    hostUrl = parsedUrl.netloc[:-3]
                else:
                    hostUrl = parsedUrl.netloc
                    absUrl = urlparse.urlunparse((parsedUrl.scheme, hostUrl, parsedUrl.path, parsedUrl.params, parsedUrl.query, parsedUrl.fragment))
                if (parsedUrl.scheme == 'http') & ((parsedUrl.netloc.endswith('.' + hostRoot)) | (parsedUrl.netloc == hostRoot)) & (absUrl not in linkz):
                    tester = absUrl.find('#')
                    if tester == -1:
                        cleanUrl = absUrl.strip()
                        cleanUrl = cleanUrl.replace('&','&')
                    print "t<url>ntt<loc>" + cleanUrl + "</loc>nt</url>"
                    linkz.append(absUrl)
                    except: 

pass 


for i in bs.findAll('img', {'src':True}):
absUrl = urlparse.urljoin(l, i['src'])
parsedUrl = urlparse.urlparse(absUrl)
if parsedUrl.port == 80:
hostUrl = parsedUrl.netloc[:-3]
else:
hostUrl = parsedUrl.netloc
absUrl = urlparse.urlunparse((parsedUrl.scheme, hostUrl, parsedUrl.path, parsedUrl.params, parsedUrl.query, parsedUrl.fragment))
if (parsedUrl.scheme == 'http') & 
((parsedUrl.netloc.endswith('.' + hostRoot)) | (parsedUrl.netloc == hostRoot)) & 
(absUrl not in imgz):
print "t<url>ntt<loc>" + absUrl + "</loc>nt</url>"
imgz.append(absUrl)
except:
pass
print "</urlset>"
print "Completed at ",strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()),"nnn"
