import scraperwiki
import urllib
import re
import urlparse

from scraperwiki import sqlite

# The Lands Tribunal site - at present - loads the data into its indexes using javascript
# There is no "nice" way to parse this, except by running something like node.js as a scraper
# or having access to something like Selenium and a browser, which is not appropriate for this kind of
# scraperwiki hosted project.
#
# For that reason I am doing the horrible hack of going to pages I know are there.


root_template="http://www.landstribunal.gov.uk/Aspx/view.aspx?id={id}"

headings={
    'Decision Number' : 'decision_no',
    'Appellant' : 'appellant', 
    'Respondent' : 'respondent', 
    'Judge/Member' : 'corum', 
    'Date of Decision' : 'decision_date',
    'Main Category' : 'category',
    'Main Subcategory' : 'subcategory',
    'Notes' : 'notes' }

search={} # search pattern for each heading

start_range=1 # can be changed to a higher number for testing
max_range=4000 # just an arbitrarily large number

for heading in headings:
    search_pattern=re.compile('{0}:?.*?</th>.*?<td[^>]*>(.*?)</td>'.format(heading), re.I | re.S)
    search[heading]=search_pattern

def debug(s):
    print(s)

def clean_string(s):
    '''Removes <br /> and replaces with newline, then strips newlines from start and end.'''
    if type(s) is str:
        (s, N)=re.subn('(?i)<br\s*/>','\n', s)
        return s.strip('\n')
    else:
        return s

def number_generator():
    for i in range(start_range, max_range):
        if i in [665, 813]: # there are some missing pages - we should be able to catch them anyway with the bad list but these I know
            continue 
        yield i
        

def scrape_pages():
    '''A generator which scrapes successive pages from the decisions database.'''

    badlist=[] # list of pages which missed
    for page_id in number_generator():
        url=root_template.format(id=page_id)
        debug(url)
        page=urllib.urlopen(url)
    
        if re.search('ErrDefault\.aspx$', page.geturl()): # site returns this if it cannot find the page
            if len(badlist) > 10:
                return
            else:
                badlist.append(page_id)
                continue
        if len(badlist) > 0:
            for bad in badlist:
                sqlite.save(unique_keys=['page_id'], data={'page_id' : page_id}, table_name="badlist")
            badlist=[]
        html=page.read()
        yield (url, html)

for (url, html) in scrape_pages():
    result={}
    problems=[]

    for heading in headings:
        database_key=headings[heading]
        mobj=search[heading].search(html)
        if mobj:
            result[database_key]=clean_string(mobj.group(1))
        else:
            result[database_key]=None
    result['url_summary']=url
    mobj=re.search(r'(?is)<th>.*?Decision(\(s\))? to Download:?.*?</th>.*?<td>(.*?)</td>', html)
    if mobj:
        href_list=re.findall('<a.*?href="([^"]*)"', mobj.group(2))
        print(href_list)
        for href in href_list:
            suffix_match=re.search('(?i)(doc|pdf)$', href)
            if suffix_match:
                result['url_{0}'.format(suffix_match.group(1))]=urlparse.urljoin(url, href)
            else:
                problems.append('Unknown suffix [{0}]'.format(href))
    result['problems']=';'.join(problems)
    sqlite.save(unique_keys=['url_summary'], data=result, table_name='summaries')
import scraperwiki
import urllib
import re
import urlparse

from scraperwiki import sqlite

# The Lands Tribunal site - at present - loads the data into its indexes using javascript
# There is no "nice" way to parse this, except by running something like node.js as a scraper
# or having access to something like Selenium and a browser, which is not appropriate for this kind of
# scraperwiki hosted project.
#
# For that reason I am doing the horrible hack of going to pages I know are there.


root_template="http://www.landstribunal.gov.uk/Aspx/view.aspx?id={id}"

headings={
    'Decision Number' : 'decision_no',
    'Appellant' : 'appellant', 
    'Respondent' : 'respondent', 
    'Judge/Member' : 'corum', 
    'Date of Decision' : 'decision_date',
    'Main Category' : 'category',
    'Main Subcategory' : 'subcategory',
    'Notes' : 'notes' }

search={} # search pattern for each heading

start_range=1 # can be changed to a higher number for testing
max_range=4000 # just an arbitrarily large number

for heading in headings:
    search_pattern=re.compile('{0}:?.*?</th>.*?<td[^>]*>(.*?)</td>'.format(heading), re.I | re.S)
    search[heading]=search_pattern

def debug(s):
    print(s)

def clean_string(s):
    '''Removes <br /> and replaces with newline, then strips newlines from start and end.'''
    if type(s) is str:
        (s, N)=re.subn('(?i)<br\s*/>','\n', s)
        return s.strip('\n')
    else:
        return s

def number_generator():
    for i in range(start_range, max_range):
        if i in [665, 813]: # there are some missing pages - we should be able to catch them anyway with the bad list but these I know
            continue 
        yield i
        

def scrape_pages():
    '''A generator which scrapes successive pages from the decisions database.'''

    badlist=[] # list of pages which missed
    for page_id in number_generator():
        url=root_template.format(id=page_id)
        debug(url)
        page=urllib.urlopen(url)
    
        if re.search('ErrDefault\.aspx$', page.geturl()): # site returns this if it cannot find the page
            if len(badlist) > 10:
                return
            else:
                badlist.append(page_id)
                continue
        if len(badlist) > 0:
            for bad in badlist:
                sqlite.save(unique_keys=['page_id'], data={'page_id' : page_id}, table_name="badlist")
            badlist=[]
        html=page.read()
        yield (url, html)

for (url, html) in scrape_pages():
    result={}
    problems=[]

    for heading in headings:
        database_key=headings[heading]
        mobj=search[heading].search(html)
        if mobj:
            result[database_key]=clean_string(mobj.group(1))
        else:
            result[database_key]=None
    result['url_summary']=url
    mobj=re.search(r'(?is)<th>.*?Decision(\(s\))? to Download:?.*?</th>.*?<td>(.*?)</td>', html)
    if mobj:
        href_list=re.findall('<a.*?href="([^"]*)"', mobj.group(2))
        print(href_list)
        for href in href_list:
            suffix_match=re.search('(?i)(doc|pdf)$', href)
            if suffix_match:
                result['url_{0}'.format(suffix_match.group(1))]=urlparse.urljoin(url, href)
            else:
                problems.append('Unknown suffix [{0}]'.format(href))
    result['problems']=';'.join(problems)
    sqlite.save(unique_keys=['url_summary'], data=result, table_name='summaries')
