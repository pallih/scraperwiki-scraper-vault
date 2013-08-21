import scraperwiki
from bs4 import BeautifulSoup

scraperwiki.sqlite.attach("fsa_commodities_operations_bulk_shipments")

urls = scraperwiki.sqlite.select("URL from fsa_commodities_operations_bulk_shipments.swdata")

for url in urls:
    html = scraperwiki.scrape(url["URL"])
    soup = BeautifulSoup(html)
    content = soup.get_text()
    data = {"URL": url["URL"], "Content": content}
    scraperwiki.sqlite.save(["URL"], data)

