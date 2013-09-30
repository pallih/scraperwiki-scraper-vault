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
import csv

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
the_list = []

list_url = "http://greencracker.net/wp-content/uploads/2013/06/elevenn.csv"
response = br.open(list_url)
html = response.read()

the_list = html.split("*")
i = 0
for item in range(len(the_list)):
    the_list[i] = the_list[i].replace("\r", "")
    the_list[i] = the_list[i].replace("'", "")
    the_list[i] = the_list[i].replace('"', "")
    the_list[i] = the_list[i].strip()
    i=i+1

print the_list


target = "http://www.nsopw.gov/en-us/Search"
response = br.open(target)
html = response.read()
print html

print "All forms:", [ form.name  for form in br.forms() ]
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
import csv

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
the_list = []

list_url = "http://greencracker.net/wp-content/uploads/2013/06/elevenn.csv"
response = br.open(list_url)
html = response.read()

the_list = html.split("*")
i = 0
for item in range(len(the_list)):
    the_list[i] = the_list[i].replace("\r", "")
    the_list[i] = the_list[i].replace("'", "")
    the_list[i] = the_list[i].replace('"', "")
    the_list[i] = the_list[i].strip()
    i=i+1

print the_list


target = "http://www.nsopw.gov/en-us/Search"
response = br.open(target)
html = response.read()
print html

print "All forms:", [ form.name  for form in br.forms() ]
    