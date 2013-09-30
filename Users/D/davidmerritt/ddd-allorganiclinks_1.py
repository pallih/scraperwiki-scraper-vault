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


scraperwiki.sqlite.save_var("source", "allorganiclinks.com")
scraperwiki.sqlite.save_var("author", "Alexey Afinogenov")

class AllorganiclinksSpider(CrawlSpider):
    name = "allorganiclinks"
    allowed_domains = ["allorganiclinks.com"]
    start_urls = [
        "http://www.allorganiclinks.com/",
    ]

    rules = (
        Rule(
            SgmlLinkExtractor(
                allow=('/category', ),
            ), 
            callback='parse_item', follow=True
        ),
    )

    def parse_item(self, response):
        my_data = []
        my_data.append(('datescraped', datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")))

        hxs = HtmlXPathSelector(response)
        items = hxs.select('//*[@class="listing"]')
        for item in items:
            try:
                my_data.append(('companyname', item.select('h4/a/text()').extract()[0])) 
                website = item.select('h4/a/@href').extract()[0]
                website = requests.get(website).url
                my_data.append(('website', website))
                my_data.append(('description', item.select('div/text()').extract()[0][:1000]))
                categories = item.select('//table/tr/td/h2/a/text()|//table/tr/td/h2/text()').extract()
                categories = [strip_non_text(category) for category in categories if strip_non_text(category)]
                my_data.append(('maincategory', categories[1]))
                if len(categories) > 2:
                    categories = ' : '.join(categories[1:])
                    my_data.append(('categories', categories))
                my_data.append(('sourceurl', response.url)) 
                scraperwiki.sqlite.save(unique_keys=['companyname'], data=dict(my_data))
            except:
                print 'Error'

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
        
    run_spider(AllorganiclinksSpider(), settings)

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


scraperwiki.sqlite.save_var("source", "allorganiclinks.com")
scraperwiki.sqlite.save_var("author", "Alexey Afinogenov")

class AllorganiclinksSpider(CrawlSpider):
    name = "allorganiclinks"
    allowed_domains = ["allorganiclinks.com"]
    start_urls = [
        "http://www.allorganiclinks.com/",
    ]

    rules = (
        Rule(
            SgmlLinkExtractor(
                allow=('/category', ),
            ), 
            callback='parse_item', follow=True
        ),
    )

    def parse_item(self, response):
        my_data = []
        my_data.append(('datescraped', datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")))

        hxs = HtmlXPathSelector(response)
        items = hxs.select('//*[@class="listing"]')
        for item in items:
            try:
                my_data.append(('companyname', item.select('h4/a/text()').extract()[0])) 
                website = item.select('h4/a/@href').extract()[0]
                website = requests.get(website).url
                my_data.append(('website', website))
                my_data.append(('description', item.select('div/text()').extract()[0][:1000]))
                categories = item.select('//table/tr/td/h2/a/text()|//table/tr/td/h2/text()').extract()
                categories = [strip_non_text(category) for category in categories if strip_non_text(category)]
                my_data.append(('maincategory', categories[1]))
                if len(categories) > 2:
                    categories = ' : '.join(categories[1:])
                    my_data.append(('categories', categories))
                my_data.append(('sourceurl', response.url)) 
                scraperwiki.sqlite.save(unique_keys=['companyname'], data=dict(my_data))
            except:
                print 'Error'

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
        
    run_spider(AllorganiclinksSpider(), settings)

if __name__ == 'scraper':
    main()

