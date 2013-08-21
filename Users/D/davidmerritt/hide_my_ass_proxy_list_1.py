#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import scraperwiki
import urllib2
import lxml.html as html
import re
import socket

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
        
class HideMyAssSpider(CrawlSpider):
    name = 'hidemyass'
    start_urls = [
    'http://hidemyass.com/proxy-list/'
    ]
    allowed_domains = ['hidemyass.com']
    
    rules = (
        ## Linux From Scratch - Chapter 3.2 - All Packages
        Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@id="container"]//div[@id="pagination"]/ul/div/li[@class="nextpageactive"]/a')),callback='parseItem', follow=True),
        )           

    def parseItem(self, response):
        self.log('No item received for %s' % response.url)
        
        hxs = HtmlXPathSelector(response)
        links = hxs.select('//tr[@class="altshade"]')
        items = []
        for link in links:
            #ipaddress = link.select('td[2]//*[not(contains(@style,"display:none"))]/text() | td[3]/text()')
            #anonimity = link.select('td[8]/text()')
            String = '.'.join(ipaddress)
            loader = WebsiteLoader(selector=link)
            loader.add_value('ipaddress', 'td[2]//*[not(contains(@style,"display:none"))]/text() | td[3]/text()')
            loader.add_xpath('port', 'td[3]/text()')
            loader.add_xpath('country', 'td[4]/span/text()')
            loader.add_xpath('_type', 'td[7]/text()')
            loader.add_value('anonimity', 'td[8]/text() | td[7]/text()')
            loader.add_value('url', response.url)
            items.append(loader.load_item())
            String = '.'.join(ipaddress)
            items.append((re.sub (r"\.+",'.', re.sub(r"\.\n",":",String)), anonimity))
        return items 
          
                        
class Website(Item):
    url = Field()
    ipaddress = Field()
    port = Field()
    country = Field()
    speed = Field()
    connection_time = Field()
    _type = Field()
    anonimity = Field()
    
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
        
    run_spider(HideMyAssSpider(), settings)

if __name__ == 'scraper':
    main()
