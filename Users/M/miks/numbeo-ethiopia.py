import scraperwiki
import sys, httplib2, urllib, re, random
from lxml import etree
import lxml.html
from StringIO import StringIO
from time import sleep


def chunks(l, n):
    ''' 
    http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks-in-python
    '''
    return [l[i:i+n] for i in range(0, len(l), n)]


def scrape(records): 
    for r in records:
        data = {}
        data['key'] = random.random()
        data['Item'] = r[0].text
        data['price'] = r[1].text
        #print r[0].text, r[1].text
        #print records.text
        #data = {}
        #data['key'] = '%s-%s-%s' % (r[0].text, r[1].text, r[2].text)
        #data['country'] = r[0].text
        scraperwiki.sqlite.save(["key"], data) #Store data in sqlite database
#once you have the raw data the scrape creates a spreadsheet
#spreadsheet is made of key and value
#they can be called anything after key

def data_prep(content):#function to grab urls
    #print content
    records = []
    doc = lxml.html.document_fromstring(content)
    datas = doc.cssselect('table.data_wide_table td')
    datas = datas[5:]
    records = chunks(datas, 3)
    #print records
    #for r in records:
        #print r
    return scrape(records)
#def data prep will need to change based on data website
#few different libraries, lxml is the data library, will read into xml data, finds table on page
#data soup is one
#regular expressions is another way
#cssselect is telling it to find an element called font
#<font....>stuff</font....>
#knew all data files had item_data_style
#every time this tag occured it will grab what is in there
#xpath might be better

def page_load(url): #function to scrape page
    link = []
    h = httplib2.Http(".cache")
    response, content = h.request(url, "GET")
    if response.status != 200:
        sys.stderr.write('Error, returned status: %s\n' % response.status)
        sys.exit(1) #bomb out, non-zero return indicates error
    return data_prep(content)

#h is data type
#get functio is what happens when you go to the web browser
#if response is 200 (it's cool), if not 200 then error is returned
#we now have dataprep content

urls = ['http://www.numbeo.com/food-prices/country_result.jsp?country=Ethiopia']

for u in urls:
    page_load(u)
    sleep(1)




import scraperwiki
import sys, httplib2, urllib, re, random
from lxml import etree
import lxml.html
from StringIO import StringIO
from time import sleep


def chunks(l, n):
    ''' 
    http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks-in-python
    '''
    return [l[i:i+n] for i in range(0, len(l), n)]


def scrape(records): 
    for r in records:
        data = {}
        data['key'] = random.random()
        data['Item'] = r[0].text
        data['price'] = r[1].text
        #print r[0].text, r[1].text
        #print records.text
        #data = {}
        #data['key'] = '%s-%s-%s' % (r[0].text, r[1].text, r[2].text)
        #data['country'] = r[0].text
        scraperwiki.sqlite.save(["key"], data) #Store data in sqlite database
#once you have the raw data the scrape creates a spreadsheet
#spreadsheet is made of key and value
#they can be called anything after key

def data_prep(content):#function to grab urls
    #print content
    records = []
    doc = lxml.html.document_fromstring(content)
    datas = doc.cssselect('table.data_wide_table td')
    datas = datas[5:]
    records = chunks(datas, 3)
    #print records
    #for r in records:
        #print r
    return scrape(records)
#def data prep will need to change based on data website
#few different libraries, lxml is the data library, will read into xml data, finds table on page
#data soup is one
#regular expressions is another way
#cssselect is telling it to find an element called font
#<font....>stuff</font....>
#knew all data files had item_data_style
#every time this tag occured it will grab what is in there
#xpath might be better

def page_load(url): #function to scrape page
    link = []
    h = httplib2.Http(".cache")
    response, content = h.request(url, "GET")
    if response.status != 200:
        sys.stderr.write('Error, returned status: %s\n' % response.status)
        sys.exit(1) #bomb out, non-zero return indicates error
    return data_prep(content)

#h is data type
#get functio is what happens when you go to the web browser
#if response is 200 (it's cool), if not 200 then error is returned
#we now have dataprep content

urls = ['http://www.numbeo.com/food-prices/country_result.jsp?country=Ethiopia']

for u in urls:
    page_load(u)
    sleep(1)




