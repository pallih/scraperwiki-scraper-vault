import scraperwiki

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from scrapy.item import Item, Field
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import MapCompose, TakeFirst
from scrapy.selector import HtmlXPathSelector

from scrapy.conf import settings
from scrapy import log

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals


from scrapy.http import Request
from urlparse import urljoin
import re

class UsaOFSpider(CrawlSpider):
    name = "usaof"
    allowed_domains = ["www.usaoilfield.com"]
    start_urls = [
            'http://www.usaoilfield.com/quicksearch.php?search=0&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=1&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=2&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=3&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=4&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=5&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=6&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=7&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=8&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=9&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=A&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=B&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=C&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=D&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=E&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=F&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=G&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=H&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=I&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=J&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=K&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=L&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=M&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=N&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=O&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=P&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=Q&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=R&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=S&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=T&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=U&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=V&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=W&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=X&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=Y&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=Z&startrow=0',
            ]

    rules = (Rule (SgmlLinkExtractor(
                        allow=("quicksearch\.php\?search=[A-Z0-9](&startrow=\d)*", ),
                        restrict_xpaths=('//table[@id="AutoNumber11"]//a[text()="Next"] | //table[@id="AutoNumber11"]//a[text()="1"]',)),
                    callback="parse_links", follow=True ),
    )

    def parse_links(self, response):
        self.parse_items(response)
        hxs = HtmlXPathSelector(response)
        for url in hxs.select("//td/a/@href").extract():
            if url:
                yield Request(urljoin(response.url, url[1:]), callback=self.parse_items)

    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)

        item = UsaOFItem()


        content = ''.join(hxs.select('//table[@id="AutoNumber12"]/tr[1]/descendant-or-self::text()').extract())
        item["company"] = re.sub(ur'(\s)\s+', ur'\1', re.sub(ur'\n|\t', u' ', content), flags=re.MULTILINE + re.UNICODE).strip()

        content = ''.join(hxs.select('//table[@id="AutoNumber12"]/tr[2]/descendant-or-self::text()').extract())
        item["address"] = re.sub(ur'(\s)\s+', ur'\1', re.sub(ur'\n|\t', u' ', content), flags=re.MULTILINE + re.UNICODE).strip()


        content = ''.join(hxs.select('//table[@id="AutoNumber12"]/tr[3]/descendant-or-self::text()').extract())
        item["phone"] = re.sub(ur'(\s)\s+', ur'\1', re.sub(ur'\n|\t', u' ', content), flags=re.MULTILINE + re.UNICODE).strip()

        yield item


class UsaOFItem(Item):
    company = Field()
    address = Field()
    phone = Field()

class WebsiteLoader(XPathItemLoader):
    default_item_class = UsaOFItem
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
        'SW_UNIQUE_KEYS': ['company'],
        'ITEM_PIPELINES': ['script.SWPipeline'],
        'DOWNLOAD_DELAY': 0.1,
    }

    settings.overrides.update(options)
        
    run_spider(UsaOFSpider(), settings)

if __name__ == 'scraper':
    main()
import scraperwiki

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from scrapy.item import Item, Field
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import MapCompose, TakeFirst
from scrapy.selector import HtmlXPathSelector

from scrapy.conf import settings
from scrapy import log

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals


from scrapy.http import Request
from urlparse import urljoin
import re

class UsaOFSpider(CrawlSpider):
    name = "usaof"
    allowed_domains = ["www.usaoilfield.com"]
    start_urls = [
            'http://www.usaoilfield.com/quicksearch.php?search=0&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=1&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=2&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=3&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=4&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=5&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=6&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=7&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=8&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=9&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=A&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=B&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=C&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=D&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=E&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=F&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=G&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=H&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=I&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=J&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=K&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=L&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=M&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=N&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=O&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=P&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=Q&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=R&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=S&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=T&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=U&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=V&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=W&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=X&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=Y&startrow=0',
            'http://www.usaoilfield.com/quicksearch.php?search=Z&startrow=0',
            ]

    rules = (Rule (SgmlLinkExtractor(
                        allow=("quicksearch\.php\?search=[A-Z0-9](&startrow=\d)*", ),
                        restrict_xpaths=('//table[@id="AutoNumber11"]//a[text()="Next"] | //table[@id="AutoNumber11"]//a[text()="1"]',)),
                    callback="parse_links", follow=True ),
    )

    def parse_links(self, response):
        self.parse_items(response)
        hxs = HtmlXPathSelector(response)
        for url in hxs.select("//td/a/@href").extract():
            if url:
                yield Request(urljoin(response.url, url[1:]), callback=self.parse_items)

    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)

        item = UsaOFItem()


        content = ''.join(hxs.select('//table[@id="AutoNumber12"]/tr[1]/descendant-or-self::text()').extract())
        item["company"] = re.sub(ur'(\s)\s+', ur'\1', re.sub(ur'\n|\t', u' ', content), flags=re.MULTILINE + re.UNICODE).strip()

        content = ''.join(hxs.select('//table[@id="AutoNumber12"]/tr[2]/descendant-or-self::text()').extract())
        item["address"] = re.sub(ur'(\s)\s+', ur'\1', re.sub(ur'\n|\t', u' ', content), flags=re.MULTILINE + re.UNICODE).strip()


        content = ''.join(hxs.select('//table[@id="AutoNumber12"]/tr[3]/descendant-or-self::text()').extract())
        item["phone"] = re.sub(ur'(\s)\s+', ur'\1', re.sub(ur'\n|\t', u' ', content), flags=re.MULTILINE + re.UNICODE).strip()

        yield item


class UsaOFItem(Item):
    company = Field()
    address = Field()
    phone = Field()

class WebsiteLoader(XPathItemLoader):
    default_item_class = UsaOFItem
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
        'SW_UNIQUE_KEYS': ['company'],
        'ITEM_PIPELINES': ['script.SWPipeline'],
        'DOWNLOAD_DELAY': 0.1,
    }

    settings.overrides.update(options)
        
    run_spider(UsaOFSpider(), settings)

if __name__ == 'scraper':
    main()
