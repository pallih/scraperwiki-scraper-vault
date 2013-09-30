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

email_pattern = re.compile(r'''(?:[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?\.)+[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[A-Za-z0-9-]*[A-Za-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])''',re.IGNORECASE)
website_pattern = re.compile(r'''(\b(?:(?:https?|ftp|file)://|www\.|ftp\.)[-A-Z0-9+&@#/%=~_|$?!:,.]*[A-Z0-9+&@#/%=~_|$])''',re.IGNORECASE)
 
scraperwiki.sqlite.save_var("source", "groceryretailonline.com")
scraperwiki.sqlite.save_var("author", "Alexey Brilenkov")
SAFESTR_RX = re.compile("^u\'(.+)\'$")
def safestr(string):
    try:
        return english_string(string).encode('utf-8', 'replace')
    except:
        return re.sub(SAFESTR_RX, '\1', repr(string))

class GrItem(Item):
    datescraped = Field()
    emails = Field()
    companyname = Field()
    dba = Field()
    website = Field()
    categories = Field()
    maincategory = Field()
    city = Field()
    state = Field()
    zip = Field()
    country = Field()
    address = Field()
    address2 = Field()
    boothnum = Field()
    sourceurl = Field()
    salesmethod = Field()
    phonenumber = Field()
    faxnumber = Field()
    contact1first = Field()
    contact1last = Field()
    contact1title = Field()
    contact2first = Field()
    contact2last = Field()
    contact2title = Field()
    contact3first = Field()
    contact3last = Field()
    contact3title = Field()
    yearfounded = Field()
    description = Field()
    certifications = Field()
    contactlink = Field()

class GrLoader(XPathItemLoader):
    default_item_class = GrItem
    default_input_processor = MapCompose(remove_tags, unquote_markup, unicode.strip)
    default_output_processor = Join()

class GrSpider(CrawlSpider):
    name = "groceryretailonline"
    allowed_domains = ["groceryretailonline.com"]
    start_urls = ('http://www.groceryretailonline.com/BuyersGuide.mvc/Sponsors',)

    rules = (
        #Rule(SgmlLinkExtractor(restrict_xpaths=('//*[@id="categories"]/li/ul/li/span/a','//*[@id="categories"]/li/ul/li/ul/li/span/a'))),
        Rule(SgmlLinkExtractor(restrict_xpaths=('//*[@id="pager"]/span/a',))),   
Rule(SgmlLinkExtractor(allow=('.*/CompanyDetail/.*'),restrict_xpaths=('//*[@class="company"]/a',)),callback='parse_item'),)                                           

    def parse_item(self, response):
        item = GrItem() 
        soup = BeautifulSoup(response.body)
        hxs = HtmlXPathSelector(response=response)

        item['datescraped'] = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")
        item['sourceurl'] = response.url
        try:
            item['companyname'] = safestr(''.join(hxs.select('//*[@class="companylink big"]/text()').extract()))
        except:
            item['companyname'] = None
        try:
            item['emails'] = ','.join(set(email_pattern.findall(str(response.body))))
        except:
            item['emails'] = None
        try:
            item['dba'] = None #???
        except:
            item['dba'] = None
        try:
            item['categories'] = safestr(re.sub('\s+',' ',re.sub('<[^<>]+>|&[a-z]+;',' ',','.join(hxs.select('//*[@class="companycategory"]').extract()))).strip().replace('&#13;',''))
        except:
            item['categories'] = None
        try:
            item['maincategory'] = safestr(''.join(hxs.select('//*[@class="toplevelcategory"]/text()').extract()))
        except:
            item['maincategory'] = None
        
        try:
            item['address'] = safestr(soup.find('span',{'class':'companylink big'}).nextSibling.nextSibling)
        except:
            item['address'] = None
        try:
            csp = soup.find('span',{'class':'companylink big'}).nextSibling.nextSibling.nextSibling.nextSibling.replace('&nbsp;','').split(',')
        except:
            pass
        try:
            item['city'] = safestr(csp[0])
        except:
            item['city'] = None
        try:
            item['state'] = safestr(csp[1].strip().split(' ')[0].strip())
        except:
            item['state'] = None
        try:
            item['zip'] = safestr(csp[1].strip().split(' ')[-1].strip())
        except:
            item['zip'] = None
        if item['state'] in item['zip']:
            item['state'] = None
        
        try:
            item['country'] = safestr(soup.find('span',{'class':'companylink big'}).nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.replace('&nbsp;','').replace('\r\n',''))
        except:
            item['country'] = None
        try:
            labels = soup.find('div',{'id':'col1_content'}).findAll('label')
        except:
            labels = []

        for label in labels:
            if 'Phone:' in label.text:
                try:
                    if '<br />' not in label.nextSibling:
                        item['phonenumber'] = label.nextSibling
                    else:
                        item['phonenumber'] = None
                except:
                    item['phonenumber'] = None
            elif 'Fax:' in label.text:
                try:
                    if '<br />' not in label.nextSibling:
                        item['faxnumber'] = label.nextSibling
                    else:
                        item['faxnumber'] = None
                except:
                    item['faxnumber'] = None
            elif 'Contact:' in label.text:
                try:
                    item['contact1first'] = safestr(label.nextSibling.split(' ')[0].strip())
                except:
                    item['contact1first'] = None
                try:
                    item['contact1last'] = safestr(label.nextSibling.split(' ')[-1].strip())
                except:
                    item['contact1last'] = None


        return item 

