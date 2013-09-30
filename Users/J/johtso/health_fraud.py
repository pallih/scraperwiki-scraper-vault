if __name__ == 'scraper':
    import scraperwiki
    scrapy_utils = scraperwiki.utils.swimport("scrapy_utils")
else:
    import scrapy_utils

import time
import pickle
import unicodedata
from urlparse import urlparse, parse_qs, urljoin
from HTMLParser import HTMLParser
import tempfile
import urllib

import lxml.html as lh

from scrapy.http import Request
from scrapy.item import Item, Field
from scrapy.spider import BaseSpider
from scrapy import log
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Identity
from scrapy.utils.misc import extract_regex
from scrapy.utils.misc import arg_to_iter


def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def no_cache(url):
    return url+'&'+str(time.time())

class FraudParser(HTMLParser):
    def __init__(self):
        self.header = True
        self.items = []
        self.finished = False
        self.in_table = False
        self.in_row = False
        self.in_cell = False
        self.current_row = []
        self.current_cell = ''
        HTMLParser.__init__(self)
    
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if not self.in_table:
            if tag == 'table':
                if ('id' in attrs) and (attrs['id'] == 'dgResult'):
                    self.in_table = True
        else:
            if tag == 'tr':
                self.in_row = True
            elif tag == 'td':
                self.in_cell = True
            elif (tag == 'a') and (len(self.current_row) == 7):
                jsfunction = attrs['href']
                uid = extract_regex(r'javascript:VerifyID\((\d+)\)', jsfunction)[0]
                self.current_cell = uid

    def handle_endtag(self, tag):
        if tag == 'tr':
            if self.in_table:
                if self.in_row:
                    self.in_row = False
                    if not self.header:                 
                        self.save_data()
                    else:
                        self.header = False
                    self.current_row = []
        elif tag == 'td':
            if self.in_table:
                if self.in_cell:
                    self.in_cell = False
                    self.current_row.append(self.current_cell.strip())
                    self.current_cell = ''
        elif (tag == 'table') and self.in_table:
            self.finished = True
    
    def handle_data(self, data):
        if not len(self.current_row) == 7:
            if self.in_cell:
                self.current_cell += data

    def save_data(self):
        loader = ExclusionLoader()
        loader.add_values(self.current_row)
        new_item = loader.load_item()
        self.items.append(new_item)

class HealthFraudSpider(BaseSpider):
    name = "healthfraud"
    allowed_domains = ['exclusions.oig.hhs.gov']
    start_urls = ['http://exclusions.oig.hhs.gov/ExclusionTypeCounts.aspx']
    storage = scrapy_utils.SWStorage()
    
    downloading = []
    
    def parse(self, response):

        tree = lh.fromstring(response.body)

        urls = [urljoin(response.url, a.attrib['href']) for a in tree.xpath("//table[@id='CountList']//a")]
        all_urls = self.storage.urls = set(urls)

        try:
            scraped_urls = self.storage.scraped
        except:
            scraped_urls = self.storage.scraped = set([])

        for url in all_urls-scraped_urls:
            yield Request('http://exclusions.oig.hhs.gov', callback=self.parse_results, meta={'nexturl':url})
            self.downloading.append(url)
            break

    def parse_results(self, response):
        current_url = response.meta['nexturl']
        filename, resp = urllib.urlretrieve(current_url)
        
        parser = FraudParser()

        for line in open(filename):
            if parser.finished:
                items = parser.items[:]
                for item in items:
                    yield item
                parser.items = []
                break
            items = parser.items[:]
            for item in items:
                yield item
            parser.items = []
            parser.feed(line)

        for item in items:
            yield item
        parser.items = []


        scraped_urls = self.storage.scraped
        scraped_urls.add(current_url)
        self.storage.scraped = scraped_urls

class ExclusionItem(scrapy_utils.FlexibleItem):
    unique_keys = ['id']

class ExclusionLoader(scrapy_utils.MultiLoader):
    default_item_class = ExclusionItem

    keys = {'main':
                ['last_name',
               'first_name',
               'business_name',
               'general',
               'specialty',
               'exclusion',
               'state',
               'id',]
           }
    
    default_keys = keys['main']

    default_output_processor = TakeFirst()

    def extract_id(self, id_cell):
        jsfunction = id_cell.xpath('.//a')[0].attrib['href']
        uid = extract_regex(r'javascript:VerifyID\((\d+)\)', jsfunction)
        return arg_to_iter(uid)

def run_spider(spider, settings):
    from scrapy.crawler import CrawlerProcess
    crawler = CrawlerProcess(settings)
    crawler.install()
    crawler.configure()
    crawler.crawl(spider)
    log.start()
    crawler.start()

def monkeypatch_load_object():
    from scrapy.utils import misc
    orig_load_object = misc.load_object
    def good_load_object(path):
        if not isinstance(path, basestring):
            return path
        else:
            return orig_load_object(path)
    misc.load_object = good_load_object

def main():    
    monkeypatch_load_object()
    from scrapy.conf import settings
    
    settings.overrides['LOG_ENABLED'] = True
    settings.overrides['LOG_LEVEL'] = 'INFO'
    settings.overrides['SAVE_BUFFER'] = 500

    if __name__ == 'scraper':
        settings.overrides['ITEM_PIPELINES'] = [scrapy_utils.SWPipeline]
        
    run_spider(HealthFraudSpider(), settings)

