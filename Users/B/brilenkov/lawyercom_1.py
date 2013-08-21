import os, sys
import scraperwiki
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import MapCompose, Join
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from w3lib.html import remove_tags, unquote_markup
from scrapy.item import Item, Field
import datetime
import re
from BeautifulSoup import BeautifulSoup
from scrapy import log, signals
from scrapy.http import Request
COOKIES_ENABLED = True
COOKIES_DEBUG = True
email_pattern = re.compile(r'''(href="#birdmessage")''',re.IGNORECASE)
 
scraperwiki.sqlite.save_var("source", "lawyercom.ru")
SAFESTR_RX = re.compile("^u\'(.+)\'$")
def safestr(string):
    try:
        return english_string(string).encode('utf-8', 'replace')
    except:
        return re.sub(SAFESTR_RX, '\1', repr(string))

class GrItem(Item):
    url = Field()
    found = Field()


class GrLoader(XPathItemLoader):
    default_item_class = GrItem
    default_input_processor = MapCompose(remove_tags, unquote_markup, unicode.strip)
    default_output_processor = Join()

class GrSpider(CrawlSpider):
    COOKIES_ENABLED = True
    COOKIES_DEBUG = True
    name = "lawyercom"
    login_page = 'http://www.lawyercom.ru/login/'
    allowed_domains = ["lawyercom.ru"]
    start_urls = ('http://www.lawyercom.ru',)

    rules = (Rule(SgmlLinkExtractor(restrict_xpaths=('//a',)),callback='parse_item'),)                                           

    def start_requests(self):
        log.msg("start_requests", log.DEBUG)
        return self.init_request()

    def init_request(self):
        log.msg("init_request ", log.DEBUG)
        """This function is called before crawling starts."""
        return Request(url=self.login_page, callback=self.login)

    def login(self, response):
        log.msg("Trying login ", log.DEBUG)
        """Generate a login request."""
        return FormRequest.from_response(response,
                    formdata={'username': 'smartyunknown@gmail.com', 'password': 'alexandg'},
                    callback=self.check_login_response)

    def check_login_response(self, response):
        log.msg("check_login_response ", log.DEBUG)
        """Check the response returned by a login request to see if we are
        successfully logged in.
        """
        if "section" in response.body:
            log.msg("check_login_response (1)", log.DEBUG)

            self.log("Successfully logged in. Let's start crawling!")
            # Now the crawling can begin..
            self.initialized()
        else:
            log.msg("check_login_response (2)", log.DEBUG)
            self.log("Bad times :(")
            # Something went wrong, we couldn't log in, so nothing happens.

    def parse_item(self, response):
        log.msg("parse_item", log.DEBUG)
        item = GrItem() 
        soup = BeautifulSoup(response.body)
        hxs = HtmlXPathSelector(response=response)

        item['url'] = response.url
        try:
            item['found'] = ','.join(set(email_pattern.findall(str(response.body))))
        except:
            item['found'] = None

        return item 

if __name__ == 'scraper':
    COOKIES_ENABLED = True
    COOKIES_DEBUG = True
    from scrapy.xlib.pydispatch import dispatcher
    from scrapy import signals

    def _item_scraped(item, spider):
        scraperwiki.sqlite.save(unique_keys=['url'], data=dict(item), verbose=0)

    dispatcher.connect(_item_scraped, signals.item_scraped)

    from scrapy.cmdline import execute
    execute(['scrapy', 'runspider', 'script.py'])