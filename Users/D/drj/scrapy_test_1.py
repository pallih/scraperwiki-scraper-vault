# Forked for SEGV
from __future__ import with_statement

if __name__ == 'scraper':
    import scraperwiki
    scrapy_utils = scraperwiki.utils.swimport("scrapy_utils")
else:
    import scrapy_utils

import os
from mmap import mmap
import re
import time
import pickle
import tempfile
import unicodedata
from urlparse import urlparse, parse_qs, urljoin

import lxml.html as lh
from lxml import etree

from scrapy.http import Request
from scrapy.item import Item, Field
from scrapy.spider import BaseSpider
from scrapy import log
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Identity
from scrapy.utils.misc import extract_regex
from scrapy.utils.misc import arg_to_iter





class HealthFraudSpider(BaseSpider):
    name = "healthfraud"
    allowed_domains = ['exclusions.oig.hhs.gov']
    #start_urls = ['http://exclusions.oig.hhs.gov/ExclusionTypeCounts.aspx']
    start_urls = ['http://exclusions.oig.hhs.gov/ExclTypeDetails.aspx?id=14']

    def parse(self, response):
        current_url = response.url
        print 'FINISHED DOWNLOADING', current_url

        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfilename = tfile.name
        tfile.write(response.body)
        del response
        tfile.seek(0)
        print 'RESPONSE NOW IN TEMP FILE'
    
        
        context = etree.iterparse(tfile, events=('start', 'end'), html=True)
        in_table = False
        header_row = True
        while context:
            try:
                event, el = context.next()
                if not in_table:
                    if (event == 'start') and (el.tag == 'table') and (el.attrib['id'] == 'dgResult'):
                        print 'found the table'
                        in_table = True
                elif (event == 'end') and (el.tag == 'tr'):
                    print 'found a row'
                    if header_row:
                        header_row = False
                        continue
                    row = el
                    loader = ExclusionLoader()
                    cells = row.xpath("td")
                    loader.add_values(cells)
                    yield loader.load_item()
                elif (event == 'end') and (el.tag == 'table') and (el.attrib['id'] == 'toc'):
                    print 'Done!'
                    break
                while el.getprevious() is not None:
                    del el.getparent()[0]

            except etree.XMLSyntaxError, e:
                print e.msg
                lineno = int(re.search(r'line (\d+),', e.msg).group(1))
                remove_line(tfilename, lineno)
                tfile = open(tfilename)
                context = etree.iterparse(tfile, events=('start', 'end'), html=True)
            except KeyError:
                print 'oops keyerror'







def remove_line(filename, lineno):
    f=os.open(filename, os.O_RDWR)
    m=mmap(f,0)
    p=0
    for i in range(lineno-1):
        p=m.find('\n',p)+1
    q=m.find('\n',p)
    m[p:q] = ' '*(q-p)
    os.close(f)

def no_cache(url):
    return url+'&'+str(time.time())

class ExclusionItem(scrapy_utils.FlexibleItem):
    unique_keys = ['id']

class ExclusionLoader(scrapy_utils.MultiLoader):
    default_item_class = ExclusionItem

    keys = ['last_name',
           'first_name',
           'business_name',
           'general',
           'specialty',
           'exclusion',
           'state',
           'id',]

    default_input_processor = MapCompose(lambda x: x.xpath('string()'), lambda x: x.strip())
    default_output_processor = TakeFirst()

    def extract_id(self, id_cell):
        jsfunction = id_cell.xpath('.//a')[0].attrib['href']
        uid = extract_regex(r'javascript:VerifyID\((\d+)\)', jsfunction)
        return arg_to_iter(uid)
    
    id_in = extract_id

def run_spider(spider, settings):
    from scrapy.crawler import CrawlerProcess
    crawler = CrawlerProcess(settings)
    crawler.install()
    crawler.configure()
    crawler.crawl(spider)
    log.start()
    crawler.start()

def monkeypatch_load_object():
    from scrapy.utils import misc
    orig_load_object = misc.load_object
    def good_load_object(path):
        if not isinstance(path, basestring):
            return path
        else:
            return orig_load_object(path)
    misc.load_object = good_load_object

def main():    
    monkeypatch_load_object()
    from scrapy.conf import settings
    
    settings.overrides['LOG_ENABLED'] = True
    settings.overrides['LOG_LEVEL'] = 'INFO'
    settings.overrides['HTTPCACHE_ENABLED'] = True
    # settings.overrides['CLOSESPIDER_ITEMCOUNT'] = 500
    # settings.overrides['CONCURRENT_REQUESTS'] = 1
    # settings.overrides['CONCURRENT_ITEMS'] = 200

    if __name__ == 'scraper':
        #settings.overrides['ITEM_PIPELINES'] = [scrapy_utils.SWPipeline]
        pass

    run_spider(HealthFraudSpider(), settings)

