import scraperwiki
import urllib

url = "http://mikulski.senate.gov/about/biography.cfm"
gurl = "http://seagrass.goatchurch.org.uk/~julian/cgi-bin/aa.cgi?url=%s" % urllib.quote(url)

print "this one works (via my proxy)"
print urllib.urlopen(gurl).read()

print "this one hangs and produces no acceptable error"
print urllib.urlopen(url).read()



