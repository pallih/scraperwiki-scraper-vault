import scraperwiki
import urlparse
import lxml.html
import lxml.etree
import re


# ---------------------------------------------------------------------------
# Parse single pages
# ---------------------------------------------------------------------------
def scrape_single_page(url):

    global counter
    counter += 1

    global recordsList

    print "Load";

    html = scraperwiki.scrape(url)
    #print html
    root = lxml.html.fromstring(html)

    # Get title
    # ------------------------------------------------
    titles = root.cssselect("p[class='title']")
    for title in titles:
        #print lxml.html.tostring(title)     
        print title.text
        carTitle = title.text

    # Get price
    # ------------------------------------------------
    prices = root.cssselect("p[class='price']") 
    for price in prices:
        #print lxml.html.tostring(price)     
        #print price.text
        carPrice = price.text

    # Get id
    # ------------------------------------------------
    ids = root.cssselect("a[title='Se lignende annonser']") 
    for id in ids:
        #print lxml.html.tostring(id)     
        #print id.text
        carId = id.text

    # Get modified time
    # ------------------------------------------------
    updates = root.cssselect("span[class='modified']") 
    for update in updates:
        #print lxml.html.tostring(update)     
        #print update.text
        carUpdated = update.text

    # Get meta info
    # ------------------------------------------------
    metas = root.cssselect("div[id='view-r'] tr")
    carMeta = {}
    for meta in metas:

        row = meta.cssselect("td")
        #print row[0].text
        #print row[1].text
        carMeta[row[0].text] = row[1].text
        #print carMeta

    # Get options
    # ------------------------------------------------
    options = root.cssselect("td[class='options']") 
    carOptions = []
    for option in options:

        #print option.text
        carOptions.append(option.text)

    # Get images
    # ------------------------------------------------
    images = root.cssselect("div[id='view-big-images'] img") 
    carImages = []
    for image in images:

        imageUrl = urlparse.urljoin(base_url, image.attrib.get('src'))
        #print imageUrl
        carImages.append(imageUrl)

    # Get meta description
    # ------------------------------------------------
    metas = root.cssselect("meta[property='og:description']") 
    for meta in metas:

        #print "DESCRIPTION: " + meta.attrib.get('content')
        carDescription = meta.attrib.get('content')



    record = {}
    if titles: 
        record['car'] = carTitle
        record['price'] = carPrice
        record['idNumber'] = carId
        record['updated'] = carUpdated
        record['meta'] = carMeta
        record['options'] = carOptions
        record['images'] = carImages
        record['about'] = carDescription

        # Print out the data we've gathered
        #print record, '------------'
        recordsList.append(record)
    
    if counter >= 10:
        # Finally, save the record to the datastore - 'Artist' is our unique key
        scraperwiki.sqlite.save(["car"], recordsList)
        counter = 0
        del recordsList[:]
        print "Saved"



# ---------------------------------------------------------------------------
# Scraping main searc page
# ---------------------------------------------------------------------------
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    #print html
    root = lxml.html.fromstring(html)
    items = root.cssselect("div[class='iteminfo']") # Get all "items"

    for item in items:
        links = item.cssselect("a")
        for link in links:
            url = urlparse.urljoin(base_url, link.attrib.get('href'))
            #print url
            scrape_single_page(url)


# ---------------------------------------------------------------------------
# START HERE
# ---------------------------------------------------------------------------

scraperwiki.sqlite.execute("drop table if exists swdata")

base_url = 'http://bil.autodb.no/'
#starting_url = urlparse.urljoin(base_url, 'http://bil.autodb.no/autodb/search.wa2?County2_Split=%3A10009%3A10010%3A10002%3A10006%3A10020%3A10004%3A10012%3A10015%3A10018%3A10005%3A10003%3A10011%3A10014%3A10008%3A10019%3A10017%3A10016%3A10007%3A10001;Limit=20000;ListOrder=amsAdItems.PayTime%20DESC;Offset=0;Status=Active;Type=hmaAuto;_cmd=results')

starting_url = urlparse.urljoin(base_url, 'http://bil.autodb.no/autodb/search.wa2?Limit=2000&ListOrder=amsAdItems.PayTime%20ASC&Status=Active&Type=hmaAuto&_cmd=results&xBrand_Multiple=0')

global counter
counter = 0

global recordsList
recordsList = []

scrape_and_look_for_next_link(starting_url)



#1251028 - AC Cobra (1)
#1101087 - Aixam (1)
#1235050 - Alfa Romeo (51)
#1254034 - American Motors (4)
#1100020 - Audi (965)
#1100023 - Austin (5)
#1100032 - Bedford (1)
#1234765 - Bentley (2)
#1100044 - BMW (1299)
#1737277 - Buddy (1)
#1100056 - Buick (25)
#1100067 - Cadillac (45)
#1572300 - Caterham (1)
#1100082 - Chevrolet (440)
#1100087 - Chrysler (96)
#1100099 - Citroen (206)
#1100113 - Daewoo (5)
#1100118 - Daihatsu (18)
#1240910 - Datsun (6)
#1237267 - De Soto (1)
#1247596 - De Tomaso (1)
#1304330 - DKW (1)
#1100133 - Dodge (77)
#1100149 - Ferrari (1)
#1100152 - Fiat (94)
#1100168 - Ford (1034)
#1101099 - Galloper (6)
#1100561 - GMC (18)
#1501374 - Gokart (1)
#1246308 - Hillman (1)
#1100197 - Honda (223)
#1100602 - Hummer (4)
#1100205 - Hyundai (184)
#1572391 - International (4)
#1100217 - Isuzu (13)
#1100730 - Iveco (9)
#1100223 - Jaguar (33)
#1100229 - Jeep (81)
#1100722 - Jensen (1)
#1100247 - KIA (94)
#1100601 - Lamborghini (2)
#1100265 - Lancia (6)
#1234994 - Land Rover (83)
#1100271 - Lexus (14)
#1100579 - Lincoln (20)
#1234958 - Lotus (5)
#1100281 - Maserati (1)
#1100288 - Mazda (240)
#1234816 - Mercedes-Benz (1132)
#1100570 - Mercury (12)
#1100302 - MG (12)
#1100760 - Mini (50)
#1100307 - Mitsubishi (359)
#1285316 - Mopedbil (1)
#1234763 - Morris (2)
#1100338 - Nissan (438)
#1100345 - Oldsmobile (17)
#1100349 - Opel (686)
#1239107 - Packard (1)
#1100361 - Peugeot (416)
#1100370 - Plymouth (19)
#1100379 - Pontiac (54)
#1100382 - Porsche (75)
#1281539 - Range Rover (1)
#1100398 - Renault (177)
#1234999 - Rolls Royce (4)
#1100404 - Rover (14)
#1100450 - Saab (130)
#1100633 - Scania (2)
#1100414 - Seat (24)
#1100426 - Skoda (136)
#1100750 - Smart (13)
#1232171 - SsangYong (47)
#1251419 - Studebaker (2)
#1100434 - Subaru (139)
#1100442 - Suzuki (163)
#1705241 - Tesla (2)
#1100467 - Toyota (755)
#1100477 - Triumph (7)
#1274570 - Vauxhall (3)
#1285420 - Volga (1)
#1100503 - Volkswagen (1427)
#1100509 - Volvo (849)
#1254079 - Willys (3)
#1477747 - Wolseley (1)
#autocreated - Andre (41)
