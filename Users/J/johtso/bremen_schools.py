import unicodedata
from urlparse import urlparse, parse_qs, urljoin

if __name__ == 'scraper':
    import scraperwiki

import lxml.html as lh

from scrapy.http import Request
from scrapy.item import Item, Field
from scrapy.spider import BaseSpider
from scrapy import log
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Identity
from scrapy.contrib.loader import ItemLoader

def url_query(url):
    return parse_qs(urlparse(url).query)

class SWPipeline(object):
    def process_item(self, item, spider):
        scraperwiki.sqlite.save(unique_keys=['school_id'], data=dict(item))

def abs_url(base_url, url):
    return urljoin(base_url, url)

class BremenSpider(BaseSpider):
    """Our ad-hoc spider"""
    name = "bremen"
    allowed_domains = ['bildung.bremen.de']
    start_urls = ['http://bildung.bremen.de/sixcms/detail.php?template=35_schuls'
                  'uche_stufe2_d&gsid=bremen117.c.22634.de&schul_name=*&schulform'
                  '=*&stadtteile=*&privatschulen_show=&var_sort=snr']

    question_list_xpath = '//div[@id="content"]//div[contains(@class, "question-summary")]'

    def parse(self, response):
        tree = lh.fromstring(response.body)

        for link in tree.cssselect('div.table_daten_container > a'):
            url = abs_url(response.url, link.attrib['href'])
            yield Request(url, callback=self.parse_school)

    def parse_school(self, response):
        tree = lh.fromstring(response.body)

        loader = SchoolLoader()

        school_id = url_query(response.url)['Sid']
        loader.add_value('school_id', school_id)

        # extract basic info:
        school_name = tree.xpath('//div[@id="vk_stammdaten"]/h1')[0].text
        loader.add_value('school_name', school_name)

        for img in tree.xpath("//div[@id='vk_stammdaten_inner']//img"):
            info_title = norm_title(img.attrib['alt'])

            if info_title == 'Homepage':
                info = img.xpath("../following-sibling::td[1]/a")[0].attrib['href']
            else:
                info = img.xpath("../following-sibling::td[1]")[0].text_content()

            loader.add_value(info_title, info)
        
        # extract detailed stuff:
        titles = tree.xpath("//div[@id='main_content']//h3")
        if titles:
            last_title = titles.pop()
            for title in titles:
                info_title = norm_title(title.text)
                info_els = self.following_elements(title, stop_tags=['h3'])
                info = '\n'.join([el.text_content() for el in info_els if el.text_content()])
                loader.add_value(info_title, info)
            
            info_title = norm_title(last_title.text)
            info_els = self.following_elements(last_title, stop_tags=['br', 'div', 'h3'])
            info = '\n'.join([el.text_content() for el in info_els if el.text_content()])
            loader.add_value(info_title, info)
        
        return loader.load_item()

    def following_elements(self, el, stop_tags):
        els = []
        for el in el.xpath("following-sibling::*"):
            try:
                tag = el.tag
            except AttributeError:
                tag = None

            if tag in stop_tags:
                break
            else:
                els.append(el)
        return els

def norm_title(title_string):
    try:
        # if the title is a unicode string, normalize it
        title_string = unicodedata.normalize('NFKD', title_string).encode('ascii','ignore')
    except TypeError:
        # if it was not a unicode string => OK, do nothing
        pass
    
    return title_string.strip(': ')

class FlexibleFields(dict):
    def __getitem__(self, key):
        if key not in self:
            self[key] = Field()
        return dict.__getitem__(self, key)

class FlexibleItem(Item):
    def __init__(self, *args, **kwargs):
        super(FlexibleItem, self).__init__(*args, **kwargs)
        object.__setattr__(self, 'fields', FlexibleFields())

class SchoolItem(FlexibleItem):
    school_id = Field(
        input_processor=Identity(),
        output_processor=TakeFirst(),
    )

class SchoolLoader(ItemLoader):
    default_item_class = SchoolItem

    default_input_processor = MapCompose(lambda x:x.strip())
    default_output_processor = TakeFirst()

def add_field_if_none(item, field):
    if field not in item:
        item[field] = Field()

class FlexibleLoader(ItemLoader):
    def add_value(self, field_name, value, *processors, **kw):
        value = self.get_value(value, *processors, **kw)
        if value is None:
            return
        if not field_name:
            for k,v in value.iteritems():
                add_field_if_none(self.item, k)
                self._add_value(k, v)
        else:
            add_field_if_none(self.item, field_name)
            self._add_value(field_name, value)

    default_item_class = FlexibleItem

def run_spider(spider, settings):
    from scrapy.crawler import CrawlerProcess
    crawler = CrawlerProcess(settings)
    crawler.install()
    crawler.configure()

    # schedule spider
    crawler.crawl(spider)
    
    log.start()
    # start engine scrapy/twisted
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
    # settings.overrides['LOG_ENABLED'] = True

    if __name__ == 'scraper':
        settings.overrides['ITEM_PIPELINES'] = [SWPipeline]

    #settings.overrides['CLOSESPIDER_ITEMCOUNT'] = 5
    settings.overrides['CONCURRENT_REQUESTS'] = 3

    run_spider(BremenSpider(), settings)

