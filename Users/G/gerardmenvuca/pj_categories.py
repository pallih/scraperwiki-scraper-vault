import scraperwiki
#import re
import time
import urllib
import lxml.html
#import mechanize

#from BeautifulSoup import BeautifulSoup
from urlparse import urlparse, parse_qsl
#from lxml import etree


scraperwiki.metadata.save('data_columns', ['code','url', 'label','level'])


def scrape_table(al):
        record = {}
        dic = dict(parse_qsl(urlparse(al)[4]))
        print dic
        if len(dic):
            

            pos1 = int(al.find("&listePas="))
            pos2 = int(al.find(";&profondeur"))
            strlbl =al[pos1+10:pos2]
            lpos1=int(strlbl.rfind(";"))
            lpos2=int(strlbl.find(":",lpos1))        

            record['url'] = al[0:al.find('#')]
            record['label'] = strlbl[lpos1+1:lpos2]
            print record['label'] 
            if lpos1<0  :
                rec = dic['listePas'] 
                rec = rec[0:rec.find(':')] 
                record['label'] = rec     
            record['code'] = dic["codeRubrique"]
            record['level'] = dic["profondeur"]            
            scraperwiki.datastore.save(["code"], record)
            
            
        

def scrape_and_look_for_next_link(url):
    root = lxml.html.parse(url).getroot()
    ullist = root.xpath("//li/a/@href")
    new_url = ""
    for a in ullist:
        new_url = a
        if urlparse(new_url)[4]!=''  :
            scrape_table(new_url)
            time.sleep(1)
            scrape_and_look_for_next_link(new_url[0:new_url.find('#')])

# ---------------------------------------------------------------------------
# START HERE
# ---------------------------------------------------------------------------
base_url = 'http://www.pagesjaunes.fr/scg/guideActivite.do'
scrape_and_look_for_next_link(base_url)import scraperwiki
#import re
import time
import urllib
import lxml.html
#import mechanize

#from BeautifulSoup import BeautifulSoup
from urlparse import urlparse, parse_qsl
#from lxml import etree


scraperwiki.metadata.save('data_columns', ['code','url', 'label','level'])


def scrape_table(al):
        record = {}
        dic = dict(parse_qsl(urlparse(al)[4]))
        print dic
        if len(dic):
            

            pos1 = int(al.find("&listePas="))
            pos2 = int(al.find(";&profondeur"))
            strlbl =al[pos1+10:pos2]
            lpos1=int(strlbl.rfind(";"))
            lpos2=int(strlbl.find(":",lpos1))        

            record['url'] = al[0:al.find('#')]
            record['label'] = strlbl[lpos1+1:lpos2]
            print record['label'] 
            if lpos1<0  :
                rec = dic['listePas'] 
                rec = rec[0:rec.find(':')] 
                record['label'] = rec     
            record['code'] = dic["codeRubrique"]
            record['level'] = dic["profondeur"]            
            scraperwiki.datastore.save(["code"], record)
            
            
        

def scrape_and_look_for_next_link(url):
    root = lxml.html.parse(url).getroot()
    ullist = root.xpath("//li/a/@href")
    new_url = ""
    for a in ullist:
        new_url = a
        if urlparse(new_url)[4]!=''  :
            scrape_table(new_url)
            time.sleep(1)
            scrape_and_look_for_next_link(new_url[0:new_url.find('#')])

# ---------------------------------------------------------------------------
# START HERE
# ---------------------------------------------------------------------------
base_url = 'http://www.pagesjaunes.fr/scg/guideActivite.do'
scrape_and_look_for_next_link(base_url)