main()if __name__ == 'scraper':
    import scraperwiki
    scrapy_utils = scraperwiki.utils.swimport("scrapy_utils")
else:
    import scrapy_utils

import time
import pickle
import unicodedata
from urlparse import urlparse, parse_qs, urljoin
from HTMLParser import HTMLParser
import tempfile
import urllib

import lxml.html as lh

from scrapy.http import Request
from scrapy.item import Item, Field
from scrapy.spider import BaseSpider
from scrapy import log
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Identity
from scrapy.utils.misc import extract_regex
from scrapy.utils.misc import arg_to_iter


def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def no_cache(url):
    return url+'&'+str(time.time())

class FraudParser(HTMLParser):
    def __init__(self):
        self.header = True
        self.items = []
        self.finished = False
        self.in_table = False
        self.in_row = False
        self.in_cell = False
        self.current_row = []
        self.current_cell = ''
        HTMLParser.__init__(self)
    
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if not self.in_table:
            if tag == 'table':
                if ('id' in attrs) and (attrs['id'] == 'dgResult'):
                    self.in_table = True
        else:
            if tag == 'tr':
                self.in_row = True
            elif tag == 'td':
                self.in_cell = True
            elif (tag == 'a') and (len(self.current_row) == 7):
                jsfunction = attrs['href']
                uid = extract_regex(r'javascript:VerifyID\((\d+)\)', jsfunction)[0]
                self.current_cell = uid

    def handle_endtag(self, tag):
        if tag == 'tr':
            if self.in_table:
                if self.in_row:
                    self.in_row = False
                    if not self.header:                 
                        self.save_data()
                    else:
                        self.header = False
                    self.current_row = []
        elif tag == 'td':
            if self.in_table:
                if self.in_cell:
                    self.in_cell = False
                    self.current_row.append(self.current_cell.strip())
                    self.current_cell = ''
        elif (tag == 'table') and self.in_table:
            self.finished = True
    
    def handle_data(self, data):
        if not len(self.current_row) == 7:
            if self.in_cell:
                self.current_cell += data

    def save_data(self):
        loader = ExclusionLoader()
        loader.add_values(self.current_row)
        new_item = loader.load_item()
        self.items.append(new_item)

class HealthFraudSpider(BaseSpider):
    name = "healthfraud"
    allowed_domains = ['exclusions.oig.hhs.gov']
    start_urls = ['http://exclusions.oig.hhs.gov/ExclusionTypeCounts.aspx']
    storage = scrapy_utils.SWStorage()
    
    downloading = []
    
    def parse(self, response):

        tree = lh.fromstring(response.body)

        urls = [urljoin(response.url, a.attrib['href']) for a in tree.xpath("//table[@id='CountList']//a")]
        all_urls = self.storage.urls = set(urls)

        try:
            scraped_urls = self.storage.scraped
        except:
            scraped_urls = self.storage.scraped = set([])

        for url in all_urls-scraped_urls:
            yield Request('http://exclusions.oig.hhs.gov', callback=self.parse_results, meta={'nexturl':url})
            self.downloading.append(url)
            break

    def parse_results(self, response):
        current_url = response.meta['nexturl']
        filename, resp = urllib.urlretrieve(current_url)
        
        parser = FraudParser()

        for line in open(filename):
            if parser.finished:
                items = parser.items[:]
                for item in items:
                    yield item
                parser.items = []
                break
            items = parser.items[:]
            for item in items:
                yield item
            parser.items = []
            parser.feed(line)

        for item in items:
            yield item
        parser.items = []


        scraped_urls = self.storage.scraped
        scraped_urls.add(current_url)
        self.storage.scraped = scraped_urls

class ExclusionItem(scrapy_utils.FlexibleItem):
    unique_keys = ['id']

class ExclusionLoader(scrapy_utils.MultiLoader):
    default_item_class = ExclusionItem

    keys = {'main':
                ['last_name',
               'first_name',
               'business_name',
               'general',
               'specialty',
               'exclusion',
               'state',
               'id',]
           }
    
    default_keys = keys['main']

    default_output_processor = TakeFirst()

    def extract_id(self, id_cell):
        jsfunction = id_cell.xpath('.//a')[0].attrib['href']
        uid = extract_regex(r'javascript:VerifyID\((\d+)\)', jsfunction)
        return arg_to_iter(uid)

def run_spider(spider, settings):
    from scrapy.crawler import CrawlerProcess
    crawler = CrawlerProcess(settings)
    crawler.install()
    crawler.configure()
    crawler.crawl(spider)
    log.start()
    crawler.start()

def monkeypatch_load_object():
    from scrapy.utils import misc
    orig_load_object = misc.load_object
    def good_load_object(path):
        if not isinstance(path, basestring):
            return path
        else:
            return orig_load_object(path)
    misc.load_object = good_load_object

def main():    
    monkeypatch_load_object()
    from scrapy.conf import settings
    
    settings.overrides['LOG_ENABLED'] = True
    settings.overrides['LOG_LEVEL'] = 'INFO'
    settings.overrides['SAVE_BUFFER'] = 500

    if __name__ == 'scraper':
        settings.overrides['ITEM_PIPELINES'] = [scrapy_utils.SWPipeline]
        
    run_spider(HealthFraudSpider(), settings)

main()