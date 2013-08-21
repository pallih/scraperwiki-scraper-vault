#!/usr/bin/python
# -*- coding: utf-8 -*-
import scraperwiki                                                                    
import urllib2
from time import sleep
from string import join
import re

def strips(s):
    "strip('<p>foo bar&nbsp;</p>' => foo bar baz"
    e = re.compile(r'<.*?>')
    ee = re.compile(r'\s+|&nbsp;')
    return ee.sub(' ', e.sub('', s))

def extract(t, s):
    """s = ['Identification number wfefwe: 31 382 266', 'Business name: foo bar baz', ...]
    extract('Identification number', s) => 31 382 266"""
    s = filter(lambda x: t in x, s)
    if s:
        return re.split(':', s[0])[-1]
    else:
        return 'n/a'

def parse_html(html):
    s = re.split(r' \(from: .*?\)', strips(html))
    n = 0
    cname = extract('Business name:', s)
    if cname == 'n/a':
        extract('Business name of the organisational unit:', s)
    if len(cname) > 3:
        cname.replace('- v likvidÃ¡cii', '')
        caddress = extract('Registered seat:', s)
        if caddress == 'n/a':
            caddress = extract('Place of business', s)
        cnumber = extract(r'Identification number', s)
        cfounding = extract('Date of entry', s)
        ctype = extract('Legal form:', s)
        ccapital = extract('Registered capital:', s)
        if ccapital == 'n/a':
            ccapital = extract('Capital:', s)
        if filter(lambda x: 'Date of deletion' in x, s) or filter(lambda x: 'Liquidators:' in x, s):
            cstatus = 'DISSOLVED'
        else:
            cstatus = 'LIVE'
        persons = ''
        if ctype != 'Self-employed individual':
            ss = join(s, sep=" ")
            persons = ss[ss.find('Management body:')+17:ss.find('Acting:')]
        else:
            persons = re.sub('-.*','', cname)
        if 'JUSTICE' in persons:
            persons = 'n/a'
        cpersons = persons.strip(' ;').replace('    ', '; ')
        return [cname, caddress, cnumber, cfounding, ctype, ccapital, cstatus, cpersons]
    else:
        return False

maxn = 100000
urls = [ "http://www.orsr.sk/vypis.asp?lan=en&ID=%s&SID=2&P=0" % n for n in range(1,maxn) ]

def go():
    n = scraperwiki.sqlite.get_var('id')
    runs = scraperwiki.sqlite.get_var('runs')
    if runs is None:
        runs = 0
    if n == maxn:
        n = 0
        scraperwiki.sqlite.save_var('id', n)
        runs = scraperwiki.sqlite.get_var('runs')
        runs += 1
        scraperwiki.sqlite.save_var('runs', r)
    if n is None:
        n = 0
    for url in urls[n:]:
        retry = 3
        while retry:
            if retry == 3:
                n += 1
            print '### URL (retry:', retry, ') No. ', str(n), url
            try:
                r = urllib2.urlopen(url)
                l = parse_html(r.read())
                if l:
                    row = map(lambda x: x.decode('windows-1250').encode('utf8'), l)
                    row.insert(0, n)
                    row.append(url)
#                    for x in row:
#                       print "-->", x
                    scraperwiki.sqlite.save(['UniqueID'],
                                            {'UniqueID': row[0],
                                             'CompanyName': row[1],
                                             'CompanyAddress': row[2],
                                             'CompanyNumber': row[3],
                                             'CompanyFounding': row[4],
                                             'EntityType': row[5],
                                             'CompanyCapital': row[6],
                                             'Status': row[7],
                                             'CompanyManagers': row[8],
                                             'RegistryUrl': row[9]
                                             })
                    scraperwiki.sqlite.save_var('id', n)
                retry = 0
            except urllib2.URLError as e:
                print '!!!/\/\/\!!! ERROR %s !!!/\/\/\!!!' % e
                try:
                            code = e.code
                except:
                            code = 0
                if code == 500:
                            retry = 0 # 500 means bad ID, so don't even retry
                else:
                            retry -= 1
                            #sleep(3)
                            print 'Retrying.....'
            except:
                print '!!!/\/\/\!!! ERROR !!!/\/\/\!!!'
                print 'Retrying.....'
                sleep(3)
                retry -= 1

go()
print "To be continued..."


