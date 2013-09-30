import scraperwiki,re
from BeautifulSoup import BeautifulSoup
import lxml.html
import re

starturl = 'http://www.althingi.is/vefur/altutg.html'


def replace_all(text, dic):
        for i, j in dic.iteritems():
            text = text.replace(i, j)
        return text

replacements = {'dómsmrh.':'','efnahrh.':'','fjmrh.':'','forsrh.':'','félmrh.':'','féltrmrh.':'','hagstrh.':'','heilbrrh.':'','iðnrh.':'','innanrrh.':'','kirkjumrh.':'','landbrh.':'','menntmrh.':'','orkumrh.':'','samgrh.':'','samstrh.':'','slrh.':'','sjútvrh.':'','trmrh.':'','umhvrh.':'','utanrrh.':'','velfrh.':'','viðskrh.':''}

#for r in replacements:
#    print repr(r)

def string_replace(dict,text):
    keys = dict.keys()
    #keys.sort()
    for n in keys:
        text = text.replace(n,dict[n])
    return text

def scrape_meeting(url):
    html = scraperwiki.scrape(url)
    
    #fjarvistir = soup.find(text=re.compile("Fjarvistarleyfi:").findParent)
    if not "Fjarvistarleyfi" in html:
        return
    else:
        root = lxml.html.fromstring(html)
        absent = {}
        absent['meeting'] = root.xpath('//h1/text()')[0]
        try:
            absent_link = root.xpath('//b[text()="Fjarvistarleyfi"]/..')[0].attrib['href']
        except:
            return
        absent['meeting_url'] = absent_link
        html = scraperwiki.scrape(absent_link)
        root = lxml.html.fromstring(html)
        absent['assembly_number'] = re.split(" ",root.xpath('//title/text()')[0])[1][:3]
        p = root.xpath('//p')
        if p:
            for x in p:
            # print x.text.strip().partition(',')[0]
            #urrg = x.text.strip().partition(',')[0].encode('utf-8')
            #print urrg
            #print string_replace(replacements,urrg)
                absent['representative'] = (string_replace(replacements,x.text.strip().partition(',')[0].encode('utf-8')).strip()).decode('utf-8')
            #absent['representative'] = re.sub(", \w.*","",p.text)
        #print absent
                scraperwiki.sqlite.save(["meeting", "assembly_number", "representative"], absent,verbose=1)


def scrape_meeting_list(url):

    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    td = root.xpath('//td[@align="RIGHT"]')
    for td in td:
        meeting_url = "http://www.althingi.is" + td[0].attrib['href']
        scrape_meeting(meeting_url)
        #scraperwiki.sqlite.save_var(url, '1')

def scrape_assembly_list(url):
    html = scraperwiki.scrape(url)
    #soup = BeautifulSoup(html)
    #soup.prettify()
    root = lxml.html.fromstring(html)
    a = root.xpath('//a')
    for a in a:
        url = a.attrib['href']
        if re.search('fulist',url):
            url = "http://althingi.is" + url
            assembly_list_seen =  scraperwiki.sqlite.get_var(url)
            if assembly_list_seen is None:
                print 'doing ', url
                scrape_meeting_list(url)
                scraperwiki.sqlite.save_var(url, '1')
            else:
                print 'done already ', url
scrape_assembly_list(starturl)
import scraperwiki,re
from BeautifulSoup import BeautifulSoup
import lxml.html
import re

starturl = 'http://www.althingi.is/vefur/altutg.html'


def replace_all(text, dic):
        for i, j in dic.iteritems():
            text = text.replace(i, j)
        return text

replacements = {'dómsmrh.':'','efnahrh.':'','fjmrh.':'','forsrh.':'','félmrh.':'','féltrmrh.':'','hagstrh.':'','heilbrrh.':'','iðnrh.':'','innanrrh.':'','kirkjumrh.':'','landbrh.':'','menntmrh.':'','orkumrh.':'','samgrh.':'','samstrh.':'','slrh.':'','sjútvrh.':'','trmrh.':'','umhvrh.':'','utanrrh.':'','velfrh.':'','viðskrh.':''}

#for r in replacements:
#    print repr(r)

def string_replace(dict,text):
    keys = dict.keys()
    #keys.sort()
    for n in keys:
        text = text.replace(n,dict[n])
    return text

def scrape_meeting(url):
    html = scraperwiki.scrape(url)
    
    #fjarvistir = soup.find(text=re.compile("Fjarvistarleyfi:").findParent)
    if not "Fjarvistarleyfi" in html:
        return
    else:
        root = lxml.html.fromstring(html)
        absent = {}
        absent['meeting'] = root.xpath('//h1/text()')[0]
        try:
            absent_link = root.xpath('//b[text()="Fjarvistarleyfi"]/..')[0].attrib['href']
        except:
            return
        absent['meeting_url'] = absent_link
        html = scraperwiki.scrape(absent_link)
        root = lxml.html.fromstring(html)
        absent['assembly_number'] = re.split(" ",root.xpath('//title/text()')[0])[1][:3]
        p = root.xpath('//p')
        if p:
            for x in p:
            # print x.text.strip().partition(',')[0]
            #urrg = x.text.strip().partition(',')[0].encode('utf-8')
            #print urrg
            #print string_replace(replacements,urrg)
                absent['representative'] = (string_replace(replacements,x.text.strip().partition(',')[0].encode('utf-8')).strip()).decode('utf-8')
            #absent['representative'] = re.sub(", \w.*","",p.text)
        #print absent
                scraperwiki.sqlite.save(["meeting", "assembly_number", "representative"], absent,verbose=1)


def scrape_meeting_list(url):

    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    td = root.xpath('//td[@align="RIGHT"]')
    for td in td:
        meeting_url = "http://www.althingi.is" + td[0].attrib['href']
        scrape_meeting(meeting_url)
        #scraperwiki.sqlite.save_var(url, '1')

def scrape_assembly_list(url):
    html = scraperwiki.scrape(url)
    #soup = BeautifulSoup(html)
    #soup.prettify()
    root = lxml.html.fromstring(html)
    a = root.xpath('//a')
    for a in a:
        url = a.attrib['href']
        if re.search('fulist',url):
            url = "http://althingi.is" + url
            assembly_list_seen =  scraperwiki.sqlite.get_var(url)
            if assembly_list_seen is None:
                print 'doing ', url
                scrape_meeting_list(url)
                scraperwiki.sqlite.save_var(url, '1')
            else:
                print 'done already ', url
scrape_assembly_list(starturl)
