from urlparse import urljoin
import requests
import lxml.html
import mechanize

def parse(html):
    return lxml.html.fromstring(html)

class HolsteinScraper(object):
    """docstring for HolsteinScraper"""
    def __init__(self):
        self.root_url = 'http://schulportraets.schleswig-holstein.de/portal/schule_suchen/'
        self.school_urls = []
        self.browser = mechanize.Browser()
    
    def start(self):
        br = self.browser
        br.open(self.root_url)

        self.search()
        print br.response().read()
        print br.forms()
        self.collect_urls()

        print self.school_urls

    def search(self):
        br = self.browser
        br.select_form(nr=0)
        items = br.form.find_control(name='sform[]').items
        br.form['sform[]'] = [item.name for item in items]
        return br.submit()

    def collect_urls(self):
        

        self.extract_links()
        
    
    def extract_links(self):
        br = self.browser
        tree = parse(br.response().read())
        links = tree.cssselect('div#content b a')
        for link in links:
            abs_url = urljoin(self.root_url, link.attrib['href'])
            self.school_urls.append(abs_url)


    def download_data(self):
        pass

def main():
    scraper = HolsteinScraper()
    scraper.start()

main()