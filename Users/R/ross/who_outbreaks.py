from datetime import datetime
import scraperwiki
import lxml.html
import re
import urlparse


months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

def parse_date(datestr):
    m = re.match('^(\d+) (\w+) (\d+)', datestr).groups(0)
    return int(m[2]), datetime(year=int(m[2]), month=months.index(m[1]) + 1, day=int(m[0]))

def parse(s):
    m = re.match('.*-(.*) in (.*) -.*', s)
    if m:
        return m.groups(0)[0], m.groups(0)[1]
    m = re.match('.*-(.*) in (.*) \(.*', s)
    if m:
        return m.groups(0)[0], m.groups(0)[1]
    m = re.match('.*-(.*) in (.*)', s)
    if m:
        return m.groups(0)[0], m.groups(0)[1]
    # Changed in 2004
    m = re.match('(.*) [Ii]n (.*)', s)
    if m:
        return m.groups(0)[0], m.groups(0)[1]
    print '**', 'Failed to parse', s
    return s, ''

base_url = "http://www.who.int/csr/don/archive/year/%s/en/index.html"


for year in range(1996, datetime.now().year + 1):
    url = base_url % (year,)
    html = scraperwiki.scrape(url)
    page = lxml.html.fromstring( html )
    l = []

    lis = page.cssselect('.auto_archive li')
    for li in lis:
        href = li.cssselect('a')[0]
        link = urlparse.urljoin( url, href.attrib.get('href') )
        year,date = parse_date( href.text_content() )
        info = li.cssselect('.link_info')[0].text_content()
        disease, where = parse(info)
        disease = disease.strip()
        where = where.strip()

        if '-' in where: 
            where = where[0:where.find('-')].strip()
        if u'–' in where: 
            where = where[0:where.find(u'–')].strip()
        for x in [',',';',':',u'\u2013' ]:
            if x in where:
                where = where[0:where.find(x)].strip()
                disease = where[where.find(x)+1:].strip() + ' ' + disease 

        d = {
            'year': year, 'date':date.isoformat(), 'link':link, 'disease': disease.title(), 'where':where.title()
        }
        l.append(d)

    scraperwiki.sqlite.save(['date','link'], l) 

        from datetime import datetime
import scraperwiki
import lxml.html
import re
import urlparse


months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

def parse_date(datestr):
    m = re.match('^(\d+) (\w+) (\d+)', datestr).groups(0)
    return int(m[2]), datetime(year=int(m[2]), month=months.index(m[1]) + 1, day=int(m[0]))

def parse(s):
    m = re.match('.*-(.*) in (.*) -.*', s)
    if m:
        return m.groups(0)[0], m.groups(0)[1]
    m = re.match('.*-(.*) in (.*) \(.*', s)
    if m:
        return m.groups(0)[0], m.groups(0)[1]
    m = re.match('.*-(.*) in (.*)', s)
    if m:
        return m.groups(0)[0], m.groups(0)[1]
    # Changed in 2004
    m = re.match('(.*) [Ii]n (.*)', s)
    if m:
        return m.groups(0)[0], m.groups(0)[1]
    print '**', 'Failed to parse', s
    return s, ''

base_url = "http://www.who.int/csr/don/archive/year/%s/en/index.html"


for year in range(1996, datetime.now().year + 1):
    url = base_url % (year,)
    html = scraperwiki.scrape(url)
    page = lxml.html.fromstring( html )
    l = []

    lis = page.cssselect('.auto_archive li')
    for li in lis:
        href = li.cssselect('a')[0]
        link = urlparse.urljoin( url, href.attrib.get('href') )
        year,date = parse_date( href.text_content() )
        info = li.cssselect('.link_info')[0].text_content()
        disease, where = parse(info)
        disease = disease.strip()
        where = where.strip()

        if '-' in where: 
            where = where[0:where.find('-')].strip()
        if u'–' in where: 
            where = where[0:where.find(u'–')].strip()
        for x in [',',';',':',u'\u2013' ]:
            if x in where:
                where = where[0:where.find(x)].strip()
                disease = where[where.find(x)+1:].strip() + ' ' + disease 

        d = {
            'year': year, 'date':date.isoformat(), 'link':link, 'disease': disease.title(), 'where':where.title()
        }
        l.append(d)

    scraperwiki.sqlite.save(['date','link'], l) 

        