main()import unicodedata
from urlparse import urlparse, parse_qs, urljoin

if __name__ == 'scraper':
    import scraperwiki

import lxml.html as lh

from scrapy.http import Request
from scrapy.item import Item, Field
from scrapy.spider import BaseSpider
from scrapy import log
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Identity
from scrapy.contrib.loader import ItemLoader

def url_query(url):
    return parse_qs(urlparse(url).query)

class SWPipeline(object):
    def process_item(self, item, spider):
        scraperwiki.sqlite.save(unique_keys=['school_id'], data=dict(item))

def abs_url(base_url, url):
    return urljoin(base_url, url)

class BremenSpider(BaseSpider):
    """Our ad-hoc spider"""
    name = "bremen"
    allowed_domains = ['bildung.bremen.de']
    start_urls = ['http://bildung.bremen.de/sixcms/detail.php?template=35_schuls'
                  'uche_stufe2_d&gsid=bremen117.c.22634.de&schul_name=*&schulform'
                  '=*&stadtteile=*&privatschulen_show=&var_sort=snr']

    question_list_xpath = '//div[@id="content"]//div[contains(@class, "question-summary")]'

    def parse(self, response):
        tree = lh.fromstring(response.body)

        for link in tree.cssselect('div.table_daten_container > a'):
            url = abs_url(response.url, link.attrib['href'])
            yield Request(url, callback=self.parse_school)

    def parse_school(self, response):
        tree = lh.fromstring(response.body)

        loader = SchoolLoader()

        school_id = url_query(response.url)['Sid']
        loader.add_value('school_id', school_id)

        # extract basic info:
        school_name = tree.xpath('//div[@id="vk_stammdaten"]/h1')[0].text
        loader.add_value('school_name', school_name)

        for img in tree.xpath("//div[@id='vk_stammdaten_inner']//img"):
            info_title = norm_title(img.attrib['alt'])

            if info_title == 'Homepage':
                info = img.xpath("../following-sibling::td[1]/a")[0].attrib['href']
            else:
                info = img.xpath("../following-sibling::td[1]")[0].text_content()

            loader.add_value(info_title, info)
        
        # extract detailed stuff:
        titles = tree.xpath("//div[@id='main_content']//h3")
        if titles:
            last_title = titles.pop()
            for title in titles:
                info_title = norm_title(title.text)
                info_els = self.following_elements(title, stop_tags=['h3'])
                info = '\n'.join([el.text_content() for el in info_els if el.text_content()])
                loader.add_value(info_title, info)
            
            info_title = norm_title(last_title.text)
            info_els = self.following_elements(last_title, stop_tags=['br', 'div', 'h3'])
            info = '\n'.join([el.text_content() for el in info_els if el.text_content()])
            loader.add_value(info_title, info)
        
        return loader.load_item()

    def following_elements(self, el, stop_tags):
        els = []
        for el in el.xpath("following-sibling::*"):
            try:
                tag = el.tag
            except AttributeError:
                tag = None

            if tag in stop_tags:
                break
            else:
                els.append(el)
        return els

def norm_title(title_string):
    try:
        # if the title is a unicode string, normalize it
        title_string = unicodedata.normalize('NFKD', title_string).encode('ascii','ignore')
    except TypeError:
        # if it was not a unicode string => OK, do nothing
        pass
    
    return title_string.strip(': ')

class FlexibleFields(dict):
    def __getitem__(self, key):
        if key not in self:
            self[key] = Field()
        return dict.__getitem__(self, key)

class FlexibleItem(Item):
    def __init__(self, *args, **kwargs):
        super(FlexibleItem, self).__init__(*args, **kwargs)
        object.__setattr__(self, 'fields', FlexibleFields())

class SchoolItem(FlexibleItem):
    school_id = Field(
        input_processor=Identity(),
        output_processor=TakeFirst(),
    )

class SchoolLoader(ItemLoader):
    default_item_class = SchoolItem

    default_input_processor = MapCompose(lambda x:x.strip())
    default_output_processor = TakeFirst()

def add_field_if_none(item, field):
    if field not in item:
        item[field] = Field()

class FlexibleLoader(ItemLoader):
    def add_value(self, field_name, value, *processors, **kw):
        value = self.get_value(value, *processors, **kw)
        if value is None:
            return
        if not field_name:
            for k,v in value.iteritems():
                add_field_if_none(self.item, k)
                self._add_value(k, v)
        else:
            add_field_if_none(self.item, field_name)
            self._add_value(field_name, value)

    default_item_class = FlexibleItem

def run_spider(spider, settings):
    from scrapy.crawler import CrawlerProcess
    crawler = CrawlerProcess(settings)
    crawler.install()
    crawler.configure()

    # schedule spider
    crawler.crawl(spider)
    
    log.start()
    # start engine scrapy/twisted
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
    # settings.overrides['LOG_ENABLED'] = True

    if __name__ == 'scraper':
        settings.overrides['ITEM_PIPELINES'] = [SWPipeline]

    #settings.overrides['CLOSESPIDER_ITEMCOUNT'] = 5
    settings.overrides['CONCURRENT_REQUESTS'] = 3

    run_spider(BremenSpider(), settings)

main()