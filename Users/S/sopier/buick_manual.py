import scraperwiki
import re

class Scraper(object):
    
    PRE_URL = 'http://www.extendedgmwarranty.com'    

    def __init__(self, url):
        self.url = url

    def get_pdf(self):
        html = scraperwiki.scrape(self.url)
        data = re.findall(re.compile(r"/owners-manual.*\.pdf"), html)
        for i in data:
            container = {'url': self.PRE_URL + i}
            scraperwiki.sqlite.save(unique_keys=[], data=container)


s = Scraper('http://www.extendedgmwarranty.com/owners-manual/buick_owner_manuals.html')
s.get_pdf()