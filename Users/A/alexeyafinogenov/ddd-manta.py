# author: Clint Eastwood

# this is an example scraper, feel free to use lxml, soup or any other html parser (in this case pure regex - multi-threaded)
# the inserted data should use the schema listed here: 
# 
# if for a specific record, one of these fields is not found, use empty string "" as the record value
# only add the fields needed or provided by the page/scrape description
# use companyname as the unique key when writing to the database

# please name the scrapers ddd-<<short identifier>>, ie ddd-housewares-1

# use scraperwiki.sqlite.save_var("source", value) to save a string of the name of the source you scraped
# example scraperwiki.sqlite.save_var("source", "NAFST - Fancy Food Show")

# use scraperwiki.sqlite.save_var("author", value) to save your name
# example scraperwiki.sqlite.save_var("author", " Clint Eastwood")

# use this to save each record to the sql database : scraperwiki.sqlite.save(unique_keys=['companyname'], data=dict(my_data))

# for good practice, trim white space on the field values and use the cleaning functions provided below
# !!!!!make sure to use use safestr() to handle internatalization issues (can't write to sql datastore with i18n characters)!!!!!

# if you need to use a proxy (some sites block the ip of scraperwiki) - please use the following code
#proxy_url = "72.77.197.214:19629" (http://www.xroxy.com/proxy-country-US.htm has good ones to use)
#proxy = urllib2.ProxyHandler({'http': proxy_url})
#user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; v' + str(random.random())
#opener = urllib2.build_opener(proxy)
#opener.addheaders = [('User-agent', user_agent)]
#page_html = opener.open(url).read()
import re
import random
import requests
import datetime

import scraperwiki

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider, Rule

from scrapy.item import Item, Field
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import MapCompose, TakeFirst
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from scrapy.conf import settings
from scrapy.http import Request
from scrapy import log

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

def remove_html(string):
    return re.sub("<.*?>", "", string)

def strip_non_text(string):
    return re.sub("\n|\r|\t| |:","",string)


scraperwiki.sqlite.save_var("source", "www.manta.com")
scraperwiki.sqlite.save_var("author", "Alexey Afinogenov")

def process_value(value):
    m = re.search("/member/join/.*?rld=(.*?)&", value)
    if m:
        return m.group(1)
    return value

