import scraperwiki
import lxml.html
import time

import httplib
import cookielib
import urllib2
import urllib
import re
# Blank Python

# function wrapper to wait if errors occur and try after 10 sec
def grab(url,params={},ua=None):
    try:
        html=scraperwiki.scrape(url, params, user_agent=ua)
    except:
        time.sleep(10)
        html=grab(url,params,ua)

    return html

# return text content of a given xpath on a parent node
def get_xpath_el(parent, xpath, default='text',index=0):
    el=parent.xpath(xpath)
    if el!=[]:
        if default=='text' or default=='':
            return el[index].text_content()
        else:
            return el[index].attrib[default]
    else:
        return ''

# grab regions
def get_regions():
    i=1

    html=scraperwiki.scrape("http://www.openbank.ru/ru/about/office/")
    r=lxml.html.document_fromstring(html)
    regions=r.xpath("//div[@id='navigation_city_panel']/table[@class='container']/tr[3]/td/table/tr")
    
    #print regions
    
    for tr in regions:
        try:
            cls=tr.attrib['class']
            
            if tr.attrib['class']=='region_section':
                oblasty=get_xpath_el(tr,"td/a",'')
                city_url=''
                city=''
    
            if tr.attrib['class']=='current_city':
                city=get_xpath_el(tr,"td/a")
                city_url=get_xpath_el(tr,"td/a","href")

            if oblasty!= '' and city != '' and city_url != '':
                scraperwiki.sqlite.save(unique_keys=['id'],data={'id':i, 'oblasty':oblasty, 'city':city, 'city_url':city_url}, table_name='regions')
                i+=1
                print oblasty, city, city_url
        except:
            pass

#get_regions()

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
            content = self.query(url)

        #r = self.opener.open(url)
        #content = r.read()


        return content


def get_branches():
    b=Browse()
    lid=1
    id=1
    scraperwiki.sqlite.execute('delete from coords_data')
    scraperwiki.sqlite.execute('delete from branch_data')
    data=scraperwiki.sqlite.select('* from regions')
    for d in data:
        
        html=b.query("http://www.openbank.ru/ru/about/office/"+d['city_url'])
        html=html.decode('windows-1251')

        #print html
        r=lxml.html.document_fromstring(html)
        
        data=[]
        branchName=''
        address=''
        for el in r.xpath("//div[@class='body_sec']//*[name()='h4' or name()='ul']"):
            #print el.tag

            #print el.tag
            if el.tag == 'h4': 
                branchName=el.text_content()
                address=''

            if el.tag == 'ul':
                address=get_xpath_el(el, 'li[1]')
            
            if branchName != '' and address!='':
                data.append({'id':id,'branch_name':branchName, 'address':address, 'city':d['city'], 'oblasty':d['oblasty']})
                branchName=''
                address=''
                id+=1

        print data
        #get coordinates
        latlon=re.findall(r'createObject\("Placemark"\, new YMaps\.GeoPoint\(([\d\.]+?),\s*([\d\.]+?)\),\s*?".*?",\s*?"(.*?)"\)\)',html, re.I|re.U)
       
        lldata=[]
        if latlon!=[]:
            for l in latlon:
                lldata.append({'lid':lid, 'lat':l[1], 'lon':l[0], 'branch_data':l[2].encode('utf-8')})
                lid+=1

        if data!=[]:        
            scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name='branch_data')

        if lldata!=[]:
            scraperwiki.sqlite.save(unique_keys=['lid'], data=lldata, table_name='coords_data')
        


get_branches()import scraperwiki
import lxml.html
import time

import httplib
import cookielib
import urllib2
import urllib
import re
# Blank Python

# function wrapper to wait if errors occur and try after 10 sec
def grab(url,params={},ua=None):
    try:
        html=scraperwiki.scrape(url, params, user_agent=ua)
    except:
        time.sleep(10)
        html=grab(url,params,ua)

    return html

# return text content of a given xpath on a parent node
def get_xpath_el(parent, xpath, default='text',index=0):
    el=parent.xpath(xpath)
    if el!=[]:
        if default=='text' or default=='':
            return el[index].text_content()
        else:
            return el[index].attrib[default]
    else:
        return ''

# grab regions
def get_regions():
    i=1

    html=scraperwiki.scrape("http://www.openbank.ru/ru/about/office/")
    r=lxml.html.document_fromstring(html)
    regions=r.xpath("//div[@id='navigation_city_panel']/table[@class='container']/tr[3]/td/table/tr")
    
    #print regions
    
    for tr in regions:
        try:
            cls=tr.attrib['class']
            
            if tr.attrib['class']=='region_section':
                oblasty=get_xpath_el(tr,"td/a",'')
                city_url=''
                city=''
    
            if tr.attrib['class']=='current_city':
                city=get_xpath_el(tr,"td/a")
                city_url=get_xpath_el(tr,"td/a","href")

            if oblasty!= '' and city != '' and city_url != '':
                scraperwiki.sqlite.save(unique_keys=['id'],data={'id':i, 'oblasty':oblasty, 'city':city, 'city_url':city_url}, table_name='regions')
                i+=1
                print oblasty, city, city_url
        except:
            pass

#get_regions()

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
            content = self.query(url)

        #r = self.opener.open(url)
        #content = r.read()


        return content


def get_branches():
    b=Browse()
    lid=1
    id=1
    scraperwiki.sqlite.execute('delete from coords_data')
    scraperwiki.sqlite.execute('delete from branch_data')
    data=scraperwiki.sqlite.select('* from regions')
    for d in data:
        
        html=b.query("http://www.openbank.ru/ru/about/office/"+d['city_url'])
        html=html.decode('windows-1251')

        #print html
        r=lxml.html.document_fromstring(html)
        
        data=[]
        branchName=''
        address=''
        for el in r.xpath("//div[@class='body_sec']//*[name()='h4' or name()='ul']"):
            #print el.tag

            #print el.tag
            if el.tag == 'h4': 
                branchName=el.text_content()
                address=''

            if el.tag == 'ul':
                address=get_xpath_el(el, 'li[1]')
            
            if branchName != '' and address!='':
                data.append({'id':id,'branch_name':branchName, 'address':address, 'city':d['city'], 'oblasty':d['oblasty']})
                branchName=''
                address=''
                id+=1

        print data
        #get coordinates
        latlon=re.findall(r'createObject\("Placemark"\, new YMaps\.GeoPoint\(([\d\.]+?),\s*([\d\.]+?)\),\s*?".*?",\s*?"(.*?)"\)\)',html, re.I|re.U)
       
        lldata=[]
        if latlon!=[]:
            for l in latlon:
                lldata.append({'lid':lid, 'lat':l[1], 'lon':l[0], 'branch_data':l[2].encode('utf-8')})
                lid+=1

        if data!=[]:        
            scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name='branch_data')

        if lldata!=[]:
            scraperwiki.sqlite.save(unique_keys=['lid'], data=lldata, table_name='coords_data')
        


get_branches()