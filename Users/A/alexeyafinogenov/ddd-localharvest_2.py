# author: Clint Eastwood

# this is an example scraper, feel free to use lxml, soup or any other html parser (in this case pure regex - multi-threaded)
# the inserted data should use the schema listed here: 
# 
# if for a specific record, one of these fields is not found, use empty string "" as the record value
# only add the fields needed or provided by the page/scrape description
# use companyname as the unique key when writing to the database

# please name the scrapers ddd-<<short identifier>>, ie ddd-housewares-1

# use scraperwiki.sqlite.save_var("source", value) to save a string of the name of the source you scraped
# example scraperwiki.sqlite.save_var("source", "NAFST - Fancy Food Show")

# use scraperwiki.sqlite.save_var("author", value) to save your name
# example scraperwiki.sqlite.save_var("author", " Clint Eastwood")

# use this to save each record to the sql database : scraperwiki.sqlite.save(unique_keys=['companyname'], data=dict(my_data))

# for good practice, trim white space on the field values and use the cleaning functions provided below
# !!!!!make sure to use use safestr() to handle internatalization issues (can't write to sql datastore with i18n characters)!!!!!

# if you need to use a proxy (some sites block the ip of scraperwiki) - please use the following code
#proxy_url = "72.77.197.214:19629" (http://www.xroxy.com/proxy-country-US.htm has good ones to use)
#proxy = urllib2.ProxyHandler({'http': proxy_url})
#user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; v' + str(random.random())
#opener = urllib2.build_opener(proxy)
#opener.addheaders = [('User-agent', user_agent)]
#page_html = opener.open(url).read()
import re
import random
import requests
import datetime

import scraperwiki

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider, Rule

from scrapy.item import Item, Field
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import MapCompose, TakeFirst
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from scrapy.conf import settings
from scrapy.http import Request
from scrapy import log

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

def strip_non_text(string):
    return re.sub("\n|\r|\t| |:","",string)


scraperwiki.sqlite.save_var("source", "localharvest.org")
scraperwiki.sqlite.save_var("author", "Alexey Afinogenov")

