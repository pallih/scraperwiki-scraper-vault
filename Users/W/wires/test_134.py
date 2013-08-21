#Database Schema:
#Categories
#catKey, catID, catName, subCatID, subCatName, catURL, crawled
#
#ProductPages
#catID, subCatID, prodURL, scraped
#
#Products
#prodID, catID, subCatID, pcatID, prodURL, prodTitle, overview, moreInfo, Articles, numImages
#
#Images
#catID, subCatID, pcatID, imgURL, smimgURL, thumbURL, thumbTitle
#
#Items
#itemID, catID, subCatID, pcatID, itemDesc, price


import scraperwiki
import lxml.html
import lxml.etree
import re
import resource
from sys import exit

def getProducts(prodPage):
    phtml = lxml.html.parse(prodPage).getroot()
    baseURL = re.sub(r'.com/\w+.*', '.com', prodPage)
    prodURL = prodPage
    prodTitle = phtml.cssselect(".categoryname")[0].text
    URLargs = prodPage.split('?')[1].split('&')[0].split('+')
    catID = URLargs[1]
    pcatID = URLargs[len(URLargs)-1]
    if len(URLargs) > 3:
        subCatID = URLargs[2]
    else: subCatID = ""
    overview = lxml.html.tostring(phtml.cssselect("#content_inc_1")[0],method="html")
    moreInfo = lxml.html.tostring(phtml.cssselect("#content_inc_2")[0],method="html")
    Articles = lxml.html.tostring(phtml.cssselect("#content_inc_5")[0],method="html")

    # Get image data for main image
    img = phtml.cssselect(r'img[src*="Categoryimages"][width]')
    try:
        smimgURL =  baseURL + img[0].get("src")
        numImages = 1
    except:
        smimgURL = ""
        numImages = 0
    try:
        imgURL = baseURL + re.sub(r'.*&large=','',img[0].getparent().get("href").split(',',1)[0].rstrip(r"'"))
    except:
        imgURL = ""
    imgData = {'imgKey': catID + subCatID + pcatID + imgURL,
        'catID': catID,
        'subCatID': subCatID,
        'pcatID': pcatID,
        'imgURL': imgURL,
        'smimgURL':smimgURL,
        'thumbURL': "",
        'thumbTitle': "" }
    if numImages > 0:
        scraperwiki.sqlite.save(unique_keys=["imgKey"], data=imgData, table_name="Images")


    # Get thumbnail images if present
    styles = phtml.cssselect('div[id^="thumb"]')
    numImages += len(styles)
    if len(styles) > 0:
        for i in styles:
            thumbURL = i.cssselect("img")[0].get("src")
            imgURL = re.sub(r'-th-','-',thumbURL, flags=re.IGNORECASE)
            thumbTitle = re.sub('\s+',' ',i.cssselect("div")[2].text_content().replace(u'\xa0',' '))
            imgData = {'imgKey': catID + subCatID + pcatID + imgURL,
                'catID': catID,
                'subCatID': subCatID,
                'pcatID': pcatID,
                'imgURL': baseURL + imgURL,
                'smimgURL': "",
                'thumbURL': baseURL + thumbURL,
                'thumbTitle': thumbTitle }
            scraperwiki.sqlite.save(unique_keys=["imgKey"], data=imgData, table_name="Images")
#    print "Found " + repr(numImages) + " image(s) for pcatID: " + pcatID

    # Get pricing information for items in this product group
    items = phtml.cssselect('#displaygrid span[style]')
    i = 0
    count = 0
