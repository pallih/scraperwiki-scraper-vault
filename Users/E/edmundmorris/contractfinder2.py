import scraperwiki
from bs4 import BeautifulSoup # documentation at http://www.crummy.com/software/BeautifulSoup/bs4/doc/

# Searching for "Department for International Development" on contracts finder excluding tenders, 177 results so made pagesize 200
search_page = "https://online.contractsfinder.businesslink.gov.uk/Search%20Contracts/Search%20Contracts%20Results.aspx?site=1000&lang=en&sc=486c568c-0405-4e67-a47d-6e2ddade541c&osc=0b164baa-8701-4c1d-b6d9-e03cd9b162d7&rb=1&ctlPageSize_pagesize=200&ctlPaging_page=2"

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
    import scraperwiki
from bs4 import BeautifulSoup # documentation at http://www.crummy.com/software/BeautifulSoup/bs4/doc/

# Searching for "Department for International Development" on contracts finder excluding tenders, 177 results so made pagesize 200
search_page = "https://online.contractsfinder.businesslink.gov.uk/Search%20Contracts/Search%20Contracts%20Results.aspx?site=1000&lang=en&sc=486c568c-0405-4e67-a47d-6e2ddade541c&osc=0b164baa-8701-4c1d-b6d9-e03cd9b162d7&rb=1&ctlPageSize_pagesize=200&ctlPaging_page=2"

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
    