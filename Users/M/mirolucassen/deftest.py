import scraperwiki
from bs4 import BeautifulSoup

#string
search_page = "http://www.contractsfinder.businesslink.gov.uk/Search%20Contracts/Search%20Contracts%20Results.aspx?site=1000&lang=en&sc=3fc5e794-0cb4-4c10-be10-557f169c4c92&osc=db8f6f68-72d4-4204-8efb-57ceb4df1372&rb=1&ctlPageSize_pagesize=200&ctlPaging_page="

html = scraperwiki.scrape(search_page + "1")
soup = BeautifulSoup(html)
#print soup maakt zooitje data

#pak het aantal resultaten uit de div met de resultaten
#maak er een lijst van en en dan een integer (getal) op basis van positie in de lijst
max = soup.find(id="resultsfound").get_text()
num = int(max.split(" ")[2])

#print num

#bereken laatste pagina
if num % 200 !=0:
    last_page = (num/200) + 1
else:
    last_page = num/200
#print last_page

for n in range(1, last_page + 1):
    html = scraperwiki.scrape(search_page + str(n))
#let op aantal pagina's als string want zoekstring is ook een string)

    soup = BeautifulSoup(html)

    links = soup.find_all("a", "notice-title")
    #print links #maakt een lijst met de elementen inclusief een url
    
    counter = (n-1)*200 + 1

    for link in links:
        url = link["href"]
        #print url
        data = {"URL": url, "id": counter} #om een unieke id te maken per record
        scraperwiki.sqlite.save(["URL"], data)
        counter+=1 #telt de counter op