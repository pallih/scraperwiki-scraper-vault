'''Scrapes the case records for cases in the UK Supreme Court, not to be confused with the judgments given in those cases which appear in a different data set. At the moment the scraping is just static, but it might be interesting to scrape so as to see when case status changes.

The case records do not appear to remain on the index for very long (I suspect pre-judgment only) but the pages do seem to stay around longer.'''

import scraperwiki
import BeautifulSoup
import re
import urlparse

from scraperwiki import sqlite

rowclass_regexp=re.compile('(odd|even)\s*$', re.I)
justices_names_pattern=re.compile('''justices(\s|&nbsp;)*allocated(\s|&nbsp;|-)*names''', re.I)
intervener_names_pattern=re.compile('''intervener(\s|&nbsp;|-)*names''', re.I)

root='http://www.supremecourt.gov.uk/current-cases/index.html'

scrape_FLAG=True # set to True if the scraper is to use the web to scrape new data, reset to False for testing data cleaning

# The following function is probably the wrong way to do it - disabled.
def fix_judge(name):
    '''Some judges' names are written incorrectly. The most common error seems to be omitting the suffix (eg 'of XXXX') from
    the title. This function does an ad-hoc fix.'''

    if re.search('(?i)Lord Carnwath', name):
        name='Lord Carnwath of Notting Hill'
    if re.search('(?i)L Hamilton', name):
        name='Lord Hamilton (Scotland)'

    return name

def case_generator(root):
    '''Generates tuples of the id, name, summary and URL for all cases found in the index at the URL given in root.'''
    
    url=root
    while True:
        html=scraperwiki.scrape(url)
        page = BeautifulSoup.BeautifulSoup(html)
        table=page.findAll('table', id='caselist')
        table_body=table[0].findAll('tbody')
        rows=table_body[0].findAll('tr', {'class' : rowclass_regexp}, recursive=False)
        for row in rows:
            case_id=row.findAll('td', {'class' : "secondColumn"})[0].contents[0]
            case_name_raw=row.findAll('td', {'class' : "thirdColumn"})[0]
            case_name=case_name_raw.findAll('strong')[0].contents[0]
            case_summary=row.findAll('td', {'class' : "fourthColumn"})[0].contents[0]
            href=row.findAll('td', {'class' : "fifthColumn"})[0].findAll('a')[0]['href']
            
            yield (case_id, case_name, case_summary, href)
            
        N=page.findAll('a', {'class' : 'active', 'title' : 'Next' })
        if len(N)==0:
            break
        else:
            url=urlparse.urljoin(root, N[0]['href'])

count=0
for (case_id, case_name, case_summary, href) in case_generator(root):
    if not scrape_FLAG:
        break
    count=count+1
    url=urlparse.urljoin(root, href)
    html=scraperwiki.scrape(url)
    page=BeautifulSoup.BeautifulSoup(html)
    DD={}
    for tr in page.findAll('tr'):
        first=tr.findAll('td', {'class' : 'firstColumn'})
        if not first:
            continue
        second=tr.findAll('td', {'class' : 'secondColumn'})
        key=re.sub("&amp;", "and", str(first[0].contents[0]))
        key=key.replace("/", "-")
        if justices_names_pattern.search(key):
            for item in second[0].findAll(text=True):
                if len(item) > 0:
                    #judge_name=fix_judge(item) # probably not the right thing to do here
                    data={'case_id' : case_id, 'judge' : item }
                    sqlite.save(unique_keys=['case_id', 'judge'], data=data, table_name="judges")
        elif intervener_names_pattern.search(key):
            for item in second[0].findAll(text=True):
                if len(item) > 0:
                    data={'case_id' : case_id, 'intervener' : item}
                    sqlite.save(unique_keys=['case_id', 'intervener'], data=data, table_name="interveners")
        else:
            value=second[0].contents[0] if second[0].contents else ''
            DD[key]=value
        
    data={
        '__table' : 'cases',
        'case_id' : case_id,
        'title'   : case_name,
        'summary' : case_summary,
        'href'    : url,
          }
    data.update(DD)
    print [ (k, type(k))  for k in data ]
    sqlite.save(unique_keys=['case_id'], data=data)

sourcescraper = 'uk-supreme-court-cases'
scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select('''judge, date_scraped, case_id from judges''')
for row in data:
    row['judge']=fix_judge(row['judge'])
    sqlite.save(unique_keys=['case_id', 'judge'], data=row, table_name='normalized_judges')