main()# Forked for SEGV
from __future__ import with_statement

if __name__ == 'scraper':
    import scraperwiki
    scrapy_utils = scraperwiki.utils.swimport("scrapy_utils")
else:
    import scrapy_utils

import os
from mmap import mmap
import re
import time
import pickle
import tempfile
import unicodedata
from urlparse import urlparse, parse_qs, urljoin

import lxml.html as lh
from lxml import etree

from scrapy.http import Request
from scrapy.item import Item, Field
from scrapy.spider import BaseSpider
from scrapy import log
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Identity
from scrapy.utils.misc import extract_regex
from scrapy.utils.misc import arg_to_iter





class HealthFraudSpider(BaseSpider):
    name = "healthfraud"
    allowed_domains = ['exclusions.oig.hhs.gov']
    #start_urls = ['http://exclusions.oig.hhs.gov/ExclusionTypeCounts.aspx']
    start_urls = ['http://exclusions.oig.hhs.gov/ExclTypeDetails.aspx?id=14']

    def parse(self, response):
        current_url = response.url
        print 'FINISHED DOWNLOADING', current_url

        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfilename = tfile.name
        tfile.write(response.body)
        del response
        tfile.seek(0)
        print 'RESPONSE NOW IN TEMP FILE'
    
        
        context = etree.iterparse(tfile, events=('start', 'end'), html=True)
        in_table = False
        header_row = True
        while context:
            try:
                event, el = context.next()
                if not in_table:
                    if (event == 'start') and (el.tag == 'table') and (el.attrib['id'] == 'dgResult'):
                        print 'found the table'
                        in_table = True
                elif (event == 'end') and (el.tag == 'tr'):
                    print 'found a row'
                    if header_row:
                        header_row = False
                        continue
                    row = el
                    loader = ExclusionLoader()
                    cells = row.xpath("td")
                    loader.add_values(cells)
                    yield loader.load_item()
                elif (event == 'end') and (el.tag == 'table') and (el.attrib['id'] == 'toc'):
                    print 'Done!'
                    break
                while el.getprevious() is not None:
                    del el.getparent()[0]

            except etree.XMLSyntaxError, e:
                print e.msg
                lineno = int(re.search(r'line (\d+),', e.msg).group(1))
                remove_line(tfilename, lineno)
                tfile = open(tfilename)
                context = etree.iterparse(tfile, events=('start', 'end'), html=True)
            except KeyError:
                print 'oops keyerror'







def remove_line(filename, lineno):
    f=os.open(filename, os.O_RDWR)
    m=mmap(f,0)
    p=0
    for i in range(lineno-1):
        p=m.find('\n',p)+1
    q=m.find('\n',p)
    m[p:q] = ' '*(q-p)
    os.close(f)

def no_cache(url):
    return url+'&'+str(time.time())

class ExclusionItem(scrapy_utils.FlexibleItem):
    unique_keys = ['id']

class ExclusionLoader(scrapy_utils.MultiLoader):
    default_item_class = ExclusionItem

    keys = ['last_name',
           'first_name',
           'business_name',
           'general',
           'specialty',
           'exclusion',
           'state',
           'id',]

    default_input_processor = MapCompose(lambda x: x.xpath('string()'), lambda x: x.strip())
    default_output_processor = TakeFirst()

    def extract_id(self, id_cell):
        jsfunction = id_cell.xpath('.//a')[0].attrib['href']
        uid = extract_regex(r'javascript:VerifyID\((\d+)\)', jsfunction)
        return arg_to_iter(uid)
    
    id_in = extract_id

def run_spider(spider, settings):
    from scrapy.crawler import CrawlerProcess
    crawler = CrawlerProcess(settings)
    crawler.install()
    crawler.configure()
    crawler.crawl(spider)
    log.start()
    crawler.start()

def monkeypatch_load_object():
    from scrapy.utils import misc
    orig_load_object = misc.load_object
    def good_load_object(path):
        if not isinstance(path, basestring):
            return path
        else:
            return orig_load_object(path)
    misc.load_object = good_load_object

def main():    
    monkeypatch_load_object()
    from scrapy.conf import settings
    
    settings.overrides['LOG_ENABLED'] = True
    settings.overrides['LOG_LEVEL'] = 'INFO'
    settings.overrides['HTTPCACHE_ENABLED'] = True
    # settings.overrides['CLOSESPIDER_ITEMCOUNT'] = 500
    # settings.overrides['CONCURRENT_REQUESTS'] = 1
    # settings.overrides['CONCURRENT_ITEMS'] = 200

    if __name__ == 'scraper':
        #settings.overrides['ITEM_PIPELINES'] = [scrapy_utils.SWPipeline]
        pass

    run_spider(HealthFraudSpider(), settings)

main()