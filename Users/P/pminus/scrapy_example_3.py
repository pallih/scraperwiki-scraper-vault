import scraperwiki
from scrapy import log
from scrapy import signals
from scrapy.http import Request
from scrapy.conf import settings
from scrapy.item import Item, Field
from scrapy.selector import HtmlXPathSelector
from scrapy.xlib.pydispatch import dispatcher
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.loader.processor import MapCompose, TakeFirst

class Craigonator(CrawlSpider):
    name = "craigorator"
    allowed_domains = ['stlouis.craigslist.org']
    start_urls = ['http://stlouis.craigslist.org/ppd/']
    rules = (
        Rule(SgmlLinkExtractor(allow=('index\100\.html')), follow=True),
        Rule(SgmlLinkExtractor(allow=(r'/ppd/\d+\.html')), callback='parse_ads', follow=True),
    )
    #start_urls = [
    #"http://stlouis.craigslist.org/ppd/%d+.html" % i for i in xrange()
    #];
    def parse_ads(self, response): #scrape results page, pass to parse_ads_1
        hxs = HtmlXPathSelector(response)
        items = [] 
        sites = hxs.select('//blockquote[@id="toc_rows"]')
        for site in sites:
            item = Magic()
            item['url'] = response.url
            item['price'] = site.select('//blockquote[@id="toc_rows"]/p[1]/span[2]/span/span[1]/span/text()').extract()
            items.append(item)
        yield Request(item[0]['url'], callback=self.parse_ads2)

    def parse_ads2(self, response):
        items = response.meta["items"] 
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//article[@id="pagecontainer"]/section')
        for site in sites:
            item['image_urls'] = site.select('//img/@src').extract()
            item['posted'] = site.select('//article[@id="pagecontainer"]/section/section[2]/div/p[2]/date/text()').extract()
            item['updated'] = site.select('//article[@id="pagecontainer"]/section/section[2]/div/p[3]/date/text()').extract()
            item['location'] = site.select('//article[@id="pagecontainer"]/section/section[2]/section[2]/ul/li[1]/text()').extract()
            item['description'] = str(site.select('//section[@id="postingbody"]/text()')).extract()
            item['title'] = site.select('//article[@id="pagecontainer"]/section/h2/text()').extract()
            items.append(item)
        return items

class Magic(Item):
    url = Field()
    image_urls = Field()
    posted = Field()
    updated = Field()
    location = Field()
    description = Field()
    title = Field()
    price = Field()

class WebsiteLoader(XPathItemLoader):
    default_item_class = Magic
    default_input_processor = MapCompose(lambda x: x.strip())
    default_output_processor = TakeFirst()

class SWPipeline(object):
    """A pipeline for saving to the Scraperwiki datastore"""
    def __init__(self):
        self.buffer = 1
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
        'SW_SAVE_BUFFER': 1,
        'SW_UNIQUE_KEYS': ['title'],
        'ITEM_PIPELINES': ['script.SWPipeline'],
    }

    settings.overrides.update(options)
        
    run_spider(Craigonator(), settings)

if __name__ == 'scraper':
    main()