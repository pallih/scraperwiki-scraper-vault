import scraperwiki
from BeautifulSoup import BeautifulSoup

starting_url = 'http://www.fsa.gov.uk/register/prohibitedIndivs.do'
html = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(html)

trs = soup.findAll('table.search-results tr') 
for tr in trs:
    print tr.td
    #record = { "td" : td.text }
    #scraperwiki.datastore.save(["td"], record) 
    import scraperwiki
from BeautifulSoup import BeautifulSoup

starting_url = 'http://www.fsa.gov.uk/register/prohibitedIndivs.do'
html = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(html)

trs = soup.findAll('table.search-results tr') 
for tr in trs:
    print tr.td
    #record = { "td" : td.text }
    #scraperwiki.datastore.save(["td"], record) 
    