import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup
import scraperwiki

# the form
# all the form vars: average=6hour&sat=2&mnemonic=%3E+70+MeV%2Fnuc+Ions&duration=3-months&outputType=list&timeFormat=ISO
url = 'http://voyager.gsfc.nasa.gov/heliopause/recenthist.html'
values = {
          'sat' : '1',  # which Voyager, 1 or 2
          'duration' : '3-months',
          'outputType' : 'list',
          'timeFormat' : 'ISO'
          }

# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# Want debugging messages?
br.set_debug_http(True)
br.set_debug_redirects(True)
br.set_debug_responses(True)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# get it!
r = br.open(url)
br.select_form(nr=0)
br.submit()
page =  br.response().read()
soup = BeautifulSoup(page)

for line in soup.find('pre').text.split("\n")[2:]: # the first 2 lines are cruft
    data = {
        'Time' : line.split()[0],
        'Counts_per_Second' : line.split()[1],
        'Error' : line.split()[2]
    }
    scraperwiki.sqlite.save(unique_keys=['Time'], data=data)

import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup
import scraperwiki

# the form
# all the form vars: average=6hour&sat=2&mnemonic=%3E+70+MeV%2Fnuc+Ions&duration=3-months&outputType=list&timeFormat=ISO
url = 'http://voyager.gsfc.nasa.gov/heliopause/recenthist.html'
values = {
          'sat' : '1',  # which Voyager, 1 or 2
          'duration' : '3-months',
          'outputType' : 'list',
          'timeFormat' : 'ISO'
          }

# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# Want debugging messages?
br.set_debug_http(True)
br.set_debug_redirects(True)
br.set_debug_responses(True)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# get it!
r = br.open(url)
br.select_form(nr=0)
br.submit()
page =  br.response().read()
soup = BeautifulSoup(page)

for line in soup.find('pre').text.split("\n")[2:]: # the first 2 lines are cruft
    data = {
        'Time' : line.split()[0],
        'Counts_per_Second' : line.split()[1],
        'Error' : line.split()[2]
    }
    scraperwiki.sqlite.save(unique_keys=['Time'], data=data)

import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup
import scraperwiki

# the form
# all the form vars: average=6hour&sat=2&mnemonic=%3E+70+MeV%2Fnuc+Ions&duration=3-months&outputType=list&timeFormat=ISO
url = 'http://voyager.gsfc.nasa.gov/heliopause/recenthist.html'
values = {
          'sat' : '1',  # which Voyager, 1 or 2
          'duration' : '3-months',
          'outputType' : 'list',
          'timeFormat' : 'ISO'
          }

# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# Want debugging messages?
br.set_debug_http(True)
br.set_debug_redirects(True)
br.set_debug_responses(True)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# get it!
r = br.open(url)
br.select_form(nr=0)
br.submit()
page =  br.response().read()
soup = BeautifulSoup(page)

for line in soup.find('pre').text.split("\n")[2:]: # the first 2 lines are cruft
    data = {
        'Time' : line.split()[0],
        'Counts_per_Second' : line.split()[1],
        'Error' : line.split()[2]
    }
    scraperwiki.sqlite.save(unique_keys=['Time'], data=data)

import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup
import scraperwiki

# the form
# all the form vars: average=6hour&sat=2&mnemonic=%3E+70+MeV%2Fnuc+Ions&duration=3-months&outputType=list&timeFormat=ISO
url = 'http://voyager.gsfc.nasa.gov/heliopause/recenthist.html'
values = {
          'sat' : '1',  # which Voyager, 1 or 2
          'duration' : '3-months',
          'outputType' : 'list',
          'timeFormat' : 'ISO'
          }

# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# Want debugging messages?
br.set_debug_http(True)
br.set_debug_redirects(True)
br.set_debug_responses(True)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# get it!
r = br.open(url)
br.select_form(nr=0)
br.submit()
page =  br.response().read()
soup = BeautifulSoup(page)

for line in soup.find('pre').text.split("\n")[2:]: # the first 2 lines are cruft
    data = {
        'Time' : line.split()[0],
        'Counts_per_Second' : line.split()[1],
        'Error' : line.split()[2]
    }
    scraperwiki.sqlite.save(unique_keys=['Time'], data=data)

