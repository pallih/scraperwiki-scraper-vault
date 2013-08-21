import scraperwiki

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
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


class WwwplusSpider(CrawlSpider):
    name = "wwwplus"
    allowed_domains = ["preprod.canalplus.fr"]
    start_urls = ["http://preprod.canalplus.fr"]
    rules = (
        Rule(SgmlLinkExtractor(allow=('.*',),deny=('/breve\.ajax\.php','/compte\.ajax\.php','/programme\.ajax\.php','/ajax/', )), callback='parse_item', follow = True),
    )

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        item = OgWwwPlusItem()
        item['url'] = response.url
        item['og_url'] = hxs.select('/html/head/meta[contains(@property, "og:url")]/@content').extract()
        item['og_type'] = hxs.select('/html/head/meta[contains(@property, "og:type")]/@content').extract()
        item['og_image'] = hxs.select('/html/head/meta[contains(@property, "image")]/@content').extract()
        item['og_name'] = hxs.select('/html/head/meta[contains(@property, "canalplusfr:name")]/@content').extract()

        return item

class OgWwwPlusItem(Item):
    url = Field()
    og_url = Field()
    og_type = Field()
    og_image = Field()
    og_name = Field()
    """
    og_actor = Field()
    og_director = Field()
    og_season_number = Field()
    og_episode_number = Field()
    og_tvshow = Field()
    og_tvprogram = Field()
    og_parent = Field()
    og_presenter = Field()
    og_guest = Field()
    og_fname = Field()
    og_lname = Field()
    og_gender = Field()
    og_video_url = Field()
    twitter_card_type = Field()
    twitter_creator = Field()
    twitter_site = Field()
    twitter_player = Field()
    """
class OgWwwwPlusLoader(XPathItemLoader):
    default_item_class = OgWwwPlusItem
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
        
    run_spider(WwwplusSpider(), settings)

if __name__ == 'scraper':
    main()