import scraperwiki
import re
from lxml import html
from lxml import etree
import urllib2

def parse_content(doc):
    content = doc.cssselect('div#content > #content_0.openSection')
    paras = content[0].cssselect(' > p')
        
    for para in paras:
        print para.text_content()

def get_description(city,uri):

    req = urllib2.Request("http://en.m.wikipedia.org/wiki/"+uri)

    try:
        resp = urllib2.urlopen(req)
    except urllib2.URLError, e:
        if e.code == 404:
            print "404"
        else:
            print "HTTP Error"    
        return
    else:
        doc_text = resp.read()
        doc = html.fromstring(doc_text)

        first_p = doc.xpath('//*[@id="content"]/p[1]')
        
        if len(first_p) > 0:
            p = first_p[0].text_content()
            if "may refer to:" in p:
                #print "now select link"
    
                alts = doc.xpath('//*[@id="content"]/ul/li/a')
                
                if len(alts) > 0:
                    
                    for alt in alts:
                        if city in alt.text_content():
                            split = alt.get('href').split('/')
                            get_description(city, split[-1])
            
            else:
                parse_content(doc)
        else:
            parse_content(doc)
                
city = "Edinburgh"
#url = "City_Restaurant"
#url = "Arthurs_Seat"
url = "Our_Dynamic_Earth"
#url = "Jenners_-_Edinburgh" #404

get_description(city,url)
import scraperwiki
import re
from lxml import html
from lxml import etree
import urllib2

def parse_content(doc):
    content = doc.cssselect('div#content > #content_0.openSection')
    paras = content[0].cssselect(' > p')
        
    for para in paras:
        print para.text_content()

def get_description(city,uri):

    req = urllib2.Request("http://en.m.wikipedia.org/wiki/"+uri)

    try:
        resp = urllib2.urlopen(req)
    except urllib2.URLError, e:
        if e.code == 404:
            print "404"
        else:
            print "HTTP Error"    
        return
    else:
        doc_text = resp.read()
        doc = html.fromstring(doc_text)

        first_p = doc.xpath('//*[@id="content"]/p[1]')
        
        if len(first_p) > 0:
            p = first_p[0].text_content()
            if "may refer to:" in p:
                #print "now select link"
    
                alts = doc.xpath('//*[@id="content"]/ul/li/a')
                
                if len(alts) > 0:
                    
                    for alt in alts:
                        if city in alt.text_content():
                            split = alt.get('href').split('/')
                            get_description(city, split[-1])
            
            else:
                parse_content(doc)
        else:
            parse_content(doc)
                
city = "Edinburgh"
#url = "City_Restaurant"
#url = "Arthurs_Seat"
url = "Our_Dynamic_Earth"
#url = "Jenners_-_Edinburgh" #404

get_description(city,url)
