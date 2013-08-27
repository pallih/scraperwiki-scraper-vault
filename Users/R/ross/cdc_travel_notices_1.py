import scraperwiki
import lxml.html
import re
import urlparse
from datetime import datetime

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

def parse_date(datestr):
    m = re.match('^(\w+) (\d+)\, (\d+)', datestr).groups(0)
    return datetime(year=int(m[2]), month=months.index(m[0]) + 1, day=int(m[1]))

def parse_location(loc):
    for r in ['(\w+.*)in (.*)','(\w+.*) for (.*)', '(\w+.*)\, (.*)' ]:
        m = re.match(r, loc)
        if m:
            return m.groups(0)[0].title(), m.groups(0)[1].title()
        

baseurl = 'http://wwwnc.cdc.gov/travel/notices.htm'
html = scraperwiki.scrape(baseurl)
page = lxml.html.fromstring(html)

links_ul = page.cssselect('.std-list-bluearrow')[0]
for li in links_ul:
    link = li.cssselect('a')[0]
    href = urlparse.urljoin(baseurl, link.attrib.get('href'))
    href_text = link.text_content()
    datestr = li.cssselect('.date')[0].text_content()
    dis, loc = parse_location( href_text)

    d = {
        'date': parse_date( datestr ).isoformat(),
        'location': loc,
        'disease' : dis, 
        'link' : href
    }
    scraperwiki.sqlite.save(['date','location'], d, table_name='notices')
    
import scraperwiki
import lxml.html
import re
import urlparse
from datetime import datetime

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

def parse_date(datestr):
    m = re.match('^(\w+) (\d+)\, (\d+)', datestr).groups(0)
    return datetime(year=int(m[2]), month=months.index(m[0]) + 1, day=int(m[1]))

def parse_location(loc):
    for r in ['(\w+.*)in (.*)','(\w+.*) for (.*)', '(\w+.*)\, (.*)' ]:
        m = re.match(r, loc)
        if m:
            return m.groups(0)[0].title(), m.groups(0)[1].title()
        

baseurl = 'http://wwwnc.cdc.gov/travel/notices.htm'
html = scraperwiki.scrape(baseurl)
page = lxml.html.fromstring(html)

links_ul = page.cssselect('.std-list-bluearrow')[0]
for li in links_ul:
    link = li.cssselect('a')[0]
    href = urlparse.urljoin(baseurl, link.attrib.get('href'))
    href_text = link.text_content()
    datestr = li.cssselect('.date')[0].text_content()
    dis, loc = parse_location( href_text)

    d = {
        'date': parse_date( datestr ).isoformat(),
        'location': loc,
        'disease' : dis, 
        'link' : href
    }
    scraperwiki.sqlite.save(['date','location'], d, table_name='notices')
    
import scraperwiki
import lxml.html
import re
import urlparse
from datetime import datetime

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

def parse_date(datestr):
    m = re.match('^(\w+) (\d+)\, (\d+)', datestr).groups(0)
    return datetime(year=int(m[2]), month=months.index(m[0]) + 1, day=int(m[1]))

def parse_location(loc):
    for r in ['(\w+.*)in (.*)','(\w+.*) for (.*)', '(\w+.*)\, (.*)' ]:
        m = re.match(r, loc)
        if m:
            return m.groups(0)[0].title(), m.groups(0)[1].title()
        

baseurl = 'http://wwwnc.cdc.gov/travel/notices.htm'
html = scraperwiki.scrape(baseurl)
page = lxml.html.fromstring(html)

links_ul = page.cssselect('.std-list-bluearrow')[0]
for li in links_ul:
    link = li.cssselect('a')[0]
    href = urlparse.urljoin(baseurl, link.attrib.get('href'))
    href_text = link.text_content()
    datestr = li.cssselect('.date')[0].text_content()
    dis, loc = parse_location( href_text)

    d = {
        'date': parse_date( datestr ).isoformat(),
        'location': loc,
        'disease' : dis, 
        'link' : href
    }
    scraperwiki.sqlite.save(['date','location'], d, table_name='notices')
    
