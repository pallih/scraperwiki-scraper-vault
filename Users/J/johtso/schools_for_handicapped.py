if __name__ == 'scraper':
    import scraperwiki
    scrapy_utils = scraperwiki.utils.swimport("scrapy_utils")
else:
    import scrapy_utils

from urlparse import urljoin

from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Identity, Compose
from scrapy.utils.misc import arg_to_iter
from scrapy import log
import lxml.html as lh



class HandiSpider(BaseSpider):
    name = 'handischools'
    allowed_domains = ['good-practice.bibb.de']
    start_urls = ['https://good-practice.bibb.de/adb/suche.php?action=result&adressliste=1']
    item_aim = 0
    total_scraped = 0
    def parse(self, response):
        tree = lh.fromstring(response.body)
        

        table = tree.xpath("//table[2]")[0]
        
        rows = table.xpath("tr")[1:]
        self.item_aim = len(rows)
        for row in rows:
            loader = ExclusionLoader()
            cells = row.xpath("td")
            loader.add_values(cells, 'main_listing')

            next_url = cells[0].xpath('.//a')[0].attrib['href']
            next_url = urljoin(response.url, next_url)

            yield Request(next_url, callback=self.parse_details, meta={'loader':loader})
    
    def parse_details(self, response):
        tree = lh.fromstring(response.body)
        loader = response.meta['loader']

        website = tree.xpath("//td[text()='Internet:']/following-sibling::td[1]")[0]
        loader.add_value('website', website)

        project_table = tree.xpath("//h3[text()='Eines unserer Projekte']/../following-sibling::div/table")[0]

        rows = project_table.xpath("tr")
        project_name = rows.pop(0).xpath("td[2]")
        loader.add_value('project_title', project_name)
        for row in rows:
            title_cell, data_cell = row.xpath("td")
            data_title = scrapy_utils.norm_title(title_cell.text_content())
            data_title = 'project_'+data_title
            if data_title:
                loader.add_value(data_title, data_cell)
    
        return loader.load_item()

class ExclusionItem(scrapy_utils.FlexibleItem):
    unique_keys = ['id']

class ExclusionLoader(scrapy_utils.MultiLoader):
    default_item_class = ExclusionItem

    keys = {
            'main_listing':
                [('name', 'id'),
               'ansprechpartner',
               'strasse',
               'ort',
               'tel',
               'fax',
               'email',],
           }
    
    default_keys = keys['main_listing']

    default_input_processor = MapCompose(lambda x: x.xpath('string()'), lambda x: x.strip())
    default_output_processor = TakeFirst()

    def extract_id(url):
        uid = scrapy_utils.url_query(url)['id'][0]
        return arg_to_iter(uid)
    
    def extract_url(cell):
        links = cell.xpath('.//a')
        if links:
            url = links[0].attrib['href']
        else:
            url = ''
        return arg_to_iter(url)

    id_in = MapCompose(extract_url, extract_id)
    website_in = Compose(extract_url)

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
    settings.overrides['LOG_LEVEL'] = 'INFO'#'DEBUG'#
    settings.overrides['HTTPCACHE_ENABLED'] = True
    #settings.overrides['CLOSESPIDER_ITEMCOUNT'] = 3
    #settings.overrides['CONCURRENT_REQUESTS'] = 10
    #settings.overrides['DOWNLOAD_DELAY'] = 1
    settings.overrides['SAVE_BUFFER'] = 20
    # settings.overrides['CONCURRENT_ITEMS'] = 200

    if __name__ == 'scraper':
        settings.overrides['ITEM_PIPELINES'] = [scrapy_utils.SWPipeline]


    run_spider(HandiSpider(), settings)

main()

    

    if __name__ == 'scraper':
    import scraperwiki
    scrapy_utils = scraperwiki.utils.swimport("scrapy_utils")
else:
    import scrapy_utils

from urlparse import urljoin

from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Identity, Compose
from scrapy.utils.misc import arg_to_iter
from scrapy import log
import lxml.html as lh



class HandiSpider(BaseSpider):
    name = 'handischools'
    allowed_domains = ['good-practice.bibb.de']
    start_urls = ['https://good-practice.bibb.de/adb/suche.php?action=result&adressliste=1']
    item_aim = 0
    total_scraped = 0
    def parse(self, response):
        tree = lh.fromstring(response.body)
        

        table = tree.xpath("//table[2]")[0]
        
        rows = table.xpath("tr")[1:]
        self.item_aim = len(rows)
        for row in rows:
            loader = ExclusionLoader()
            cells = row.xpath("td")
            loader.add_values(cells, 'main_listing')

            next_url = cells[0].xpath('.//a')[0].attrib['href']
            next_url = urljoin(response.url, next_url)

            yield Request(next_url, callback=self.parse_details, meta={'loader':loader})
    
    def parse_details(self, response):
        tree = lh.fromstring(response.body)
        loader = response.meta['loader']

        website = tree.xpath("//td[text()='Internet:']/following-sibling::td[1]")[0]
        loader.add_value('website', website)

        project_table = tree.xpath("//h3[text()='Eines unserer Projekte']/../following-sibling::div/table")[0]

        rows = project_table.xpath("tr")
        project_name = rows.pop(0).xpath("td[2]")
        loader.add_value('project_title', project_name)
        for row in rows:
            title_cell, data_cell = row.xpath("td")
            data_title = scrapy_utils.norm_title(title_cell.text_content())
            data_title = 'project_'+data_title
            if data_title:
                loader.add_value(data_title, data_cell)
    
        return loader.load_item()

class ExclusionItem(scrapy_utils.FlexibleItem):
    unique_keys = ['id']

class ExclusionLoader(scrapy_utils.MultiLoader):
    default_item_class = ExclusionItem

    keys = {
            'main_listing':
                [('name', 'id'),
               'ansprechpartner',
               'strasse',
               'ort',
               'tel',
               'fax',
               'email',],
           }
    
    default_keys = keys['main_listing']

    default_input_processor = MapCompose(lambda x: x.xpath('string()'), lambda x: x.strip())
    default_output_processor = TakeFirst()

    def extract_id(url):
        uid = scrapy_utils.url_query(url)['id'][0]
        return arg_to_iter(uid)
    
    def extract_url(cell):
        links = cell.xpath('.//a')
        if links:
            url = links[0].attrib['href']
        else:
            url = ''
        return arg_to_iter(url)

    id_in = MapCompose(extract_url, extract_id)
    website_in = Compose(extract_url)

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
    settings.overrides['LOG_LEVEL'] = 'INFO'#'DEBUG'#
    settings.overrides['HTTPCACHE_ENABLED'] = True
    #settings.overrides['CLOSESPIDER_ITEMCOUNT'] = 3
    #settings.overrides['CONCURRENT_REQUESTS'] = 10
    #settings.overrides['DOWNLOAD_DELAY'] = 1
    settings.overrides['SAVE_BUFFER'] = 20
    # settings.overrides['CONCURRENT_ITEMS'] = 200

    if __name__ == 'scraper':
        settings.overrides['ITEM_PIPELINES'] = [scrapy_utils.SWPipeline]


    run_spider(HandiSpider(), settings)

main()

    

    