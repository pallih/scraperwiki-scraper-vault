# -*- coding: utf-8 -*-

import scraperwiki
import urllib2
import sys
import datetime
from lxml import etree

# This scraper aims to archive metadata about radio features including MP3 url
# for the public German radio stations Deutschlandfunk, Deutschlandradio Kultur
# and DRadio Wissen


# complete url examples:

# http://www.dradio.de/aodflash/get/get_audiolist.xml.php?station=1&page=1
# http://www.dradio.de/aodflash/get/get_audiolist.xml.php?station=4&date=20110622
# http://www.dradio.de/aodflash/get/get_audiolist.xml.php?station=1&date=20110621&page=3

# Stations
stations = {
    1: 'Deutschlandfunk',
    3: 'Deutschlandradio Kultur',
    4: 'DRadio Wissen'
}

def get_list_page(station_id, page=0, start_date=None):
    global stations
    result = {}
    url = 'http://www.dradio.de/aodflash/get/get_audiolist.xml.php?station=%d&page=%d' % (station_id, page)
    if start_date is not None:
        url += '&date=' + start_date.strftime('%Y%m%d')
    print url
    try:
        f = urllib2.urlopen(url)
    except URLError, msg:
        sys.stderr.write('Could not open ' + url + '. ' + msg)
        return false
    xml = f.read()
    root = etree.fromstring(xml)

    # get header information
    # <... date="" init="" date_to="" station="1" broadcast="" theme="" search="" ids="" count="17120" page="0" pages="571" from="0" to="30">
    if root.get('count') is not None:
        result['count'] = int(root.get('count'))
    if root.get('pages') is not None:
        result['pages'] = int(root.get('pages'))
    if root.get('from') is not None:
        result['from'] = int(root.get('from'))
    if root.get('to') is not None:
        result['to'] = int(root.get('to'))
    
    itemcount = 0
    for item in root.iter('item'):
        itemcount += 1
        if 'items' not in result:
            result['items'] = []
        itemdict = {}
        # get item content as dict
        itemdict['id'] = int(item.get('id'))
        itemdict['file_id'] = item.get('file_id')
        itemdict['url'] = item.get('url')
        itemdict['timestamp'] = int(item.get('timestamp'))
        itemdict['duration'] = int(item.get('duration'))
        itemdict['station'] = stations[int(item.get('station'))]
        for element in item.iter('datetime'):
            #print "datetime: " + element.text
            itemdict['datetime'] = element.text
        for element in item.iter('title'):
            #print "title: " + element.text
            itemdict['title'] = element.text
        for element in item.iter('author'):
            #print "author: " + element.text
            itemdict['author'] = element.text
        for element in item.iter('sendung'):
            #print "sendung: " + element.text
            if element.get('id') is not None and element.get('id') != '':
                itemdict['sendung_id'] = int(element.get('id'))
            if element.get('target') is not None:
                itemdict['sendung_target'] = element.get('target')
        for element in item.iter('article'):
            if element.get('id') is not None and element.get('id') != '':
                #print "article id: " + element.get('id')
                itemdict['article_id'] = int(element.get('id'))
        result['items'].append(itemdict)
    return result

def save_result_items(items):
    scraperwiki.sqlite.save(unique_keys=['id', 'station'], data=items, table_name="beitraege")

def get_article_details(id):
    url = 'http://www.dradio.de/aodflash/get/get_article.xml.php?id=%d' % (id)

def get_sendungen():
    urlmask = 'http://www.dradio.de/aodflash/get/get_sendungen.xml.php?station=%d'
    stations = [0,1,3,4]
    for station in stations:
        url = urlmask % station
        try:
            f = urllib2.urlopen(url)
        except URLError, msg:
            sys.stderr.write('Could not open ' + url + '. ' + msg)
            return false
        sendungen = []
        xml = f.read()
        root = etree.fromstring(xml)
        for item in root.iter('item'):
            sendung = {}
            if item.get('id') is not None:
                sendung['id'] = item.get('id')
            if item.get('target') is not None and item.get('target') != '':
                sendung['target'] = item.get('target')
            sendung['name'] = item.text.strip()
            sendungen.append(sendung)
        scraperwiki.sqlite.save(unique_keys=['id'], data=sendungen, table_name="sendungen")

