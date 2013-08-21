# Standard Python library imports

# 3rd party imports
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item, Field
from scrapy.conf import settings 
# My imports

HTML_FILE_NAME = r'.+\.html'
class Website:
    url = Field()
class WelchParser(object):    
    def parse_links(self, response):
        hxs = HtmlXPathSelector(response)
        item = Website()
        # All poetry text is in pre tags
        item['url']= hxs.select('//a/@href').extract() 
        # head/title contains title - a poem by author
        return item


class PoetrySpider(CrawlSpider, WelchParser):
    name = 'example.com_poetry'
    allowed_domains = ['http://dir.yahoo.com/']
    start_urls = ['http://dir.yahoo.com/government/',
                  'http://dir.yahoo.com/recreation/']
    rules = (Rule(SgmlLinkExtractor(allow=()), follow = True,
                                    callback='parse_links'),
             Rule(SgmlLinkExtractor(allow=()), callback='parse_links'))
def run_spider(spider, settings):
    """Run a spider with given settings"""
    from scrapy.crawler import CrawlerProcess
    crawler = CrawlerProcess(settings)
    crawler.install()
    crawler.configure()
    crawler.crawl(spider)
    log.start()
    crawler.start()
run_spider(PoetrySpider, settings)
