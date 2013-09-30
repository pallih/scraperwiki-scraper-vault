# -*- coding: iso-8859-15 -*-
currency = u"€"
print currency


baseurl = "http://ec.europa.eu/europeaid/work/funding/beneficiaries/index.cfm"
url ="""http://ec.europa.eu/europeaid/work/funding/beneficiaries/index.cfm?lang=EN&mode=SM&type=grant&order=false&direc=false&paging.offset=4&paging.len=3"""

import scraperwiki
import re

import mechanize 
from BeautifulSoup import BeautifulSoup

# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    # process_individual_page(soup)

    atags = soup.findAll('a')
    for atag_inst in atags:
        atag = atag_inst.find(text=re.compile("Next"))
        if atag:
            next_link = atag_inst['href']
            #print next_link
            if next_link:
                next_url = base_url + next_link['href']
                print next_url
                scrape_and_look_for_next_link(next_url)

def process_individual_page(html):
    soup = BeautifulSoup(html)
    trs = soup.findAll('tr')
    r = []
    title_count = False
    for count,tr in enumerate(trs):
        if count == 3:
            for title_count,tds in enumerate(tr.findAll(style = 'color:white')):
                print tds.strong.text
                r.append(tds.strong.text)
        
            scraperwiki.metadata.save('data_columns', r)
        if count> 3 and title_count:
            record = {}
            for td_count,td in enumerate(tr.findAll('td')):     
                #print td_count,r[td_count],td.text
                record[r[td_count]] = td.text
            #print 'td_count:-', td_count, 'title_count:-', title_count
            if td_count == title_count:  # Sanity Check
                scraperwiki.datastore.save([r[0]], record)
        

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
br = mechanize.Browser()
br.open(baseurl)

br.select_form(name="searchGrants")
br["year"] = ["2009"]
br["amount"] = ["> 2000000"]
 
# and submit the form
br.submit()  

html = br.response().read()


#scrape_and_look_for_next_link(html)

process_individual_page(html)# -*- coding: iso-8859-15 -*-
currency = u"€"
print currency


baseurl = "http://ec.europa.eu/europeaid/work/funding/beneficiaries/index.cfm"
url ="""http://ec.europa.eu/europeaid/work/funding/beneficiaries/index.cfm?lang=EN&mode=SM&type=grant&order=false&direc=false&paging.offset=4&paging.len=3"""

import scraperwiki
import re

import mechanize 
from BeautifulSoup import BeautifulSoup

# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    # process_individual_page(soup)

    atags = soup.findAll('a')
    for atag_inst in atags:
        atag = atag_inst.find(text=re.compile("Next"))
        if atag:
            next_link = atag_inst['href']
            #print next_link
            if next_link:
                next_url = base_url + next_link['href']
                print next_url
                scrape_and_look_for_next_link(next_url)

def process_individual_page(html):
    soup = BeautifulSoup(html)
    trs = soup.findAll('tr')
    r = []
    title_count = False
    for count,tr in enumerate(trs):
        if count == 3:
            for title_count,tds in enumerate(tr.findAll(style = 'color:white')):
                print tds.strong.text
                r.append(tds.strong.text)
        
            scraperwiki.metadata.save('data_columns', r)
        if count> 3 and title_count:
            record = {}
            for td_count,td in enumerate(tr.findAll('td')):     
                #print td_count,r[td_count],td.text
                record[r[td_count]] = td.text
            #print 'td_count:-', td_count, 'title_count:-', title_count
            if td_count == title_count:  # Sanity Check
                scraperwiki.datastore.save([r[0]], record)
        

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
br = mechanize.Browser()
br.open(baseurl)

br.select_form(name="searchGrants")
br["year"] = ["2009"]
br["amount"] = ["> 2000000"]
 
# and submit the form
br.submit()  

html = br.response().read()


#scrape_and_look_for_next_link(html)

process_individual_page(html)