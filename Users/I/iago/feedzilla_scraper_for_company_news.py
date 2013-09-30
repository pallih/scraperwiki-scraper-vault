import scraperwiki   
import requests
import json
import urllib
import re

# Blank Python

def tidy(text):
    return text.strip('\l\r\n\t\f').replace('\t','').replace('\r','').replace('\n','')


##### MAIN #####

companies = ['DePuy Orthopaedics', 'Stryker Orthopaedics', 'Zimmer Holdings', 'Medtronic Spine', 'Smith & Nephew', 'Synthes', 'Biomet', 'DJO Global']

feedZillaBase = 'http://api.feedzilla.com/v1/articles/search.json?q={query}'

articles = []

for company in companies:
    term = urllib.quote_plus(company)
    #print term
    response = requests.get(feedZillaBase.format(query=term))
    responseJson = response.json()      
    
    #print json.dumps(responseJson['articles'],  sort_keys=True, indent=2, separators=(',', ': '))
    print "found {c} article(s) for term {t}".format(c=len(responseJson['articles']), t=term)

    for article in responseJson['articles']:        
        p1 = re.compile("^\w{3},\s([^\+]+)\s\+\d+")
        match = p1.match(article['publish_date'])

        if match:       
            cleanDate = match.group(1)
            article['publish_date'] = cleanDate

        article['company'] = company
        article['title'] = tidy(article['title'])
        tidyText = tidy(article['summary'])
        article['summary'] = tidyText
        print article
        articles.append(article)    
        
# save scraped data to scraperwiki
my_keys = ['publish_date', 'source', 'source_url', 'title', 'summary']
scraperwiki.sqlite.save(unique_keys=my_keys, data=articles)




