from scrapy.spider import BaseSpider
import lxml.html 
from scrapy.item import Item



class Webspider(BaseSpider):
    name = 'subcrawler'
    allowed_domains = ['paratyquantum.info/']
    start_urls = ['http://paratyquantum.info/']

    def parse(self, response):
        root = lxml.html.fromhtml(response)

        items = []

        item = Item()
        item['url'] = response
        items.append(item)
        
        return items
     

crawler = Webspider()

crawler.start_requests()

print crawler.itemsfrom scrapy.spider import BaseSpider
import lxml.html 
from scrapy.item import Item



class Webspider(BaseSpider):
    name = 'subcrawler'
    allowed_domains = ['paratyquantum.info/']
    start_urls = ['http://paratyquantum.info/']

    def parse(self, response):
        root = lxml.html.fromhtml(response)

        items = []

        item = Item()
        item['url'] = response
        items.append(item)
        
        return items
     

crawler = Webspider()

crawler.start_requests()

print crawler.items