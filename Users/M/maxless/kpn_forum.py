import scraperwiki
import requests
import lxml.html
import urllib


def get_site(url):
    r = requests.get(url, verify=False)
    return lxml.html.fromstring(r.text)

for page in range(1,6):
    print "Scraping page %d" % page
    dom = get_site("http://forum.kpn.com/t5/Vast-Zakelijk-Bellen-en-Internet/bd-p/zmvast/page/%d" % page)
    
    results = dom.cssselect('tbody')
    for tr in results:
        thread = {
          "date": tr.cssselect('.DateTime')[0].text_content(),
          "title": tr.cssselect('.message-subject')[0].text_content(),
          "replies": tr.cssselect('.repliesCountColumn')[0].text_content(),
          "author": tr.cssselect('span.UserName')[0].text_content(),
          "views": tr.cssselect( '.viewsCountColumn')[0].text_content()   

        }      
    scraperwiki.sqlite.save(['title'], thread)


    
import scraperwiki
import requests
import lxml.html
import urllib


def get_site(url):
    r = requests.get(url, verify=False)
    return lxml.html.fromstring(r.text)

for page in range(1,6):
    print "Scraping page %d" % page
    dom = get_site("http://forum.kpn.com/t5/Vast-Zakelijk-Bellen-en-Internet/bd-p/zmvast/page/%d" % page)
    
    results = dom.cssselect('tbody')
    for tr in results:
        thread = {
          "date": tr.cssselect('.DateTime')[0].text_content(),
          "title": tr.cssselect('.message-subject')[0].text_content(),
          "replies": tr.cssselect('.repliesCountColumn')[0].text_content(),
          "author": tr.cssselect('span.UserName')[0].text_content(),
          "views": tr.cssselect( '.viewsCountColumn')[0].text_content()   

        }      
    scraperwiki.sqlite.save(['title'], thread)


    
import scraperwiki
import requests
import lxml.html
import urllib


def get_site(url):
    r = requests.get(url, verify=False)
    return lxml.html.fromstring(r.text)

for page in range(1,6):
    print "Scraping page %d" % page
    dom = get_site("http://forum.kpn.com/t5/Vast-Zakelijk-Bellen-en-Internet/bd-p/zmvast/page/%d" % page)
    
    results = dom.cssselect('tbody')
    for tr in results:
        thread = {
          "date": tr.cssselect('.DateTime')[0].text_content(),
          "title": tr.cssselect('.message-subject')[0].text_content(),
          "replies": tr.cssselect('.repliesCountColumn')[0].text_content(),
          "author": tr.cssselect('span.UserName')[0].text_content(),
          "views": tr.cssselect( '.viewsCountColumn')[0].text_content()   

        }      
    scraperwiki.sqlite.save(['title'], thread)


    
import scraperwiki
import requests
import lxml.html
import urllib


def get_site(url):
    r = requests.get(url, verify=False)
    return lxml.html.fromstring(r.text)

for page in range(1,6):
    print "Scraping page %d" % page
    dom = get_site("http://forum.kpn.com/t5/Vast-Zakelijk-Bellen-en-Internet/bd-p/zmvast/page/%d" % page)
    
    results = dom.cssselect('tbody')
    for tr in results:
        thread = {
          "date": tr.cssselect('.DateTime')[0].text_content(),
          "title": tr.cssselect('.message-subject')[0].text_content(),
          "replies": tr.cssselect('.repliesCountColumn')[0].text_content(),
          "author": tr.cssselect('span.UserName')[0].text_content(),
          "views": tr.cssselect( '.viewsCountColumn')[0].text_content()   

        }      
    scraperwiki.sqlite.save(['title'], thread)


    
