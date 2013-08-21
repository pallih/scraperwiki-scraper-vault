import scraperwiki
import lxml.html           

def scrape(page):
    html = scraperwiki.scrape("http://srx.com.sg/srx/searchListings/search.srx?propertyType=0&keywords=&location=0&maxPrice=&minSize=&Search+=Search&completed=0&tenure=0&minAge=0&maxAge=0&type=S&showAdvanceOption=N&maxSize=&minPrice=&fullSearch=false&itemsPerPage=100&page=" + str(page))

    root = lxml.html.fromstring(html)

    for div in root.cssselect(".listingData"):
        url = "http://srx.com.sg" + div.cssselect(".listingHeader a")[0].attrib['href']
        temp = div.cssselect("span.textHighlightYellow")
        temp2 = div.cssselect(".fieldLabelHighlight")
        coordinate = div.cssselect("img[src*='http://maps.googleapis.com/maps/api/staticmap?']")[0].attrib['src'].split('|')[1].split('&')[0].split(',')
        
        data = {
            "address": temp[0].text_content(),
            "house_type": temp[1].text_content(),
            "asking_price": int(temp2[0].text_content().replace("$","").replace(",","").replace("K","000")) if not temp2[0].text_content() == "CALL" else -1,
            "psf": int(temp2[1].text_content().replace("($","").replace(",","").replace(" psf)","")) if len(temp2) == 2 else -1,
            "lat": float(coordinate[0]),
            "lon": float(coordinate[1]),
            "floor": div.cssselect(".remarksTextHolder")[0].text_content() if div.cssselect(".remarksTextHolder") else "",
            "url": url
        }
    
        scraperwiki.sqlite.save(unique_keys=["url"], data=data, table_name="srx_sale")

for page in range(0,10):
    scrape(page)
    print "page %d complete" % page