def get_themen():
    url = 'http://www.dradio.de/aodflash/get/get_themen.xml.php?station=0'
    try:
        f = urllib2.urlopen(url)
    except URLError, msg:
        sys.stderr.write('Could not open ' + url + '. ' + msg)
        return false
    themen = []
    xml = f.read()
    root = etree.fromstring(xml)
    for item in root.iter('item'):
        thema = {}
        if item.get('id') is not None:
            thema['id'] = item.get('id')
        if item.get('target') is not None and item.get('target') != '':
            thema['target'] = item.get('target')
        thema['name'] = item.text.strip()
        themen.append(thema)
    scraperwiki.sqlite.save(unique_keys=['id'], data=themen, table_name="themen")

def main():
    get_sendungen()
    get_themen()
    for station_id in stations.keys():
        print "Scraping station", station_id, "-", stations[station_id]
        result = get_list_page(station_id)
        # store first page items
        if 'items' in result:
            save_result_items(result['items'])
        # get subsequent pages
        if 'pages' in result:
            if result['pages'] > 1:
                print "Getting", result['pages'], "result pages"
                for pagenum in range(1, (result['pages']-1)):
                    result2 = get_list_page(station_id, pagenum)
                    if 'items' in result2:
                        save_result_items(result2['items'])

main()
# -*- coding: utf-8 -*-

import scraperwiki
import urllib2
import sys
import datetime
from lxml import etree

# This scraper aims to archive metadata about radio features including MP3 url
# for the public German radio stations Deutschlandfunk, Deutschlandradio Kultur
# and DRadio Wissen


# complete url examples:

# http://www.dradio.de/aodflash/get/get_audiolist.xml.php?station=1&page=1
# http://www.dradio.de/aodflash/get/get_audiolist.xml.php?station=4&date=20110622
# http://www.dradio.de/aodflash/get/get_audiolist.xml.php?station=1&date=20110621&page=3

# Stations
stations = {
    1: 'Deutschlandfunk',
    3: 'Deutschlandradio Kultur',
    4: 'DRadio Wissen'
}

def get_list_page(station_id, page=0, start_date=None):
    global stations
    result = {}
    url = 'http://www.dradio.de/aodflash/get/get_audiolist.xml.php?station=%d&page=%d' % (station_id, page)
    if start_date is not None:
        url += '&date=' + start_date.strftime('%Y%m%d')
    print url
    try:
        f = urllib2.urlopen(url)
    except URLError, msg:
        sys.stderr.write('Could not open ' + url + '. ' + msg)
        return false
    xml = f.read()
    root = etree.fromstring(xml)

    # get header information
    # <... date="" init="" date_to="" station="1" broadcast="" theme="" search="" ids="" count="17120" page="0" pages="571" from="0" to="30">
    if root.get('count') is not None:
        result['count'] = int(root.get('count'))
    if root.get('pages') is not None:
        result['pages'] = int(root.get('pages'))
    if root.get('from') is not None:
        result['from'] = int(root.get('from'))
    if root.get('to') is not None:
        result['to'] = int(root.get('to'))
    
    itemcount = 0
    for item in root.iter('item'):
        itemcount += 1
        if 'items' not in result:
            result['items'] = []
        itemdict = {}
        # get item content as dict
        itemdict['id'] = int(item.get('id'))
        itemdict['file_id'] = item.get('file_id')
        itemdict['url'] = item.get('url')
        itemdict['timestamp'] = int(item.get('timestamp'))
        itemdict['duration'] = int(item.get('duration'))
        itemdict['station'] = stations[int(item.get('station'))]
        for element in item.iter('datetime'):
            #print "datetime: " + element.text
            itemdict['datetime'] = element.text
        for element in item.iter('title'):
            #print "title: " + element.text
            itemdict['title'] = element.text
        for element in item.iter('author'):
            #print "author: " + element.text
            itemdict['author'] = element.text
        for element in item.iter('sendung'):
            #print "sendung: " + element.text
            if element.get('id') is not None and element.get('id') != '':
                itemdict['sendung_id'] = int(element.get('id'))
            if element.get('target') is not None:
                itemdict['sendung_target'] = element.get('target')
        for element in item.iter('article'):
            if element.get('id') is not None and element.get('id') != '':
                #print "article id: " + element.get('id')
                itemdict['article_id'] = int(element.get('id'))
        result['items'].append(itemdict)
    return result

