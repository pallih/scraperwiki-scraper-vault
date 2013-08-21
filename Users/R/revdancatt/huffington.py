###############################################################################
# START HERE: Tutorial 2: Basic scraping and saving to the data store.
# Follow the actions listed in BLOCK CAPITALS below.
###############################################################################
from BeautifulSoup import BeautifulSoup
import scraperwiki

html = scraperwiki.scrape('http://www.google.com/search?q=site:huffingtonpost.com+"Read+the+whole+story:+The+Guardian"+"WHAT\'S+YOUR+REACTION%3F"&hl=en&safe=off&client=firefox-a&hs=nsg&tbo=1&channel=s&prmd=iv&source=lnt&tbs=rltm:1&sa=X')


results = BeautifulSoup(html) # turn our HTML into a BeautifulSoup object
links = results.findAll("a", {"class": "l"}) # get all the <td> tags
counter = 0
for a in links:
    
    article_html = scraperwiki.scrape(a['href'])
    article = BeautifulSoup(article_html)
    
    g_links = article.findAll("a", {"target": "_blank"})
    for g_link in g_links:
        if "Read the whole story" in g_link.text:
            print g_link['href']
            scraperwiki.datastore.save(["link"], {"link": g_link['href']})

    counter+=1
    if counter >= 6:
        break
#    print td.text # just the text inside the HTML tag

# -----------------------------------------------------------------------------
# 2. Save the data in the ScraperWiki datastore.
# -- UNCOMMENT THE TWO LINES BELOW
# -- CLICK THE 'RUN' BUTTON BELOW
# Check the 'Data' tab - here you'll see the data saved in the ScraperWiki store. 
# -----------------------------------------------------------------------------

#for td in tds:
#     record = { "td" : td.text } # column name and value
#     scraperwiki.datastore.save(["td"], record) # save the records one by one
    
# -----------------------------------------------------------------------------
# Go back to the Tutorials page and continue to Tutorial 3 to learn about 
# more complex scraping methods.
# -----------------------------------------------------------------------------

