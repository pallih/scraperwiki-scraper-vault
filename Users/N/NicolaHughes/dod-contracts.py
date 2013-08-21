import scraperwiki
from bs4 import BeautifulSoup # documentation at http://www.crummy.com/software/BeautifulSoup/bs4/doc/


# Searching for "Minsitry of Defence" on contracts finder excluding tenders fewing 200 results per page
search_page = "http://www.contractsfinder.businesslink.gov.uk/Search%20Contracts/Search%20Contracts%20Results.aspx?site=1000&lang=en&sc=3fc5e794-0cb4-4c10-be10-557f169c4c92&osc=db8f6f68-72d4-4204-8efb-57ceb4df1372&rb=1&ctlPageSize_pagesize=200&ctlPaging_page="

# We need to know how many result pages we have to scrape i.e. when to stop scraping. The number of results is on the first page
# BeautifulSoup allows the programme to read html elements rather than seeing it as raw text
html = scraperwiki.scrape(search_page + "1")
soup = BeautifulSoup(html)

# Finding the number of results
# We isolate the html element containing the number of results
max = soup.find(id="resultsfound")
num = int(max.get_text().strip().split(" ")[2])
#print num

# Calculating the last page number when we have asked for 200 results per page
if num % 200 != 0:
    last_page = int(num/200) + 1
else:
    last_page = int(num/200)
#print last_page

# Paginate over pages up to last page
for n in range(1,last_page + 1):
    # Extract html
    html = scraperwiki.scrape(search_page + str(n))

    # Make it searchable by BeautifulSoup
    soup = BeautifulSoup(html)
    

    # Links to contracts have attribute "a" with class "notice-title" so pulling out all of those
    links = soup.find_all("a", "notice-title")

    #Adding ids to each row
    counter = (n -1 ) * 200 + 1

    # Getting the individual links and saving them into ScraperWiki database
    for link in links:
        url = link['href']
        data = {"URL": url, "id": counter}
        scraperwiki.sqlite.save(["URL"], data)
        # Increment the counter
        counter += 1
    