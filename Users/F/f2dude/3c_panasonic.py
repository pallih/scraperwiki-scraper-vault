import scraperwiki
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item, Field
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import MapCompose, Join
from w3lib.html import remove_tags, unquote_markup

## define Item Camera with Fields we want to extract
class Camera(Item):
    url = Field()
    model = Field()
    typ = Field()
    focusmodes = Field()
    price = Field()
    description = Field()
    url = Field()

## ItemLoader with general input and output processors to clean data stored in Item
class CamLoader(XPathItemLoader):
    default_item_class = Camera
    default_input_processor = MapCompose(remove_tags, unquote_markup, unicode.strip)
    default_output_processor = Join()

## BaseSpider which fetches three urls of the Models we are interested in
class PanasonicSpider(BaseSpider):
    name = "panasonic"
    allowed_domains = ["panasonic.de"]
    start_urls = [
            'http://www.panasonic.de/html/de_DE/Produkte/Lumix+Digitalkameras/LUMIX+G+DSLM/DMC-GF5/Technische+Daten/9397076/index.html',
            'http://www.panasonic.de/html/de_DE/Produkte/Lumix+Digitalkameras/LUMIX+G+DSLM/DMC-GX1/Technische+Daten/8314315/index.html',
            'http://www.panasonic.de/html/de_DE/Produkte/Lumix+Digitalkameras/LUMIX+G+DSLM/DMC-GF3/Technische+Daten/7732394/index.html',
        ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        il = CamLoader(response=response)
        ## add xpath selectors for the fields we want to extract
        il.add_xpath('model', './/*[@id="RANGE_content"]/div[1]/div[1]/div/h2[1]')
        il.add_xpath('typ', '//table[@class="tableLayout inwidth4 specifications"][1]/tbody/tr[1]/td[2]/text()')
        il.add_xpath('focusmodes', '//table[@class="tableLayout inwidth4 specifications"][4]/tbody/tr[2]/td[2]/text()')
        il.add_xpath('price', '//span[@class="priceValue"][1]/text()')
        il.add_xpath('description', '//*[@id="RANGE_content"]/div[1]/div[1]/div/div/ul/li/text()')
        il.add_value('url', response.url)
        return il.load_item()



if __name__ == 'scraper':
    # Store scraped item to sqlite
    from scrapy.xlib.pydispatch import dispatcher
    from scrapy import signals
    def _item_scraped(item, spider):
        scraperwiki.sqlite.save(['model'], data=dict(item), verbose=0)
        print ('Parsed Model: %s !' % item['model'])

    # Listen for signal item_scraped and call my _item_scraped()
    dispatcher.connect(_item_scraped, signals.item_scraped)

    # Run scrapy spider using `runspider` command
    from scrapy.cmdline import execute
    execute(['scrapy', 'runspider', 'script.py'])
import scraperwiki
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item, Field
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import MapCompose, Join
from w3lib.html import remove_tags, unquote_markup

## define Item Camera with Fields we want to extract
class Camera(Item):
    url = Field()
    model = Field()
    typ = Field()
    focusmodes = Field()
    price = Field()
    description = Field()
    url = Field()

## ItemLoader with general input and output processors to clean data stored in Item
class CamLoader(XPathItemLoader):
    default_item_class = Camera
    default_input_processor = MapCompose(remove_tags, unquote_markup, unicode.strip)
    default_output_processor = Join()

## BaseSpider which fetches three urls of the Models we are interested in
class PanasonicSpider(BaseSpider):
    name = "panasonic"
    allowed_domains = ["panasonic.de"]
    start_urls = [
            'http://www.panasonic.de/html/de_DE/Produkte/Lumix+Digitalkameras/LUMIX+G+DSLM/DMC-GF5/Technische+Daten/9397076/index.html',
            'http://www.panasonic.de/html/de_DE/Produkte/Lumix+Digitalkameras/LUMIX+G+DSLM/DMC-GX1/Technische+Daten/8314315/index.html',
            'http://www.panasonic.de/html/de_DE/Produkte/Lumix+Digitalkameras/LUMIX+G+DSLM/DMC-GF3/Technische+Daten/7732394/index.html',
        ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        il = CamLoader(response=response)
        ## add xpath selectors for the fields we want to extract
        il.add_xpath('model', './/*[@id="RANGE_content"]/div[1]/div[1]/div/h2[1]')
        il.add_xpath('typ', '//table[@class="tableLayout inwidth4 specifications"][1]/tbody/tr[1]/td[2]/text()')
        il.add_xpath('focusmodes', '//table[@class="tableLayout inwidth4 specifications"][4]/tbody/tr[2]/td[2]/text()')
        il.add_xpath('price', '//span[@class="priceValue"][1]/text()')
        il.add_xpath('description', '//*[@id="RANGE_content"]/div[1]/div[1]/div/div/ul/li/text()')
        il.add_value('url', response.url)
        return il.load_item()



if __name__ == 'scraper':
    # Store scraped item to sqlite
    from scrapy.xlib.pydispatch import dispatcher
    from scrapy import signals
    def _item_scraped(item, spider):
        scraperwiki.sqlite.save(['model'], data=dict(item), verbose=0)
        print ('Parsed Model: %s !' % item['model'])

    # Listen for signal item_scraped and call my _item_scraped()
    dispatcher.connect(_item_scraped, signals.item_scraped)

    # Run scrapy spider using `runspider` command
    from scrapy.cmdline import execute
    execute(['scrapy', 'runspider', 'script.py'])