class LocalharvestSpider(CrawlSpider):
    name = "localharvest"
    allowed_domains = ["anonymouse.org"]
    proxy_url = 'http://anonymouse.org/cgi-bin/anon-www.cgi/'
    start_urls = [
        proxy_url + 'http://www.localharvest.org/search.jsp?lat=48.539215&lon=-100.60518&scale=2'
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('p=\d+')), follow=True),
        Rule(SgmlLinkExtractor(allow=('-M\d+')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        my_data = []
        my_data.append(('datescraped', datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")))

        hxs = HtmlXPathSelector(response)
        companyname = hxs.select('//*[@id="listingbody"]/table[1]/tr/td/h1[1]/text()').extract()[0] 
        categories = hxs.select('').extract()[0]
        maincategory = hxs.select('//td[@background="/images/tabs/tab_back_on.gif"]/nobr/a/text()').extract()[0]
        location = hxs.select('//*[@id="listingbody"]/table[2]/tr/td[1]/p[1]/text()').extract()           
        address = strip_non_text(location[0])
        city, loc_data = location[1].split(', ')
        state, zip = loc_data.split(' ') 
        country = 'USA'
        sourceurl = response.url.replace(proxy_url, '')
        #my_data.append(('sourceurl', response.url))
        website = hxs.select('//*[@id="listingbody"]/table[2]/tr/td[1]/p[2]/a[1]/@href').extract()
        if website:
            website = website[0]
        contact_info = hxs.select('//*[@id="listingbody"]/table[2]/tr/td[1]/p[2]/text()').extract()
        contact = contact_info[0].split(' ')
        contact1first, contact1last = ' '.join(contact[:-1]), contact[-1]
        phonenumber = contact_info[1]
        description = hxs.select('//*[@id="listingbody"]/table[2]/tr/td[1]/font[1]/p[1]/text()').extract()[0]
        contactlink = hxs.select('//img[@src="/images/email_18.png"]../a/@href').extract()
        if contactlink:
            contactlink = contactlink[0]

#        scraperwiki.sqlite.save(unique_keys=['companyname'], data=dict(my_data))

        return None


def run_spider(spider, settings):
    """Run a spider with given settings"""
    from scrapy.crawler import CrawlerProcess
    crawler = CrawlerProcess(settings)
    crawler.install()
    crawler.configure()
    crawler.crawl(spider)
    log.start()
    crawler.start()

def main():
    import sys
    sys.path.append("/home/scriptrunner/")
    print sys.path
    options = {
        'SW_SAVE_BUFFER': 30,
        'SW_UNIQUE_KEYS': ['url'],
    }

    settings.overrides.update(options)
    
    run_spider(LocalharvestSpider(), settings)

if __name__ == 'scraper':
    main()

# author: Clint Eastwood

# this is an example scraper, feel free to use lxml, soup or any other html parser (in this case pure regex - multi-threaded)
# the inserted data should use the schema listed here: 
# 
# if for a specific record, one of these fields is not found, use empty string "" as the record value
# only add the fields needed or provided by the page/scrape description
# use companyname as the unique key when writing to the database

# please name the scrapers ddd-<<short identifier>>, ie ddd-housewares-1

# use scraperwiki.sqlite.save_var("source", value) to save a string of the name of the source you scraped
# example scraperwiki.sqlite.save_var("source", "NAFST - Fancy Food Show")

# use scraperwiki.sqlite.save_var("author", value) to save your name
# example scraperwiki.sqlite.save_var("author", " Clint Eastwood")

# use this to save each record to the sql database : scraperwiki.sqlite.save(unique_keys=['companyname'], data=dict(my_data))

# for good practice, trim white space on the field values and use the cleaning functions provided below
# !!!!!make sure to use use safestr() to handle internatalization issues (can't write to sql datastore with i18n characters)!!!!!

# if you need to use a proxy (some sites block the ip of scraperwiki) - please use the following code
#proxy_url = "72.77.197.214:19629" (http://www.xroxy.com/proxy-country-US.htm has good ones to use)
#proxy = urllib2.ProxyHandler({'http': proxy_url})
#user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; v' + str(random.random())
#opener = urllib2.build_opener(proxy)
#opener.addheaders = [('User-agent', user_agent)]
#page_html = opener.open(url).read()
import re
import random
import requests
import datetime

import scraperwiki

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider, Rule

from scrapy.item import Item, Field
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import MapCompose, TakeFirst
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from scrapy.conf import settings
from scrapy.http import Request
from scrapy import log

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

def strip_non_text(string):
    return re.sub("\n|\r|\t| |:","",string)


scraperwiki.sqlite.save_var("source", "localharvest.org")
scraperwiki.sqlite.save_var("author", "Alexey Afinogenov")

class LocalharvestSpider(CrawlSpider):
    name = "localharvest"
    allowed_domains = ["anonymouse.org"]
    proxy_url = 'http://anonymouse.org/cgi-bin/anon-www.cgi/'
    start_urls = [
        proxy_url + 'http://www.localharvest.org/search.jsp?lat=48.539215&lon=-100.60518&scale=2'
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('p=\d+')), follow=True),
        Rule(SgmlLinkExtractor(allow=('-M\d+')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        my_data = []
        my_data.append(('datescraped', datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")))

        hxs = HtmlXPathSelector(response)
        companyname = hxs.select('//*[@id="listingbody"]/table[1]/tr/td/h1[1]/text()').extract()[0] 
        categories = hxs.select('').extract()[0]
        maincategory = hxs.select('//td[@background="/images/tabs/tab_back_on.gif"]/nobr/a/text()').extract()[0]
        location = hxs.select('//*[@id="listingbody"]/table[2]/tr/td[1]/p[1]/text()').extract()           
        address = strip_non_text(location[0])
        city, loc_data = location[1].split(', ')
        state, zip = loc_data.split(' ') 
        country = 'USA'
        sourceurl = response.url.replace(proxy_url, '')
        #my_data.append(('sourceurl', response.url))
        website = hxs.select('//*[@id="listingbody"]/table[2]/tr/td[1]/p[2]/a[1]/@href').extract()
        if website:
            website = website[0]
        contact_info = hxs.select('//*[@id="listingbody"]/table[2]/tr/td[1]/p[2]/text()').extract()
        contact = contact_info[0].split(' ')
        contact1first, contact1last = ' '.join(contact[:-1]), contact[-1]
        phonenumber = contact_info[1]
        description = hxs.select('//*[@id="listingbody"]/table[2]/tr/td[1]/font[1]/p[1]/text()').extract()[0]
        contactlink = hxs.select('//img[@src="/images/email_18.png"]../a/@href').extract()
        if contactlink:
            contactlink = contactlink[0]

#        scraperwiki.sqlite.save(unique_keys=['companyname'], data=dict(my_data))

        return None


def run_spider(spider, settings):
    """Run a spider with given settings"""
    from scrapy.crawler import CrawlerProcess
    crawler = CrawlerProcess(settings)
    crawler.install()
    crawler.configure()
    crawler.crawl(spider)
    log.start()
    crawler.start()

def main():
    import sys
    sys.path.append("/home/scriptrunner/")
    print sys.path
    options = {
        'SW_SAVE_BUFFER': 30,
        'SW_UNIQUE_KEYS': ['url'],
    }

    settings.overrides.update(options)
    
    run_spider(LocalharvestSpider(), settings)

if __name__ == 'scraper':
    main()