print "Scrape completed\n%s cases parsed" % count


'''Scrapes the case records for cases in the UK Supreme Court, not to be confused with the judgments given in those cases which appear in a different data set. At the moment the scraping is just static, but it might be interesting to scrape so as to see when case status changes.

The case records do not appear to remain on the index for very long (I suspect pre-judgment only) but the pages do seem to stay around longer.'''

import scraperwiki
import BeautifulSoup
import re
import urlparse

from scraperwiki import sqlite

rowclass_regexp=re.compile('(odd|even)\s*$', re.I)
justices_names_pattern=re.compile('''justices(\s|&nbsp;)*allocated(\s|&nbsp;|-)*names''', re.I)
intervener_names_pattern=re.compile('''intervener(\s|&nbsp;|-)*names''', re.I)

root='http://www.supremecourt.gov.uk/current-cases/index.html'

scrape_FLAG=True # set to True if the scraper is to use the web to scrape new data, reset to False for testing data cleaning

# The following function is probably the wrong way to do it - disabled.
def fix_judge(name):
    '''Some judges' names are written incorrectly. The most common error seems to be omitting the suffix (eg 'of XXXX') from
    the title. This function does an ad-hoc fix.'''

    if re.search('(?i)Lord Carnwath', name):
        name='Lord Carnwath of Notting Hill'
    if re.search('(?i)L Hamilton', name):
        name='Lord Hamilton (Scotland)'

    return name

def case_generator(root):
    '''Generates tuples of the id, name, summary and URL for all cases found in the index at the URL given in root.'''
    
    url=root
    while True:
        html=scraperwiki.scrape(url)
        page = BeautifulSoup.BeautifulSoup(html)
        table=page.findAll('table', id='caselist')
        table_body=table[0].findAll('tbody')
        rows=table_body[0].findAll('tr', {'class' : rowclass_regexp}, recursive=False)
        for row in rows:
            case_id=row.findAll('td', {'class' : "secondColumn"})[0].contents[0]
            case_name_raw=row.findAll('td', {'class' : "thirdColumn"})[0]
            case_name=case_name_raw.findAll('strong')[0].contents[0]
            case_summary=row.findAll('td', {'class' : "fourthColumn"})[0].contents[0]
            href=row.findAll('td', {'class' : "fifthColumn"})[0].findAll('a')[0]['href']
            
            yield (case_id, case_name, case_summary, href)
            
        N=page.findAll('a', {'class' : 'active', 'title' : 'Next' })
        if len(N)==0:
            break
        else:
            url=urlparse.urljoin(root, N[0]['href'])

count=0
for (case_id, case_name, case_summary, href) in case_generator(root):
    if not scrape_FLAG:
        break
    count=count+1
    url=urlparse.urljoin(root, href)
    html=scraperwiki.scrape(url)
    page=BeautifulSoup.BeautifulSoup(html)
    DD={}
    for tr in page.findAll('tr'):
        first=tr.findAll('td', {'class' : 'firstColumn'})
        if not first:
            continue
        second=tr.findAll('td', {'class' : 'secondColumn'})
        key=re.sub("&amp;", "and", str(first[0].contents[0]))
        key=key.replace("/", "-")
        if justices_names_pattern.search(key):
            for item in second[0].findAll(text=True):
                if len(item) > 0:
                    #judge_name=fix_judge(item) # probably not the right thing to do here
                    data={'case_id' : case_id, 'judge' : item }
                    sqlite.save(unique_keys=['case_id', 'judge'], data=data, table_name="judges")
        elif intervener_names_pattern.search(key):
            for item in second[0].findAll(text=True):
                if len(item) > 0:
                    data={'case_id' : case_id, 'intervener' : item}
                    sqlite.save(unique_keys=['case_id', 'intervener'], data=data, table_name="interveners")
        else:
            value=second[0].contents[0] if second[0].contents else ''
            DD[key]=value
        
    data={
        '__table' : 'cases',
        'case_id' : case_id,
        'title'   : case_name,
        'summary' : case_summary,
        'href'    : url,
          }
    data.update(DD)
    print [ (k, type(k))  for k in data ]
    sqlite.save(unique_keys=['case_id'], data=data)

sourcescraper = 'uk-supreme-court-cases'
scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select('''judge, date_scraped, case_id from judges''')
for row in data:
    row['judge']=fix_judge(row['judge'])
    sqlite.save(unique_keys=['case_id', 'judge'], data=row, table_name='normalized_judges')


print "Scrape completed\n%s cases parsed" % count