if __name__ == 'scraper':
    from scrapy.xlib.pydispatch import dispatcher
    from scrapy import signals

    def _item_scraped(item, spider):
        scraperwiki.sqlite.save(unique_keys=['companyname'], data=dict(item), verbose=0)

    dispatcher.connect(_item_scraped, signals.item_scraped)

    from scrapy.cmdline import execute
    execute(['scrapy', 'runspider', 'script.py'])import os, sys
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

email_pattern = re.compile(r'''(?:[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?\.)+[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[A-Za-z0-9-]*[A-Za-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])''',re.IGNORECASE)
website_pattern = re.compile(r'''(\b(?:(?:https?|ftp|file)://|www\.|ftp\.)[-A-Z0-9+&@#/%=~_|$?!:,.]*[A-Z0-9+&@#/%=~_|$])''',re.IGNORECASE)
 
scraperwiki.sqlite.save_var("source", "groceryretailonline.com")
scraperwiki.sqlite.save_var("author", "Alexey Brilenkov")
SAFESTR_RX = re.compile("^u\'(.+)\'$")
def safestr(string):
    try:
        return english_string(string).encode('utf-8', 'replace')
    except:
        return re.sub(SAFESTR_RX, '\1', repr(string))

class GrItem(Item):
    datescraped = Field()
    emails = Field()
    companyname = Field()
    dba = Field()
    website = Field()
    categories = Field()
    maincategory = Field()
    city = Field()
    state = Field()
    zip = Field()
    country = Field()
    address = Field()
    address2 = Field()
    boothnum = Field()
    sourceurl = Field()
    salesmethod = Field()
    phonenumber = Field()
    faxnumber = Field()
    contact1first = Field()
    contact1last = Field()
    contact1title = Field()
    contact2first = Field()
    contact2last = Field()
    contact2title = Field()
    contact3first = Field()
    contact3last = Field()
    contact3title = Field()
    yearfounded = Field()
    description = Field()
    certifications = Field()
    contactlink = Field()

class GrLoader(XPathItemLoader):
    default_item_class = GrItem
    default_input_processor = MapCompose(remove_tags, unquote_markup, unicode.strip)
    default_output_processor = Join()

