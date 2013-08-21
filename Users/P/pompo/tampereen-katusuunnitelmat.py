###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
import uuid
from BeautifulSoup import BeautifulSoup



def gettitles(url):
    titleshtml = scraperwiki.scrape(url)
    titlessoup = BeautifulSoup(titleshtml, convertEntities="html")
    titles = titlessoup.findAll("h2", "h2_input")
    titletexts = []
    for title in titles:
        titlelink = title.find("a", "anchorlink")
        titletexts.append(titlelink.text)
    return titletexts

def getnavi(html):
    soup = BeautifulSoup(html, convertEntities="html")
    navi = soup.findAll("div", "level1") 
    for it in navi:
        url = it.find('a')['href']
        date = it.text
        titles = gettitles(url)
        guid = url 
        record = { "date" : date, "url" : url, "titles": titles, "guid": url}
        # save records to the datastore
        scraperwiki.datastore.save(["date"], record)




# retrieve a page
starting_url = 'http://www.tampere.fi/liikennejakadut/katusuunnitelmat.html'
html = scraperwiki.scrape(starting_url)
getnavi(html)
