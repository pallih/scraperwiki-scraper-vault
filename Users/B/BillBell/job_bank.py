from BeautifulSoup import BeautifulSoup, NavigableString

import scraperwiki
from re import compile

data = scraperwiki.sqlite.select('datetime()')
startedAt = data [ 0 ] [ 'datetime()' ]

scraperwiki.sqlite.execute("drop table if exists swdata")
scraperwiki.sqlite.commit()

PageNum = 0

def get_href ( attrs ) :
    return [ attrs [ i ] [ 1 ]  for i in range ( len ( attrs ) ) if attrs [ i ] [ 0 ] == 'href' ] [ 0 ]

def clean ( item ) :
    return item . replace ( '&nbsp;', '' )
            
finished = False
needBe = True
while not finished :
    PageNum += 1
    URL = 'http://www.jobbank.gc.ca/res-eng.aspx?ProvId=99&kwd=4213+OR+4215&OpPage=50&Stdnt=No&PgNum=%s' % PageNum

    HTML = scraperwiki . scrape ( URL )

    if 'currently unavailable due to technical difficulties' in HTML :
        break

    soup = BeautifulSoup ( HTML )
    jobLinks = soup . findAll ( attrs = {'id' : compile("^RepeaterSearchResults_")})

    for jobLink in jobLinks :
        jobTitle = jobLink . string
        link = '<a href="http://www.jobbank.gc.ca/%s">%s</a>' % ( get_href ( jobLink . attrs ), jobTitle )

        facts = { 'employer': '', 'salary': '', 'jurisdiction': '', 'community': '', 'dateposted': '', }
        p = jobLink . findParent ( )
        g = p . nextSiblingGenerator ( )
        while True :
            try :
                item = g . next ( )
            except :
                break
            if '<img' in item . __repr__ ( ) :
                break
            if not type ( item ) == NavigableString :
                if item and item . string and item . string . strip ( ) . endswith ( ':' ) :
                    label = item . string . strip ( )
                    content = clean ( g . next ( ) . strip ( ) )
                    if label == 'Employer:' :
                        facts [ 'employer' ] = content
                    elif label == 'Salary:' :
                        facts [ 'salary' ] = content
                    elif label == 'Location:' :
                        facts [ 'jurisdiction' ] = content [ -2 : ]
                        facts [ 'community' ] = content [ : -4 ]
                    elif label == 'Date Posted:' :
                        facts [ 'dateposted' ] = content . replace ( '/', '-' )

        record = {
            'salary': facts [ 'salary' ],
            'jobTitle': jobTitle ,
            'jurisdiction': facts ['jurisdiction' ],
            'community': facts [ 'community' ],
            'employer': facts [ 'employer' ],
            'source': 'JB',
            'link': link,
            'startedAt': startedAt,
            'conditions': '',
            'deadline': '',
            'dateposted': facts [ 'dateposted' ],
            }

        next = soup . findAll ( 'a', { 'title': 'Go to next page of result' } )
        finished = len ( next ) == 0        

        scraperwiki.sqlite.save ( [ 'link' ], record )
        needBe = False

if needBe :

    record = {
            'salary': '',
            'jobTitle': '-',
            'jurisdiction': '-',
            'community': '-',
            'employer': '-',
            'source': 'JB',
            'link': '-',
            'startedAt': startedAt,
            'conditions': '-',
            'deadline': '-',
            'dateposted': '',
            }
    scraperwiki.sqlite.save ( [ 'source' ], record )
from BeautifulSoup import BeautifulSoup, NavigableString

import scraperwiki
from re import compile

data = scraperwiki.sqlite.select('datetime()')
startedAt = data [ 0 ] [ 'datetime()' ]

scraperwiki.sqlite.execute("drop table if exists swdata")
scraperwiki.sqlite.commit()

PageNum = 0

def get_href ( attrs ) :
    return [ attrs [ i ] [ 1 ]  for i in range ( len ( attrs ) ) if attrs [ i ] [ 0 ] == 'href' ] [ 0 ]

def clean ( item ) :
    return item . replace ( '&nbsp;', '' )
            
finished = False
needBe = True
while not finished :
    PageNum += 1
    URL = 'http://www.jobbank.gc.ca/res-eng.aspx?ProvId=99&kwd=4213+OR+4215&OpPage=50&Stdnt=No&PgNum=%s' % PageNum

    HTML = scraperwiki . scrape ( URL )

    if 'currently unavailable due to technical difficulties' in HTML :
        break

    soup = BeautifulSoup ( HTML )
    jobLinks = soup . findAll ( attrs = {'id' : compile("^RepeaterSearchResults_")})

    for jobLink in jobLinks :
        jobTitle = jobLink . string
        link = '<a href="http://www.jobbank.gc.ca/%s">%s</a>' % ( get_href ( jobLink . attrs ), jobTitle )

        facts = { 'employer': '', 'salary': '', 'jurisdiction': '', 'community': '', 'dateposted': '', }
        p = jobLink . findParent ( )
        g = p . nextSiblingGenerator ( )
        while True :
            try :
                item = g . next ( )
            except :
                break
            if '<img' in item . __repr__ ( ) :
                break
            if not type ( item ) == NavigableString :
                if item and item . string and item . string . strip ( ) . endswith ( ':' ) :
                    label = item . string . strip ( )
                    content = clean ( g . next ( ) . strip ( ) )
                    if label == 'Employer:' :
                        facts [ 'employer' ] = content
                    elif label == 'Salary:' :
                        facts [ 'salary' ] = content
                    elif label == 'Location:' :
                        facts [ 'jurisdiction' ] = content [ -2 : ]
                        facts [ 'community' ] = content [ : -4 ]
                    elif label == 'Date Posted:' :
                        facts [ 'dateposted' ] = content . replace ( '/', '-' )

        record = {
            'salary': facts [ 'salary' ],
            'jobTitle': jobTitle ,
            'jurisdiction': facts ['jurisdiction' ],
            'community': facts [ 'community' ],
            'employer': facts [ 'employer' ],
            'source': 'JB',
            'link': link,
            'startedAt': startedAt,
            'conditions': '',
            'deadline': '',
            'dateposted': facts [ 'dateposted' ],
            }

        next = soup . findAll ( 'a', { 'title': 'Go to next page of result' } )
        finished = len ( next ) == 0        

        scraperwiki.sqlite.save ( [ 'link' ], record )
        needBe = False

if needBe :

    record = {
            'salary': '',
            'jobTitle': '-',
            'jurisdiction': '-',
            'community': '-',
            'employer': '-',
            'source': 'JB',
            'link': '-',
            'startedAt': startedAt,
            'conditions': '-',
            'deadline': '-',
            'dateposted': '',
            }
    scraperwiki.sqlite.save ( [ 'source' ], record )
