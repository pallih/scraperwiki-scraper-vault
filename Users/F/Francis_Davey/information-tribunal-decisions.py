import scraperwiki
import urllib
import re
import urlparse

from scraperwiki import sqlite

# This is an adaptation of the Lands Tribunal scraper which loads the data into its indexes using javascript
# There is no "nice" way to parse this, except by running something like node.js as a scraper
# or having access to something like Selenium and a browser, which is not appropriate for this kind of
# scraperwiki hosted project.
#
# For that reason I am doing the horrible hack of going to pages I know are there.


root_template="http://www.informationtribunal.gov.uk/Public/search.aspx?Page={id}"

search={} # search pattern for each heading

max_range=900

def debug(s):
    print(s)

def clean_string(s):
    '''Removes <br /> and replaces with newline, then strips newlines from start and end.'''
    if type(s) is str:
        (s, N)=re.subn('(?i)<br\s*/>','\n', s)
        return s.strip('\n')
    else:
        return s

known_bad_list=[]
def number_generator():
    for i in range(1, max_range):
        if i in known_bad_list: # there are some missing pages - we should be able to catch them anyway with the bad list but these I know
            continue 
        yield i
        
def end_check(page, html):
    mobj=re.search('(?i)Displaying results (\d+) to (\d+) \(of (\d+)\)</div>', html)
    #print(mobj.group(2), mobj.group(3))
    if mobj:
        if int(mobj.group(2)) == int(mobj.group(3)):
            return True
        else:
            return False
    else:
        return True

def scrape_pages():
    '''A generator which scrapes successive pages from the decisions database.'''

    badlist=[] # list of pages which missed
    for page_id in number_generator():
        url=root_template.format(id=page_id)
        debug(url)
        page=urllib.urlopen(url)
        html=page.read()
    
        if end_check(page, html):
            debug('End {0}'.format(page.geturl()))
            if len(badlist) > 10:
                return
            else:
                badlist.append(page_id)
                continue
        if len(badlist) > 0:
            for bad in badlist:
                sqlite.save(unique_keys=['page_id'], data={'page_id' : page_id}, table_name="badlist")
            badlist=[]
        yield (url, html)

tr_match=re.compile('(?is)<tr(?:"[^"]*"|\s)*?>(.*?)</tr>') #'
td_match=re.compile('(?is)<td(?:"[^"]*"|\s)*?>(.*?)</td>')
tbody_match=re.compile('<tbody>')

for (url, html) in scrape_pages():
    result={}
    problems=[]

    mobj=re.search('''(?is)<table summary="Decisions"(.*?)</table>''', html)
    table_contents=mobj.group(1)
    pos=tbody_match.search(table_contents).start()
    row_no=0
    for row in tr_match.finditer(table_contents, pos):
        #print(row)
        row_no=row_no + 1
        cells=td_match.findall(row.group(1))
        elements=re.split('(?i)\s*<br */>\s*', cells[1])
        ref_match=re.search('(?is)<a.*?href="([^"]*)".*?>(.*?)</a>', elements[0]) #"
        if ref_match:
            decision=urlparse.urljoin(url, ref_match.group(1))
            title=ref_match.group(2)
        else:
            sqlite.save(unique_keys=['row_no'], data={'url': url, 'no' : row_no, 'name' : 'ref_match', 'data' : elements}, table_name='problems')
            decision=None
        debug('decision={0}, zero element=[{1}]'.format(decision, elements[0]))
        additional_party=elements[1].split('span>')[1].strip()
        (ref, N) = re.subn('</?span.*?>','',elements[2])
        ref=ref.strip()
        
        appeal_match=re.search('(?is)(.*?)<a.*?href="([^"]*)".*?>(.*?)</a>', cells[4])
        if appeal_match:
            disposal=appeal_match.group(1).strip()
            appeal_court=appeal_match.group(3).strip()
            if len(appeal_court)==0:
                appeal_link=None
                appeal_court=None
            else:
                appeal_link=urlparse.urljoin(url, appeal_match.group(2))
                #debug('{0} appeal_link={1}'.format(url, appeal_link))
        else:
            disposal=None
            appeal_court=None
            appeal_link=None

        summary_match=re.search('<a.*?href="([^"]*)".*?>(.+?)</a>', cells[3])
        if summary_match:
            summary=summary_match.group(2)
            summary_link=urlparse.urljoin(url, summary_match.group(1))
        else:
            summary=None
            summary_link=None


        data={
            'jurisdiction' : re.sub('(?i)<br ?/>', '\n', cells[0]).strip(),
            'date' : cells[2],
            'decision' : decision,
            'title' : title,
            'additional_party' : additional_party,
            'reference' : ref,
            'appeal_court' : appeal_court,
            'appeal_link' : appeal_link,
            'summary' : summary_link,
            'disposal' : disposal
        }
        
        sqlite.save(unique_keys=['decision'], data=data, table_name='summaries') 
