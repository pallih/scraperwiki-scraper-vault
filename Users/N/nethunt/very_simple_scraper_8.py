import scraperwiki
from BeautifulSoup import BeautifulSoup

n = 10
while n <= 12:

    address='https://www.eura2007.fi/rrtiepa/projekti.php?projektikoodi=S100'
    laskuri_address = address + str(n)
#    print 'Osoite: ', laskuri_address, 'ja n: ', n 
    html = scraperwiki.scrape(laskuri_address)
    soup = BeautifulSoup(html)
    n = n + 1
    tds = soup.findAll('p')

#        table_cells = row.findAll("td")

    print laskuri_address

for td in tds:
#    print td
    record = { "td" : td.text }

    record['Name'] = table_cells[0].text
    record['Town'] = table_cells[1].text
    record['Country'] = table_cells[2].text
    scraperwiki.sqlite.save(["td"], record)

print "Onnistui :)"
    