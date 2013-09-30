import scraperwiki
import urllib
import urllib2,sys
from bs4 import BeautifulSoup as Soup
import re

# werkwijze: open een pagina, haal de inhoud op, geef aan welke data je wilt hebben, sla die op, ga naar de volgende pagina 
  
#samenstellen van de url die uit 3 elementen bestaat: vaste base_url, een oplopende id en een vaste uitgang

base_url = "http://evenementen.uitslagen.nl/2013/marathonrotterdam/details.php?s="
end_url = "&o=1&t=nl"

for num in range(1, 3):
    html = base_url+str(num)
    url = html+end_url #dit koppelt de drie elementen van de url aan elkaar
    soup = Soup(urllib.urlopen(url)) #open de pagina


    # onderstaand blokje is uit ammar: blok ruwe data/tags in één veld
    #for url in urls:
    #print "Scraping", url
    #page = scraperwiki.scrape(url)
    #if page is not None:    
    #naam = re.findall("Naam(.*?)</table>", page, re.DOTALL)        
    #data = {'Naam': naam}  
    #scraperwiki.sqlite.save(['Naam'], data) 


    # alle losse cellen in aparte velden, maar wel drie keer de tabel 
    #table = soup.find("table")
    #for row in table.findAll("tr"):
     #   for cell in row.findAll("td"):
      #      print cell.findAll(text=True)

    # best so far: alle data min of meer opgeschoond in één cel
    
    startnr = soup.find("td", "k").get_text().replace("Startnummer", "") #table data K startnummer ophalen en het woord startnummer weglaten
    info = soup.find("table").get_text().replace("Persoonlijke video+foto", "").replace("Deel je uitslag", "").replace("Naam", "Naam: ") #.strip() # de hele tabel ophalen
    

    data = {"NR":num, "BIB":startnr, "Gegeves":info} #definieren wat ik wil opslaan in de database
    scraperwiki.sqlite.save(["NR"], data) #opslaan in de database

    
    
  

    #print soup

    #info = soup.find_all("table") #kijken hoe de scraper de tabel ziet
    #print info

    #for info in soup.find_all("table"):
        



     # print link.get('title').encode("utf-8")," :: ", # deze heb ik niet gebruikt 
     # print "%s%s.rss" % (base_url, link.get('href') ) # deze heb ik niet gebruikt


#scraperwiki.scrape(url)

#print "STARTNR", num # testen of het crawlen van nums via for range werkt


    #soup = Soup(urllib.urlopen(url))
    
   # for link in soup.find_all(attrs={'class': 'knav_link'}): #niet gebruikt
 #       print link.get('title').encode("utf-8")," :: ", #niet gebruikt
  #      print "%s%s.rss" % (base_url, link.get('href') ) # niet gebruikt








#html =  "%s%d" % (base_url, page) link creeren met vaste basurl plus range-id, dus 2 elementen
 #   soup = Soup(urllib.urlopen(url))
import scraperwiki
import urllib
import urllib2,sys
from bs4 import BeautifulSoup as Soup
import re

# werkwijze: open een pagina, haal de inhoud op, geef aan welke data je wilt hebben, sla die op, ga naar de volgende pagina 
  
#samenstellen van de url die uit 3 elementen bestaat: vaste base_url, een oplopende id en een vaste uitgang

base_url = "http://evenementen.uitslagen.nl/2013/marathonrotterdam/details.php?s="
end_url = "&o=1&t=nl"

for num in range(1, 3):
    html = base_url+str(num)
    url = html+end_url #dit koppelt de drie elementen van de url aan elkaar
    soup = Soup(urllib.urlopen(url)) #open de pagina


    # onderstaand blokje is uit ammar: blok ruwe data/tags in één veld
    #for url in urls:
    #print "Scraping", url
    #page = scraperwiki.scrape(url)
    #if page is not None:    
    #naam = re.findall("Naam(.*?)</table>", page, re.DOTALL)        
    #data = {'Naam': naam}  
    #scraperwiki.sqlite.save(['Naam'], data) 


    # alle losse cellen in aparte velden, maar wel drie keer de tabel 
    #table = soup.find("table")
    #for row in table.findAll("tr"):
     #   for cell in row.findAll("td"):
      #      print cell.findAll(text=True)

    # best so far: alle data min of meer opgeschoond in één cel
    
    startnr = soup.find("td", "k").get_text().replace("Startnummer", "") #table data K startnummer ophalen en het woord startnummer weglaten
    info = soup.find("table").get_text().replace("Persoonlijke video+foto", "").replace("Deel je uitslag", "").replace("Naam", "Naam: ") #.strip() # de hele tabel ophalen
    

    data = {"NR":num, "BIB":startnr, "Gegeves":info} #definieren wat ik wil opslaan in de database
    scraperwiki.sqlite.save(["NR"], data) #opslaan in de database

    
    
  

    #print soup

    #info = soup.find_all("table") #kijken hoe de scraper de tabel ziet
    #print info

    #for info in soup.find_all("table"):
        



     # print link.get('title').encode("utf-8")," :: ", # deze heb ik niet gebruikt 
     # print "%s%s.rss" % (base_url, link.get('href') ) # deze heb ik niet gebruikt


#scraperwiki.scrape(url)

#print "STARTNR", num # testen of het crawlen van nums via for range werkt


    #soup = Soup(urllib.urlopen(url))
    
   # for link in soup.find_all(attrs={'class': 'knav_link'}): #niet gebruikt
 #       print link.get('title').encode("utf-8")," :: ", #niet gebruikt
  #      print "%s%s.rss" % (base_url, link.get('href') ) # niet gebruikt








#html =  "%s%d" % (base_url, page) link creeren met vaste basurl plus range-id, dus 2 elementen
 #   soup = Soup(urllib.urlopen(url))
