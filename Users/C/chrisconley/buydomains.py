import scraperwiki
from BeautifulSoup import BeautifulSoup

baseUrl = 'http://www.buydomains.com/find-premium-domains/search-results.jsp?searchType=advanced&keyword_s=contains&require_price=Y&exclude_hyphens=Y&exclude_numbers=Y&p=.org+.com+.net&pageSize=10000&pageNum='

for pageNum in range(165):
    print pageNum
    html = scraperwiki.scrape(baseUrl + str(pageNum+1))

    soup = BeautifulSoup(html) # turn our HTML into a BeautifulSoup object
    tbody = soup.find(id="searchResultsBody") # get all the <td> tags
    trs = tbody.findAll('tr')
    for tr in trs:
        tds = tr.findAll('td')
        record = {"name" : tds[1].text, "price" : tds[3].text }
        scraperwiki.datastore.save(["name", "price"], record)