def save_result_items(items):
    scraperwiki.sqlite.save(unique_keys=['id', 'station'], data=items, table_name="beitraege")

def get_article_details(id):
    url = 'http://www.dradio.de/aodflash/get/get_article.xml.php?id=%d' % (id)

def get_sendungen():
    urlmask = 'http://www.dradio.de/aodflash/get/get_sendungen.xml.php?station=%d'
    stations = [0,1,3,4]
    for station in stations:
        url = urlmask % station
        try:
            f = urllib2.urlopen(url)
        except URLError, msg:
            sys.stderr.write('Could not open ' + url + '. ' + msg)
            return false
        sendungen = []
        xml = f.read()
        root = etree.fromstring(xml)
        for item in root.iter('item'):
            sendung = {}
            if item.get('id') is not None:
                sendung['id'] = item.get('id')
            if item.get('target') is not None and item.get('target') != '':
                sendung['target'] = item.get('target')
            sendung['name'] = item.text.strip()
            sendungen.append(sendung)
        scraperwiki.sqlite.save(unique_keys=['id'], data=sendungen, table_name="sendungen")

def get_themen():
    url = 'http://www.dradio.de/aodflash/get/get_themen.xml.php?station=0'
    try:
        f = urllib2.urlopen(url)
    except URLError, msg:
        sys.stderr.write('Could not open ' + url + '. ' + msg)
        return false
    themen = []
    xml = f.read()
    root = etree.fromstring(xml)
    for item in root.iter('item'):
        thema = {}
        if item.get('id') is not None:
            thema['id'] = item.get('id')
        if item.get('target') is not None and item.get('target') != '':
            thema['target'] = item.get('target')
        thema['name'] = item.text.strip()
        themen.append(thema)
    scraperwiki.sqlite.save(unique_keys=['id'], data=themen, table_name="themen")

def main():
    get_sendungen()
    get_themen()
    for station_id in stations.keys():
        print "Scraping station", station_id, "-", stations[station_id]
        result = get_list_page(station_id)
        # store first page items
        if 'items' in result:
            save_result_items(result['items'])
        # get subsequent pages
        if 'pages' in result:
            if result['pages'] > 1:
                print "Getting", result['pages'], "result pages"
                for pagenum in range(1, (result['pages']-1)):
                    result2 = get_list_page(station_id, pagenum)
                    if 'items' in result2:
                        save_result_items(result2['items'])

main()
# -*- coding: utf-8 -*-

import scraperwiki
import urllib2
import sys
import datetime
from lxml import etree

# This scraper aims to archive metadata about radio features including MP3 url
# for the public German radio stations Deutschlandfunk, Deutschlandradio Kultur
# and DRadio Wissen


# complete url examples:

# http://www.dradio.de/aodflash/get/get_audiolist.xml.php?station=1&page=1
# http://www.dradio.de/aodflash/get/get_audiolist.xml.php?station=4&date=20110622
# http://www.dradio.de/aodflash/get/get_audiolist.xml.php?station=1&date=20110621&page=3

# Stations
stations = {
    1: 'Deutschlandfunk',
    3: 'Deutschlandradio Kultur',
    4: 'DRadio Wissen'
}

