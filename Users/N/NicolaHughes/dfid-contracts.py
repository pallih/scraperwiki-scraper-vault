import scraperwiki
from bs4 import BeautifulSoup # documentation at http://www.crummy.com/software/BeautifulSoup/bs4/doc/

# Searching for "Department for International Development" on contracts finder excluding tenders, 177 results so made pagesize 200
search_page = "http://www.contractsfinder.businesslink.gov.uk/Search%20Contracts/Search%20Contracts%20Results.aspx?site=1000&lang=en&sc=9d049372-a4c2-46af-bb24-2f7e132aa5ce&osc=db8f6f68-72d4-4204-8efb-57ceb4df1372&rb=1&ctlPageSize_pagesize=200"

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
search_page = "http://www.contractsfinder.businesslink.gov.uk/Search%20Contracts/Search%20Contracts%20Results.aspx?site=1000&lang=en&sc=9d049372-a4c2-46af-bb24-2f7e132aa5ce&osc=db8f6f68-72d4-4204-8efb-57ceb4df1372&rb=1&ctlPageSize_pagesize=200"

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
    