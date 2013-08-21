import urllib, scraperwiki
try:
    import json
except ImportError:
    import simplejson as json

from scrapely.htmlpage import HtmlPage
from scrapely.template import TemplateMaker, best_match
from scrapely.extraction import InstanceBasedLearningExtractor
from scrapely import Scraper

class Scraper2(Scraper):

    def train(self, url=None, data=None, html=None, encoding='utf-8'):
        assert data, "Cannot train with empty data"
        page = self._get_page(url, encoding, html)
        tm = TemplateMaker(page)
        for field, values in data.items():
            if not hasattr(values, '__iter__'):
                values = [values]
            for value in values:
                if isinstance(value, str):
                    value = value.decode(encoding)
                tm.annotate(field, best_match(value))
        self.templates.append(tm.get_template())

    def scrape(self, url=None, html=None, encoding='utf-8'): 
        ## not version from https://github.com/scrapy/scrapely/blob/master/scrapely/extraction/pageparsing.py
        ## may need to replace with version from inspect.getsourcelines(Scraper.scrape), as this version is

        page = self._get_page(url, encoding, html)
        ex = InstanceBasedLearningExtractor(self.templates)
        return ex.extract(page)[0]

    @staticmethod
    def _get_page(url=None, encoding=None, html=None):
        if html:
            body=html.decode(encoding)
        else:
            body = urllib.urlopen(url).read().decode(encoding)
        return HtmlPage(url, body=body, encoding=encoding)

### Basic usage:
### s=Scraper2()
### data = {'name':'value pairs'} # like normal Scrapely
### s.train(data=data, html=string_of_html)
### output = s.scrape(html=different_string_of_html)

### Everything below this line is an example from https://github.com/scrapy/scrapely, with edits.

s = Scraper2()                             # note how we're *not* using Scraper() - this uses our custom version
url1 = 'http://pypi.python.org/pypi/w3lib'
html1 = scraperwiki.scrape(url1)           # get the HTML - this could be the output from mechanize
data = {'name': 'w3lib 1.0', 'author': 'Scrapy project', 'description': 'Library of web-related functions'}
s.train(data)                  # pick one of these lines
#s.train(url1,data)
url2 = 'http://pypi.python.org/pypi/Django/1.3'
html2 = scraperwiki.scrape(url2)
print s.scrape(None, html2)               # pick one of these lines.
#print s.scrape(url2)