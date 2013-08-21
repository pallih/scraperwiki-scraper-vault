import scraperwiki
import urllib
import urlparse
import re


def ParseRegion(rurl):
    
    grid = re.search('RiversAgency1', rurl) and 'IE' or 'GB'  # only way to tell it's Northern Ireland
    
    rhtml = urllib.urlopen(rurl).read()
    lines = re.findall('(?s)<TR>(.*?)(?=<TR|</TABLE>)', rhtml)
    headers = [ re.sub('<[^>]*?>|\s|\(|\)|\.', '', th)  for th in re.findall('(?s)<TH[^>]*>(.*?)(?=<TH|$)', lines[0]) ]
    assert headers == ['Number', 'River', 'Location', 'GridRef', 'Operator', 'CatAreakm2', ''], headers
    headers[-1] = 'discontinued'
    
    for line in lines[1:]:
        row = re.findall('(?s)<TD[^>]*>\s*(.*?)\s*(?=<TD|$)', line)
        row = [ re.sub('\s+', ' ', v).strip()  for v in row ]
        data = dict(zip(headers, row))
        
        mnumber = re.match('<A\s*HREF="([^"]*)">([^<]*)</A>$', data['Number'])
        if mnumber:
            data['url'] = urlparse.urljoin(rurl, mnumber.group(1))
            data['Number'] = mnumber.group(2)
        else:
            assert re.match('\d+$', data['Number']), data['Number']

        if data['discontinued'] == '&nbsp;':
            del data['discontinued']
        else:
            assert data['discontinued'] == '*', data

        mgrid = re.match('(\d\d)\s\((\w\w)\)\s(\d\d\d)\s(\d\d\d)$', data['GridRef'])
        assert mgrid, data['GridRef']
        #print mgrid.groups() == "PENDING"
        easting = mgrid.group(1)[0]+mgrid.group(3)+'00'
        northing = mgrid.group(1)[1]+mgrid.group(4)+'00'
        latlng = scraperwiki.geo.os_easting_northing_to_latlng(int(easting), int(northing), grid)
        scraperwiki.datastore.save(unique_keys=['Number'], data=data, latlng=latlng)
        

def Main():
    url = "http://www.nerc-wallingford.ac.uk/ih/nrfa/station_summaries/sht.html"
    html = urllib.urlopen(url).read()
    for ur in re.findall('<A\s*HREF="(op/.*?.html)">', html):
        print ur
        ParseRegion(urlparse.urljoin(url, ur))

Main()

import scraperwiki
import urllib
import urlparse
import re


def ParseRegion(rurl):
    
    grid = re.search('RiversAgency1', rurl) and 'IE' or 'GB'  # only way to tell it's Northern Ireland
    
    rhtml = urllib.urlopen(rurl).read()
    lines = re.findall('(?s)<TR>(.*?)(?=<TR|</TABLE>)', rhtml)
    headers = [ re.sub('<[^>]*?>|\s|\(|\)|\.', '', th)  for th in re.findall('(?s)<TH[^>]*>(.*?)(?=<TH|$)', lines[0]) ]
    assert headers == ['Number', 'River', 'Location', 'GridRef', 'Operator', 'CatAreakm2', ''], headers
    headers[-1] = 'discontinued'
    
    for line in lines[1:]:
        row = re.findall('(?s)<TD[^>]*>\s*(.*?)\s*(?=<TD|$)', line)
        row = [ re.sub('\s+', ' ', v).strip()  for v in row ]
        data = dict(zip(headers, row))
        
        mnumber = re.match('<A\s*HREF="([^"]*)">([^<]*)</A>$', data['Number'])
        if mnumber:
            data['url'] = urlparse.urljoin(rurl, mnumber.group(1))
            data['Number'] = mnumber.group(2)
        else:
            assert re.match('\d+$', data['Number']), data['Number']

        if data['discontinued'] == '&nbsp;':
            del data['discontinued']
        else:
            assert data['discontinued'] == '*', data

        mgrid = re.match('(\d\d)\s\((\w\w)\)\s(\d\d\d)\s(\d\d\d)$', data['GridRef'])
        assert mgrid, data['GridRef']
        #print mgrid.groups() == "PENDING"
        easting = mgrid.group(1)[0]+mgrid.group(3)+'00'
        northing = mgrid.group(1)[1]+mgrid.group(4)+'00'
        latlng = scraperwiki.geo.os_easting_northing_to_latlng(int(easting), int(northing), grid)
        scraperwiki.datastore.save(unique_keys=['Number'], data=data, latlng=latlng)
        