class GrSpider(CrawlSpider):
    name = "groceryretailonline"
    allowed_domains = ["groceryretailonline.com"]
    start_urls = ('http://www.groceryretailonline.com/BuyersGuide.mvc/Sponsors',)

    rules = (
        #Rule(SgmlLinkExtractor(restrict_xpaths=('//*[@id="categories"]/li/ul/li/span/a','//*[@id="categories"]/li/ul/li/ul/li/span/a'))),
        Rule(SgmlLinkExtractor(restrict_xpaths=('//*[@id="pager"]/span/a',))),   
Rule(SgmlLinkExtractor(allow=('.*/CompanyDetail/.*'),restrict_xpaths=('//*[@class="company"]/a',)),callback='parse_item'),)                                           

    def parse_item(self, response):
        item = GrItem() 
        soup = BeautifulSoup(response.body)
        hxs = HtmlXPathSelector(response=response)

        item['datescraped'] = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")
        item['sourceurl'] = response.url
        try:
            item['companyname'] = safestr(''.join(hxs.select('//*[@class="companylink big"]/text()').extract()))
        except:
            item['companyname'] = None
        try:
            item['emails'] = ','.join(set(email_pattern.findall(str(response.body))))
        except:
            item['emails'] = None
        try:
            item['dba'] = None #???
        except:
            item['dba'] = None
        try:
            item['categories'] = safestr(re.sub('\s+',' ',re.sub('<[^<>]+>|&[a-z]+;',' ',','.join(hxs.select('//*[@class="companycategory"]').extract()))).strip().replace('&#13;',''))
        except:
            item['categories'] = None
        try:
            item['maincategory'] = safestr(''.join(hxs.select('//*[@class="toplevelcategory"]/text()').extract()))
        except:
            item['maincategory'] = None
        
        try:
            item['address'] = safestr(soup.find('span',{'class':'companylink big'}).nextSibling.nextSibling)
        except:
            item['address'] = None
        try:
            csp = soup.find('span',{'class':'companylink big'}).nextSibling.nextSibling.nextSibling.nextSibling.replace('&nbsp;','').split(',')
        except:
            pass
        try:
            item['city'] = safestr(csp[0])
        except:
            item['city'] = None
        try:
            item['state'] = safestr(csp[1].strip().split(' ')[0].strip())
        except:
            item['state'] = None
        try:
            item['zip'] = safestr(csp[1].strip().split(' ')[-1].strip())
        except:
            item['zip'] = None
        if item['state'] in item['zip']:
            item['state'] = None
        
        try:
            item['country'] = safestr(soup.find('span',{'class':'companylink big'}).nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.replace('&nbsp;','').replace('\r\n',''))
        except:
            item['country'] = None
        try:
            labels = soup.find('div',{'id':'col1_content'}).findAll('label')
        except:
            labels = []

        for label in labels:
            if 'Phone:' in label.text:
                try:
                    if '<br />' not in label.nextSibling:
                        item['phonenumber'] = label.nextSibling
                    else:
                        item['phonenumber'] = None
                except:
                    item['phonenumber'] = None
            elif 'Fax:' in label.text:
                try:
                    if '<br />' not in label.nextSibling:
                        item['faxnumber'] = label.nextSibling
                    else:
                        item['faxnumber'] = None
                except:
                    item['faxnumber'] = None
            elif 'Contact:' in label.text:
                try:
                    item['contact1first'] = safestr(label.nextSibling.split(' ')[0].strip())
                except:
                    item['contact1first'] = None
                try:
                    item['contact1last'] = safestr(label.nextSibling.split(' ')[-1].strip())
                except:
                    item['contact1last'] = None


        return item 

if __name__ == 'scraper':
    from scrapy.xlib.pydispatch import dispatcher
    from scrapy import signals

    def _item_scraped(item, spider):
        scraperwiki.sqlite.save(unique_keys=['companyname'], data=dict(item), verbose=0)

    dispatcher.connect(_item_scraped, signals.item_scraped)

    from scrapy.cmdline import execute
    execute(['scrapy', 'runspider', 'script.py'])