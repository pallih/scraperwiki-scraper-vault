import scraperwiki
from BeautifulSoup import BeautifulSoup

class BrokenLinkException(Exception):
       def __init__(self, value):
           self.parameter = value
       def __str__(self):
           return repr(self.parameter)

broken = False
broken_links = []

print "Scraping html from Brigade site..."
html = scraperwiki.scrape('http://brigade.codeforamerica.org/pages/forums')

print "Collecting links..."
root = BeautifulSoup(html)
table = root.findAll('table')[1]
links = table.findAll('a',href=True)

print "Checking links..."
for link in links:
    if "mailto" not in link['href']:
        try:
            #Uncomment the line below to print each link as it is checked
            print "Now checking: " + link['href']
            html = scraperwiki.scrape(link['href'])
        except:
            print "ERROR! Broken link at: " + link['href']
            broken = True
            broken_links.append(link['href'])

if broken == True:
    print str(len(broken_links)) + " links are broken."
    print "Broken links: "
    for broken_link in broken_links:
        print broken_link
    raise BrokenLinkException("Broken links were detected.")
else:
    print "No links broken!"

import scraperwiki
from BeautifulSoup import BeautifulSoup

class BrokenLinkException(Exception):
       def __init__(self, value):
           self.parameter = value
       def __str__(self):
           return repr(self.parameter)

broken = False
broken_links = []

print "Scraping html from Brigade site..."
html = scraperwiki.scrape('http://brigade.codeforamerica.org/pages/forums')

print "Collecting links..."
root = BeautifulSoup(html)
table = root.findAll('table')[1]
links = table.findAll('a',href=True)

print "Checking links..."
for link in links:
    if "mailto" not in link['href']:
        try:
            #Uncomment the line below to print each link as it is checked
            print "Now checking: " + link['href']
            html = scraperwiki.scrape(link['href'])
        except:
            print "ERROR! Broken link at: " + link['href']
            broken = True
            broken_links.append(link['href'])

if broken == True:
    print str(len(broken_links)) + " links are broken."
    print "Broken links: "
    for broken_link in broken_links:
        print broken_link
    raise BrokenLinkException("Broken links were detected.")
else:
    print "No links broken!"

