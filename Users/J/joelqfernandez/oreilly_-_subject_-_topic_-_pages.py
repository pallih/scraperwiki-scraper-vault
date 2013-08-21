import scraperwiki

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from scrapy.item import Item, Field
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import MapCompose, TakeFirst

from scrapy.conf import settings
from scrapy import log

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.http import Request
from urlparse import urljoin

from scrapy.conf import settings
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/534.56.5 (KHTML, like Gecko) Version/5.1.6 Safari/534.56.5'


class PagesSpider(BaseSpider):
    name = 'pages'
    start_urls = [
    'http://shop.oreilly.com/category/browse-subjects.do'
    ]
    allowed_domains = ['shop.oreilly.com']

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        subjects = hxs.select("//div[@class='navLeft2Off']/a/@href").extract()
        for subject in subjects:
            subjectLink = urljoin(response.url, subject)
            yield Request(subjectLink, self.parseTopic)
            
    def parseTopic(self, response):
        hxs = HtmlXPathSelector(response)
        topics=hxs.select("//div[@class='navLeft2Off']/a/@href").extract()
        for topic in topics:
            topicLink = urljoin(response.url, topic)
            yield Request(topicLink, self.parsePages)

    def parsePages(self, response):
        hxs = HtmlXPathSelector(response)
        pages=hxs.select('//tr[3]/td//tr/td[@class="default"]').extract()
        items = []
        for page in pages:
            loader = WebsiteLoader(selector=page)
            #loader.add_xpath('name', 'string()')
            loader.add_xpath('url', 'concat("http://shop.oreilly.com", select/option/@value)' )
            #loader.add_xpath('description', 'select/option/text()')
            items.append(loader.load_item())
            # yield Request(topicLink, self.parsePages)
            #print page
        return items            

class Website(Item):
    topics = Field()
    url = Field()
    page = Field()

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
        
    run_spider(PagesSpider(), settings)

if __name__ == 'scraper':
    main()
