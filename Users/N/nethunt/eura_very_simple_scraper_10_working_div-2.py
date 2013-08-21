import scraperwiki
from BeautifulSoup import BeautifulSoup

n = 0
urlia = 'S1000'
# Säätele mitkä fileet
while n < 10:
    k = 0
    if n < 10:
        urlia = 'S1000'
    if 9 < n < 100:
        urlia = 'S100'
    if 99 < n < 1000:
        urlia = 'S10'
    address='https://www.eura2007.fi/rrtiepa/projekti.php?projektikoodi='
    laskuri_address = address + urlia + str(n)
#    print 'Osoite: ', laskuri_address, 'ja n: ', n 
    html = scraperwiki.scrape(laskuri_address)
    soup = BeautifulSoup(html)
    n = n + 1

    row = soup.find("div", { "class" : "description" })
    tds = row.findAll("p")

#        table_cells = row.findAll("td")

    print data_table

    for td in tds:
        print td.txt
        k = k + 1
#        print "urlia: ", n, " - n: ", k
#        kalaa = { "td" : td.text }
#        scraperwiki.sqlite.save(["td"], kalaa)

print "Onnistui :)"