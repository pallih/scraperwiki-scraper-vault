import sys, logging, urllib, mechanize, urllib2, scraperwiki
from BeautifulSoup import BeautifulSoup

# Retrieve page
url = "http://whois.afrinic.net/cgi-bin/whois"
ip = '41.1.0.0'

br = mechanize.Browser()
br.set_handle_robots(False)

br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.2.6) Gecko/20100625 Firefox/3.6.6 (.NET CLR 3.5.30729)')]

br.set_debug_http(True)
br.set_debug_redirects(True)
br.set_debug_responses(True)

br.open(url)
br.select_form(1)
br['full_query_string'] = ""
br['do_search'] = "Search"
br['searchtext'] = ip
response = br.submit()

#soup = BeautifulSoup(response)
#print response

