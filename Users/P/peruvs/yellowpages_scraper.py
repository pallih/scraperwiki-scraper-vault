import scraperwiki
import lxml.html

items = [
    "http://www.yellowpages.com/indianapolis-in/doctors?g=Indianapolis%2C+IN&q=Doctors"
]

def store_data(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    for div in root.cssselect("div.ypgListing"):
        address = div.cssselect("div.listing-content div.info div.listing-address adr")
        if address:
            address = address[0].text
        else:
            address = ""
    
        website = div.cssselect("div.listing-content ul.features li.website-feature a")
        if website:
            website = website[0].attrib['href'][7:]
        else:
            website = ""
    
        categories = []
        for cat in div.cssselect("div.ypgExtra span.ypgCategoryLink"):
            text = cat.text_content()
            if text and text != "Category:":
                categories.append(text)
        phone = div.cssselect("div.listingDetail h4.phoneLink div")[0].text
        if phone:
            data = {
                "phone": phone,
                "name": div.cssselect("div.listingDetail h3 a span")[0].text,
                "address": address,
                "website": website,
                "categories": categories,
            }
            scraperwiki.sqlite.save(unique_keys=['phone'], data=data)


for item in items:
    store_data(item)