import scraperwiki

###############################################################################
# START HERE: Tutorial for scraping ASP.NET pages (HTML pages that end .aspx), using the
# very powerful Mechanize library. In general, when you follow a 'next' link on 
# .aspx pages, you're actually submitting a form.
# This tutorial demonstrates scraping a particularly tricky example. 
###############################################################################
import scraperwiki
import urllib2
import urllib
import time, random
import mechanize
from BeautifulSoup import BeautifulSoup

def startscrap(br, cat, pages):
    for start in range(0, pages):
        wt = random.uniform(2, 5) # Random wait, should seem like a human
        time.sleep(wt)
        url = "http://www.google.com/search?q=" + urllib.pathname2url(cat) + "&start=" + str(start*10)
        print url
        # open the page
        br.open(url)
        soup = BeautifulSoup(br.response().read())
        foundSomething = False
        for link in soup.findAll('a'):
            if link.has_key('href'):
                potential = link['href']
                if "http" == potential[:4]:
                    if not "google" in link['href']: 
                        foundSomething = True
                        print link['href'], "\t", cat, "\n"
        if not foundSomething:
            break;


# ---------------------------------------------------------------------------
# START HERE: setting up Mechanize
# We need to set the user-agent header so the page thinks we're a browser, 
# as otherwise it won't show all the fields we need
# ---------------------------------------------------------------------------
br = mechanize.Browser()
br.set_handle_robots(False)
# Set the user-agent as Mozilla - if the page knows we're Mechanize, it won't return all fields
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
# Have a look at 'soup': note the 'onSubmit' JavaScript function that is called when 
# you click on the 'next' link. We'll mimic this in the function above.
# start scraping
startscrap(br,"sports", 10)

import scraperwiki

###############################################################################
# START HERE: Tutorial for scraping ASP.NET pages (HTML pages that end .aspx), using the
# very powerful Mechanize library. In general, when you follow a 'next' link on 
# .aspx pages, you're actually submitting a form.
# This tutorial demonstrates scraping a particularly tricky example. 
###############################################################################
import scraperwiki
import urllib2
import urllib
import time, random
import mechanize
from BeautifulSoup import BeautifulSoup

def startscrap(br, cat, pages):
    for start in range(0, pages):
        wt = random.uniform(2, 5) # Random wait, should seem like a human
        time.sleep(wt)
        url = "http://www.google.com/search?q=" + urllib.pathname2url(cat) + "&start=" + str(start*10)
        print url
        # open the page
        br.open(url)
        soup = BeautifulSoup(br.response().read())
        foundSomething = False
        for link in soup.findAll('a'):
            if link.has_key('href'):
                potential = link['href']
                if "http" == potential[:4]:
                    if not "google" in link['href']: 
                        foundSomething = True
                        print link['href'], "\t", cat, "\n"
        if not foundSomething:
            break;


# ---------------------------------------------------------------------------
# START HERE: setting up Mechanize
# We need to set the user-agent header so the page thinks we're a browser, 
# as otherwise it won't show all the fields we need
# ---------------------------------------------------------------------------
br = mechanize.Browser()
br.set_handle_robots(False)
# Set the user-agent as Mozilla - if the page knows we're Mechanize, it won't return all fields
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
# Have a look at 'soup': note the 'onSubmit' JavaScript function that is called when 
# you click on the 'next' link. We'll mimic this in the function above.
# start scraping
startscrap(br,"sports", 10)