class MantaSpider(CrawlSpider):
    name = "manta"
    allowed_domains = ["manta.com"]
    start_urls = [
        'http://www.manta.com/mb_33_C2_000/food',
        'http://www.manta.com/mb_34_B81A5_000/cutlery',
        'http://www.manta.com/mb_34_B8107_000/fine_earthenware_whiteware_table_and_kitchen_articles',
        'http://www.manta.com/mb_34_B8277_000/household_cooking_equipment',
        'http://www.manta.com/mb_34_B834C_000/perfumes_cosmetics_and_other_toilet_preparations',
        'http://www.manta.com/mb_34_B63AE_000/book_stores',
        'http://www.manta.com/mb_34_B61B9_000/candy_nut_and_confectionery_stores',
        'http://www.manta.com/mb_34_B61C3_000/dairy_products_stores',
        'http://www.manta.com/mb_34_B6390_000/drug_stores_and_proprietary_stores',
        'http://www.manta.com/mb_34_B61AF_000/fruit_and_vegetable_markets',
        'http://www.manta.com/mb_34_B61F3_000/miscellaneous_food_stores',
        'http://www.manta.com/mb_34_B6399_000/liquor_stores',
        'http://www.manta.com/mb_34_B608D_000/groceries_general_line',
        'http://www.manta.com/mb_34_B619B_000/grocery_stores',
        'http://www.manta.com/mb_34_B61CD_000/retail_bakeries',
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('/mb_'), restrict_xpaths=('a[@name="Subcategory"]/../div[@class="cols"]')), follow=True),
        Rule(SgmlLinkExtractor(allow=('/c/'), deny=('/connections/recommendations'), process_value=process_value), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        my_data = []
        my_data.append(('datescraped', datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")))

        hxs = HtmlXPathSelector(response)
        decoded_email = hxs.select('//*[@id="profile-main_email"]/script/text()').extract()
        if decoded_email:
            decoded_email = decoded_email[0] 
            email = remove_html(''.join(re.findall('wr\("(.*?)"\)', decoded_email)))
            my_data.append(('email ', email )) 
            print email
        companyname = hxs.select('//*[@itemprop="name"]/text()').extract()[0] 
        my_data.append(('companyname', companyname)) 
        print companyname
        categories = hxs.select('//*[@id="profile-categories"]/a/text()|//*[@id="profile-categories"]/text()').extract()
        categories = ''.join(categories)
        my_data.append(('categories', categories)) 
        print categories
        maincategory = hxs.select('//*[@itemprop="breadcrumb"]/li/a/span/text()').extract()
        if maincategory:            
            maincategory = ' ~ '.join(maincategory[2:4])
            my_data.append(('maincategory', maincategory)) 
            print maincategory
        city = hxs.select('//*[@itemprop="addressLocality"]/text()').extract()
        if city:
            city = city[0]
            my_data.append(('city', city)) 
            print city
        state = hxs.select('//*[@itemprop="addressRegion"]/text()').extract()
        if state:
            state = state[0]
            my_data.append(('state', state)) 
            print state
        zip = hxs.select('//*[@itemprop="postalCode"]/text()').extract()
        if zip:
            zip = zip[0]
            my_data.append(('zip', zip)) 
            print zip
        country = 'U.S.'
        my_data.append(('country', country))
        print country
        address = hxs.select('//*[@itemprop="streetAddress"]/text()').extract()
        if address:
            address = address[0]
            my_data.append(('address', address))
            print address
        sourceurl = response.url
        my_data.append(('sourceurl', sourceurl))
        print sourceurl
        phonenumber = hxs.select('//*[@itemprop="telephone"]/text()').extract()
        if phonenumber:
            phonenumber = phonenumber[0]
            my_data.append(('phonenumber', phonenumber))
            print phonenumber 
        contact = hxs.select('//*[@class="udated-profile-info"]/p/a/text()').extract()
        if contact:
            contact = contact[0]
            contact1first, contact1last = contact.split(' ')
            my_data.append(('contact1first', contact1first))
            my_data.append(('contact1last', contact1last))
            print contact1first, contact1last
        contact_text = hxs.select('//*[@class="udated-profile-info"]/p/text()').extract()
        if contact_text:
            contact_text = contact_text[0]
            contact1title = contact_text.split(',')[1].strip()
            my_data.append(('contact1title', contact1title))
            print contact1title 
        description= hxs.select('//*[@itemprop="description"]/text()').extract()
        if description:
            description = description[0]
            my_data.append(('description', description))
            print description

        scraperwiki.sqlite.save(unique_keys=['companyname'], data=dict(my_data))

        return None


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
    }

    settings.overrides.update(options)
    
    run_spider(MantaSpider(), settings)

if __name__ == 'scraper':
    main()

# author: Clint Eastwood

# this is an example scraper, feel free to use lxml, soup or any other html parser (in this case pure regex - multi-threaded)
# the inserted data should use the schema listed here: 
# 
# if for a specific record, one of these fields is not found, use empty string "" as the record value
# only add the fields needed or provided by the page/scrape description
# use companyname as the unique key when writing to the database

# please name the scrapers ddd-<<short identifier>>, ie ddd-housewares-1

# use scraperwiki.sqlite.save_var("source", value) to save a string of the name of the source you scraped
# example scraperwiki.sqlite.save_var("source", "NAFST - Fancy Food Show")

# use scraperwiki.sqlite.save_var("author", value) to save your name
# example scraperwiki.sqlite.save_var("author", " Clint Eastwood")

# use this to save each record to the sql database : scraperwiki.sqlite.save(unique_keys=['companyname'], data=dict(my_data))

# for good practice, trim white space on the field values and use the cleaning functions provided below
# !!!!!make sure to use use safestr() to handle internatalization issues (can't write to sql datastore with i18n characters)!!!!!

# if you need to use a proxy (some sites block the ip of scraperwiki) - please use the following code
#proxy_url = "72.77.197.214:19629" (http://www.xroxy.com/proxy-country-US.htm has good ones to use)
#proxy = urllib2.ProxyHandler({'http': proxy_url})
#user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; v' + str(random.random())
#opener = urllib2.build_opener(proxy)
#opener.addheaders = [('User-agent', user_agent)]
#page_html = opener.open(url).read()
import re
import random
import requests
import datetime

import scraperwiki

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider, Rule

from scrapy.item import Item, Field
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import MapCompose, TakeFirst
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from scrapy.conf import settings
from scrapy.http import Request
from scrapy import log

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

def remove_html(string):
    return re.sub("<.*?>", "", string)

def strip_non_text(string):
    return re.sub("\n|\r|\t| |:","",string)


scraperwiki.sqlite.save_var("source", "www.manta.com")
scraperwiki.sqlite.save_var("author", "Alexey Afinogenov")

def process_value(value):
    m = re.search("/member/join/.*?rld=(.*?)&", value)
    if m:
        return m.group(1)
    return value

class MantaSpider(CrawlSpider):
    name = "manta"
    allowed_domains = ["manta.com"]
    start_urls = [
        'http://www.manta.com/mb_33_C2_000/food',
        'http://www.manta.com/mb_34_B81A5_000/cutlery',
        'http://www.manta.com/mb_34_B8107_000/fine_earthenware_whiteware_table_and_kitchen_articles',
        'http://www.manta.com/mb_34_B8277_000/household_cooking_equipment',
        'http://www.manta.com/mb_34_B834C_000/perfumes_cosmetics_and_other_toilet_preparations',
        'http://www.manta.com/mb_34_B63AE_000/book_stores',
        'http://www.manta.com/mb_34_B61B9_000/candy_nut_and_confectionery_stores',
        'http://www.manta.com/mb_34_B61C3_000/dairy_products_stores',
        'http://www.manta.com/mb_34_B6390_000/drug_stores_and_proprietary_stores',
        'http://www.manta.com/mb_34_B61AF_000/fruit_and_vegetable_markets',
        'http://www.manta.com/mb_34_B61F3_000/miscellaneous_food_stores',
        'http://www.manta.com/mb_34_B6399_000/liquor_stores',
        'http://www.manta.com/mb_34_B608D_000/groceries_general_line',
        'http://www.manta.com/mb_34_B619B_000/grocery_stores',
        'http://www.manta.com/mb_34_B61CD_000/retail_bakeries',
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('/mb_'), restrict_xpaths=('a[@name="Subcategory"]/../div[@class="cols"]')), follow=True),
        Rule(SgmlLinkExtractor(allow=('/c/'), deny=('/connections/recommendations'), process_value=process_value), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        my_data = []
        my_data.append(('datescraped', datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")))

        hxs = HtmlXPathSelector(response)
        decoded_email = hxs.select('//*[@id="profile-main_email"]/script/text()').extract()
        if decoded_email:
            decoded_email = decoded_email[0] 
            email = remove_html(''.join(re.findall('wr\("(.*?)"\)', decoded_email)))
            my_data.append(('email ', email )) 
            print email
        companyname = hxs.select('//*[@itemprop="name"]/text()').extract()[0] 
        my_data.append(('companyname', companyname)) 
        print companyname
        categories = hxs.select('//*[@id="profile-categories"]/a/text()|//*[@id="profile-categories"]/text()').extract()
        categories = ''.join(categories)
        my_data.append(('categories', categories)) 
        print categories
        maincategory = hxs.select('//*[@itemprop="breadcrumb"]/li/a/span/text()').extract()
        if maincategory:            
            maincategory = ' ~ '.join(maincategory[2:4])
            my_data.append(('maincategory', maincategory)) 
            print maincategory
        city = hxs.select('//*[@itemprop="addressLocality"]/text()').extract()
        if city:
            city = city[0]
            my_data.append(('city', city)) 
            print city
        state = hxs.select('//*[@itemprop="addressRegion"]/text()').extract()
        if state:
            state = state[0]
            my_data.append(('state', state)) 
            print state
        zip = hxs.select('//*[@itemprop="postalCode"]/text()').extract()
        if zip:
            zip = zip[0]
            my_data.append(('zip', zip)) 
            print zip
        country = 'U.S.'
        my_data.append(('country', country))
        print country
        address = hxs.select('//*[@itemprop="streetAddress"]/text()').extract()
        if address:
            address = address[0]
            my_data.append(('address', address))
            print address
        sourceurl = response.url
        my_data.append(('sourceurl', sourceurl))
        print sourceurl
        phonenumber = hxs.select('//*[@itemprop="telephone"]/text()').extract()
        if phonenumber:
            phonenumber = phonenumber[0]
            my_data.append(('phonenumber', phonenumber))
            print phonenumber 
        contact = hxs.select('//*[@class="udated-profile-info"]/p/a/text()').extract()
        if contact:
            contact = contact[0]
            contact1first, contact1last = contact.split(' ')
            my_data.append(('contact1first', contact1first))
            my_data.append(('contact1last', contact1last))
            print contact1first, contact1last
        contact_text = hxs.select('//*[@class="udated-profile-info"]/p/text()').extract()
        if contact_text:
            contact_text = contact_text[0]
            contact1title = contact_text.split(',')[1].strip()
            my_data.append(('contact1title', contact1title))
            print contact1title 
        description= hxs.select('//*[@itemprop="description"]/text()').extract()
        if description:
            description = description[0]
            my_data.append(('description', description))
            print description

        scraperwiki.sqlite.save(unique_keys=['companyname'], data=dict(my_data))

        return None


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
    }

    settings.overrides.update(options)
    
    run_spider(MantaSpider(), settings)

if __name__ == 'scraper':
    main()

