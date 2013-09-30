import scraperwiki
import mechanize, urllib, logging
from BeautifulSoup import BeautifulSoup
class Techcrunch:


    def __init__(self):
        self.browser = mechanize.Browser()
        self.browser.set_handle_robots(False)
        self.BASE_URL = 'http://www.techcrunch.com/'


    def action(self):
        resp = self.browser.open(self.BASE_URL)
        html = resp.read()
        soup = BeautifulSoup(html)

        news_chunk1 = soup.fetch('div',{'class':'item'})
        news_chunk2 = soup.fetch('div',{'class':'headline'})
        news_chunk3 = soup.fetch('div',{'class':'body-copy'})

        for new in news_chunk1:
            head = new.findAll('a')
            for hd in head:
                print_ = str(hd).split('=')
                print print_[3].replace('''"thumb" src''','').replace('onclick', '').replace('"','').replace('&nbsp;', '')
                


run = Techcrunch()
run.action()
    import scraperwiki
import mechanize, urllib, logging
from BeautifulSoup import BeautifulSoup
class Techcrunch:


    def __init__(self):
        self.browser = mechanize.Browser()
        self.browser.set_handle_robots(False)
        self.BASE_URL = 'http://www.techcrunch.com/'


    def action(self):
        resp = self.browser.open(self.BASE_URL)
        html = resp.read()
        soup = BeautifulSoup(html)

        news_chunk1 = soup.fetch('div',{'class':'item'})
        news_chunk2 = soup.fetch('div',{'class':'headline'})
        news_chunk3 = soup.fetch('div',{'class':'body-copy'})

        for new in news_chunk1:
            head = new.findAll('a')
            for hd in head:
                print_ = str(hd).split('=')
                print print_[3].replace('''"thumb" src''','').replace('onclick', '').replace('"','').replace('&nbsp;', '')
                


run = Techcrunch()
run.action()
    