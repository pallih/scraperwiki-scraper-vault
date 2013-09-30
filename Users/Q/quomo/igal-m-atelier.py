import scraperwiki
import mechanize
import lxml.html


def fetch_dom(startUrl, addPath):
    scrape = scraperwiki.scrape(startUrl + addPath)
    result = lxml.html.fromstring(scrape)
    return result

start_url = 'http://igalcalderpicassowarhol.com/'

scrape = scraperwiki.scrape(start_url)

dom = lxml.html.fromstring(scrape)

#1. get the main navigation links
nav_links = []

for el in dom.cssselect('div#nav-product ul li a'):
    one_link = el.attrib['href']
    nav_links.append(one_link)

print nav_links


#2. go through each section (nav destination, and start collecting each item there)

ourData = []

for curr_path in nav_links:
    page_dom = fetch_dom(start_url, curr_path)

    #2a, get category
    for el in page_dom.cssselect('title'):
        category = el.text

    #3. Go through each item and start gathering
    item_links = []
    for elem in page_dom.cssselect('div.name a'):
        item_link = elem.attrib['href']
        item_links.append(item_link)

    for curr_item in item_links:

        item_dom = fetch_dom(start_url, curr_item)
        
        #3a. get item ID
        for element0 in item_dom.cssselect('div.code em'):
            itemId = element0.text

        for element1 in item_dom.cssselect('div.itemFormName'):
            itemTitle = element1.text

        if item_dom.cssselect('div.price'):
            for element2 in item_dom.cssselect('div.price'):
                itemPrice = element2.text
        else:
            for element2 in item_dom.cssselect('div.price-bold'):
                itemPrice = element2.text

        if item_dom.cssselect('div.sale-price-bold'):
            for element2b in item_dom.cssselect('div.sale-price-bold em'):
                salePrice = element2b.text
        else:
                salePrice = 'na'

        for element3 in item_dom.cssselect('div#caption div'):
            itemDescription = element3.text

        for element4 in item_dom.cssselect('div#itemarea>a'):
            itemImage = element4.attrib['href']
            
        for element5 in item_dom.cssselect('div#itemarea>a>img'):
            itemThumb = element5.attrib['src']

        itemShipping = []
        for element6 in item_dom.cssselect('div.itemform select'):
            for opt in element6:
                itemShipping.append(opt.get('value'))
            
        uniqueId = itemId + '$' + itemTitle        
            
        ourData.append({
            "category": category,
            "id": itemId,
            "unique_id": uniqueId,
            "url": start_url+curr_item,
            "title": itemTitle,
            "description": itemDescription,
            "price": itemPrice,
            "sale_price": salePrice,
            "item_shipping": itemShipping,
            "image": itemImage,
            "img_thumb": itemThumb        
        })    
        
                    
scraperwiki.sqlite.save(unique_keys=["unique_id"], data=ourData, table_name="igal_products")

        


import scraperwiki
import mechanize
import lxml.html


def fetch_dom(startUrl, addPath):
    scrape = scraperwiki.scrape(startUrl + addPath)
    result = lxml.html.fromstring(scrape)
    return result

start_url = 'http://igalcalderpicassowarhol.com/'

scrape = scraperwiki.scrape(start_url)

dom = lxml.html.fromstring(scrape)

#1. get the main navigation links
nav_links = []

for el in dom.cssselect('div#nav-product ul li a'):
    one_link = el.attrib['href']
    nav_links.append(one_link)

print nav_links


#2. go through each section (nav destination, and start collecting each item there)

ourData = []

for curr_path in nav_links:
    page_dom = fetch_dom(start_url, curr_path)

    #2a, get category
    for el in page_dom.cssselect('div#bodycontent > div.breadcrumbs'):
        category = el.text_content()
        print category

    #3. Go through each item and start gathering
    item_links = []
    for elem in page_dom.cssselect('div.name a'):
        item_link = elem.attrib['href']
        item_links.append(item_link)

    for curr_item in item_links:

        item_dom = fetch_dom(start_url, curr_item)
        
        #3a. get item ID
        for element0 in item_dom.cssselect('div.code em'):
            itemId = element0.text

        for element1 in item_dom.cssselect('#item-contenttitle'):#might be going by multiple elem. hence errors.
            itemTitle = element1.text
            
        if item_dom.cssselect('div.price'):
            for element2 in item_dom.cssselect('div.price'):
                itemPrice = element2.text
        else:
            for element2 in item_dom.cssselect('div.price-bold'):
                itemPrice = element2.text

        if item_dom.cssselect('div.sale-price-bold'):
            for element2b in item_dom.cssselect('div.sale-price-bold em'):
                salePrice = element2b.text
        else:
                salePrice = 'na'

        for element3 in item_dom.cssselect('div#caption div'):
            itemDescription = element3.text_content() #using .text_content() is prefereable to .text as the latter stops at <br> elements, not retrieving all text.
            itemDescriptionHtml = lxml.html.tostring(element3)


        for element4 in item_dom.cssselect('div#itemarea>a'):
            itemImage = element4.attrib['href']
            
        for element5 in item_dom.cssselect('div#itemarea>a>img'):
            itemThumb = element5.attrib['src']

        itemShipping = []
        for element6 in item_dom.cssselect('div.itemform select'):
            for opt in element6:
                itemShipping.append(opt.get('value'))
            
        uniqueId = itemId + itemPrice + '$' + itemTitle        
            
        ourData.append({
            "category": category,
            "id": itemId,
            "unique_id": uniqueId,
            "url": start_url+curr_item,
            "title": itemTitle,
            "description": itemDescription,
            "descriptionHtml": itemDescriptionHtml,
            "price": itemPrice,
            "sale_price": salePrice,
            "item_shipping": itemShipping,
            "image": itemImage,
            "img_thumb": itemThumb        
        })    
        
                    
scraperwiki.sqlite.save(unique_keys=["unique_id"], data=ourData, table_name="igal_products")

        