def get_list_page(station_id, page=0, start_date=None):
    global stations
    result = {}
    url = 'http://www.dradio.de/aodflash/get/get_audiolist.xml.php?station=%d&page=%d' % (station_id, page)
    if start_date is not None:
        url += '&date=' + start_date.strftime('%Y%m%d')
    print url
    try:
        f = urllib2.urlopen(url)
    except URLError, msg:
        sys.stderr.write('Could not open ' + url + '. ' + msg)
        return false
    xml = f.read()
    root = etree.fromstring(xml)

    # get header information
    # <... date="" init="" date_to="" station="1" broadcast="" theme="" search="" ids="" count="17120" page="0" pages="571" from="0" to="30">
    if root.get('count') is not None:
        result['count'] = int(root.get('count'))
    if root.get('pages') is not None:
        result['pages'] = int(root.get('pages'))
    if root.get('from') is not None:
        result['from'] = int(root.get('from'))
    if root.get('to') is not None:
        result['to'] = int(root.get('to'))
    
    itemcount = 0
    for item in root.iter('item'):
        itemcount += 1
        if 'items' not in result:
            result['items'] = []
        itemdict = {}
        # get item content as dict
        itemdict['id'] = int(item.get('id'))
        itemdict['file_id'] = item.get('file_id')
        itemdict['url'] = item.get('url')
        itemdict['timestamp'] = int(item.get('timestamp'))
        itemdict['duration'] = int(item.get('duration'))
        itemdict['station'] = stations[int(item.get('station'))]
        for element in item.iter('datetime'):
            #print "datetime: " + element.text
            itemdict['datetime'] = element.text
        for element in item.iter('title'):
            #print "title: " + element.text
            itemdict['title'] = element.text
        for element in item.iter('author'):
            #print "author: " + element.text
            itemdict['author'] = element.text
        for element in item.iter('sendung'):
            #print "sendung: " + element.text
            if element.get('id') is not None and element.get('id') != '':
                itemdict['sendung_id'] = int(element.get('id'))
            if element.get('target') is not None:
                itemdict['sendung_target'] = element.get('target')
        for element in item.iter('article'):
            if element.get('id') is not None and element.get('id') != '':
                #print "article id: " + element.get('id')
                itemdict['article_id'] = int(element.get('id'))
        result['items'].append(itemdict)
    return result

def save_result_items(items):
    scraperwiki.sqlite.save(unique_keys=['id', 'station'], data=items, table_name="beitraege")

def get_article_details(id):
    url = 'http://www.dradio.de/aodflash/get/get_article.xml.php?id=%d' % (id)

def get_sendungen():
    urlmask = 'http://www.dradio.de/aodflash/get/get_sendungen.xml.php?station=%d'
    stations = [0,1,3,4]
    for station in stations:
        url = urlmask % station
        try:
            f = urllib2.urlopen(url)
        except URLError, msg:
            sys.stderr.write('Could not open ' + url + '. ' + msg)
            return false
        sendungen = []
        xml = f.read()
        root = etree.fromstring(xml)
        for item in root.iter('item'):
            sendung = {}
            if item.get('id') is not None:
                sendung['id'] = item.get('id')
            if item.get('target') is not None and item.get('target') != '':
                sendung['target'] = item.get('target')
            sendung['name'] = item.text.strip()
            sendungen.append(sendung)
        scraperwiki.sqlite.save(unique_keys=['id'], data=sendungen, table_name="sendungen")

def get_themen():
    url = 'http://www.dradio.de/aodflash/get/get_themen.xml.php?station=0'
    try:
        f = urllib2.urlopen(url)
    except URLError, msg:
        sys.stderr.write('Could not open ' + url + '. ' + msg)
        return false
    themen = []
    xml = f.read()
    root = etree.fromstring(xml)
    for item in root.iter('item'):
        thema = {}
        if item.get('id') is not None:
            thema['id'] = item.get('id')
        if item.get('target') is not None and item.get('target') != '':
            thema['target'] = item.get('target')
        thema['name'] = item.text.strip()
        themen.append(thema)
    scraperwiki.sqlite.save(unique_keys=['id'], data=themen, table_name="themen")

def main():
    get_sendungen()
    get_themen()
    for station_id in stations.keys():
        print "Scraping station", station_id, "-", stations[station_id]
        result = get_list_page(station_id)
        # store first page items
        if 'items' in result:
            save_result_items(result['items'])
        # get subsequent pages
        if 'pages' in result:
            if result['pages'] > 1:
                print "Getting", result['pages'], "result pages"
                for pagenum in range(1, (result['pages']-1)):
                    result2 = get_list_page(station_id, pagenum)
                    if 'items' in result2:
                        save_result_items(result2['items'])

main()
