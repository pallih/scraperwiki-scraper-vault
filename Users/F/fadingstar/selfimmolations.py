import scraperwiki
from HTMLParser import HTMLParser
import lxml.etree
import lxml.html

import urllib2



class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return self.fed

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


response = urllib2.urlopen('http://www.freetibet.org/newsmedia/selfimmolations')
html = response.read()


#string = '<p class="storytitle"><img border="0" width="157" height="38" alt="" src="http://www.freetibet.org/themes/freetibet/logo.png" /><b>Lobsang Kalsang and Damchoek, Ngaba Town, 27 August 2012, both died<br /></b></p><p><span style="font-size: small;">The two men, one monk and one former monk, set themselves on fire outside Kirti Monastery. They later died. </span><a href="http://www.freetibet.org/newsmedia/number-self-immolation-protests-breaks-50-mark"><span style="font-size: small;">Read more</span></a></p>'



root = lxml.html.fromstring(html)  # an lxml.etree.Element object
i=0
for node in root.cssselect("p.storytitle"):
    html_story_fragment = lxml.etree.tostring(node)
    title = strip_tags(html_story_fragment)[0]

    if (',' in title):
        i = i+1
        print title

        img_src = node.xpath('img//@src')


        print img_src
    
        record = {}
        record["title"] = title
        if (len(img_src) > 0): 
            
            if img_src[0].startswith("/files"): 
                img_src[0] = "http://www.freetibet.org"+img_src[0]

            record["img"] = img_src[0]

        else:
            record["img"] = "http://www.freetibet.org/themes/freetibet/logo.png"
        scraperwiki.sqlite.save(["title"],record, table_name="tibet_self_imm", verbose=2) 

import scraperwiki
from HTMLParser import HTMLParser
import lxml.etree
import lxml.html

import urllib2



class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return self.fed

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


response = urllib2.urlopen('http://www.freetibet.org/newsmedia/selfimmolations')
html = response.read()


#string = '<p class="storytitle"><img border="0" width="157" height="38" alt="" src="http://www.freetibet.org/themes/freetibet/logo.png" /><b>Lobsang Kalsang and Damchoek, Ngaba Town, 27 August 2012, both died<br /></b></p><p><span style="font-size: small;">The two men, one monk and one former monk, set themselves on fire outside Kirti Monastery. They later died. </span><a href="http://www.freetibet.org/newsmedia/number-self-immolation-protests-breaks-50-mark"><span style="font-size: small;">Read more</span></a></p>'



root = lxml.html.fromstring(html)  # an lxml.etree.Element object
i=0
for node in root.cssselect("p.storytitle"):
    html_story_fragment = lxml.etree.tostring(node)
    title = strip_tags(html_story_fragment)[0]

    if (',' in title):
        i = i+1
        print title

        img_src = node.xpath('img//@src')


        print img_src
    
        record = {}
        record["title"] = title
        if (len(img_src) > 0): 
            
            if img_src[0].startswith("/files"): 
                img_src[0] = "http://www.freetibet.org"+img_src[0]

            record["img"] = img_src[0]

        else:
            record["img"] = "http://www.freetibet.org/themes/freetibet/logo.png"
        scraperwiki.sqlite.save(["title"],record, table_name="tibet_self_imm", verbose=2) 

