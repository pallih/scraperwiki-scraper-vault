from scraperwiki import scrape, sqlite
from lxml import html

import re

SIZE_REGEX = re.compile("\s([0-9]+[GTP]B)\s")
PID_REGEX = re.compile(r"\?productId=([0-9]+)")

def main():
    print "Scraping"
    content = scrape("http://www.aria.co.uk/Products/Components/Solid+State+Drives/?p_productsPerPage=200")
    rows = html.fromstring(content).cssselect("table.listTable tr")
    
    for row in rows:
        cols = row.cssselect("td")
        if len(cols) != 6 : continue
        
        _, product, _, _, price, _ = cols
        
        p = price.cssselect("span.price.bold")
        if not p: continue
        price = p[0].text_content().lstrip(u"£")

        (product_link,) = product.cssselect("a")

        name = product_link.text_content()

        product_id = PID_REGEX.search(product_link.get("href"))
        if product_id:
            (product_id,) = product_id.groups()
            product_id = int(product_id)
        else:
            product_id = None

        size = SIZE_REGEX.search(name)
        if size:
            (size,) = size.groups()
        else:
            size = None

        sqlite.save(
            unique_keys=["product_id"],
            data=dict(
                product_id=product_id,
                price=price,
                size=size,
                name=name,
            ))

if __name__ in ("__main__", "scraper"):
    main()