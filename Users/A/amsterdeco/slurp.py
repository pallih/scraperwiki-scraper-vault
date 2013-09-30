import scraperwiki
import lxml.html
import re
import urllib2

def get_page(url):
    return urllib2.urlopen(url).read().decode('utf-8', 'ignore').encode('utf-8')

def scrape_wine(URL):
    try:
        tree = lxml.html.fromstring(get_page(URL))
    except:
        return False

    wine ={}

    wine["title"] = tree.xpath("//li[@class='bc_title']/span")[0].text
    wine["price"] = float(re.findall("([0-9]+.[0-9]+)",tree.xpath("//p[@id='selling_price']/span")[0].text)[0].replace(",",""))
    wine["url"] = URL

    for row in  tree.xpath("//table[@class='list1']/tr") + tree.xpath("//table[@class='list2']/tr"):
        key = row.xpath("th")[0].text
        value = row.xpath("td")[0].text
        wine[key]=value 

    scraperwiki.sqlite.save(unique_keys=["title"], data=wine, table_name="wines")

    return True

start_page=1
end_page=409

if False:
    for page in range(start_page,end_page+1):
        print page
        page_url = "http://www.slurp.co.uk/search/page%d/?sort=title_az" %page
        print page_url
        tree = lxml.html.parse(page_url)
        for row in  tree.xpath("//h2[@class='title']/a"):
            print row.attrib["href"]
            scraperwiki.sqlite.save(unique_keys=["url"], data={"url":row.attrib["href"]}, table_name="urls")

urls=scraperwiki.sqlite.select("* from urls where scraped is not '1'")
#cheap_wines=scraperwiki.sqlite.select("* from wines where price < 5")
#urls = []
#for cheap_wine in cheap_wines:
#    urls.append({'url': cheap_wine['url'][len('http://www.slurp.co.uk'):],})

print "Found %d to scrape" % len(urls)

i = 0
for row in urls:
    #if i > 100:
    #    break
    
    section = row["url"].split("/")[1]
    if section not in ["accessories","sake","cider","liqueurs","spirits","alcohol-free-wine","tasting-event-beers","specialist-beers","gift-boxes"]:
        row["scraped"] = scrape_wine("http://www.slurp.co.uk" + row["url"])
        scraperwiki.sqlite.save(unique_keys=["url"], data=row, table_name="urls")

        i += 1
import scraperwiki
import lxml.html
import re
import urllib2

def get_page(url):
    return urllib2.urlopen(url).read().decode('utf-8', 'ignore').encode('utf-8')

def scrape_wine(URL):
    try:
        tree = lxml.html.fromstring(get_page(URL))
    except:
        return False

    wine ={}

    wine["title"] = tree.xpath("//li[@class='bc_title']/span")[0].text
    wine["price"] = float(re.findall("([0-9]+.[0-9]+)",tree.xpath("//p[@id='selling_price']/span")[0].text)[0].replace(",",""))
    wine["url"] = URL

    for row in  tree.xpath("//table[@class='list1']/tr") + tree.xpath("//table[@class='list2']/tr"):
        key = row.xpath("th")[0].text
        value = row.xpath("td")[0].text
        wine[key]=value 

    scraperwiki.sqlite.save(unique_keys=["title"], data=wine, table_name="wines")

    return True

start_page=1
end_page=409

if False:
    for page in range(start_page,end_page+1):
        print page
        page_url = "http://www.slurp.co.uk/search/page%d/?sort=title_az" %page
        print page_url
        tree = lxml.html.parse(page_url)
        for row in  tree.xpath("//h2[@class='title']/a"):
            print row.attrib["href"]
            scraperwiki.sqlite.save(unique_keys=["url"], data={"url":row.attrib["href"]}, table_name="urls")

urls=scraperwiki.sqlite.select("* from urls where scraped is not '1'")
#cheap_wines=scraperwiki.sqlite.select("* from wines where price < 5")
#urls = []
#for cheap_wine in cheap_wines:
#    urls.append({'url': cheap_wine['url'][len('http://www.slurp.co.uk'):],})

print "Found %d to scrape" % len(urls)

i = 0
for row in urls:
    #if i > 100:
    #    break
    
    section = row["url"].split("/")[1]
    if section not in ["accessories","sake","cider","liqueurs","spirits","alcohol-free-wine","tasting-event-beers","specialist-beers","gift-boxes"]:
        row["scraped"] = scrape_wine("http://www.slurp.co.uk" + row["url"])
        scraperwiki.sqlite.save(unique_keys=["url"], data=row, table_name="urls")

        i += 1
