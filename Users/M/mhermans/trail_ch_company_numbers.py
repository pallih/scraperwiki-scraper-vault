# Scraper for Swiss Business Names Index - Federal Commercial Registry Office 
# http://www.zefix.admin.ch/
# pages of 1500 results: BeautifulSoup to slow, switch to lxml?

import urllib2, re, pprint, sys, uuid
from BeautifulSoup import BeautifulSoup as bs
from lxml import html
from time import sleep
from string import ascii_lowercase
import scraperwiki


def parseResultsPage(query, offset=0):
    url = 'http://www.zefix.admin.ch/WebServices/Zefix/Zefix.asmx/SearchFirm?name=%s' % query
    if offset: url = ''.join([url, '&posMin=', str(offset)])

    stats = {}
    data = {}
    root = html.parse(url).getroot()
    stats['info'] = root.cssselect('b')[1].text
    p = re.compile('\d+')
    stats['nr_results'] = p.search(stats['info']).group()
    if stats['nr_results'] == '0':
        stats['early_return'] = True
        return data, stats, offset
    print stats

    records = root.cssselect('i')
    records.pop(0) # remove first/header

    i = offset+1
    for r in records:
        ond = {}
        ond['location'] = r.find('a').text
        ond['name'] = r.getprevious().text
        if ond['name'] == None: # getting bolded names
            ond['name'] = r.getprevious().tail
        ond['companynr'] = r.getnext().getnext().text
        
        # need key for storage
        if ond['companynr'] == None: ond['companynr'] = str(uuid.uuid4())[0:17]

        ond['recordurl'] = r.getnext().getnext().get('href')
        p = re.compile('parId=(\d+)\&')
        parId = r.getnext().get('href')
        ond['internalid'] = p.search(parId).group(1)
        data[i] = ond
        i += 1
    
    final_url = root.cssselect('a')[-1].text

    offset = None
    if final_url.find('Weiter') > -1:
        p = re.compile('\d+')
        offset = int(p.search(final_url).group())

    stats['nr_parsed'] = len(data)
    return data, stats, offset


def xselections(items, n):
    if n==0: yield []
    else:
        for i in xrange(len(items)):
            for ss in xselections(items, n-1):
                yield [items[i]]+ss

def execute(query, offset=0):
    joint_stats = []
    results, stats, offset = parseResultsPage(query, offset)
    joint_stats.append(stats)

    for recnr, record in results.iteritems():
        scraperwiki.sqlite.save(['companynr'], record)

    if offset: 
        joint_stats.append(execute(query, offset))

    return joint_stats

try:
    for query in xselections(ascii_lowercase, 3):
        q = ''.join(query)
        if not scraperwiki.sqlite.get_var(q):
            #print q
            joint_stats = execute(q,0)
            scraperwiki.sqlite.save_var(q, joint_stats)
            sleep(2)
except Exception as e: # ('ScraperWiki CPU time exceeded')
    print e
