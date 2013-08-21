import scraperwiki
from BeautifulSoup import BeautifulSoup

n = 1
urlia = 'S1000'
while n <= 10:

    address='https://www.eura2007.fi/rrtiepa/projekti.php?projektikoodi='
    laskuri_address = address + urlia + str(n)
#    print 'Osoite: ', laskuri_address, 'ja n: ', n 
    html = scraperwiki.scrape(laskuri_address)
    soup = BeautifulSoup(html)
    n = n + 1
    tds = soup.findAll('p')

#        table_cells = row.findAll("td")

    print laskuri_address

for td in tds:
#    print td.txt
    kalaa = { "td" : td.text }
    scraperwiki.sqlite.save(["td"], kalaa) 

print "Onnistui :)"
    