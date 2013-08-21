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

class IndeedSpider(CrawlSpider):
    name = "indeed"
    allowed_domains = ["indeed.com"]
    start_urls = ["http://www.indeed.com/jobs?q=engineer&l="]

    rules = (
    Rule(SgmlLinkExtractor( restrict_xpaths=('//div[@class="pagination"]',),), callback='parse_items', follow=True),)


    def parse_items(self, response):
        self.log('Hi, this is an item page! %s' % response.url)
        hxs = HtmlXPathSelector(response)
        jobs = hxs.select("//td[@id='resultsCol']/div/h2")
        items = []
        for j in jobs:
            loader = WebsiteLoader(selector=j)
            loader.add_xpath('job_title', 'a/@title')
            link = j.select('a/@href').extract()
            #loader.add_xpath('url', 'a/@href')
            loader.add_value('url',"http://www.indeed.com" + link[0])
            items.append(loader.load_item())
        print items
        return items

class Indeed(Item):
    job_title = Field()
    url = Field()

class WebsiteLoader(XPathItemLoader):
    default_item_class = Indeed
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
        
    run_spider(IndeedSpider(), settings)

if __name__ == 'scraper':
    main()
