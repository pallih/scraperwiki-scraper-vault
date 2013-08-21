# http://odysseus.ieee.org/query.html?lk=2&style=standard&st=26

import scraperwiki
import re
import urllib
from BeautifulSoup import BeautifulSoup
from datetime import date
from datetime import timedelta

limit = 25
searchURL = 'http://odysseus.ieee.org/query.html?lk=2&style=standard'
baseURL = 'http://standards.ieee.org'

def scrape_search_page(offset):
    html = scraperwiki.scrape(searchURL +'&st='+str(offset))
    html = BeautifulSoup(html,convertEntities=BeautifulSoup.HTML_ENTITIES)
    div = html.find('div', { "class" : "results" })
    links = div.findAll('a', href=re.compile(r'cs\.html\?url=.*'))
    for a in links:
        match = re.search( r'cs\.html\?url=(.*?)&.*', a['href'], re.M|re.I)
        if match:
            url = urllib.unquote(match.group(1))
            try:
                scrape_standard_page(url)
            except:
                print 'error for URL '+url
        else:
            print 'no match for '+a['href']

def scrape_standard_page(url):
    std = {'id': url}
    html = scraperwiki.scrape(url)
    html = BeautifulSoup(html,convertEntities=BeautifulSoup.HTML_ENTITIES)
    div = html.find('div', id='content')
    std ['title'] = div.find('div', id='title-banner').find('h1').text
    content = div.find('div', id='content-type-landing-content')
    std['description'] = content.find('div', {'class': 'description'}).find('span',{'class': 'description'}).text
    std['status'] = content.find('div', {'class': 'status-box'}).find('img')['alt']
    working_group = content.find('strong', text= 'Working Group:')
    if working_group != None:
        working_group = working_group.findNextSibling('strong')
        if working_group != None:
            std['working_group_name'] = working_group.text
            working_group = working_group.find('a')
            if working_group != None:
                std['working_group_url'] = baseURL + working_group['href']
    
    oversight_committee = content.find('strong', text= 'Oversight Committee:')
    if oversight_committee != None:
        oversight_committee = oversight_committee.findNextSibling('strong')
        if oversight_committee != None:
            std['oversight_committee_name'] = oversight_committee.text
            oversight_committee = oversight_committee.find('a')
            if oversight_committee != None:
                std['oversight_committee_url'] = oversight_committee['href']

    sponsor = content.find('strong', text= 'Sponsor:')
    if sponsor != None:
        sponsor = sponsor.findNextSibling('strong')
        if sponsor != None:
            std['sponsor_name'] = sponsor.text
            sponsor = sponsor.find('a')
            if sponsor != None:
                std['sponsor_url'] = sponsor['href'] 
    
     
    scraperwiki.sqlite.save(unique_keys=['id'], data = std,table_name="standards")

if scraperwiki.sqlite.get_var('offset') == None:
    scraperwiki.sqlite.save_var('offset',0)
offset = scraperwiki.sqlite.get_var('offset')
while offset < 2800:
    scrape_search_page(offset)
    scraperwiki.sqlite.save_var('offset',offset)
    offset = offset+limit

#scrape_search_page(0)
#scrape_standard_page('http://standards.ieee.org/findstds/standard/1159-2009.html')