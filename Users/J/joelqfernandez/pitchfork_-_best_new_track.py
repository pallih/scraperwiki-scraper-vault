#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import scraperwiki

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

#from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from scrapy.item import Item, Field
from scrapy.http import Request
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import MapCompose, TakeFirst

from scrapy.conf import settings
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/534.56.5 (KHTML, like Gecko) Version/5.1.6 Safari/534.56.5'
DEPTH_LIMIT = '1'
from scrapy import log

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
        
class PitchforkSpider(CrawlSpider):
    name = 'pitchfork'
    start_urls = [
    'http://pitchfork.com/features/staff-lists/8727-the-top-50-albums-of-2011/'
    ]
    allowed_domains = ['pitchfork.com']
    
    rules = (
        ## Pitchfork - Top 50 - 2011
        #Rule(SgmlLinkExtractor(allow=('/features/staff-lists/8727-the-top-50-albums-of-2011/'))),
        Rule(SgmlLinkExtractor(restrict_xpaths=('//*[@id="main"]/div/span[2]/a'))),
        Rule(SgmlLinkExtractor(restrict_xpaths=('//*[@id="main"]//ul/li/a'), deny=('/artists/')), callback='parseItem', follow=True)
        )           

    def parseItem(self, response):
        #self.log('No item received for %s' % response.url)
        
        hxs = HtmlXPathSelector(response)
        links = hxs.select('//div[@id="main"]')
        items = []
        for link in links:
            loader = WebsiteLoader(selector=link)
            #loader.add_xpath('data_pk', 'ul/li/@data-pk')
            loader.add_xpath('artist', 'ul/li/div/h1/a/text()')
            loader.add_xpath('track', 'ul/li/div/h2/text()')
            loader.add_xpath('pub_date', 'ul/li/div[2]/h4/span[@class="pub-date"]/text()')
            loader.add_xpath('img_src', 'ul/li/div/img/@src')
            #loader.add_xpath('amazon', 'ul/li/div[2]/ul/li[2]/a[3]/@href')
            #loader.add_xpath('score', 'ul/li/div/span/text()')
            loader.add_xpath('detail', 'div/div[@class="editorial"]/p')
            loader.add_value('url', response.url)
            items.append(loader.load_item())
        return items   
        
class Website(Item):
    artist = Field()
    album = Field()
    track = Field()
    reissue = Field()
    img_src = Field()
    pub_date = Field()
    score = Field()
    amazon = Field()
    detail = Field()
    url = Field()
    page = Field()
    data_pk = Field()

class WebsiteLoader(XPathItemLoader):
    default_item_class = Website
    default_input_processor = MapCompose(lambda x: x.strip())
    default_output_processor = TakeFirst()

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
        
    run_spider(PitchforkSpider(), settings)

if __name__ == 'scraper':
    main()
