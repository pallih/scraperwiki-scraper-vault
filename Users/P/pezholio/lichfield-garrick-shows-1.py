###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
import dateutil.parser
import datetime

from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://www.lichfieldgarrick.com/'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
shows = soup.find('div', { "id" : "fullListing"}).findAll('div', { "class" : "show" }) 
for show in shows:
    title = show.findAll('h3')[0].text
    showdate = show.findAll('p', { "class" : "date" })[0].text
    description = show.findAll('p', { "class" : "info" })[0].text
    dates = showdate.split("-")
    fromdate = dateutil.parser.parse(dates[0])
    if len(dates) > 1:
        todate = dateutil.parser.parse(dates[1])
    else:
        todate = None
    link = "http://www.lichfieldgarrick.com" + show.findAll('a', { "class" : "button-red" })[0]['href']

    record = { "title" : title, "description" : description, "fromdate" : fromdate, "todate" : todate, "link" : link }
    # save records to the datastore
    scraperwiki.datastore.save(['title'], data = record, date = fromdate) 
    