import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re
import time

for pg in range(1,960):
    part_url = "http://www.fanfiction.net/book/Harry_Potter/10/0/0/1/40/0/0/0/0/"

    url = part_url + str(pg)
    
    page = lxml.html.parse(url).getroot()
    if page is not None:
        fics = page.find_class("z-list")
    
        for item in fics:
            fic = {}
            fic["num"] = int(item.text[:-2])
            fic["title"] = item.findall("a")[0].text if item.findall("a")[0].text!='' else 'Untitled Fic'
            fic["url"] = item.findall("a")[0].attrib["href"]
            details =  item.find_class("z-padtop2")[0].text
        
            rx = re.compile(r'.* - Reviews: (?P<revs>[0-9,]*)')
            m = rx.match(details)
            fic["reviews"] =  int(m.group('revs')) if m else 0
    
            #if there are no reviews, author is in the 2nd (not 3rd) link
            fic["author"] = item.findall("a")[2].text if m else item.findall("a")[1].text 
        
            rx = re.compile(r'.* - Words: (?P<words>[0-9,]*)')
            m = rx.match(details)
            fic["words"] =  int(m.group('words').replace(',','')) if m else 0
        
            #Chapters:
            rx = re.compile(r'.* - Chapters: (?P<chapts>[0-9]*)')
            m = rx.match(details)
            fic["chapters"] =  int(m.group('chapts')) if m else 0
        
            #Updated:
            rx = re.compile(r'.* - Updated: (?P<upd>[0-9\-]*)')
            m = rx.match(details)
            fic["updated"] =  time.strftime("%Y-%m-%d", time.strptime(m.group('upd'), "%m-%d-%y")) if m else 0
        
            #Published:
            rx = re.compile(r'.* - Published: (?P<pubd>[0-9\-]*)')
            m = rx.match(details)
            fic["published"] =  time.strftime("%Y-%m-%d", time.strptime(m.group('pubd'), "%m-%d-%y")) if m else 0
    
            #Rating:
            rx = re.compile(r'.*Rated: (?P<rate>[KTM][+]?)')
            m = rx.match(details)
            fic["rating"] =  m.group('rate') if m else 0        
        
            scraperwiki.sqlite.save(["num"], fic) # save the records one by one