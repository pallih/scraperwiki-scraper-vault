import scraperwiki
from BeautifulSoup import BeautifulSoup

#viimeinen hakemus id "S12162"
# retrieve a page
starting_url = 'https://www.eura2007.fi/rrtiepa/projekti.php?projektikoodi=S10001'
html = scraperwiki.scrape(starting_url)
#print html
print starting_url
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
tds = soup.findAll('p') 
for td in tds:
    print td
    record = { "td" : td.text }
    # save records to the datastore
    scraperwiki.sqlite.save(["td"], record) 
    