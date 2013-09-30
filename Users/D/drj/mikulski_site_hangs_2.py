import os
import urllib

url = "http://mikulski.senate.gov/about/biography.cfm"
gurl = "http://seagrass.goatchurch.org.uk/~julian/cgi-bin/aa.cgi?url=%s" % urllib.quote(url)

# print os.environ

print "this one hangs and produces no acceptable error"
print urllib.urlopen(url).read()


os.system("netstat -nr")

print "this one works (via my proxy)"
print urllib.urlopen(gurl).read()




import os
import urllib

url = "http://mikulski.senate.gov/about/biography.cfm"
gurl = "http://seagrass.goatchurch.org.uk/~julian/cgi-bin/aa.cgi?url=%s" % urllib.quote(url)

# print os.environ

print "this one hangs and produces no acceptable error"
print urllib.urlopen(url).read()


os.system("netstat -nr")

print "this one works (via my proxy)"
print urllib.urlopen(gurl).read()




