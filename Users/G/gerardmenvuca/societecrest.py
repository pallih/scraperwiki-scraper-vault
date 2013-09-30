import scraperwiki
#import re
import time
import urllib
import lxml.html
import mechanize

#from BeautifulSoup import BeautifulSoup
from urlparse import urlparse, parse_qsl
#from lxml import etree


scraperwiki.metadata.save('data_columns', ['siret','nom', 'adresse','rcs','activite'])


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
            
def load_data_from_url(url):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.set_handle_referer(False)
    reponse = br.open(url).read()
    data = lxml.html.document_fromstring(reponse)
    return data  
         
def scrap_data(url):
    record = {}
    print url
    root = load_data_from_url(url)
    print root
    record['siret'] = root.xpath("//td[@class='main']/table/tbody/tr[5]/td/table/tbody/tr/td[1]/table/tbody/tr[7]/td/table/tbody/tr[1]/td[2]/table/tbody/tr[1]/td[2]")
    print record['siret'] 
    #scraperwiki.datastore.save(["siret"], record)    

def scrape_and_look_for_next_link(url):

    root = load_data_from_url(url) 
    print root
    ullist = root.xpath('//a[@class=Ablk2]')
    print ullist 
    new_url = ""
    #[a.attrib['href'] for a in result.xpath("//a[@target='_blank']")]
    for a in ullist:
        new_url = a
        print a.attrib['href']
        scrap_data(base_site + a.attrib['href'])
        time.sleep(10)
        #if urlparse(new_url)[4]!=''  :
            #print(
            #scrap_data(new_url)
            #scrape_table(new_url)
            #time.sleep(1)
            #scrape_and_look_for_next_link(new_url[0:new_url.find('#')])

# ---------------------------------------------------------------------------
# START HERE
# ---------------------------------------------------------------------------
base_site = 'http://www.societe.com' 
base_url = base_site +'/cgi-bin/listeens?nom=&naf=47&adr=&num=&ville=Crest&dep=26&imageField=Rechercher&debut=1'

scrape_and_look_for_next_link(base_url)import scraperwiki
#import re
import time
import urllib
import lxml.html
import mechanize

#from BeautifulSoup import BeautifulSoup
from urlparse import urlparse, parse_qsl
#from lxml import etree


scraperwiki.metadata.save('data_columns', ['siret','nom', 'adresse','rcs','activite'])


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
            
def load_data_from_url(url):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.set_handle_referer(False)
    reponse = br.open(url).read()
    data = lxml.html.document_fromstring(reponse)
    return data  
         
def scrap_data(url):
    record = {}
    print url
    root = load_data_from_url(url)
    print root
    record['siret'] = root.xpath("//td[@class='main']/table/tbody/tr[5]/td/table/tbody/tr/td[1]/table/tbody/tr[7]/td/table/tbody/tr[1]/td[2]/table/tbody/tr[1]/td[2]")
    print record['siret'] 
    #scraperwiki.datastore.save(["siret"], record)    

def scrape_and_look_for_next_link(url):

    root = load_data_from_url(url) 
    print root
    ullist = root.xpath('//a[@class=Ablk2]')
    print ullist 
    new_url = ""
    #[a.attrib['href'] for a in result.xpath("//a[@target='_blank']")]
    for a in ullist:
        new_url = a
        print a.attrib['href']
        scrap_data(base_site + a.attrib['href'])
        time.sleep(10)
        #if urlparse(new_url)[4]!=''  :
            #print(
            #scrap_data(new_url)
            #scrape_table(new_url)
            #time.sleep(1)
            #scrape_and_look_for_next_link(new_url[0:new_url.find('#')])

# ---------------------------------------------------------------------------
# START HERE
# ---------------------------------------------------------------------------
base_site = 'http://www.societe.com' 
base_url = base_site +'/cgi-bin/listeens?nom=&naf=47&adr=&num=&ville=Crest&dep=26&imageField=Rechercher&debut=1'

scrape_and_look_for_next_link(base_url)