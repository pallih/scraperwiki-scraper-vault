import scraperwiki

###############################################################################
# START HERE: Tutorial 1: Getting used to the ScraperWiki editing interface.
# Follow the actions listed with -- BLOCK CAPITALS below.
###############################################################################

# -----------------------------------------------------------------------------
# 1. Start by running a really simple Python script, just to make sure that 
# everything is working OK.
# -- CLICK THE 'RUN' BUTTON BELOW
# You should see some numbers print in the 'Console' tab below. If it doesn't work, 
# try reopening this page in a different browser - Chrome or the latest Firefox.
# -----------------------------------------------------------------------------

for i in range(10):
    print "Hello", i

# -----------------------------------------------------------------------------
# 2. Next, try scraping an actual web page and getting some raw HTML.
# -- UNCOMMENT THE THREE LINES BELOW (i.e. delete the # at the start of the lines)
# -- CLICK THE 'RUN' BUTTON AGAIN 
# You should see the raw HTML at the bottom of the 'Console' tab. 
# Click on the 'more' link to see it all, and the 'Sources' tab to see our URL - 
# you can click on the URL to see the original page. 
# -----------------------------------------------------------------------------

scraperwiki.cache(True)

#import scraperwiki
import urllib2
urllib2.urlopen('http://scraperwiki.com/hello_world.html')
html = scraperwiki.scrape('http://scraperwiki.com/hello_world.html')

print html


data = { }
for i in range(50):
    data[str(i)] = i*i

for j in range(20):
    data["1"] = j
    scraperwiki.datastore.save(unique_keys=["1"], data=data)

# for handling the bug: https://bitbucket.org/ScraperWiki/scraperwiki/issue/111/data-tab-does-not-allow-users-to-see-allimport scraperwiki

###############################################################################
# START HERE: Tutorial 1: Getting used to the ScraperWiki editing interface.
# Follow the actions listed with -- BLOCK CAPITALS below.
###############################################################################

# -----------------------------------------------------------------------------
# 1. Start by running a really simple Python script, just to make sure that 
# everything is working OK.
# -- CLICK THE 'RUN' BUTTON BELOW
# You should see some numbers print in the 'Console' tab below. If it doesn't work, 
# try reopening this page in a different browser - Chrome or the latest Firefox.
# -----------------------------------------------------------------------------

for i in range(10):
    print "Hello", i

# -----------------------------------------------------------------------------
# 2. Next, try scraping an actual web page and getting some raw HTML.
# -- UNCOMMENT THE THREE LINES BELOW (i.e. delete the # at the start of the lines)
# -- CLICK THE 'RUN' BUTTON AGAIN 
# You should see the raw HTML at the bottom of the 'Console' tab. 
# Click on the 'more' link to see it all, and the 'Sources' tab to see our URL - 
# you can click on the URL to see the original page. 
# -----------------------------------------------------------------------------

scraperwiki.cache(True)

#import scraperwiki
import urllib2
urllib2.urlopen('http://scraperwiki.com/hello_world.html')
html = scraperwiki.scrape('http://scraperwiki.com/hello_world.html')

print html


data = { }
for i in range(50):
    data[str(i)] = i*i

for j in range(20):
    data["1"] = j
    scraperwiki.datastore.save(unique_keys=["1"], data=data)

# for handling the bug: https://bitbucket.org/ScraperWiki/scraperwiki/issue/111/data-tab-does-not-allow-users-to-see-allimport scraperwiki

###############################################################################
# START HERE: Tutorial 1: Getting used to the ScraperWiki editing interface.
# Follow the actions listed with -- BLOCK CAPITALS below.
###############################################################################

# -----------------------------------------------------------------------------
# 1. Start by running a really simple Python script, just to make sure that 
# everything is working OK.
# -- CLICK THE 'RUN' BUTTON BELOW
# You should see some numbers print in the 'Console' tab below. If it doesn't work, 
# try reopening this page in a different browser - Chrome or the latest Firefox.
# -----------------------------------------------------------------------------

for i in range(10):
    print "Hello", i

