#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import scraperwiki
import urllib2
import lxml, lxml.html as html
import re
import socket

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from scrapy.selector import HtmlXPathSelector

from scrapy.item import Item, Field
from scrapy.http import Request
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import MapCompose, TakeFirst

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
        Rule(SgmlLinkExtractor(
                restrict_xpaths=(
                    '//div[@id="container"]//div[@id="pagination"]/ul/div/li[@class="nextpageactive"]/a')
                ),
            callback='parse', follow=True),
    )

    def parse(self, response):
        self.log('No item received for %s' % response.url)

        for elem in super(HideMyAssSpider, self).parse(response):
            yield elem       

        hxs = HtmlXPathSelector(response)
        links = hxs.select('//tr[@class="altshade"]')

        for link in links:
            ipaddress_parts = link.select('td[2]/span')

            style_text = ipaddress_parts.select('style/text()').extract()
            style_text = style_text[0].split('\n')
            display_none = [style[1:style.index('{')]
                            for style in style_text
                            if 'none' in style]
            display_inline = [style[1:style.index('{')]
                            for style in style_text
                            if 'inline' in style]
            display_none = set(display_none)
            display_inline = set(display_inline)

            ipaddress = []

            for ipaddress_part in ipaddress_parts.select('span|div|text()'):
                tag_class = tag_style = tag_name = None
                try:
                    tag_class = ipaddress_part.select('@class').extract()
                except TypeError:
                    # Workaround bug in lxml.etree: Argument 'element' has incorrect type (expected lxml.etree._Element, got _ElementStringResult)
                    pass

                try:
                    tag_style = ipaddress_part.select('@style').extract()
                except TypeError:
                    # Workaround bug in lxml.etree: Argument 'element' has incorrect type (expected lxml.etree._Element, got _ElementStringResult)
                    pass

                try:                
                    tag_name = ipaddress_part.select("name()")
                except TypeError:
                    # Workaround bug in lxml.etree: Argument 'element' has incorrect type (expected lxml.etree._Element, got _ElementStringResult) 
                    pass

                if tag_name:
                    tag_text = ipaddress_part.select('text()').extract()
                else:
                    tag_text = ipaddress_part.extract()

                if tag_style and 'none' in tag_style[0]:
                    continue
                if tag_class and tag_class[0] in display_none:
                    continue

                if isinstance(tag_text, list):
                    tag_text = ''.join(tag_text)

                tag_texts = tag_text.split('.')
                for tag_text in tag_texts:
                    tag_text = tag_text.strip()
                    if not tag_text.isdigit():
                        continue
                    ipaddress.append(tag_text)

            ipaddress = '.'.join(ipaddress)

            loader = WebsiteLoader(selector=link)
            loader.add_value('ipaddress', ipaddress)
            loader.add_xpath('port', 'td[3]/text()')
            loader.add_xpath('country', 'td[4]/span/text()')
            loader.add_xpath('_type', 'td[7]/text()')
            loader.add_xpath('anonimity', 'td[8]/text()')
            loader.add_value('url', response.url)

            item = loader.load_item()
            
            yield item

                        
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
        #unique_keys = spider.settings.get('SW_UNIQUE_KEYS', ['ipaddress'])
        unique_keys = ['ipaddress']
        scraperwiki.sqlite.save(table_name=spider.name, unique_keys=unique_keys, data=self.data)
        self.data = []

def run_spider(spider, settings):
    """Run a spider with given settings"""
    from scrapy import signals
    from scrapy.xlib.pydispatch import dispatcher
    from scrapy.settings import CrawlerSettings
      
    def catch_item(sender, item, **kwargs):
        #log.msg("Got:" + str(item))
        pass
       
    dispatcher.connect(catch_item, signal=signals.item_passed)

    from scrapy.crawler import CrawlerProcess

    settings = CrawlerSettings(values=settings)

    crawler = CrawlerProcess(settings)
    crawler.install()
    crawler.configure()
    crawler.crawl(spider)

    #log.start(loglevel='DEBUG')

    crawler.start()

def main():
    options = {
        'LOG_LEVEL': 'DEBUG',
        'FEED_URI': 'proxylist.json',
        'FEED_FORMAT': 'jsonlines',
    }

    run_spider(HideMyAssSpider(), options)

def scraper():
    import sys
    sys.path.append("/home/scriptrunner/")
    print sys.path
    options = {
        'SW_SAVE_BUFFER': 30,
        'SW_UNIQUE_KEYS': ['url'],
        'ITEM_PIPELINES': ['script.SWPipeline'],
    }

       
    run_spider(HideMyAssSpider(), options)


if __name__ == '__main__':
    main()

if __name__ == 'scraper':
    scraper()
