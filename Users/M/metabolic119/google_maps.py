import scraperwiki
import lxml.html



html = scraperwiki.scrape("http://www.interspar.at/c/subsidiaries/subsidiary")


root = lxml.html.fromstring(html)


for tr in root.cssselect("div.search-table table tr"):
    address = tr.cssselect("td address")
    
    if len(address) > 0:
        scraperwiki.sqlite.save(unique_keys=[], data={"address":address[0].text}, table_name="addresses")