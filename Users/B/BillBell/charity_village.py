from urllib import urlopen
from BeautifulSoup import BeautifulSoup, NavigableString
from string import split
from datetime import datetime, date
import scraperwiki

data = scraperwiki.sqlite.select('datetime()')
startedAt = data [ 0 ] [ 'datetime()' ]

scraperwiki.sqlite.execute("drop table if exists swdata")
scraperwiki.sqlite.commit()

URL = 'http://www.charityvillage.com/cvnet/job_search.aspx?SearchMode=SEARCH2&sk=0&pt=10000&jc=10000&cl=10000&sie=True&sf=0&st=2147483647&yef=0&yet=2147483647&kito=True&kw=employ,employment,job,jobs,career,vocational&lr=10000&IsPop=True&seoctl00_cphPageContent_fraSearchResults_gvListings=page15'

HTML = urlopen ( URL ) . read ( )
#~ file ( 'HTML.htm', 'w' ) . write ( HTML )

def getInnerText ( item ) :
    result = ''
    if type ( item ) is NavigableString :
        return unicode ( item ) . strip ( )
    else :
        for content in item . contents :
            result += ' %s' % getInnerText ( content ) 
    return result . replace ( '&nbsp;', '' ) . strip ( )
            
#~ HTML = file ( 'HTML.htm' ) . read ( )
p1 = HTML . find ( '<tr id="ctl00_cphPageContent_fraSearchResults_gvListings_DXDataRow0"' )
p2 = HTML [ p1 : ] . find ( '</table' )
HTML = '<table>%s' % HTML [ p1 : p1 + p2 + 9 ]

soup = BeautifulSoup ( HTML )

trs = soup . findAll ( 'tr' )

for tr in trs :
    tds = tr . findAll ( 'td' )
        
    for attr in tds [ 1 ] . contents [ 1 ] . attrs :
        if attr [ 0 ] == 'href' :
            link = attr [ 1 ]
            break
            
    p1 = link . find ( '?id=' )
    p2 = link [ p1 : ] . find ( '&' )
    id = link [ p1 + 4 : p1 + p2 ]
    jobTitle = getInnerText ( tds [ 1 ] )
    
    link = '<a href="%s">%s</a>' % ( link, jobTitle, )
    employer = getInnerText ( tds [ 2 ] )
    jurisdiction = getInnerText ( tds [ 3 ] ) . strip ( ) [ : 2 ]
    community = getInnerText ( tds [ 4 ] )
    
    deadline = tds [ 5 ] . contents [ 0 ]
    d_pieces = [ int ( item ) for item in split ( deadline, '/' ) ]
    if len ( d_pieces ) == 3 :
        deadline = datetime ( d_pieces [ 2 ], d_pieces [ 0 ], d_pieces [ 1 ] ) . strftime ( '%A %d %B %Y' )
        
    record = {
        'salary': '',
        'jobTitle': jobTitle,
        'jurisdiction': jurisdiction,
        'community': community,
        'employer': employer,
        'source': 'CV',
        'link': link,
        'startedAt': startedAt,
        'conditions': '',
        'deadline': deadline,
        'dateposted': '',
        }

    scraperwiki.sqlite.save ( [ 'link' ], record )

record = {
            'salary': '',
            'jobTitle': '-',
            'jurisdiction': '-',
            'community': '-',
            'employer': '-',
            'source': 'CP',
            'link': '-',
            'startedAt': startedAt,
            'conditions': '-',
            'deadline': '-',
            'dateposted': '',
            }
scraperwiki.sqlite.save ( [ 'source' ], record )

from urllib import urlopen
from BeautifulSoup import BeautifulSoup, NavigableString
from string import split
from datetime import datetime, date
import scraperwiki

data = scraperwiki.sqlite.select('datetime()')
startedAt = data [ 0 ] [ 'datetime()' ]

scraperwiki.sqlite.execute("drop table if exists swdata")
scraperwiki.sqlite.commit()

URL = 'http://www.charityvillage.com/cvnet/job_search.aspx?SearchMode=SEARCH2&sk=0&pt=10000&jc=10000&cl=10000&sie=True&sf=0&st=2147483647&yef=0&yet=2147483647&kito=True&kw=employ,employment,job,jobs,career,vocational&lr=10000&IsPop=True&seoctl00_cphPageContent_fraSearchResults_gvListings=page15'

HTML = urlopen ( URL ) . read ( )
#~ file ( 'HTML.htm', 'w' ) . write ( HTML )

def getInnerText ( item ) :
    result = ''
    if type ( item ) is NavigableString :
        return unicode ( item ) . strip ( )
    else :
        for content in item . contents :
            result += ' %s' % getInnerText ( content ) 
    return result . replace ( '&nbsp;', '' ) . strip ( )
            
#~ HTML = file ( 'HTML.htm' ) . read ( )
p1 = HTML . find ( '<tr id="ctl00_cphPageContent_fraSearchResults_gvListings_DXDataRow0"' )
p2 = HTML [ p1 : ] . find ( '</table' )
HTML = '<table>%s' % HTML [ p1 : p1 + p2 + 9 ]

soup = BeautifulSoup ( HTML )

trs = soup . findAll ( 'tr' )

for tr in trs :
    tds = tr . findAll ( 'td' )
        
    for attr in tds [ 1 ] . contents [ 1 ] . attrs :
        if attr [ 0 ] == 'href' :
            link = attr [ 1 ]
            break
            
    p1 = link . find ( '?id=' )
    p2 = link [ p1 : ] . find ( '&' )
    id = link [ p1 + 4 : p1 + p2 ]
    jobTitle = getInnerText ( tds [ 1 ] )
    
    link = '<a href="%s">%s</a>' % ( link, jobTitle, )
    employer = getInnerText ( tds [ 2 ] )
    jurisdiction = getInnerText ( tds [ 3 ] ) . strip ( ) [ : 2 ]
    community = getInnerText ( tds [ 4 ] )
    
    deadline = tds [ 5 ] . contents [ 0 ]
    d_pieces = [ int ( item ) for item in split ( deadline, '/' ) ]
    if len ( d_pieces ) == 3 :
        deadline = datetime ( d_pieces [ 2 ], d_pieces [ 0 ], d_pieces [ 1 ] ) . strftime ( '%A %d %B %Y' )
        
    record = {
        'salary': '',
        'jobTitle': jobTitle,
        'jurisdiction': jurisdiction,
        'community': community,
        'employer': employer,
        'source': 'CV',
        'link': link,
        'startedAt': startedAt,
        'conditions': '',
        'deadline': deadline,
        'dateposted': '',
        }

    scraperwiki.sqlite.save ( [ 'link' ], record )

record = {
            'salary': '',
            'jobTitle': '-',
            'jurisdiction': '-',
            'community': '-',
            'employer': '-',
            'source': 'CP',
            'link': '-',
            'startedAt': startedAt,
            'conditions': '-',
            'deadline': '-',
            'dateposted': '',
            }
scraperwiki.sqlite.save ( [ 'source' ], record )

