import scraperwiki
from bs4 import BeautifulSoup

scraperwiki.sqlite.attach("fsa_commodities_operations_pcas")

urls = scraperwiki.sqlite.select("* from fsa_commodities_operations_pcas.swdata")
#print urls

for url in urls:
    html = scraperwiki.scrape(url["URL"])
    soup = BeautifulSoup(html)
    content = soup.get_text()
    data = {"URL": url["URL"], "Year": url["Year"], "Content": content}
    #print data
    scraperwiki.sqlite.save(["URL"], data)