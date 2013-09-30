import scraperwiki
from BeautifulSoup import BeautifulSoup

#viimeinen hakemus id "S12162"
n = 10
urlia = 'S110'
while n < 20:
    k = 0
    starting_url='https://www.eura2007.fi/rrtiepa/projekti.php?projektikoodi='
    current_url = starting_url + urlia + str(n)
    html = scraperwiki.scrape(current_url)
#print html
    print current_url
    soup = BeautifulSoup(html)
    n = n + 1

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
n = 10
urlia = 'S110'
while n < 20:
    k = 0
    starting_url='https://www.eura2007.fi/rrtiepa/projekti.php?projektikoodi='
    current_url = starting_url + urlia + str(n)
    html = scraperwiki.scrape(current_url)
#print html
    print current_url
    soup = BeautifulSoup(html)
    n = n + 1

# use BeautifulSoup to get all <td> tags
    tds = soup.findAll('p') 
    for td in tds:
        print td
        record = { "td" : td.text }
        # save records to the datastore
        scraperwiki.sqlite.save(["td"], record) 
    