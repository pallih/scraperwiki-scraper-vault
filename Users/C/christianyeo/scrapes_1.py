import scraperwiki, sys
from bs4 import BeautifulSoup

search = 'http://www.contractsfinder.businesslink.gov.uk/Search%20Contracts/Search%20Contracts%20Results.aspx?site=1000&lang=en&sc=3fc5e794-0cb4-4c10-be10-557f169c4c92&osc=db8f6f68-72d4-4204-8efb-57ceb4df1372&rb=1&ctlPageSize_pagesize=200&ctlPaging_page='

for a in range(1,9):
    search_url = search + str(a)
    html = scraperwiki.scrape(search_url)
    soup = BeautifulSoup(html)
    #print soup

    links = soup.find_all('a', 'notice-title')
    #print linksß
    for link in links:
        url = link['href']
        #print url
        data = {"URL":url}
        scraperwiki.sqlite.save(["URL"], data)import scraperwiki, sys
from bs4 import BeautifulSoup

search = 'http://www.contractsfinder.businesslink.gov.uk/Search%20Contracts/Search%20Contracts%20Results.aspx?site=1000&lang=en&sc=3fc5e794-0cb4-4c10-be10-557f169c4c92&osc=db8f6f68-72d4-4204-8efb-57ceb4df1372&rb=1&ctlPageSize_pagesize=200&ctlPaging_page='

for a in range(1,9):
    search_url = search + str(a)
    html = scraperwiki.scrape(search_url)
    soup = BeautifulSoup(html)
    #print soup

    links = soup.find_all('a', 'notice-title')
    #print linksß
    for link in links:
        url = link['href']
        #print url
        data = {"URL":url}
        scraperwiki.sqlite.save(["URL"], data)