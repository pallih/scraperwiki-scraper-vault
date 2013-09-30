import scraperwiki
from bs4 import BeautifulSoup # documentation at http://www.crummy.com/software/BeautifulSoup/bs4/doc/

#URL-commonpart of pages with search results within a particular website to scrape (in this case with 200 results per page)
search_page ="http://www.contractsfinder.businesslink.gov.uk/Search%20Contracts/Search%20Contracts%20Results.aspx?site=1000&lang=en&sc=3fc5e794-0cb4-4c10-be10-557f169c4c92&osc=db8f6f68-72d4-4204-8efb-57ceb4df1372&rb=1&ctlPageSize_pagesize=200&ctlPaging_page="

# We need to know how many result pages we have to scrape i.e. when to stop scraping. The number of results is on the first page
# BeautifulSoup allows the programme to read html elements rather than seeing it as raw text
# full URL of first searchpage
html = scraperwiki.scrape(search_page + "1")
# interpret html source code of this page
soup = BeautifulSoup(html)

# We isolate the html element containing the number of results
# find the html element of your choice by its id, only gives the first one
max = soup.find(id="resultsfound").get_text() #only extract the text of the element
#split the text into a list and extract the number of results found
num = int(max.split(" ")[2])
# OR:
#max = soup.find(id="resultsfound")
#num = int(max.get_text().strip().split(" ")[2])
#print num

#calculate the number of the last results page to know where to stop scraping (200 results per page)
if num % 200 != 0:
    last_page = int(num/200) + 1
else:
    last_page = int(num/200)
#print last_page

# Paginate over pages up to last results page
for n in range(1, last_page + 1):
    # generate full html of the results page
    html = scraperwiki.scrape(search_page + str(n))
# interpret html to make it searchable
    soup = BeautifulSoup(html)
# on the search results page find the URLs of each of the results, search for '<a' tag and class 'notice-title' (first argument always tag, second always class; or overrule with explicit argument statements, see above id= ...)
    links = soup.find_all("a", "notice-title")
    #Adding ids to each row of results
    counter = (n-1)*200 + 1
#print links
   
#extract the individual URLs of each of the search results and save them into ScraperWiki database
    for link in links:
        url = link["href"]
#        print url
        data = {"URL": url, "id": counter}
#save into the data store, giving the unique parameter
        scraperwiki.sqlite.save(["URL"],data)
        counter+=1
#first save source code of all the pages and then digest (keep all source code as original data proof in case the site is changed)


import scraperwiki
from bs4 import BeautifulSoup # documentation at http://www.crummy.com/software/BeautifulSoup/bs4/doc/

#URL-commonpart of pages with search results within a particular website to scrape (in this case with 200 results per page)
search_page ="http://www.contractsfinder.businesslink.gov.uk/Search%20Contracts/Search%20Contracts%20Results.aspx?site=1000&lang=en&sc=3fc5e794-0cb4-4c10-be10-557f169c4c92&osc=db8f6f68-72d4-4204-8efb-57ceb4df1372&rb=1&ctlPageSize_pagesize=200&ctlPaging_page="

# We need to know how many result pages we have to scrape i.e. when to stop scraping. The number of results is on the first page
# BeautifulSoup allows the programme to read html elements rather than seeing it as raw text
# full URL of first searchpage
html = scraperwiki.scrape(search_page + "1")
# interpret html source code of this page
soup = BeautifulSoup(html)

# We isolate the html element containing the number of results
# find the html element of your choice by its id, only gives the first one
max = soup.find(id="resultsfound").get_text() #only extract the text of the element
#split the text into a list and extract the number of results found
num = int(max.split(" ")[2])
# OR:
#max = soup.find(id="resultsfound")
#num = int(max.get_text().strip().split(" ")[2])
#print num

#calculate the number of the last results page to know where to stop scraping (200 results per page)
if num % 200 != 0:
    last_page = int(num/200) + 1
else:
    last_page = int(num/200)
#print last_page

# Paginate over pages up to last results page
for n in range(1, last_page + 1):
    # generate full html of the results page
    html = scraperwiki.scrape(search_page + str(n))
# interpret html to make it searchable
    soup = BeautifulSoup(html)
# on the search results page find the URLs of each of the results, search for '<a' tag and class 'notice-title' (first argument always tag, second always class; or overrule with explicit argument statements, see above id= ...)
    links = soup.find_all("a", "notice-title")
    #Adding ids to each row of results
    counter = (n-1)*200 + 1
#print links
   
#extract the individual URLs of each of the search results and save them into ScraperWiki database
    for link in links:
        url = link["href"]
#        print url
        data = {"URL": url, "id": counter}
#save into the data store, giving the unique parameter
        scraperwiki.sqlite.save(["URL"],data)
        counter+=1
#first save source code of all the pages and then digest (keep all source code as original data proof in case the site is changed)


