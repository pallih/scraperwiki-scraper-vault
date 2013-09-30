import scraperwiki
import lxml.html
import time

import httplib
import cookielib
import urllib2
import urllib

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

    def query(self, url):
        headers=[
            ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11')]
        
       
        self.opener.addheaders = headers
        try:
            r = self.opener.open(url)
            content = r.read()
        except:
            time.sleep(10)
            content = self.query(url)

        #r = self.opener.open(url)
        #content = r.read()


        return content


def get_xpath_el(parent, xpath, default='text',index=0):
    el=parent.xpath(xpath)
    if el!=[]:
        if default=='text' or default=='':
            return el[index].text_content()
        else:
            return el[index].attrib[default]
    else:
        return ''

# Blank Python
b=Browse()
html=b.query("http://www.sovcombank.ru/offices")
root=lxml.html.document_fromstring(html)
id=1

for r in root.xpath("//div[@class='contentContact']//h4[@class='title']/a"):
    region_name=r.text_content()
    region_url=r.attrib['href']
    html=b.query("http://www.sovcombank.ru" + region_url + "1/")
    root1=lxml.html.document_fromstring(html)
    data=[]
    for e in root1.xpath("//div[@id='content']/div[@class='contactItem']"):
        branch_name=get_xpath_el(e,"h4[@class='title']")
        address=get_xpath_el(e,"table/tr[1]/td[2]")
        latlon=get_xpath_el(e,"h4[@class='title']/a", "onclick")
        data.append({'id':id, 'region_name':region_name, 'region_url': region_url , 'branch_name':branch_name, 'address':address, 'latlon':latlon})
        id+=1
    scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name="data")
    #exit()


        import scraperwiki
import lxml.html
import time

import httplib
import cookielib
import urllib2
import urllib

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

    def query(self, url):
        headers=[
            ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11')]
        
       
        self.opener.addheaders = headers
        try:
            r = self.opener.open(url)
            content = r.read()
        except:
            time.sleep(10)
            content = self.query(url)

        #r = self.opener.open(url)
        #content = r.read()


        return content


def get_xpath_el(parent, xpath, default='text',index=0):
    el=parent.xpath(xpath)
    if el!=[]:
        if default=='text' or default=='':
            return el[index].text_content()
        else:
            return el[index].attrib[default]
    else:
        return ''

# Blank Python
b=Browse()
html=b.query("http://www.sovcombank.ru/offices")
root=lxml.html.document_fromstring(html)
id=1

for r in root.xpath("//div[@class='contentContact']//h4[@class='title']/a"):
    region_name=r.text_content()
    region_url=r.attrib['href']
    html=b.query("http://www.sovcombank.ru" + region_url + "1/")
    root1=lxml.html.document_fromstring(html)
    data=[]
    for e in root1.xpath("//div[@id='content']/div[@class='contactItem']"):
        branch_name=get_xpath_el(e,"h4[@class='title']")
        address=get_xpath_el(e,"table/tr[1]/td[2]")
        latlon=get_xpath_el(e,"h4[@class='title']/a", "onclick")
        data.append({'id':id, 'region_name':region_name, 'region_url': region_url , 'branch_name':branch_name, 'address':address, 'latlon':latlon})
        id+=1
    scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name="data")
    #exit()


        