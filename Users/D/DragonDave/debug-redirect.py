import scraperwiki

# Blank Python

# import urllib2; print urllib2.urlopen("http://www.parkrun.org.uk/richmond/results/latestresults").geturl()

import urllib2
headers = { 'User-Agent' : 'Mozilla/5.0' }
headers={} # comment out this line to make it work.

class MyHTTPRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        print code,msg,"\n\n",headers
        print "Cookie Manip Right Here"
        return urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)

    http_error_301 = http_error_303 = http_error_307 = http_error_302

cookieprocessor = urllib2.HTTPCookieProcessor()

opener = urllib2.build_opener(MyHTTPRedirectHandler, cookieprocessor)
urllib2.install_opener(opener)

response =urllib2.Request("http://www.parkrun.org.uk/richmond/results/latestresults",headers=headers)
print urllib2.urlopen(response).read()

print cookieprocessor.cookiejar