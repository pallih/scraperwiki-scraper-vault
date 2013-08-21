import scraperwiki
import lxml.html 
from datetime import datetime

rundate = datetime.now().replace(microsecond=0)


def marktplaats_run():
    queries = [""]
    query = queries[0]

    def marktplaats_parse_page(html):
        ret = []
        root = lxml.html.fromstring(html)
        has_next_page = len(root.cssselect(".pagination-next")) > 0
        for tr in root.cssselect(".search-result:not(.bottom-listing)"):
            data = {"source":"marktplaats", "timestamp":rundate}
            data["title"] = tr.cssselect(".mp-listing-title.wrapped")[0].text_content()
            data["description"] = tr.cssselect(".mp-listing-description.wrapped")[0].text_content()
            data["price"] = tr.cssselect(".price")[0].text_content()
            data["link"] = tr.cssselect(".listing-title-description a")[0].get("href")
            data["thumblink"] = tr.cssselect(".thumb-placeholder.juiceless-link")[0].get("style").replace("background-image: url('","http:").replace("')","")
            ret.append(data)
        return(ret, has_next_page)
    
    for query in queries:
        page = 1
        while True:
            url = "http://www.marktplaats.nl/z/watersport-en-boten/kajuitzeilboten-en-zeiljachten/etap.html?query={0}&categoryId=985&searchOnTitleAndDescription=true&priceFrom=1.00&priceTo=20.000%2C00&startDateFrom=&currentPage={1}&numberOfResultsPerPage=50".format(query, page)
            html = scraperwiki.scrape(url)
            data, has_next_page = marktplaats_parse_page(html)
            for item in data:
                scraperwiki.sqlite.save(unique_keys=[], data=item, table_name="marktplaats")
            if len(data) <= 0 or not has_next_page:
                break
            page += 1

marktplaats_run()