#    print "found " + repr(len(items)) + " spans for pcatID: " + pcatID
    while i < (len(items) - 1):
        if items[i+1].get("style").find('line-through') == -1:
            price = items[i+1].text_content().strip().lstrip('$')
            content = items[i].text_content()
            itemDesc1 = re.sub('\s+',' ',content[0:content.rfind(',')].strip().replace(u'\xa0',' '))
            itemDesc = itemDesc1[0:itemDesc1.rfind(',')]
            itemID = itemDesc1[itemDesc1.rfind(',')+1:].strip()
            i += 2
            itemData = {'itemID': itemID,
                'catID': catID,
                'subCatID': subCatID,
                'pcatID': pcatID,
                'itemDesc': itemDesc,
                'price': price }
            scraperwiki.sqlite.save(unique_keys=["itemID"], data=itemData, table_name="Items")
            count += 1
        else:
            if ((i+2) < len(items)):
                if items[i+2].text_content().strip()[0] == '$':
                    price = items[i+2].text_content().strip().lstrip('$')
                    content = items[i].text_content()
                    itemDesc1 = re.sub('\s+',' ',content[0:content.rfind(',')].strip().replace(u'\xa0',' '))
                    itemDesc = itemDesc1[0:itemDesc1.rfind(',')]
                    itemID = itemDesc1[itemDesc1.rfind(',')+1:].strip()
                    i += 3
                    itemData = {'itemID': itemID,
                        'catID': catID,
                        'subCatID': subCatID,
                        'pcatID': pcatID,
                        'itemDesc': itemDesc,
                        'price': price }
                    scraperwiki.sqlite.save(unique_keys=["itemID"], data=itemData, table_name="Items")
                    count += 1
                else:
                    price = items[i+1].text_content().strip().lstrip('$')
                    content = items[i].text_content()
                    itemDesc1 = re.sub('\s+',' ',content[0:content.rfind(',')].strip().replace(u'\xa0',' '))
                    itemDesc = itemDesc1[0:itemDesc1.rfind(',')]
                    itemID = itemDesc1[itemDesc1.rfind(',')+1:].strip()
                    i += 2
                    itemData = {'itemID': itemID,
                        'catID': catID,
                        'subCatID': subCatID,
                        'pcatID': pcatID,
                        'itemDesc': itemDesc,
                        'price': price }
                    scraperwiki.sqlite.save(unique_keys=["itemID"], data=itemData, table_name="Items")
                    count += 1
            else:
                price = items[i+1].text_content().strip().lstrip('$')
                content = items[i].text_content()
                itemDesc1 = re.sub('\s+',' ',content[0:content.rfind(',')].strip().replace(u'\xa0',' '))
                itemDesc = itemDesc1[0:itemDesc1.rfind(',')]
                itemID = itemDesc1[itemDesc1.rfind(',')+1:].strip()
                i += 2
                itemData = {'itemID': itemID,
                    'catID': catID,
                    'subCatID': subCatID,
                    'pcatID': pcatID,
                    'itemDesc': itemDesc,
                    'price': price }
                scraperwiki.sqlite.save(unique_keys=["itemID"], data=itemData, table_name="Items")
                count += 1

#    print "Found " + repr(count) + " item(s) for pcatID: " + pcatID

    # save product info to datastore
#Products
#prodID, catID, subCatID, pcatID, prodURL, prodTitle, overview, moreInfo, Articles, numImages
    productData = {'pcatID': pcatID,
        'catID': catID,
        'subCatID': subCatID,
        'prodURL': prodURL,
        'prodTitle': prodTitle,
        'overview': overview,
        'moreInfo': moreInfo,
        'Articles': Articles,
        'numImages': numImages }
    scraperwiki.sqlite.save(unique_keys=["prodURL"], data=productData, table_name="Products")
#    print "Saved product information to database for pcatID: " + pcatID
    return 1

def getCategories(pageURL):
    html = lxml.html.parse(pageURL).getroot()
    baseURL = re.sub(r'.com/\w+.*', '.com', pageURL)
    categories = html.cssselect('#e2 li')
    for x in categories:
        catURL = x.cssselect('a')[0].get("href")
        catID = catURL.rsplit('/',1)[1]
        if catID == "23479":
            continue
        catName = re.sub('\s+',' ',x.cssselect('div')[0].text_content().replace(u'\xa0',' '))
        catKey = "3578" + catID
        catData = {'catKey': catKey,
            'catID': catID,
            'catName': catName,
            'subCatID': "",
            'subCatName': "",
            'catURL': baseURL + catURL,
            'crawled': 0 }
        scraperwiki.sqlite.save(unique_keys=["catKey"], data=catData, table_name="Categories")
        getSubCats(baseURL + catURL)
    return 1

def getSubCats(pageURL):
    html = lxml.html.parse(pageURL).getroot()
    baseURL = re.sub(r'.com/\w+.*', '.com', pageURL)
    subCats = html.cssselect('#subCats li')
    if len(subCats) > 0:
        catName = re.sub('\s+',' ',subCats[0].cssselect('div')[0].text_content().replace(u'\xa0',' '))
        j = 1
        while j < len(subCats):
            catURL = subCats[j].cssselect('a')[0].get("href")
            catID = catURL.rsplit('/',2)[1]
            subCatID = catURL.rsplit('/',2)[2]
            subCatName = re.sub('\s+',' ',subCats[j].cssselect('div')[0].text_content().replace(u'\xa0',' '))
            catKey = "3578" + catID + subCatID
            catData = {'catKey': catKey,
                'catID': catID,
                'catName': catName,
                'subCatID': subCatID,
                'subCatName': subCatName,
                'catURL': baseURL + catURL,
                'crawled': 0 }
            j += 1
            scraperwiki.sqlite.save(unique_keys=["catKey"], data=catData, table_name="Categories")

def getProdURLs(pageURL):
    html = lxml.html.parse(pageURL).getroot()
    baseURL = re.sub(r'.com/\w+.*', '.com', pageURL)
    prodURLs = html.cssselect('.product_link > img')
    for i in prodURLs:
        catID = i.getparent().get("href").split('+')[1]
        if len(i.getparent().get("href").split('+')) > 3:
            subCatID = i.getparent().get("href").split('+')[2]
        else:
            subCatID = ""
        pcatID = i.getparent().get("href").split('=')[2]
        thumbURL = baseURL + i.get("src")
        prodURL = baseURL + i.getparent().get("href")
        prodData = {'catID': catID,
            'subCatID': subCatID,
            'thumbURL': thumbURL,
            'prodURL': prodURL,
            'pcatID': pcatID,
            'scraped': 0}
        scraperwiki.sqlite.save(unique_keys=["pcatID"], data=prodData, table_name="ProductPages")
    return 1

