import scraperwiki
from bs4 import BeautifulSoup

zoekpagina = 'https://www.rijksictdashboard.nl/projecten/0/total/all/all'

html = scraperwiki.scrape(zoekpagina)
soup = BeautifulSoup(html)
# De BeautifulSoup maakt structuur van de meuk


tabel = soup.find("table", { "class" : "investment-list sticky-enabled" })
print tabel
ding = tabel.find_all("a")
print ding
gstring = str(ding)
fstring = gstring.split('"')
lang = len(fstring)/2
print lang
for n in range(1,lang+1):
    link = fstring[(n*2)-1]
    data  = {"URL": link, "id": n}
    scraperwiki.sqlite.save(["URL"], data)

#num =int(max.split(" ")[2])


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
    


# Standaard voor find_all is div, class  (bovenin heb je dus een id in met je resultsfound)import scraperwiki
from bs4 import BeautifulSoup

zoekpagina = 'https://www.rijksictdashboard.nl/projecten/0/total/all/all'

html = scraperwiki.scrape(zoekpagina)
soup = BeautifulSoup(html)
# De BeautifulSoup maakt structuur van de meuk


tabel = soup.find("table", { "class" : "investment-list sticky-enabled" })
print tabel
ding = tabel.find_all("a")
print ding
gstring = str(ding)
fstring = gstring.split('"')
lang = len(fstring)/2
print lang
for n in range(1,lang+1):
    link = fstring[(n*2)-1]
    data  = {"URL": link, "id": n}
    scraperwiki.sqlite.save(["URL"], data)

#num =int(max.split(" ")[2])


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