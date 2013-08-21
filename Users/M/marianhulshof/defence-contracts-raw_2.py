import scraperwiki
from bs4 import BeautifulSoup 

search_page = "http://www.contractsfinder.businesslink.gov.uk/Search%20Contracts/Search%20Contracts%20Results.aspx?site=1000&lang=en&sc=3fc5e794-0cb4-4c10-be10-557f169c4c92&osc=db8f6f68-72d4-4204-8efb-57ceb4df1372&rb=1&ctlPageSize_pagesize=200&ctlPaging_page="

html = scraperwiki.scrape(search_page + '1')
soup = BeautifulSoup(html)
#print soup 

max = soup.find(id='resultsfound').get_text()
num = int(max.split(" ")[2])
#print num

if num % 200 !=0:
    last_page = (num/200) + 1

else:
    last_pagenum/200
#print last_page
for n in range(1, last_page + 1):
    html = scraperwiki.scrape (search_page + str(n))

    soup = BeautifulSoup(html)

    links = soup.find_all("a", "notice-title")
    #print links

    counter = (n-1)*200 + 1

    for link in links:
        url = link["href"]
        #print url
        data = {"URL": url, "id": counter}#om een unieke id te maken per record
        scraperwiki.sqlite.save (["URL"], data)
        counter+=1


