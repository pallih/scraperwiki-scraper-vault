################################################
# Scraper to grab article text related to      #
# 2011 Irish Presidential Elections            #
################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

irishtimes_pages_url = 'http://www.rte.ie/news/presidential-special-reports.html'
html = scraperwiki.scrape(irishtimes_pages_url)
soup = BeautifulSoup(html)
i = 0

# This gives us the list of all article titles & short 
# descriptions on the elections page today 
datatable = soup.find("div", { "class" : "rte_gr_8 no_margin_top" } )
rows = datatable.findAll("li")

# print rows
storyUrl = ""

for row in rows:
    i = i+1
    data = {}

    # First get the headline text
    articleTitle = row.findAll(['h2','h3'])
    if articleTitle:
        link = articleTitle[0].find('a');
        storyUrl = link["href"]
        data['url'] = storyUrl
        print storyUrl
        data['uniqueID'] = i

        headline = link.text
        data['title'] = headline

        # Next get the article description
        articleDesc = row.findAll("p")
        if articleDesc: 
            link2 = articleDesc[1].find('a');
            descText = link2.text
            data['description'] = descText
    
            scraperwiki.sqlite.save(["url"],data)

