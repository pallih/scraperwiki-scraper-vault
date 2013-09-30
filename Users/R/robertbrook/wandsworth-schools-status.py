#ashx scrape
#

import scraperwiki
from BeautifulSoup import BeautifulSoup

starting_url = 'https://support.lgfl.org.uk/public/bits/opencheck.ashx?code=212' ## this page kept timing out on me :(
html = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(html)

spans = soup.findAll('span') 
for span in spans:
    if span["class"] == "school":
        school = span.contents
    elif span["class"] == "message":
        message = span.contents
    else:
        update = span.contents
        record = { "school" : school, "message" : message, "update" : update}
        scraperwiki.datastore.save(["school"], record) 
    #ashx scrape
#

import scraperwiki
from BeautifulSoup import BeautifulSoup

starting_url = 'https://support.lgfl.org.uk/public/bits/opencheck.ashx?code=212' ## this page kept timing out on me :(
html = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(html)

spans = soup.findAll('span') 
for span in spans:
    if span["class"] == "school":
        school = span.contents
    elif span["class"] == "message":
        message = span.contents
    else:
        update = span.contents
        record = { "school" : school, "message" : message, "update" : update}
        scraperwiki.datastore.save(["school"], record) 
    