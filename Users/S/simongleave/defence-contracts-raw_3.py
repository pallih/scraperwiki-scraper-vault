# import libraries for saving to data store and interpreting the source code for the webpage

import scraperwiki
from bs4 import BeautifulSoup

# identify rootpage from where the data will be scraped

search_page = "http://www.contractsfinder.businesslink.gov.uk/Search%20Contracts/Search%20Contracts%20Results.aspx?site=1000&lang=en&sc=3fc5e794-0cb4-4c10-be10-557f169c4c92&osc=db8f6f68-72d4-4204-8efb-57ceb4df1372&rb=1&ctlPageSize_pagesize=200&ctlPaging_page="

# assign variable and use BeautifulSoup library to make sense of it

html = scraperwiki.scrape(search_page + "1")
soup = BeautifulSoup(html)

# assign variable and use BeautifulSoup library to discover the number of results. get_text strips the tags off

max = soup.find(id="resultsfound").get_text()
num = int(max.split(" ")[2])

# Let's calculate the number of the last page

if num % 200 != 0:
    last_page = (num/200) + 1
else:
    last_page = num/200
# Always print after each step to check that the code works. ie print last_page

# Counting through the different pages and identifying the pages we want. Then the elements

for n in range(1, last_page + 1):
    html = scraperwiki.scrape(search_page + str(n))

    soup = BeautifulSoup(html)

    links = soup.find_all("a", "notice-title")

# Counter is set up in order to identify the objects on each page as well as the page itself
    
    counter = (n-1)*200 + 1

    for link in links:
        url = link ["href"]
        data = {"URL": url, "id": counter}
        scraperwiki.sqlite.save(["URL"], data)
        counter+=1 