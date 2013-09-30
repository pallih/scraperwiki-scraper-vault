import os, sys
import scraperwiki
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import MapCompose, Join
from w3lib.html import remove_tags, unquote_markup
from scrapy.item import Item, Field


class SpeakerItem(Item):
    name = Field()
    description = Field()
    image = Field()


class SpeakerLoader(XPathItemLoader):
    default_item_class = SpeakerItem
    default_input_processor = MapCompose(remove_tags, unquote_markup, unicode.strip)
    default_output_processor = Join()


class SpeakersSpider(BaseSpider):
    name = "speakers"
    allowed_domains = ["eventioz.com"]
    start_urls = (
            'https://eventioz.com/events/python-day-uruguay-2011/speakers',
        )

    def parse(self, response):
        hxs = HtmlXPathSelector(response=response)
        for sel in hxs.select('//div[@class="speaker_container"]'):
            il = SpeakerLoader(selector=sel)
            il.add_xpath('name', './/div[@class="speaker_name"]/text()')
            il.add_xpath('image', './/div[@class="speaker_image"]/img/@src')
            il.add_xpath('description', './/div[@class="speaker_description"]/*')
            yield il.load_item()


if __name__ == 'scraper':
    # Save scraped item to sqlite
    from scrapy.xlib.pydispatch import dispatcher
    from scrapy import signals
    def _item_scraped(item, spider):
        scraperwiki.sqlite.save(['name'], data=dict(item), verbose=0)

    dispatcher.connect(_item_scraped, signals.item_scraped)

    # Run scrapy spider using `runspider` command
    from scrapy.cmdline import execute
    execute(['scrapy', 'runspider', 'script.py'])
import os, sys
import scraperwiki
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import MapCompose, Join
from w3lib.html import remove_tags, unquote_markup
from scrapy.item import Item, Field


class SpeakerItem(Item):
    name = Field()
    description = Field()
    image = Field()


class SpeakerLoader(XPathItemLoader):
    default_item_class = SpeakerItem
    default_input_processor = MapCompose(remove_tags, unquote_markup, unicode.strip)
    default_output_processor = Join()


class SpeakersSpider(BaseSpider):
    name = "speakers"
    allowed_domains = ["eventioz.com"]
    start_urls = (
            'https://eventioz.com/events/python-day-uruguay-2011/speakers',
        )

    def parse(self, response):
        hxs = HtmlXPathSelector(response=response)
        for sel in hxs.select('//div[@class="speaker_container"]'):
            il = SpeakerLoader(selector=sel)
            il.add_xpath('name', './/div[@class="speaker_name"]/text()')
            il.add_xpath('image', './/div[@class="speaker_image"]/img/@src')
            il.add_xpath('description', './/div[@class="speaker_description"]/*')
            yield il.load_item()


if __name__ == 'scraper':
    # Save scraped item to sqlite
    from scrapy.xlib.pydispatch import dispatcher
    from scrapy import signals
    def _item_scraped(item, spider):
        scraperwiki.sqlite.save(['name'], data=dict(item), verbose=0)

    dispatcher.connect(_item_scraped, signals.item_scraped)

    # Run scrapy spider using `runspider` command
    from scrapy.cmdline import execute
    execute(['scrapy', 'runspider', 'script.py'])