def Main():
    url = "http://www.nerc-wallingford.ac.uk/ih/nrfa/station_summaries/sht.html"
    html = urllib.urlopen(url).read()
    for ur in re.findall('<A\s*HREF="(op/.*?.html)">', html):
        print ur
        ParseRegion(urlparse.urljoin(url, ur))

Main()

import scraperwiki
import urllib
import urlparse
import re


def ParseRegion(rurl):
    
    grid = re.search('RiversAgency1', rurl) and 'IE' or 'GB'  # only way to tell it's Northern Ireland
    
    rhtml = urllib.urlopen(rurl).read()
    lines = re.findall('(?s)<TR>(.*?)(?=<TR|</TABLE>)', rhtml)
    headers = [ re.sub('<[^>]*?>|\s|\(|\)|\.', '', th)  for th in re.findall('(?s)<TH[^>]*>(.*?)(?=<TH|$)', lines[0]) ]
    assert headers == ['Number', 'River', 'Location', 'GridRef', 'Operator', 'CatAreakm2', ''], headers
    headers[-1] = 'discontinued'
    
    for line in lines[1:]:
        row = re.findall('(?s)<TD[^>]*>\s*(.*?)\s*(?=<TD|$)', line)
        row = [ re.sub('\s+', ' ', v).strip()  for v in row ]
        data = dict(zip(headers, row))
        
        mnumber = re.match('<A\s*HREF="([^"]*)">([^<]*)</A>$', data['Number'])
        if mnumber:
            data['url'] = urlparse.urljoin(rurl, mnumber.group(1))
            data['Number'] = mnumber.group(2)
        else:
            assert re.match('\d+$', data['Number']), data['Number']

        if data['discontinued'] == '&nbsp;':
            del data['discontinued']
        else:
            assert data['discontinued'] == '*', data

        mgrid = re.match('(\d\d)\s\((\w\w)\)\s(\d\d\d)\s(\d\d\d)$', data['GridRef'])
        assert mgrid, data['GridRef']
        #print mgrid.groups() == "PENDING"
        easting = mgrid.group(1)[0]+mgrid.group(3)+'00'
        northing = mgrid.group(1)[1]+mgrid.group(4)+'00'
        latlng = scraperwiki.geo.os_easting_northing_to_latlng(int(easting), int(northing), grid)
        scraperwiki.datastore.save(unique_keys=['Number'], data=data, latlng=latlng)
        

def Main():
    url = "http://www.nerc-wallingford.ac.uk/ih/nrfa/station_summaries/sht.html"
    html = urllib.urlopen(url).read()
    for ur in re.findall('<A\s*HREF="(op/.*?.html)">', html):
        print ur
        ParseRegion(urlparse.urljoin(url, ur))

Main()

import scraperwiki
import urllib
import urlparse
import re


