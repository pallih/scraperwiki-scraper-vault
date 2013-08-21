import scraperwiki
from BeautifulSoup import BeautifulSoup

n = 0
urlia = 'S1000'
# Säätele mitkä fileet
while n < 5:
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

    kalaa = soup.find("div", { "class" : "description" })
    print kalaa

   divs = kalaa.findAll('p')
##    tds = soup.findAll('h3') 

##        table_cells = row.findAll("td")


   for div in divs:
##        print td.txt
#        k = k + 1
##        print "urlia: ", n, " - n: ", k
        record = {}
        record['Name'] = div[1].text
#        kalkkua = { "kalaa" : kalaa.txt }
        scraperwiki.sqlite.save(["kalaa"], kalkkua)

print "Onnistui :)"