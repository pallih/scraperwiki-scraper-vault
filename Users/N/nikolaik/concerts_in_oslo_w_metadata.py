import scraperwiki, re
from datetime import datetime

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from scrapy.item import Item, Field
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from scrapy.conf import settings
from scrapy import log

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

from lxml.html.clean import Cleaner

# Concerts in Oslo w/ metadata for narrow filtering
# Using: http://scrapy.org/
#
# Data model:

class ConcertItem(Item):
    name = Field()
    start_datetime = Field()
    description = Field()
    venue = Field()
    url = Field()

# Pulling from 
# Rockefeller/Sentrum Scene/John Dee
# Parkteateret
# Mono
# Mir
# Studentersamfundet

class ConcertSpider(CrawlSpider):
    # Rockefeller/Sentrum Scene/John Dee

    name = 'concerts_in_oslo'
    allowed_domains = ['rockefeller.no', 'www.revolveroslo.no']
    start_urls = ['http://rockefeller.no/index.html', 'http://www.revolveroslo.no/nb/program']
    # One rule per site
    rules = [
        Rule(SgmlLinkExtractor(allow=[r'rockefeller\.no/jd\d+', r'rockefeller\.no/rf\d+', r'rockefeller\.no/sc\d+']), 'parse_rockefeller_concert'),
        Rule(SgmlLinkExtractor(allow=[r'revolveroslo\.no/nb/program/[\w-]+'], deny=[r'revolveroslo\.no/nb/program/old']), 'parse_revolver_concert')]

    def parse_rockefeller_concert(self, response):
        x = HtmlXPathSelector(response)

        concert = ConcertItem()
        
        s = x.select('//span[2]/b/text()').extract()[0]
        s = re.search(r'(?P<date>\d{2}/\d{2}-\d{4})\s+(?P<venue>.+)', s).groupdict()
        date = datetime.strptime(s['date'], '%d/%m-%Y')
        concert['venue'] = s['venue']
        concert['url'] = response.url
        name = x.select('//span[3]/text()').extract()
        concert['name'] = " ".join([n.strip() for n in name])
        concert['description'] = x.select('//span[4]/text()').extract()[0].strip()
        concert['start_datetime'] = date
        return concert


    def parse_revolver_concert(self, response):
        x = HtmlXPathSelector(response)

        concert = ConcertItem()
        concert['venue'] = 'Revolver'
        concert['url'] = response.url
        concert['name'] = x.select('//*[@id="page-title"]/text()').extract()[0]
        description = "\n".join(x.select('//*[contains(@class,"field-name-body")]/div/div/p').extract())
        cleaner = Cleaner(style=True)
        concert['description'] = cleaner.clean_html(description)
        concert['start_datetime'] = x.select('//*[@datatype="xsd:dateTime"]/@content').extract()[0]
        return concert

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

if __name__ == 'scraper':
    import sys
    sys.path.append("/home/scriptrunner/")
    options = {
        'SW_SAVE_BUFFER': 30,
        'SW_UNIQUE_KEYS': ['url'],
        'ITEM_PIPELINES': ['script.SWPipeline'],
    }

    settings.overrides.update(options)
        
    run_spider(ConcertSpider(), settings)

import scraperwiki, re
from datetime import datetime

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from scrapy.item import Item, Field
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from scrapy.conf import settings
from scrapy import log

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

from lxml.html.clean import Cleaner

# Concerts in Oslo w/ metadata for narrow filtering
# Using: http://scrapy.org/
#
# Data model:

class ConcertItem(Item):
    name = Field()
    start_datetime = Field()
    description = Field()
    venue = Field()
    url = Field()

# Pulling from 
# Rockefeller/Sentrum Scene/John Dee
# Parkteateret
# Mono
# Mir
# Studentersamfundet

class ConcertSpider(CrawlSpider):
    # Rockefeller/Sentrum Scene/John Dee

    name = 'concerts_in_oslo'
    allowed_domains = ['rockefeller.no', 'www.revolveroslo.no']
    start_urls = ['http://rockefeller.no/index.html', 'http://www.revolveroslo.no/nb/program']
    # One rule per site
    rules = [
        Rule(SgmlLinkExtractor(allow=[r'rockefeller\.no/jd\d+', r'rockefeller\.no/rf\d+', r'rockefeller\.no/sc\d+']), 'parse_rockefeller_concert'),
        Rule(SgmlLinkExtractor(allow=[r'revolveroslo\.no/nb/program/[\w-]+'], deny=[r'revolveroslo\.no/nb/program/old']), 'parse_revolver_concert')]

    def parse_rockefeller_concert(self, response):
        x = HtmlXPathSelector(response)

        concert = ConcertItem()
        
        s = x.select('//span[2]/b/text()').extract()[0]
        s = re.search(r'(?P<date>\d{2}/\d{2}-\d{4})\s+(?P<venue>.+)', s).groupdict()
        date = datetime.strptime(s['date'], '%d/%m-%Y')
        concert['venue'] = s['venue']
        concert['url'] = response.url
        name = x.select('//span[3]/text()').extract()
        concert['name'] = " ".join([n.strip() for n in name])
        concert['description'] = x.select('//span[4]/text()').extract()[0].strip()
        concert['start_datetime'] = date
        return concert


    def parse_revolver_concert(self, response):
        x = HtmlXPathSelector(response)

        concert = ConcertItem()
        concert['venue'] = 'Revolver'
        concert['url'] = response.url
        concert['name'] = x.select('//*[@id="page-title"]/text()').extract()[0]
        description = "\n".join(x.select('//*[contains(@class,"field-name-body")]/div/div/p').extract())
        cleaner = Cleaner(style=True)
        concert['description'] = cleaner.clean_html(description)
        concert['start_datetime'] = x.select('//*[@datatype="xsd:dateTime"]/@content').extract()[0]
        return concert

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

if __name__ == 'scraper':
    import sys
    sys.path.append("/home/scriptrunner/")
    options = {
        'SW_SAVE_BUFFER': 30,
        'SW_UNIQUE_KEYS': ['url'],
        'ITEM_PIPELINES': ['script.SWPipeline'],
    }

    settings.overrides.update(options)
        
    run_spider(ConcertSpider(), settings)

