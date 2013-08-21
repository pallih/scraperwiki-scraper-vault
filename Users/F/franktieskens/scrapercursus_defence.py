import scraperwiki
from bs4 import BeautifulSoup

zoekpagina = 'http://www.contractsfinder.businesslink.gov.uk/Search%20Contracts/Search%20Contracts%20Results.aspx?site=1000&lang=en&sc=3fc5e794-0cb4-4c10-be10-557f169c4c92&osc=db8f6f68-72d4-4204-8efb-57ceb4df1372&rb=1&ctlPageSize_pagesize=200&ctlPaging_page='

html = scraperwiki.scrape(zoekpagina + "1")
soup = BeautifulSoup(html)
# De BeautifulSoup maakt structuur van de meuk

max = soup.find(id="resultsfound").get_text()
num =int(max.split(" ")[2])


if num %200 != 0:
    laatste = (num/200) + 1
else:
    laatste = num/200
# Denk eraan als je met hele getallen rekent, hij geeft altijd gehele getallen, afgerond naar beneden
print laatste

#Maak een string van 'n'!!!!

for n in range(1,laatste+1):
    htmlnu = scraperwiki.scrape(zoekpagina + str(n)) 
    soup = BeautifulSoup(htmlnu)
    
    links = soup.find_all("a","notice-title")
    #print links
    telraam = (n-1)*200 + 1
    for link in links:
        url = link["href"]
        data  = {"URL"; url, "id": telraam}
        scraperwiki.sqlite.save(["URL"], data)
        telraam+=1
    


# Standaard voor find_all is div, class  (bovenin heb je dus een id in met je resultsfound)