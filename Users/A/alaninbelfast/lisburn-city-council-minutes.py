# Draft scraper to export details of Lisburn City Council committee meetings
# from http://www.lisburncity.gov.uk/your-city-council/council-minutes-and-reports/
# into a more usable form.
#
# Alan in Belfast (18/11/2010)
#
# The ultimate aim is to produce an RSS feed of each type of council report that
# is published online

# NEXT STEPS
# * Need to cope tihe NEXT PAGE links
# * Need to spider into the links being returned to get the actual link to the PDFs
# * Need to stop hardcoding the 'Committee' tag

import scraperwiki
from BeautifulSoup import BeautifulSoup

scraperwiki.metadata.save('data_columns', ['Date', 'Committee', 'Title', 'Link'])

#starting_url = 'http://www.lisburncity.gov.uk/your-city-council/council-minutes-and-reports/index.php?month=6&year=2010&committee=15&freshform=no'
starting_url = 'http://www.lisburncity.gov.uk/your-city-council/council-minutes-and-reports/index.php?year=2010&committee=15&freshform=no'


html = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(html)

#Find the data we want to use in the page by looking for the table ID; we're then making
#an array of all the rows in that table

datatable = soup.findAll("ol", { "type": "1" } )
#print datatable

for ol in datatable:
       
    record = {}
    datestring = ol.find("i").text
    date_rest = datestring[4:]
    date_day_pre = datestring[:4]
    date_day = date_day_pre.rstrip('thrdstn ')

    #record['Date'] = ol.find("i").text
    record['Date'] = date_day + ' ' + date_rest.lstrip()

    record['Committee'] = 'Full Monthly Council Meeting' #not in the search results page!
    link = ol.find("a")
    record['Title'] = link.text
    record['Link'] = 'http://www.lisburncity.gov.uk/your-city-council/council-minutes-and-reports/index.php' + link['href']
    # Print out the data we've gathered
    print record, '------------'
    scraperwiki.datastore.save(["Date"], record)


