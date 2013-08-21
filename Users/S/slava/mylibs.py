import scraperwiki
import lxml.html
import time

import sys
import httplib
import cookielib
import urllib2
import urllib

# This is a library with common used functions


#scrape function wrapper into a classs
class Browse:

    def __init__(self):
        cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

    def patch_http_response_read(func):
        def inner(*args):
            try:
                return func(*args)
            except httplib.IncompleteRead, e:
                return e.partial
    
        return inner
    httplib.HTTPResponse.read = patch_http_response_read(httplib.HTTPResponse.read)

    def query(self, url, params=None):
        content=""
        headers=[
            ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11')]
        
       
        self.opener.addheaders = headers
        try:
            if params != None:
                data = urllib.urlencode(params)
                r = self.opener.open(url, data)
            else:
                r = self.opener.open(url)

            content = r.read()
        except:
            print sys.exc_info()[0]
            #time.sleep(10)
            #content = self.query(url, params)

        #r = self.opener.open(url)
        #content = r.read()


        return content

def boo(test):
    test+=" YEAH!"
    return test

# Extract html element text content or attribute value
def get_xpath_el(parent, xpath, default='text',index=0):
    el=parent.xpath(xpath)
    if el!=[] and index in el:
        if default=='text' or default=='':
            return el[index].text_content()
        else:
            return el[index].attrib[default]
    else:
        return ''