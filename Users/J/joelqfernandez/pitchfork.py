#!/usr/bin/env python

import scraperwiki
import re
import unicodedata
from urllib import quote

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

#from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from scrapy.item import Item, Field
from scrapy.http import Request
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import MapCompose, TakeFirst

from scrapy.conf import settings
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/534.56.5 (KHTML, like Gecko) Version/5.1.6 Safari/534.56.5'
DEPTH_LIMIT = '1'
from scrapy import log

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

class PitchforkSpider(CrawlSpider):
    name = 'pitchfork'
    start_urls = [
    'http://pitchfork.com/reviews/best/albums/1/'
    ]
    allowed_domains = [
    'pitchfork.com',
    'kat.ph',
    'bing.com' ]

    rules = (
    ## Pitchfork - Best New Albums
    Rule(SgmlLinkExtractor(allow=('/reviews/best/[albums],[tracks],[reissues]/[1-9],[0-9][0-9]/'))),
    Rule(SgmlLinkExtractor(restrict_xpaths=('//*[@id="main"]/div/span[2]/a','//span[@class="page-number current-page "]/a'))),
    #Rule(SgmlLinkExtractor(restrict_xpaths=('//tr[2]/td/div[@class="iaconbox floatright"]'))),
    Rule(SgmlLinkExtractor(restrict_xpaths=('//*[@id="main"]/ul/li/div[2]/a')), callback='parseItem', follow=True)
    ## Pitchfork - All Albums
    #Rule(SgmlLinkExtractor(allow=('/reviews/[albums],[tracks],[reissues]/[1-999]/'))),
    #Rule(SgmlLinkExtractor(restrict_xpaths=('//*[@id="main"]/div/span[2]/a','//span[@class="page-number current-page "]/a'))),
    #Rule(SgmlLinkExtractor(restrict_xpaths=('//*[@id="main"]/ul/li/ul/li/a')), callback='parseItem', follow=True)
    )

    def parseItem(self, response):
        hxs = HtmlXPathSelector(response)
        links = hxs.select('//*[@id="main"]')
        for link in links:
            artist = link.select('ul/li/div/h1/a/text()').extract() [0]
            album = link.select('ul/li/div/h2/text()').extract() [0]
            kat_base_url = "http://kat.ph/search/"
            kat_search_string = "/?field=size&sorder=desc"
            kat_slug_string = artist + ' ' + album
            
            kat_slug = unicodedata.normalize('NFKD', kat_slug_string)
            kat_slug = kat_slug.encode('ascii', 'ignore').lower()
            kat_slug = re.sub(r'[^a-z0-9]+', '-', kat_slug).strip('-')
            kat_slug = re.sub(r'[-]+', '-', kat_slug)
            kat_slug = kat_base_url + kat_slug + kat_search_string
            
            bing_base_url = "http://www.bing.com/images/search?&q="
            bing_search_string = "&qft=+filterui:imagesize-large"
            bing_slug_string = artist + '+' + album
            
            bing_slug = unicodedata.normalize('NFKD', bing_slug_string)
            bing_slug = bing_slug.encode('ascii', 'ignore').lower()
            bing_slug = re.sub(r'[^a-z0-9]+', '-', bing_slug).strip('-')
            bing_slug = re.sub(r'[-]+', '+', bing_slug)
            bing_slug = bing_base_url + bing_slug + bing_search_string
            yield Request(bing_slug, self.parseImage)
            
    def parseImage(self, response):
        hxs = HtmlXPathSelector(response)
        images=hxs.select('//div[@class="border imgres"]')
        items = []
        for image in images:
            img_src = image.select('div[1]/a/@t3')
            loader = WebsiteLoader(selector=image)
            loader.add_value('cover', img_src)
            items.append(loader.load_item())
            
        return items


google = "http://www.google.com/search?as_st=y&tbm=isch&hl=en&as_q=&as_epq="
artist_google = link.select('ul/li/div/h1/a/text()').extract() [0]
artist_google = re.sub(' ', '+', artist_google)
album_google = link.select('ul/li/div/h2/text()').extract() [0]
lbum_google = re.sub(' ', '+', album_google)
cover_search = google + ('%22' + artist_google + '%22') + '+' + ('%22' + album_google + '%22')
loader = WebsiteLoader(selector=link)
loader.add_value('torrent', album_search)
loader.add_value('cover', cover_search)
loader.add_xpath('album', 'ul/li/div/h2/text()')
loader.add_xpath('artist', 'ul/li/div/h1/a/text()')
loader.add_xpath('score', 'ul/li/div/span/text()')
loader.add_xpath('pub_date', 'ul/li/div[2]/h4/span[@class="pub-date"]/text()')
loader.add_xpath('img_src', 'ul/li/div/img/@src')
loader.add_value('url', response.url)
items.append(loader.load_item())



class Website(Item):
    flac = Field()
    torrent = Field()
    cover = Field()
    mp3 = Field()
    link = Field()
    album = Field()
    artist = Field()
    img_src = Field()
    pub_date = Field()
    score = Field()
    amazon = Field()
    detail = Field()
    url = Field()
    page = Field()
    data_pk = Field()
    search = Field()
    
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
        unique_keys = spider.settings.get('SW_UNIQUE_KEYS', ['cover'])
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
        'SW_UNIQUE_KEYS': ['cover'],
        'ITEM_PIPELINES': ['script.SWPipeline'],
    }

    settings.overrides.update(options)
        
    run_spider(PitchforkSpider(), settings)

if __name__ == 'scraper':
    main()
