import scraperwiki
import urllib2

#f = open("currencies", "w")
page = urllib2.urlopen("http://www.ecb.eu/stats/exchange/eurofxref/html/index.en.html")

from BeautifulSoup import BeautifulSoup
#dit is de hele pagina in de html soup
soup = BeautifulSoup(page)
#zoeken in html soup
rate = soup.findAll(attrs={"class":"rate"})
cur = soup.findAll(attrs={"class":"alignLeft"})
#print de resulaten van het zoeken
#print rate
#print cur
#print een alzonderlijke  rij waarden
#print rate[0]
#print cur[0]
#print alleen de inhoud van de gevonden vrij
#print rate[0].string
#print cur[0].string
#maak een loop voor alle landen, totaal 33

for num in range (0,34):
    #print num
    #print rate[num].string
    #print cur[num].string
# maak van de gevonden waarden data
    waarde = rate[num].string
    land = cur[num].string
    data ={"waarde":waarde,"land":land}
    #print data  
#bewaar de data in een database
    scraperwiki.sqlite.save(["waarde"], data)
    #f.write(waarde + "," + land)
    #f.close()
