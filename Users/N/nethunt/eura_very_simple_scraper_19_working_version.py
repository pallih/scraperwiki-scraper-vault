import scraperwiki
from BeautifulSoup import BeautifulSoup

#viimeinen hakemus id "S12162"
n = 160
k = 163
urlia = 'S1200'
while n < k:
    if n < 10:
        urlia = 'S1200'
    if 9 < n < 100:
        urlia = 'S120'
    if 99 < n < 1000:
        urlia = 'S12'
    starting_url='https://www.eura2007.fi/rrtiepa/projekti.php?projektikoodi='
    current_url = starting_url + urlia + str(n)
    html = scraperwiki.scrape(current_url)
#    print urlia
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