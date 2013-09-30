# Scraper for Curaçao Chamber of Commerce                                                  #
# http://www.curacao-chamber.an/info/

import urllib2, re, pprint, sys, httplib
from BeautifulSoup import BeautifulSoup as bs
from time import sleep
import scraperwiki

import socket

# timeout in seconds
timeout = 10
socket.setdefaulttimeout(timeout)

def parse(id):
    url = 'http://www.curacao-chamber.an/info/registry/excerpt.asp?companyid=%s&establishmentnr=0' % id
    #h = {'Connection': 'keep-alive'}
    #req = urllib2.Request(url, headers=h)
    resp = urllib2.urlopen(url)
    print resp.info()
    soup = bs(resp.read())
    datatable = soup.find(id='maintable').table
    result = {}
    
    nr, sep, label = soup.find(text=re.compile('registered under number')).partition(':')
    p = re.compile('\d+')
    result['companynr'] =  p.search(nr).group()
    result['label'] = label.strip()
    try:
        result['info'] = soup.find(attrs={'class': re.compile('warning|status')}).text
    except:
        result['info'] = None    
    for row in datatable.findAll(id=re.compile('data_cell')):
        result[str(row['id'])] = row.text
    return result

def cleanActivityInfo(rawstring):
    p = re.compile('In bankruptcy|In liquidation|The business is not longer registered|The legal entity does not longer exist under local laws|The business is discontinued')
    return p.match(rawstring).group()


"""
leftoff_nr = int(scraperwiki.sqlite.get_var('lastnr'))
for nr in range(leftoff_nr+1,122697):
#for nr in range(21093,122697):
    nr = str(nr)
    if True: #not scraperwiki.sqlite.get_var(nr): #scraperwiki.metadata.get(nr):
        print nr
        try:
            result = parse(nr)
            scraperwiki.sqlite.save(['companynr'], result)
            stats = 1
        except Exception, e: #urllib2.HTTPError, e:
            stats  = e
            print e
        scraperwiki.sqlite.save_var(nr, stats)
        scraperwiki.sqlite.save_var('lastnr', nr)
        sleep(0.5)
"""
# Scraper for Curaçao Chamber of Commerce                                                  #
# http://www.curacao-chamber.an/info/

import urllib2, re, pprint, sys, httplib
from BeautifulSoup import BeautifulSoup as bs
from time import sleep
import scraperwiki

import socket

# timeout in seconds
timeout = 10
socket.setdefaulttimeout(timeout)

def parse(id):
    url = 'http://www.curacao-chamber.an/info/registry/excerpt.asp?companyid=%s&establishmentnr=0' % id
    #h = {'Connection': 'keep-alive'}
    #req = urllib2.Request(url, headers=h)
    resp = urllib2.urlopen(url)
    print resp.info()
    soup = bs(resp.read())
    datatable = soup.find(id='maintable').table
    result = {}
    
    nr, sep, label = soup.find(text=re.compile('registered under number')).partition(':')
    p = re.compile('\d+')
    result['companynr'] =  p.search(nr).group()
    result['label'] = label.strip()
    try:
        result['info'] = soup.find(attrs={'class': re.compile('warning|status')}).text
    except:
        result['info'] = None    
    for row in datatable.findAll(id=re.compile('data_cell')):
        result[str(row['id'])] = row.text
    return result

def cleanActivityInfo(rawstring):
    p = re.compile('In bankruptcy|In liquidation|The business is not longer registered|The legal entity does not longer exist under local laws|The business is discontinued')
    return p.match(rawstring).group()


"""
leftoff_nr = int(scraperwiki.sqlite.get_var('lastnr'))
for nr in range(leftoff_nr+1,122697):
#for nr in range(21093,122697):
    nr = str(nr)
    if True: #not scraperwiki.sqlite.get_var(nr): #scraperwiki.metadata.get(nr):
        print nr
        try:
            result = parse(nr)
            scraperwiki.sqlite.save(['companynr'], result)
            stats = 1
        except Exception, e: #urllib2.HTTPError, e:
            stats  = e
            print e
        scraperwiki.sqlite.save_var(nr, stats)
        scraperwiki.sqlite.save_var('lastnr', nr)
        sleep(0.5)
"""
