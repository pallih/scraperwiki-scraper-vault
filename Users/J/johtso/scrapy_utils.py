import re
import scraperwiki
from scrapy.item import Item, Field
from scrapy.contrib.loader import ItemLoader
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import unicodedata
from urlparse import urlparse, parse_qs
import pickle
from scrapy.utils.misc import arg_to_iter

class SWStorage(object):
    def __init__(self):
        pass 
        
    def __getattr__(self, name):
        return pickle.loads(scraperwiki.sqlite.get_var(name))
    def __setattr__(self, name, value):
        return scraperwiki.sqlite.save_var(name, pickle.dumps(value))
    __getitem__ = __getattr__
    __setitem__ = __setattr__

class SWPipeline(object):
    def __init__(self):
        self.data = []
        self.counter = 0
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def process_item(self, item, spider):
        save_buffer = spider.settings['SAVE_BUFFER']
        self.data.append(dict(item))
        if len(self.data) >= save_buffer:
            self.write_data(spider)
        return item

    def spider_closed(self, spider):
        self.write_data(spider)
    
    def write_data(self, spider):
        #print 'SAVING %i' % (len(self.data), )
        scraperwiki.sqlite.save(unique_keys=['id'], data=self.data)
        #print 'SAVED %i' % (len(self.data), )
        if hasattr(spider, 'item_aim') and hasattr(spider, 'total_scraped'):
            spider.total_scraped += len(self.data)
            print '%i out of %i' % (spider.total_scraped, spider.item_aim)
        self.data = []


class FlexibleFields(dict):
    def __getitem__(self, key):
        if key not in self:
            self[key] = Field()
        return dict.__getitem__(self, key)

class FlexibleItem(Item):
    def __init__(self, *args, **kwargs):
        super(FlexibleItem, self).__init__(*args, **kwargs)
        object.__setattr__(self, 'fields', FlexibleFields())

class MultiLoader(ItemLoader):
    def __init__(self, item=None, keys=None, **context):
        if keys:
            self.keys = default_keys
        super(MultiLoader, self).__init__(item, **context)
    
    def add_values(self, values, keys=None):
        if not keys:
            keys = self.default_keys
        elif isinstance(keys, basestring):
            keys = self.keys[keys]
        
        for k, v in zip(keys, values):
            if k:
                for k in arg_to_iter(k):
                    self.add_value(k, v)

def url_query(url):
    return parse_qs(urlparse(url).query)

def norm_title(title_string):
    try:
        # if the title is a unicode string, normalize it
        title_string = unicodedata.normalize('NFKD', title_string).encode('ascii','ignore')
    except TypeError:
        # if it was not a unicode string => OK, do nothing
        pass
    
    ts = re.sub(r'[^\w\s]', '', title_string.lower())
    ts = ts.strip()
    ts = ts.replace(' ', '_')
    return ts

def following_elements(el, stop_tags):
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