# -*- coding: utf-8 -*-

import scraperwiki
from lxml.html import parse
import urllib, urlparse
import datetime
import urllib2


def getFullSpeech(url):
    html = urllib2.urlopen(url)
    html = parse(html).getroot()
    try:
        discurso = html.cssselect('div#content p[align="justify"] font[face="Arial"]')
        discurso = discurso[0].text_content().strip()
    except Exception as error:
        print error.message + '-' + url
        discurso = ''
    return discurso

def fixUrl(url):
    # turn string into unicode
    if not isinstance(url,unicode):
        url = url.decode('utf8')

    # parse it
    parsed = urlparse.urlsplit(url)

    # divide the netloc further
    userpass,at,hostport = parsed.netloc.partition('@')
    user,colon1,pass_ = userpass.partition(':')
    host,colon2,port = hostport.partition(':')

    # encode each component
    scheme = parsed.scheme.encode('utf8')
    user = urllib.quote(user.encode('utf8'))
    colon1 = colon1.encode('utf8')
    pass_ = urllib.quote(pass_.encode('utf8'))
    at = at.encode('utf8')
    host = host.encode('idna')
    colon2 = colon2.encode('utf8')
    port = port.encode('utf8')
    path = '/'.join(  # could be encoded slashes!
        urllib.quote(urllib.unquote(pce).encode('utf8'),'')
        for pce in parsed.path.split('/')
    )
    query = urllib.quote(urllib.unquote(parsed.query).encode('utf8'),'=&?/')
    fragment = urllib.quote(urllib.unquote(parsed.fragment).encode('utf8'))

    # put it back together
    netloc = ''.join((user,colon1,pass_,at,host,colon2,port))
    return urlparse.urlunsplit((scheme,netloc,path,query,fragment))


def rockndroll(last_date):
    while True:
        print 'Scraping ' + last_date
        speeches = scraperwiki.sqlite.select('* from swdata WHERE date==?', last_date)
        for speech in speeches:
            speech['abstract'] = speech['text'] #move o texto pra abstract
            speech['text'] = getFullSpeech(fixUrl(speech['source_uri'])) #get the full text
            if speech['text']:
                speech['full_text'] = 1 #set the full_text flag to true!
            else:
                speech['full_text'] = 0
                
            scraperwiki.sqlite.save(['id'], speech, table_name='full_speeches')
        scraperwiki.sqlite.save_var('last_date', last_date) #saves today after scraping
        yesterday = datetime.datetime.strptime(last_date, '%d/%m/%Y')-datetime.timedelta(1) #moves the system day by day. safer!
        last_date = yesterday.strftime('%d/%m/%Y')
        #re-run scraper

#scraperwiki.sqlite.save_var('last_date', '22/09/2011')
last_date = scraperwiki.sqlite.get_var('last_date', '22/10/2011') #try to get last scraped date formated as %d/%m/%Y

scraperwiki.sqlite.attach('ogdc-brazillian-congress-speeches')

rockndroll(last_date)# -*- coding: utf-8 -*-

import scraperwiki
from lxml.html import parse
import urllib, urlparse
import datetime
import urllib2


def getFullSpeech(url):
    html = urllib2.urlopen(url)
    html = parse(html).getroot()
    try:
        discurso = html.cssselect('div#content p[align="justify"] font[face="Arial"]')
        discurso = discurso[0].text_content().strip()
    except Exception as error:
        print error.message + '-' + url
        discurso = ''
    return discurso

def fixUrl(url):
    # turn string into unicode
    if not isinstance(url,unicode):
        url = url.decode('utf8')

    # parse it
    parsed = urlparse.urlsplit(url)

    # divide the netloc further
    userpass,at,hostport = parsed.netloc.partition('@')
    user,colon1,pass_ = userpass.partition(':')
    host,colon2,port = hostport.partition(':')

    # encode each component
    scheme = parsed.scheme.encode('utf8')
    user = urllib.quote(user.encode('utf8'))
    colon1 = colon1.encode('utf8')
    pass_ = urllib.quote(pass_.encode('utf8'))
    at = at.encode('utf8')
    host = host.encode('idna')
    colon2 = colon2.encode('utf8')
    port = port.encode('utf8')
    path = '/'.join(  # could be encoded slashes!
        urllib.quote(urllib.unquote(pce).encode('utf8'),'')
        for pce in parsed.path.split('/')
    )
    query = urllib.quote(urllib.unquote(parsed.query).encode('utf8'),'=&?/')
    fragment = urllib.quote(urllib.unquote(parsed.fragment).encode('utf8'))

    # put it back together
    netloc = ''.join((user,colon1,pass_,at,host,colon2,port))
    return urlparse.urlunsplit((scheme,netloc,path,query,fragment))


def rockndroll(last_date):
    while True:
        print 'Scraping ' + last_date
        speeches = scraperwiki.sqlite.select('* from swdata WHERE date==?', last_date)
        for speech in speeches:
            speech['abstract'] = speech['text'] #move o texto pra abstract
            speech['text'] = getFullSpeech(fixUrl(speech['source_uri'])) #get the full text
            if speech['text']:
                speech['full_text'] = 1 #set the full_text flag to true!
            else:
                speech['full_text'] = 0
                
            scraperwiki.sqlite.save(['id'], speech, table_name='full_speeches')
        scraperwiki.sqlite.save_var('last_date', last_date) #saves today after scraping
        yesterday = datetime.datetime.strptime(last_date, '%d/%m/%Y')-datetime.timedelta(1) #moves the system day by day. safer!
        last_date = yesterday.strftime('%d/%m/%Y')
        #re-run scraper

#scraperwiki.sqlite.save_var('last_date', '22/09/2011')
last_date = scraperwiki.sqlite.get_var('last_date', '22/10/2011') #try to get last scraped date formated as %d/%m/%Y

scraperwiki.sqlite.attach('ogdc-brazillian-congress-speeches')

rockndroll(last_date)