def getNumProds(pageURL):
    html = lxml.html.parse(pageURL).getroot()
    numResults = html.cssselect('#pagerefine1 div')[2].text_content().split(' ')[0].strip()
    return numResults



# MAIN SCRIPT

# clean up tables from previous executions
# 0: normal operation
# 1: reset which categories have been crawled already
# 2: reset which product pages have been scraped already
# 3: skip category crawling and go straight to product scraping
# 4: delete Items table
# 5: delete Products table
# 6: reset product pages scraped and delete items and products tables

clean = 3

if clean == 1:
    scraperwiki.sqlite.execute("DELETE FROM Categories WHERE subCatID = 'aquarium-fish-supplies.cfm?c=2190'")
    scraperwiki.sqlite.execute("UPDATE Categories SET crawled = 0 WHERE crawled = 1")
    scraperwiki.sqlite.commit()

if clean == 2:
    scraperwiki.sqlite.execute("UPDATE ProductPages SET scraped = 0")
    scraperwiki.sqlite.commit()

if clean == 4:
    scraperwiki.sqlite.execute("DELETE FROM Items")
    scraperwiki.sqlite.commit()

if clean == 5:
    scraperwiki.sqlite.execute("DELETE FROM Products")
    scraperwiki.sqlite.commit()

if clean == 6:
    scraperwiki.sqlite.execute("UPDATE ProductPages SET scraped = 0")
    scraperwiki.sqlite.execute("DELETE FROM Items")
    scraperwiki.sqlite.execute("DELETE FROM Products")
    scraperwiki.sqlite.commit()

# check if categories exist
#scraperwiki.sqlite.execute("CREATE TABLE `Categories` (`subCatID` text, `catID` text, `catKey` text, `catURL` text, `catName` text, `crawled` integer, `subCatName` text)")
#scraperwiki.sqlite.commit()
#exit()
#cats = scraperwiki.sqlite.execute("SELECT COUNT(*) FROM Categories")
#if cats['data'] == [[0]]:
#    getCategories("http://www.drsfostersmith.com/fish-supplies/pr/c/3578")
#exit()

# get category URL pages from datastore
if clean == 0:
    categories = scraperwiki.sqlite.select("* FROM Categories WHERE crawled = 0 ORDER BY subCatID ASC")
else:
    categories = {}

for i in categories:
    print "catURL = " + i['catURL']
    try:
        newURL = i['catURL'] + "?count=" + getNumProds(i['catURL']) + "&s=ts"
    except:
        continue
    try:
        if getProdURLs(newURL):
            catData = {'catKey': i['catKey'],
                'catID': i['catID'],
                'catName': i['catName'],
                'subCatID': i['subCatID'],
                'subCatName': i['subCatName'],
                'catURL': i['catURL'],
                'crawled': 1 }
            scraperwiki.sqlite.save(unique_keys=["catKey"], data=catData, table_name="Categories")
        else:
            print "Error while crawling categories for products."
    except scraperwiki.CPUTimeExceededError:
        print "CPU time exception while processing category page: " + catURL
        print "time in user mode: " + resource.getrusage()[0]
        print "time in system mode: " + resource.getrusage()[1]
    except:
        print "Unknown error while processing category page: " + catURL
        raise



# crawl product pages
if clean == 0 | clean == 3:
    products = scraperwiki.sqlite.select("* FROM ProductPages WHERE scraped = 0")
else:
    products = {}

pcount = 0
for i in products:
    try:
#        if getProducts(i['prodURL']) & (pcount < 5):
        if getProducts(i['prodURL']):
            prodData = {'catID': i['catID'],
                'subCatID': i['subCatID'],
                'thumbURL': i['thumbURL'],
                'prodURL': i['prodURL'],
                'pcatID': i['pcatID'],
                'scraped': 1}
            scraperwiki.sqlite.save(unique_keys=["pcatID"], data=prodData, table_name="ProductPages")
            pcount += 1
            if ((pcount%5) == 0):
                print "Scraped " + repr(pcount) + " pages so far. User mode time: " + repr(resource.getrusage(resource.RUSAGE_SELF)[0]) + \
                ". Sytem mode time: " + repr(resource.getrusage(resource.RUSAGE_SELF)[1])
        elif pcount >= 5:
            print "Stopped after " + repr(pcount) + " products."
            break
        else:
            print "Error while scraping product pages."
    except scraperwiki.CPUTimeExceededError:
        print "CPU time exception while processing product page: " + i['prodURL']
        print "time in user mode: " + resource.getrusage(resource.RUSAGE_SELF)[0]
        print "time in system mode: " + resource.getrusage(resource.RUSAGE_SELF)[1]
    except:
        print "Unknown error while processing product page: " + i['prodURL']
        raise

