import scraperwiki
from BeautifulSoup import BeautifulSoup

#viimeinen hakemus id "S12162"
# retrieve a page
#URLin counter-numero ja aloitusnumero
n = 0
#URLin lopetusnumero
k = 10
urlia = 'S1000'
while n < k:
    if n < 10:
        urlia = 'S1000'
    if 9 < n < 100:
        urlia = 'S100'
    if 99 < n < 1000:
        urlia = 'S10'
starting_url = 'https://www.eura2007.fi/rrtiepa/projekti.php?projektikoodi='
running_url = starting_url + urlia + str(n)
html = scraperwiki.scrape(running_url)
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
    import scraperwiki
from BeautifulSoup import BeautifulSoup

#viimeinen hakemus id "S12162"
# retrieve a page
#URLin counter-numero ja aloitusnumero
n = 0
#URLin lopetusnumero
k = 10
urlia = 'S1000'
while n < k:
    if n < 10:
        urlia = 'S1000'
    if 9 < n < 100:
        urlia = 'S100'
    if 99 < n < 1000:
        urlia = 'S10'
starting_url = 'https://www.eura2007.fi/rrtiepa/projekti.php?projektikoodi='
running_url = starting_url + urlia + str(n)
html = scraperwiki.scrape(running_url)
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
    