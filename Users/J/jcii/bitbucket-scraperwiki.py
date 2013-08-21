# Blank Python
# Blank Python
import scraperwiki
import logging
from BeautifulSoup import BeautifulSoup


# retrieve a page
starting_url = 'http://hg.telking.com/ScraperWiki/scraperwiki/issues'
html = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(html)

tables = soup.findAll('table', {"class" : "maintable"})
if len(tables) > 0:
    rows = tables[0].tbody.findAll('tr')
    print "There are %d rows" % len(rows)
    for row in rows:
        cells = row.findAll('td')

        issuenum = cells[0].text
        issuedesc = cells[1].text
        issuestate = cells[2].text
        responsible= cells[3].text
        citystatezip = cells[4].text
        employer = cells[5].text
        interest_category = cells[6].text
        amount = cells[7].text
