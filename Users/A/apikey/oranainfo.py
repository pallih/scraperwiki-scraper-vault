import urllib2

url = "http://orana.info"
filein = urllib2.urlopen(url)

print "The page has been loaded (see the 'Sources' tab below)"

html = filein.read()
print "The page is %d bytes long" % len(html)

print "The first 2000 characters of the page is:", html[:2000]