# -----------------------------------------------------------------------------
# 2. Next, try scraping an actual web page and getting some raw HTML.
# -- UNCOMMENT THE THREE LINES BELOW (i.e. delete the # at the start of the lines)
# -- CLICK THE 'RUN' BUTTON AGAIN 
# You should see the raw HTML at the bottom of the 'Console' tab. 
# Click on the 'more' link to see it all, and the 'Sources' tab to see our URL - 
# you can click on the URL to see the original page. 
# -----------------------------------------------------------------------------

scraperwiki.cache(True)

#import scraperwiki
import urllib2
urllib2.urlopen('http://scraperwiki.com/hello_world.html')
html = scraperwiki.scrape('http://scraperwiki.com/hello_world.html')

print html


data = { }
for i in range(50):
    data[str(i)] = i*i

for j in range(20):
    data["1"] = j
    scraperwiki.datastore.save(unique_keys=["1"], data=data)

# for handling the bug: https://bitbucket.org/ScraperWiki/scraperwiki/issue/111/data-tab-does-not-allow-users-to-see-allimport scraperwiki

###############################################################################
# START HERE: Tutorial 1: Getting used to the ScraperWiki editing interface.
# Follow the actions listed with -- BLOCK CAPITALS below.
###############################################################################

# -----------------------------------------------------------------------------
# 1. Start by running a really simple Python script, just to make sure that 
# everything is working OK.
# -- CLICK THE 'RUN' BUTTON BELOW
# You should see some numbers print in the 'Console' tab below. If it doesn't work, 
# try reopening this page in a different browser - Chrome or the latest Firefox.
# -----------------------------------------------------------------------------

for i in range(10):
    print "Hello", i

# -----------------------------------------------------------------------------
# 2. Next, try scraping an actual web page and getting some raw HTML.
# -- UNCOMMENT THE THREE LINES BELOW (i.e. delete the # at the start of the lines)
# -- CLICK THE 'RUN' BUTTON AGAIN 
# You should see the raw HTML at the bottom of the 'Console' tab. 
# Click on the 'more' link to see it all, and the 'Sources' tab to see our URL - 
# you can click on the URL to see the original page. 
# -----------------------------------------------------------------------------

scraperwiki.cache(True)

#import scraperwiki
import urllib2
urllib2.urlopen('http://scraperwiki.com/hello_world.html')
html = scraperwiki.scrape('http://scraperwiki.com/hello_world.html')

print html


data = { }
for i in range(50):
    data[str(i)] = i*i

for j in range(20):
    data["1"] = j
    scraperwiki.datastore.save(unique_keys=["1"], data=data)

# for handling the bug: https://bitbucket.org/ScraperWiki/scraperwiki/issue/111/data-tab-does-not-allow-users-to-see-allimport scraperwiki

###############################################################################
# START HERE: Tutorial 1: Getting used to the ScraperWiki editing interface.
# Follow the actions listed with -- BLOCK CAPITALS below.
###############################################################################

# -----------------------------------------------------------------------------
# 1. Start by running a really simple Python script, just to make sure that 
# everything is working OK.
# -- CLICK THE 'RUN' BUTTON BELOW
# You should see some numbers print in the 'Console' tab below. If it doesn't work, 
# try reopening this page in a different browser - Chrome or the latest Firefox.
# -----------------------------------------------------------------------------

for i in range(10):
    print "Hello", i

# -----------------------------------------------------------------------------
# 2. Next, try scraping an actual web page and getting some raw HTML.
# -- UNCOMMENT THE THREE LINES BELOW (i.e. delete the # at the start of the lines)
# -- CLICK THE 'RUN' BUTTON AGAIN 
# You should see the raw HTML at the bottom of the 'Console' tab. 
# Click on the 'more' link to see it all, and the 'Sources' tab to see our URL - 
# you can click on the URL to see the original page. 
# -----------------------------------------------------------------------------

scraperwiki.cache(True)

#import scraperwiki
import urllib2
urllib2.urlopen('http://scraperwiki.com/hello_world.html')
html = scraperwiki.scrape('http://scraperwiki.com/hello_world.html')

print html


data = { }
for i in range(50):
    data[str(i)] = i*i

for j in range(20):
    data["1"] = j
    scraperwiki.datastore.save(unique_keys=["1"], data=data)

# for handling the bug: https://bitbucket.org/ScraperWiki/scraperwiki/issue/111/data-tab-does-not-allow-users-to-see-all