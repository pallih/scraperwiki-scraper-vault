#!/usr/bin/env python

#####
#
# New Zealand Early Education Institutions
# The data originates from this url:
# http://www.educationcounts.govt.nz/statistics/tertiary_education/27436 
# Yes - it's a confusingly minted URL.
#
####

import urllib
import csv
import scraperwiki
from time import sleep
from random import randint
import json
from BeautifulSoup import BeautifulSoup
import re
import sys
from scrapemark import scrape

def locate(address):
    """ 
    Wrapper for google geocoder
    Returns lat,lng tuple or None 
    """
    url = "http://maps.googleapis.com/maps/api/geocode/json?%s" % \
        urllib.urlencode({ 'address':address, 'sensor':'false' })
    jd = json.loads(scraperwiki.scrape(url))
    # sleep a little so as not to batter the geocoding api
    sleep(randint(2,4))

    if jd['status'] == 'OK':
        return (float(jd['results'][0]['geometry']['location']['lat']),\
            float(jd['results'][0]['geometry']['location']['lng']))
    else: 
        return None

def get_csv_link():
    """ Return up-to-date csv link """
    csv_pattern = """{*<a href="{{ href }}" title="Click here to download this file." target="blank">
    ECE Directory .csv*}</a>"""
    det = scrape(csv_pattern, url='http://www.educationcounts.govt.nz/directories/early-childhood-services')
    return 'http://www.educationcounts.govt.nz%s' % det['href']
    
url = get_csv_link()

print 'opening %s' %url
fin = urllib.urlopen(url)
print fin
lines = fin.readlines()
clist = list(csv.reader(lines))[3:]
print clist
headers = clist.pop(0)
headers  = [ h.strip().replace(' ','_').replace('*','').replace('^', '') for h in headers ] # clean up 
continue_from  = scraperwiki.sqlite.get_var('last_clist_index', default=0)
print 'continuing from: ', continue_from
n = continue_from

while n < len(clist):
    try:
        data = dict(zip(headers, clist[n]))
        
        location = data['Name'] + ', ' + data['Street'] + ', ' + data['Suburb'] + ', \
            ' + data['City'] + ', ' + ', New Zealand'
        latlng = locate(location)
        #Fix
        data['Maori_electorate'] = data['M?ori_Electorate']
        del data['M?ori_Electorate']
        if latlng: data['lat'], data['lng'] = latlng
        data['Management_Contact_Name'] = data['Management_Contact_Name'].title()
        scraperwiki.sqlite.save(unique_keys=['Institution_Number',], data=data)
        print 'saved rec ', n
        n += 1
    except Exception, e:
        # save state in case of exception
        print str(e)
        print 'Save at record: ', n
        scraperwiki.metadata.save('last_clist_index',n)
        sys.exit()

scraperwiki.metadata.save('last_clist_index',0)#!/usr/bin/env python

#####
#
# New Zealand Early Education Institutions
# The data originates from this url:
# http://www.educationcounts.govt.nz/statistics/tertiary_education/27436 
# Yes - it's a confusingly minted URL.
#
####

import urllib
import csv
import scraperwiki
from time import sleep
from random import randint
import json
from BeautifulSoup import BeautifulSoup
import re
import sys
from scrapemark import scrape

def locate(address):
    """ 
    Wrapper for google geocoder
    Returns lat,lng tuple or None 
    """
    url = "http://maps.googleapis.com/maps/api/geocode/json?%s" % \
        urllib.urlencode({ 'address':address, 'sensor':'false' })
    jd = json.loads(scraperwiki.scrape(url))
    # sleep a little so as not to batter the geocoding api
    sleep(randint(2,4))

    if jd['status'] == 'OK':
        return (float(jd['results'][0]['geometry']['location']['lat']),\
            float(jd['results'][0]['geometry']['location']['lng']))
    else: 
        return None

def get_csv_link():
    """ Return up-to-date csv link """
    csv_pattern = """{*<a href="{{ href }}" title="Click here to download this file." target="blank">
    ECE Directory .csv*}</a>"""
    det = scrape(csv_pattern, url='http://www.educationcounts.govt.nz/directories/early-childhood-services')
    return 'http://www.educationcounts.govt.nz%s' % det['href']
    
url = get_csv_link()

print 'opening %s' %url
fin = urllib.urlopen(url)
print fin
lines = fin.readlines()
clist = list(csv.reader(lines))[3:]
print clist
headers = clist.pop(0)
headers  = [ h.strip().replace(' ','_').replace('*','').replace('^', '') for h in headers ] # clean up 
continue_from  = scraperwiki.sqlite.get_var('last_clist_index', default=0)
print 'continuing from: ', continue_from
n = continue_from

while n < len(clist):
    try:
        data = dict(zip(headers, clist[n]))
        
        location = data['Name'] + ', ' + data['Street'] + ', ' + data['Suburb'] + ', \
            ' + data['City'] + ', ' + ', New Zealand'
        latlng = locate(location)
        #Fix
        data['Maori_electorate'] = data['M?ori_Electorate']
        del data['M?ori_Electorate']
        if latlng: data['lat'], data['lng'] = latlng
        data['Management_Contact_Name'] = data['Management_Contact_Name'].title()
        scraperwiki.sqlite.save(unique_keys=['Institution_Number',], data=data)
        print 'saved rec ', n
        n += 1
    except Exception, e:
        # save state in case of exception
        print str(e)
        print 'Save at record: ', n
        scraperwiki.metadata.save('last_clist_index',n)
        sys.exit()

scraperwiki.metadata.save('last_clist_index',0)