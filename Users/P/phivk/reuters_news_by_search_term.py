'''
scrape reuters' first page of search results
'''

import scraperwiki
import lxml.html
import re

def extractArticleInfo(searchResult,searchTerm):    
    item = {
        "itemURL": "",
        "itemHeadline": "",
        "itemSearchBlurb": "",
        "itemTimestamp": "",
        "company":searchTerm
    }
    
    item["itemURL"] = searchResult.find_class("searchHeadline")[0].findall("a")[0].get("href")   
    item["itemHeadline"] = searchResult.find_class("searchHeadline")[0].text_content()
    item["itemSearchBlurb"] = searchResult.find_class("searchBlurb")[0].text_content()
    item["itemTimestamp"] = searchResult.find_class("timestamp")[0].text_content()
    
    return item
    


##### MAIN #####

# http://www.reuters.com/search?blob=DePuy+orthopedics

URLBase = "http://www.reuters.com/search?blob="

# use "+" for [space] 
searchTerms = ['DePuy+orthopaedics', 'Stryker+Orthopaedics', 'Zimmer+Holdings', 'Medtronic+Spine', 'Smith&amp;Nephew', 'Synthes', 'Biomet', 'DJO+Global']

newsItems = []

for searchTerm in searchTerms:
    url =  URLBase + searchTerm
    print "... now scraping: ", url
    
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    body = root[1]
    
    contentTable = body.find_class("moduleBody")[1]
    searchResults = contentTable.find_class("searchResult")
    
    for searchResult in searchResults:
        scrapedArticle = extractArticleInfo(searchResult, searchTerm)
        newsItems.append(scrapedArticle)



# print first n records
n = min(5, len(newsItems))
print "len(newsItems): ", len(newsItems)
for j in range(n):
    print newsItems[j]

# save scraped data to scraperwiki
my_keys = ["itemURL", "itemHeadline", "itemSearchBlurb", "itemTimestamp"]
scraperwiki.sqlite.save(unique_keys=my_keys, data=newsItems)

