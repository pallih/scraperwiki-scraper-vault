###############################################################################
#here is a very hard-coded scrape of Georgia Public Notices
###############################################################################
import mechanize 
import urllib
import cookielib
import time
from BeautifulSoup import BeautifulSoup
import re
import scraperwiki
import lxml.html

# Browser
br = mechanize.Browser(factory=mechanize.RobustFactory())
#print "ok mechanize"
    
# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)
    
#print "ok cookie"
    
# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
    
#print "ok options"
    
# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    
#print "ok handle"
# Want debugging messages?
br.set_debug_http(True)
br.set_debug_redirects(True)
br.set_debug_responses(True)
    
# User-Agent 
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
#print "ok headers"
#list_of_names = []
#list_url = "http://greencracker.net/wp-content/uploads/2012/06/patchsenate.csv"
#response = br.open(list_url)
#html = response.read()
#list_of_names = html.split()
#print list_of_names

url = "http://en.wikipedia.org/wiki/Hypocorism"
big_list = []
small_list = []
#---- end declarations
response = br.open(url)
html = response.read()
root = lxml.html.fromstring(html)

for list_item in (root.cssselect('ul')):
    for item in list_item.cssselect('li'):
        small_list = []
        for name in item.cssselect('i'):
            name = lxml.etree.tostring(name)
            small_list.append(name)
        #print small_list
        big_list.append(small_list)
        #data = {small_list}
print big_list
        #scraperwiki.sqlite.save(unique_keys=['small_list'], data=data)






    
    