import scraperwiki
from bs4 import BeautifulSoup

zoekpagina = 'http://blog.prorail.nl/'

html = scraperwiki.scrape(zoekpagina)
soup = BeautifulSoup(html)
# De BeautifulSoup maakt structuur van de meuk

print soup


zoek = soup.find("div", { "class" : "percentage" }).get_text()
dag = soup.find("h4", { "class" : "widgettitle" }).get_text()+" 2013"
print zoek 
print dag

data = {"dag": dag, "telaat" : zoek}

print data

scraperwiki.sqlite.save(["dag"], data)
#if num %200 != 0:
 #   laatste = (num/200) + 1
#else:
 #   laatste = num/200
# Denk eraan als je met hele getallen rekent, hij geeft altijd gehele getallen, afgerond naar beneden
#print laatste

#Maak een string van 'n'!!!!

#for n in range(1,laatste+1):
 #   htmlnu = scraperwiki.scrape(zoekpagina + str(n)) 
  #  soup = BeautifulSoup(htmlnu)
    
   # links = soup.find_all("a","notice-title")
    #print links
    #telraam = (n-1)*200 + 1
    #for link in links:
     #   url = link["href"]
      #  data  = {"URL"; url, "id": telraam}
       # scraperwiki.sqlite.save(["URL"], data)
        #telraam+=1
    


# Standaard voor find_all is div, class  (bovenin heb je dus een id in met je resultsfound)