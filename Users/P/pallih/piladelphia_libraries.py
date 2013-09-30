# -*- coding: utf-8 -*-
import scraperwiki
#import urllib2
import requests
#import json
import lxml.html
import time
import re


starturl = 'http://libwww.freelibrary.org/branches/brnlist.cfm'
regex_zip = re.compile("(PA \d.+) \(")
regex_street = re.compile("(.*) Philadelphia")
def process_library(link):
    record = {}
    html = get(link)
    root = lxml.html.fromstring(html)
    branch = root.xpath('/html/body/table/tr[4]/td[2]/div/b[3]')[0].text
    address = root.xpath('//div[@id="globaltext"]')[0]
    phone = root.xpath('//div[@id="globaltext"]')[1]
    #print address.text_content()
    full_address = re.sub(r"\s+", " ", address.text_content()).lstrip('Street Address').rstrip('Directions | Map  | Bus Schedule ') #this is probably a very lame way to clean this up
    zip = regex_zip.findall(full_address)[0]
    street = regex_street.findall(full_address)[0]
    phone = re.sub(r"\s+", " ", phone.text_content()).lstrip('Contact ')
    openings = root.xpath('//div[@id="redlinks"]/table/tr')
    sunday = openings[0][1].text
    monday = openings[1][1].text
    tuesday = openings[2][1].text
    wednesday = openings[3][1].text
    thursday = openings[4][1].text
    friday = openings[5][1].text
    saturday = openings[6][1].text
    if sunday != 'CLOSED':
        sunday_open = sunday.split('-')[0]
        sunday_close = sunday.split('-')[1]
    else: 
        sunday_open = 'CLOSED'
        sunday_close = 'CLOSED' 
    if monday != 'CLOSED':
        monday_open = monday.split('-')[0]
        monday_close = monday.split('-')[1]
    else: 
        monday_open = 'CLOSED'
        monday_close = 'CLOSED'
    if tuesday != 'CLOSED':
        tuesday_open = tuesday.split('-')[0]
        tuesday_close = tuesday.split('-')[1]
    else: 
        tuesday_open = 'CLOSED'
        tuesday = 'CLOSED' 
    if wednesday != 'CLOSED':
        wednesday_open = wednesday.split('-')[0]
        wednesday_close = wednesday.split('-')[1]
    else: 
        wednesday_open = 'CLOSED'
        wednesday_close = 'CLOSED'
    if thursday != 'CLOSED':
        thursday_open = thursday.split('-')[0]
        thursday_close = thursday.split('-')[1]
    else: 
        thursday_open = 'CLOSED'
        thursday_close = 'CLOSED' 
    if friday != 'CLOSED':
        friday_open = friday.split('-')[0]
        friday_close = friday.split('-')[1]
    else: 
        friday_open = 'CLOSED'
        friday_close = 'CLOSED'
    if saturday != 'CLOSED':
        saturday_open = saturday.split('-')[0]
        saturday_close = saturday.split('-')[1]
    else: 
        saturday_open = 'CLOSED'
        saturday_close = 'CLOSED'

    record['full_address'] = full_address
    record['zip'] = zip
    record['street'] = street
    record['phone'] = phone
    record['branch'] = branch
    record['sunday'] = sunday
    record['monday'] = monday
    record['tuesday'] = tuesday
    record['wednesday'] = wednesday
    record['thursday'] = thursday
    record['friday'] = friday
    record['saturday'] = saturday
    record['sunday_open'] = sunday_open
    record['sunday_close'] = sunday_close
    record['monday_open'] = monday_open
    record['monday_close'] = monday_close 
    record['tuesday_open'] = tuesday_open
    record['tuesday_close'] = tuesday_close
    record['wednesday_open'] = wednesday_open
    record['wednesday_close'] = wednesday_close
    record['thursday_open'] = thursday_open
    record['thursday_close'] = thursday_close
    record['friday_open'] = friday_open
    record['friday_close'] = friday_close
    record['saturday_open'] = saturday_open
    record['saturday_close'] = saturday_close 
    scraperwiki.sqlite.save(['branch'], data=record, table_name='philadelphia_libraries', verbose=2)
    print 'done with ', branch          

def process_list(html):
    xpath = '//td/div/table/tr/td/div/a'
    root = lxml.html.fromstring(html)
    for tr in root.xpath(xpath):
        link = 'http://libwww.freelibrary.org/branches/' + tr.attrib['href']
        process_library(link)
    print ' All done '       
def get(url):
    headers = {'User-agent':'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1)'}
    r = requests.post(url,headers=headers,allow_redirects=True)
    content = r.content
    #content = (content.decode('unicode_escape')).replace('\\/', '/').strip('"')
    return content

