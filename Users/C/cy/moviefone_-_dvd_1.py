import scraperwiki
import urlparse

from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector

from scrapy.item import Item, Field
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import MapCompose, TakeFirst

from scrapy.conf import settings
from scrapy import log

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

import mechanize
cookies = mechanize.CookieJar()
opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(cookies))
opener.addheaders = [("User-agent", 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/534.56.5 (KHTML, like Gecko) Version/5.1.6 Safari/534.56.5'),
                     ("From", "responsible.person@example.com")]

class MoviefoneSpider(CrawlSpider):
    name = 'moviefone'
    allowed_domains = [ 'www.moviefone.com' ]
    start_urls = [ 'http://www.moviefone.com/dvd/' ]

    rules = (
        ## Pitchfork - Top 50 - 2011
        Rule(SgmlLinkExtractor(allow=('/dvd/?page'))),
        Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@class="hub-body"]/div[43]/div[2]/div[1]/a')), follow=True),
        Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@class="hub-body"]/div/div/a[@class="movieTitle"]')), callback='parseItem',  follow=True)
        )           
    
    def parseItem(self, response):
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//div[@id="main-column"]')
        items = []
        for site in sites:
            loader = WebsiteLoader(selector=site)

            loader.add_xpath('title', '//div[@id="movie-nav-title"]/h1/text()')
            loader.add_xpath('theatrical_release_date', '//div[contains(div,"Theatrical Release Date")]/div[@class="info"]/text()')
            loader.add_xpath('dvd_release_date', '//div[contains(div,"DVD Release Date")]/div[@class="info"]/text()')
            loader.add_xpath('run_time', '//div[contains(div,"Run Time")]/div[@class="info"]/text()')
            loader.add_xpath('distributor', '//div[contains(div,"Distributor")]/div[@class="info"]/text()')
            loader.add_xpath('genre', '//div[contains(div,"Genre")]/div[@class="info"]/text()')
            loader.add_xpath('mpaa_rating', '//div[contains(div,"MPAA Rating")]/div[@class="info"]/text()')
            loader.add_xpath('director', '//div[contains(div,"Director")]/div[@class="info"]/text()')
            loader.add_value('starring', ', '.join(site.select('//div[contains(div,"Starring")]/div[@class="info"]/a/text()').extract()))
            loader.add_xpath('plot', '//meta[@property="og:description"]/@content')
            loader.add_xpath('sd480P', '//div[@class="hd-trailers"]/span[2]/a/@href')
            loader.add_xpath('hd720P', '//div[@class="hd-trailers"]/span[3]/a/@href')
            loader.add_xpath('hd1080P', '//div[@class="hd-trailers"]/span[4]/a/@href')
            loader.add_xpath('poster', '//div[@class="movie-info-poster"]/img/@src')
            loader.add_value('url', response.url)
            items.append(loader.load_item())
        return items

class Website(Item):
    title = Field()
    theatrical_release_date = Field()
    dvd_release_date = Field()
    run_time = Field()
    distributor = Field()
    genre = Field()
    mpaa_rating = Field()
    director = Field()
    starring = Field()
    plot = Field()
    sd480P = Field()
    hd720P = Field()
    hd1080P = Field()
    poster = Field()
    url = Field()

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
        
    run_spider(MoviefoneSpider(), settings)

if __name__ == 'scraper':
    main()