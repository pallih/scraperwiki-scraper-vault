# -*- coding: utf-8 -*-                                                                                                                                                                                                                              
import scraperwiki
import urllib2
import re
from BeautifulSoup import BeautifulSoup

base_url = 'http://groups.google.com/group/thackday/topics?gvc=2&sa=N&start='

def scrape(url):
    headers = { 'User-Agent' : 'Mozilla/5.0' }
    req = urllib2.Request(url, None, headers)
    html = urllib2.urlopen(req).read()
    return html

def scrape_msgs(url=''):
    #html = unicode(scraperwiki.scrape(url), 'utf-8', 'ignore')
    html = scrape(url)
    soup = BeautifulSoup(html, fromEncoding='utf-8')

    chunk = soup.find("div", "maincontoutboxatt")
    chunk = chunk.findAll("tr", { "valign" : "baseline" })

    for row in chunk:
        cell = row.findAll("td")
        data = {}
        data['title'] = cell[1].a.text
        data['link'] = 'http://groups.google.com/' + cell[1].a['href']
        data['msgs'] = cell[3].span.contents[1]
        data['msgs'] = data['msgs'].lstrip('of ') #remove o of quando tiver
        data['orig_author'] = cell[4].contents[0]
        data['other_authors'] = cell[4].contents[1].font.text
        #remove os authors todos
        data['other_authors'] = data['other_authors'].lstrip('(')
        data['other_authors'] = data['other_authors'].rstrip(' author)')
        data['other_authors'] = data['other_authors'].rstrip(' authors)')             
        data['date'] = cell[5].text
        data['id'] = cell[0].a['id']
        scraperwiki.sqlite.save(['id'], data) # save the records one by one                          

def scrape_group(url, group_name='thackday'):
    first_page = 0
    url = url + str(first_page)
    html = scrape(url)
    soup = BeautifulSoup(html, fromEncoding='utf-8')
    chunk = soup.find("div", "maincontboxhead")
    chunk = chunk.find("td", { "rowspan" : "3" })
    chunk = chunk.findAll("b")
    msgs_end = chunk[2].text
    return int(msgs_end)

msgs = 0
url = base_url + str(msgs)
msgs_end = scrape_group(url)

while msgs < msgs_end:
    url = base_url + str(msgs)
    scrape_msgs(url)
    msgs = int(msgs) + 30
    print msgs# -*- coding: utf-8 -*-                                                                                                                                                                                                                              
import scraperwiki
import urllib2
import re
from BeautifulSoup import BeautifulSoup

base_url = 'http://groups.google.com/group/thackday/topics?gvc=2&sa=N&start='

def scrape(url):
    headers = { 'User-Agent' : 'Mozilla/5.0' }
    req = urllib2.Request(url, None, headers)
    html = urllib2.urlopen(req).read()
    return html

def scrape_msgs(url=''):
    #html = unicode(scraperwiki.scrape(url), 'utf-8', 'ignore')
    html = scrape(url)
    soup = BeautifulSoup(html, fromEncoding='utf-8')

    chunk = soup.find("div", "maincontoutboxatt")
    chunk = chunk.findAll("tr", { "valign" : "baseline" })

    for row in chunk:
        cell = row.findAll("td")
        data = {}
        data['title'] = cell[1].a.text
        data['link'] = 'http://groups.google.com/' + cell[1].a['href']
        data['msgs'] = cell[3].span.contents[1]
        data['msgs'] = data['msgs'].lstrip('of ') #remove o of quando tiver
        data['orig_author'] = cell[4].contents[0]
        data['other_authors'] = cell[4].contents[1].font.text
        #remove os authors todos
        data['other_authors'] = data['other_authors'].lstrip('(')
        data['other_authors'] = data['other_authors'].rstrip(' author)')
        data['other_authors'] = data['other_authors'].rstrip(' authors)')             
        data['date'] = cell[5].text
        data['id'] = cell[0].a['id']
        scraperwiki.sqlite.save(['id'], data) # save the records one by one                          

def scrape_group(url, group_name='thackday'):
    first_page = 0
    url = url + str(first_page)
    html = scrape(url)
    soup = BeautifulSoup(html, fromEncoding='utf-8')
    chunk = soup.find("div", "maincontboxhead")
    chunk = chunk.find("td", { "rowspan" : "3" })
    chunk = chunk.findAll("b")
    msgs_end = chunk[2].text
    return int(msgs_end)

msgs = 0
url = base_url + str(msgs)
msgs_end = scrape_group(url)

while msgs < msgs_end:
    url = base_url + str(msgs)
    scrape_msgs(url)
    msgs = int(msgs) + 30
    print msgs