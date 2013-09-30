import scraperwiki

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from scrapy.item import Item, Field
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import MapCompose, TakeFirst

from scrapy.conf import settings
from scrapy import log

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

import datetime


"""Define data container"""
class GameItem(Item):
    title = Field()
    url = Field()
    price = Field()
    quantity = Field()
    timestamp = Field()

class ThreeSpider(CrawlSpider):
    name = "03_crawl"
    DOWNLOAD_DELAY = 1
    COOKIES_ENABLED = True
    start_urls = ["http://bit.ly/LJ09mM"]
    rules = (Rule(SgmlLinkExtractor(allow=('pact=',)), follow=True, callback='parse_item'),)

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//table/tr[3]/td/table/tr/td[2]/table/tr/td/table/tr/td[2]/table/tr/td/table/tr/td/table[2]/tr')          
        items = []
        for site in sites:
            item = GameItem()
            title  = site.select('td/div/font/b/a/text()').extract()
            item['title']= title[0].replace(",","")
            item['url'] = 'http://www.masqueoca.com/tienda' + (site.select('td/div/font/b/a/@href').extract()).pop()
            
            
            price = site.select('td/div/font/b/text()').re('\d+,\d+')
            if len(price) == 0:
                price = site.select('td/div/font/b/text()').re('\d+')
                if len(price) == 0:
                    price = site.select('td/div/font/text()').re('\d+,\d+')
                    if len(price) == 0:
                        price = site.select('td/div/font/text()').re('\d+')
                        if len(price) == 0:
                            price = site.select('td/div/font/i/b/b/text()').re('\d+,\d+')

            

            if len(price) > 0:
                price = price.pop()
                price = price.replace(",", ".")
                item['price'] = float(price)
            else:
                item['price'] = 0

            
            quantity =  (site.select('td/div[4]/a[2]/img/@src').re('/\w+')).pop()

            if quantity == '/b_add_conj':
                item['quantity'] = 1
            else:
                item['quantity'] = 0
            
            item['timestamp'] = datetime.datetime.now()
            items.append(item)
        return items


class SWPipeline(object):
    """A pipeline for saving to the Scraperwiki datastore"""
    def __init__(self):
        self.buffer = 20
        self.data = []
        self.counter = 0
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def process_item(self, item, spider):
        self.data.append(dict(item))
        if len(self.data) >= self.buffer:
            self.write_data(spider)
        return item

    def spider_closed(self, spider):
        if self.data:
            self.write_data(spider)
    
    def write_data(self, spider):
        unique_keys = spider.settings.get('SW_UNIQUE_KEYS', ['id'])
        scraperwiki.sqlite.save(table_name=spider.name, unique_keys=unique_keys, data=self.data)
        self.data = []

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
        'ITEM_PIPELINES': ['script.SWPipeline'],
    }

    settings.overrides.update(options)
        
    run_spider(ThreeSpider(), settings)

if __name__ == 'scraper':
    scraperwiki.sqlite.execute("drop table if exists spider.name")
    main()
import scraperwiki

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from scrapy.item import Item, Field
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import MapCompose, TakeFirst

from scrapy.conf import settings
from scrapy import log

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

import datetime


"""Define data container"""
class GameItem(Item):
    title = Field()
    url = Field()
    price = Field()
    quantity = Field()
    timestamp = Field()

class ThreeSpider(CrawlSpider):
    name = "03_crawl"
    DOWNLOAD_DELAY = 1
    COOKIES_ENABLED = True
    start_urls = ["http://bit.ly/LJ09mM"]
    rules = (Rule(SgmlLinkExtractor(allow=('pact=',)), follow=True, callback='parse_item'),)

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//table/tr[3]/td/table/tr/td[2]/table/tr/td/table/tr/td[2]/table/tr/td/table/tr/td/table[2]/tr')          
        items = []
        for site in sites:
            item = GameItem()
            title  = site.select('td/div/font/b/a/text()').extract()
            item['title']= title[0].replace(",","")
            item['url'] = 'http://www.masqueoca.com/tienda' + (site.select('td/div/font/b/a/@href').extract()).pop()
            
            
            price = site.select('td/div/font/b/text()').re('\d+,\d+')
            if len(price) == 0:
                price = site.select('td/div/font/b/text()').re('\d+')
                if len(price) == 0:
                    price = site.select('td/div/font/text()').re('\d+,\d+')
                    if len(price) == 0:
                        price = site.select('td/div/font/text()').re('\d+')
                        if len(price) == 0:
                            price = site.select('td/div/font/i/b/b/text()').re('\d+,\d+')

            

            if len(price) > 0:
                price = price.pop()
                price = price.replace(",", ".")
                item['price'] = float(price)
            else:
                item['price'] = 0

            
            quantity =  (site.select('td/div[4]/a[2]/img/@src').re('/\w+')).pop()

            if quantity == '/b_add_conj':
                item['quantity'] = 1
            else:
                item['quantity'] = 0
            
            item['timestamp'] = datetime.datetime.now()
            items.append(item)
        return items


class SWPipeline(object):
    """A pipeline for saving to the Scraperwiki datastore"""
    def __init__(self):
        self.buffer = 20
        self.data = []
        self.counter = 0
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def process_item(self, item, spider):
        self.data.append(dict(item))
        if len(self.data) >= self.buffer:
            self.write_data(spider)
        return item

    def spider_closed(self, spider):
        if self.data:
            self.write_data(spider)
    
    def write_data(self, spider):
        unique_keys = spider.settings.get('SW_UNIQUE_KEYS', ['id'])
        scraperwiki.sqlite.save(table_name=spider.name, unique_keys=unique_keys, data=self.data)
        self.data = []

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
        'ITEM_PIPELINES': ['script.SWPipeline'],
    }

    settings.overrides.update(options)
        
    run_spider(ThreeSpider(), settings)

if __name__ == 'scraper':
    scraperwiki.sqlite.execute("drop table if exists spider.name")
    main()
