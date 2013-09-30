################################################
# Scraper to grab article text related to      #
# 2011 Irish Presidential Elections            #
# from IrishTimes                              #
################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

irishtimes_pages_url = 'http://www.irishtimes.com/search/index.html?rm=listresults&filter=datedesc&keywords=aras&rows=100'
html = scraperwiki.scrape(irishtimes_pages_url)
soup = BeautifulSoup(html)
i = 0

# This gives us the list of all article titles & short 
# descriptions on the elections page today 
datatable = soup.find("ul", { "class" : "results" } )
rows = datatable.findAll("a")

# print rows
storyUrl = ""

for row in rows:
    i = i+1
    data = {}
    data['uniqueID'] = i

    storyUrl = row["href"]
    data['url'] = 'http://www.irishtimes.com' + storyUrl
    # print storyUrl

    # First get the headline text
    articleTitle = row.find("span", { "class" : "h2" } )
    # print articleTitle.text
    data['title'] = articleTitle.text

    articleDesc = row.find("span", { "class" : "result" } )
    print articleDesc.text
    data['description'] = articleDesc.text

    scraperwiki.sqlite.save(["url"],data)

################################################
# Scraper to grab article text related to      #
# 2011 Irish Presidential Elections            #
# from IrishTimes                              #
################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

irishtimes_pages_url = 'http://www.irishtimes.com/search/index.html?rm=listresults&filter=datedesc&keywords=aras&rows=100'
html = scraperwiki.scrape(irishtimes_pages_url)
soup = BeautifulSoup(html)
i = 0

# This gives us the list of all article titles & short 
# descriptions on the elections page today 
datatable = soup.find("ul", { "class" : "results" } )
rows = datatable.findAll("a")

# print rows
storyUrl = ""

for row in rows:
    i = i+1
    data = {}
    data['uniqueID'] = i

    storyUrl = row["href"]
    data['url'] = 'http://www.irishtimes.com' + storyUrl
    # print storyUrl

    # First get the headline text
    articleTitle = row.find("span", { "class" : "h2" } )
    # print articleTitle.text
    data['title'] = articleTitle.text

    articleDesc = row.find("span", { "class" : "result" } )
    print articleDesc.text
    data['description'] = articleDesc.text

    scraperwiki.sqlite.save(["url"],data)

