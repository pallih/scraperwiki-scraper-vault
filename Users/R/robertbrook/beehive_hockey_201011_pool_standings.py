import scraperwiki
from BeautifulSoup import BeautifulSoup

starting_url = 'http://beehive.uwaterloo.ca/pools/hockey1011/standings.html'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)

tds = soup.findAll('td', align="center") 
for td in tds:
    print td
    record = { "td" : td.text }
    # save records to the datastore
    scraperwiki.sqlite.save(["td"], record) 
    import scraperwiki
from BeautifulSoup import BeautifulSoup

starting_url = 'http://beehive.uwaterloo.ca/pools/hockey1011/standings.html'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)

tds = soup.findAll('td', align="center") 
for td in tds:
    print td
    record = { "td" : td.text }
    # save records to the datastore
    scraperwiki.sqlite.save(["td"], record) 
    