def ParseRegion(rurl):
    
    grid = re.search('RiversAgency1', rurl) and 'IE' or 'GB'  # only way to tell it's Northern Ireland
    
    rhtml = urllib.urlopen(rurl).read()
    lines = re.findall('(?s)<TR>(.*?)(?=<TR|</TABLE>)', rhtml)
    headers = [ re.sub('<[^>]*?>|\s|\(|\)|\.', '', th)  for th in re.findall('(?s)<TH[^>]*>(.*?)(?=<TH|$)', lines[0]) ]
    assert headers == ['Number', 'River', 'Location', 'GridRef', 'Operator', 'CatAreakm2', ''], headers
    headers[-1] = 'discontinued'
    
    for line in lines[1:]:
        row = re.findall('(?s)<TD[^>]*>\s*(.*?)\s*(?=<TD|$)', line)
        row = [ re.sub('\s+', ' ', v).strip()  for v in row ]
        data = dict(zip(headers, row))
        
        mnumber = re.match('<A\s*HREF="([^"]*)">([^<]*)</A>$', data['Number'])
        if mnumber:
            data['url'] = urlparse.urljoin(rurl, mnumber.group(1))
            data['Number'] = mnumber.group(2)
        else:
            assert re.match('\d+$', data['Number']), data['Number']

        if data['discontinued'] == '&nbsp;':
            del data['discontinued']
        else:
            assert data['discontinued'] == '*', data

        mgrid = re.match('(\d\d)\s\((\w\w)\)\s(\d\d\d)\s(\d\d\d)$', data['GridRef'])
        assert mgrid, data['GridRef']
        #print mgrid.groups() == "PENDING"
        easting = mgrid.group(1)[0]+mgrid.group(3)+'00'
        northing = mgrid.group(1)[1]+mgrid.group(4)+'00'
        latlng = scraperwiki.geo.os_easting_northing_to_latlng(int(easting), int(northing), grid)
        scraperwiki.datastore.save(unique_keys=['Number'], data=data, latlng=latlng)
        

def Main():
    url = "http://www.nerc-wallingford.ac.uk/ih/nrfa/station_summaries/sht.html"
    html = urllib.urlopen(url).read()
    for ur in re.findall('<A\s*HREF="(op/.*?.html)">', html):
        print ur
        ParseRegion(urlparse.urljoin(url, ur))

Main()

import scraperwiki
import urllib
import urlparse
import re


def ParseRegion(rurl):
    
    grid = re.search('RiversAgency1', rurl) and 'IE' or 'GB'  # only way to tell it's Northern Ireland
    
    rhtml = urllib.urlopen(rurl).read()
    lines = re.findall('(?s)<TR>(.*?)(?=<TR|</TABLE>)', rhtml)
    headers = [ re.sub('<[^>]*?>|\s|\(|\)|\.', '', th)  for th in re.findall('(?s)<TH[^>]*>(.*?)(?=<TH|$)', lines[0]) ]
    assert headers == ['Number', 'River', 'Location', 'GridRef', 'Operator', 'CatAreakm2', ''], headers
    headers[-1] = 'discontinued'
    
    for line in lines[1:]:
        row = re.findall('(?s)<TD[^>]*>\s*(.*?)\s*(?=<TD|$)', line)
        row = [ re.sub('\s+', ' ', v).strip()  for v in row ]
        data = dict(zip(headers, row))
        
        mnumber = re.match('<A\s*HREF="([^"]*)">([^<]*)</A>$', data['Number'])
        if mnumber:
            data['url'] = urlparse.urljoin(rurl, mnumber.group(1))
            data['Number'] = mnumber.group(2)
        else:
            assert re.match('\d+$', data['Number']), data['Number']

        if data['discontinued'] == '&nbsp;':
            del data['discontinued']
        else:
            assert data['discontinued'] == '*', data

        mgrid = re.match('(\d\d)\s\((\w\w)\)\s(\d\d\d)\s(\d\d\d)$', data['GridRef'])
        assert mgrid, data['GridRef']
        #print mgrid.groups() == "PENDING"
        easting = mgrid.group(1)[0]+mgrid.group(3)+'00'
        northing = mgrid.group(1)[1]+mgrid.group(4)+'00'
        latlng = scraperwiki.geo.os_easting_northing_to_latlng(int(easting), int(northing), grid)
        scraperwiki.datastore.save(unique_keys=['Number'], data=data, latlng=latlng)
        

def Main():
    url = "http://www.nerc-wallingford.ac.uk/ih/nrfa/station_summaries/sht.html"
    html = urllib.urlopen(url).read()
    for ur in re.findall('<A\s*HREF="(op/.*?.html)">', html):
        print ur
        ParseRegion(urlparse.urljoin(url, ur))

Main()

