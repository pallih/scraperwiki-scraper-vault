import scraperwiki
from BeautifulSoup import BeautifulSoup


starting_url = 'http://www.fsa.gov.uk/register/eMoney.do'
html = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(html)


tds = soup.findAll('td') 
for td in tds:
    record = { "issuer" : td.text.replace("&nbsp;","") }
    scraperwiki.datastore.save(["issuer"], record) 
    import scraperwiki
from BeautifulSoup import BeautifulSoup


starting_url = 'http://www.fsa.gov.uk/register/eMoney.do'
html = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(html)


tds = soup.findAll('td') 
for td in tds:
    record = { "issuer" : td.text.replace("&nbsp;","") }
    scraperwiki.datastore.save(["issuer"], record) 
    