###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
import HTMLParser
import re
import htmlentitydefs

##
# Removes HTML or XML character references and entities from a text string.
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.

def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

def scrape_page(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)

    # Datastore for event details
    event = {}
    
    h2s = soup.findAll('h2', text=True)

    for h2 in h2s:
        if h2.a != None:
            print h2.a.text
            event['Title'] = h2.a.text

            event_url = h2.a['href']

            event['URL'] = event_url
        
            date = unescape(h2.parent.p.contents[0])
            event['Date'] = date

            scraperwiki.sqlite.save(["Title"], event)
    

    res = soup.findAll(text=re.compile("Next Page"))
    if len(res) != 0:
        nextLink = res[0].parent['href']
        print nextLink
        scrape_page(nextLink)
    
        
    

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
starting_url = 'http://www.nuffieldtheatre.co.uk/events/category/C80/'



scrape_page(starting_url)
