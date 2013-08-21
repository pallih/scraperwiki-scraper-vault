import scraperwiki
from lxml import etree
import httplib2
from StringIO import StringIO


def get_disaster_rss(url): #function to grab data from RSS feeds for each Year-Month combo.
    
    h = httplib2.Http(".cache")
    response, content = h.request("http://reliefweb.int/disasters/rss.xml?" + url, "GET")
    if response.status != 200:
        sys.stderr.write('Error, returned status: %s\n' % response.status)
        sys.exit(1) #bomb out, non-zero return indicates error
    
    doc = etree.parse(StringIO(content), parser=etree.XMLParser())
    items = doc.findall('//item')
    for item in items: #Store all the data available in the RSS feeds
        data = {}
        data['title']= item.findtext("title")
        data['link']= item.findtext("link")
        data['description']= item.findtext("description")
        data['guid']= item.findtext("guid")
        data['pubDate']= item.findtext("pubDate")
        data['current']= item.findtext("{http://reliefweb.int/reliefwebRssModule}current")
        data['glide']= item.findtext("{http://reliefweb.int/reliefwebRssModule}glide")
        data['country']= item.findtext("{http://reliefweb.int/reliefwebRssModule}country")
        data['iso3']= item.findtext("{http://reliefweb.int/reliefwebRssModule}iso3")
        data['disaster_type']= item.findtext("{http://reliefweb.int/reliefwebRssModule}disaster_type")
        scraperwiki.sqlite.save(["guid"], data) #Store data in sqlite database


def get_dates(content):#function to increment through the dates.  This is because RSS has max of 30 records.
    date_urls = []
    doc = etree.parse(StringIO(content), parser=etree.HTMLParser())
    for element in doc.xpath('//*[@id="block-searchlight-facets-disaster-listing"]/div/div/div[3]/ul'):
        for row in element.xpath('li'):
            for div in row.xpath('div'):
                for a in div.xpath('a/@href'):
                    date_urls += [(a[11:])] #Ignoring the first 11 characters of each URL because they are not needed
    return date_urls

def get_main_page(): #function to grab main page.
    h = httplib2.Http(".cache")
    response, content = h.request("http://reliefweb.int/disasters", "GET")
    if response.status != 200:
        sys.stderr.write('Error, returned status: %s\n' % response.status)
        sys.exit(1) #bomb out, non-zero return indicates error
    return get_dates(content)


urls = get_main_page()

for url in urls:
    get_disaster_rss(url)