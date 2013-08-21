import scraperwiki

from bs4 import BeautifulSoup # documentation at http://www.crummy.com/software/BeautifulSoup/bs4/doc/

# Searching for "*" on contracts finder, 14702 results so made pagesize 500
search_page = "https://online.contractsfinder.businesslink.gov.uk/Search%20Contracts/Search%20Contracts%20Results.aspx?site=1000&lang=en&sc=91f7adbc-35a1-4f5e-aed3-38d12097a511&osc=b05afb61-d473-4cf1-a53f-6bfe5bfa6bb0&rb=1&ctlPageSize_pagesize=500"

# Notice that of 10251 of the total are actually closed contracts, i.e. awarded.


# add &ctlPaging_page=2 per page, considering that there are about 30 pages.. scrape them all is going to be fast with a cycle


for i in range(8, 31):

    search_page = "https://online.contractsfinder.businesslink.gov.uk/Search%20Contracts/Search%20Contracts%20Results.aspx?site=1000&lang=en&sc=91f7adbc-35a1-4f5e-aed3-38d12097a511&osc=b05afb61-d473-4cf1-a53f-6bfe5bfa6bb0&rb=1&ctlPageSize_pagesize=500&ctlPaging_page=" + `i` + ""
    
    # Extract html
    html = scraperwiki.scrape(search_page)
    
    # Make it searchable by BeautifulSoup
    soup = BeautifulSoup(html)
    
    # Links to contracts have attribute "a" with class "notice-title" so pulling out all of those
    links = soup.find_all("a", "notice-title")
    
    # Getting the individual links and saving them into ScraperWiki database
    for link in links:
        url = link['href']
        data = {"URL": url}
        scraperwiki.sqlite.save(["URL"], data)
    