html = get(starturl)

process_list(html)

# -*- coding: utf-8 -*-
import scraperwiki
#import urllib2
import requests
#import json
import lxml.html
import time
import re


starturl = 'http://libwww.freelibrary.org/branches/brnlist.cfm'
regex_zip = re.compile("(PA \d.+) \(")
regex_street = re.compile("(.*) Philadelphia")
def process_library(link):
    record = {}
    html = get(link)
    root = lxml.html.fromstring(html)
    branch = root.xpath('/html/body/table/tr[4]/td[2]/div/b[3]')[0].text
    address = root.xpath('//div[@id="globaltext"]')[0]
    phone = root.xpath('//div[@id="globaltext"]')[1]
    #print address.text_content()
    full_address = re.sub(r"\s+", " ", address.text_content()).lstrip('Street Address').rstrip('Directions | Map  | Bus Schedule ') #this is probably a very lame way to clean this up
    zip = regex_zip.findall(full_address)[0]
    street = regex_street.findall(full_address)[0]
    phone = re.sub(r"\s+", " ", phone.text_content()).lstrip('Contact ')
    openings = root.xpath('//div[@id="redlinks"]/table/tr')
    sunday = openings[0][1].text
    monday = openings[1][1].text
    tuesday = openings[2][1].text
    wednesday = openings[3][1].text
    thursday = openings[4][1].text
    friday = openings[5][1].text
    saturday = openings[6][1].text
    if sunday != 'CLOSED':
        sunday_open = sunday.split('-')[0]
        sunday_close = sunday.split('-')[1]
    else: 
        sunday_open = 'CLOSED'
        sunday_close = 'CLOSED' 
    if monday != 'CLOSED':
        monday_open = monday.split('-')[0]
        monday_close = monday.split('-')[1]
    else: 
        monday_open = 'CLOSED'
        monday_close = 'CLOSED'
    if tuesday != 'CLOSED':
        tuesday_open = tuesday.split('-')[0]
        tuesday_close = tuesday.split('-')[1]
    else: 
        tuesday_open = 'CLOSED'
        tuesday = 'CLOSED' 
    if wednesday != 'CLOSED':
        wednesday_open = wednesday.split('-')[0]
        wednesday_close = wednesday.split('-')[1]
    else: 
        wednesday_open = 'CLOSED'
        wednesday_close = 'CLOSED'
    if thursday != 'CLOSED':
        thursday_open = thursday.split('-')[0]
        thursday_close = thursday.split('-')[1]
    else: 
        thursday_open = 'CLOSED'
        thursday_close = 'CLOSED' 
    if friday != 'CLOSED':
        friday_open = friday.split('-')[0]
        friday_close = friday.split('-')[1]
    else: 
        friday_open = 'CLOSED'
        friday_close = 'CLOSED'
    if saturday != 'CLOSED':
        saturday_open = saturday.split('-')[0]
        saturday_close = saturday.split('-')[1]
    else: 
        saturday_open = 'CLOSED'
        saturday_close = 'CLOSED'

    record['full_address'] = full_address
    record['zip'] = zip
    record['street'] = street
    record['phone'] = phone
    record['branch'] = branch
    record['sunday'] = sunday
    record['monday'] = monday
    record['tuesday'] = tuesday
    record['wednesday'] = wednesday
    record['thursday'] = thursday
    record['friday'] = friday
    record['saturday'] = saturday
    record['sunday_open'] = sunday_open
    record['sunday_close'] = sunday_close
    record['monday_open'] = monday_open
    record['monday_close'] = monday_close 
    record['tuesday_open'] = tuesday_open
    record['tuesday_close'] = tuesday_close
    record['wednesday_open'] = wednesday_open
    record['wednesday_close'] = wednesday_close
    record['thursday_open'] = thursday_open
    record['thursday_close'] = thursday_close
    record['friday_open'] = friday_open
    record['friday_close'] = friday_close
    record['saturday_open'] = saturday_open
    record['saturday_close'] = saturday_close 
    scraperwiki.sqlite.save(['branch'], data=record, table_name='philadelphia_libraries', verbose=2)
    print 'done with ', branch          

def process_list(html):
    xpath = '//td/div/table/tr/td/div/a'
    root = lxml.html.fromstring(html)
    for tr in root.xpath(xpath):
        link = 'http://libwww.freelibrary.org/branches/' + tr.attrib['href']
        process_library(link)
    print ' All done '       
def get(url):
    headers = {'User-agent':'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1)'}
    r = requests.post(url,headers=headers,allow_redirects=True)
    content = r.content
    #content = (content.decode('unicode_escape')).replace('\\/', '/').strip('"')
    return content

html = get(starturl)

process_list(html)

