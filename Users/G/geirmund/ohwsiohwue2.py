import scraperwiki

#From http://palewi.re/posts/2008/04/20/python-recipe-grab-a-page-scrape-a-table-download-a-file/

#!/usr/bin/env python
from mechanize import Browser
from BeautifulSoup import BeautifulSoup

def extract(soup, year):
    #print soup
    #print year
    tables = soup.findChildren('table')
    table = tables[4]
    for row in table.findAll('tr'):
        h3 = row.findAll('h3')
        name = h3[0].string
        print name
        td = row.findAll('td')
        role = td[2].string
        print role
        #cover_link = col[3].img['src']
        record = (str(year), name, role)
        print "|".join(record)

mech = Browser()
url = "http://europa.eu/whoiswho/public/index.cfm?fuseaction=idea.hierarchy&nodeID=370629&personID=150128&lang=en"
page1 = mech.open(url)
html1 = page1.read()
soup1 = BeautifulSoup(html1)
extract(soup1, 2007)
#page2 = mech.follow_link(text_regex="Next")
#html2 = page2.read()
#soup2 = BeautifulSoup(html2)
#extract(soup2, 2006)import scraperwiki

#From http://palewi.re/posts/2008/04/20/python-recipe-grab-a-page-scrape-a-table-download-a-file/

#!/usr/bin/env python
from mechanize import Browser
from BeautifulSoup import BeautifulSoup

def extract(soup, year):
    #print soup
    #print year
    tables = soup.findChildren('table')
    table = tables[4]
    for row in table.findAll('tr'):
        h3 = row.findAll('h3')
        name = h3[0].string
        print name
        td = row.findAll('td')
        role = td[2].string
        print role
        #cover_link = col[3].img['src']
        record = (str(year), name, role)
        print "|".join(record)

mech = Browser()
url = "http://europa.eu/whoiswho/public/index.cfm?fuseaction=idea.hierarchy&nodeID=370629&personID=150128&lang=en"
page1 = mech.open(url)
html1 = page1.read()
soup1 = BeautifulSoup(html1)
extract(soup1, 2007)
#page2 = mech.follow_link(text_regex="Next")
#html2 = page2.read()
#soup2 = BeautifulSoup(html2)
#extract(soup2, 2006)