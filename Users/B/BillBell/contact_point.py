from BeautifulSoup import BeautifulSoup, NavigableString 
from re import compile, IGNORECASE


from string import split
import scraperwiki
import datetime

itemsRE = compile ( "([a-z\s-]+)\(([a-z\s-]+)\)\s-\s([a-z\s-]+)", IGNORECASE )

scraperwiki.sqlite.execute("drop table if exists swdata")
scraperwiki.sqlite.commit()

data = scraperwiki.sqlite.select('datetime()')
startedAt = data [ 0 ] [ 'datetime()' ]

HTML = scraperwiki . scrape ( 'http://contactpoint.ca/index.php?option=com_jobboard&view=list&Itemid=' )
soup = BeautifulSoup ( HTML [ HTML . find ( '<!-- job coloring -->' ) : ] )
links = soup . findAll ( 'a', { 'class' : "JobLink" } )

recNo = 0
for link in links :
    target = link . contents [ 0 ]
    m = itemsRE . search ( target )
    employer = ''
    if m :
        jobTitle, employer, community = m . groups ( )
    else :
        jobTitle = target [ : target . find ( '- ' ) ]
        community = target [ target . rfind ( ' -' ) : ] [ 2 : ]
    jobTitle = jobTitle . strip ( )
    employer = employer . strip ( )
    community = community . strip ( )

    href = 'http://contactpoint.ca%s' % link . attrMap [ 'href' ]

    recNo += 1
    recId = '%s:%s' % ( datetime.datetime.now().strftime('%Y-%m-%d-%H.%M'), recNo, )

    record = {
            'salary': '',
            'jobTitle': jobTitle,
            'jurisdiction': '',
            'community': community,
            'employer': employer,
            'source': 'CP',
            'link': '<a href="%s">%s</a>' % ( href, target, ),
            'startedAt': startedAt,
            'conditions': '',
            'deadline': '',
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
            'link': 'CP',
            'startedAt': startedAt,
            'conditions': '-',
            'deadline': '-',
            'dateposted': '',
            }
scraperwiki.sqlite.save ( [ 'link' ], record )
    
from BeautifulSoup import BeautifulSoup, NavigableString 
from re import compile, IGNORECASE


from string import split
import scraperwiki
import datetime

itemsRE = compile ( "([a-z\s-]+)\(([a-z\s-]+)\)\s-\s([a-z\s-]+)", IGNORECASE )

scraperwiki.sqlite.execute("drop table if exists swdata")
scraperwiki.sqlite.commit()

data = scraperwiki.sqlite.select('datetime()')
startedAt = data [ 0 ] [ 'datetime()' ]

HTML = scraperwiki . scrape ( 'http://contactpoint.ca/index.php?option=com_jobboard&view=list&Itemid=' )
soup = BeautifulSoup ( HTML [ HTML . find ( '<!-- job coloring -->' ) : ] )
links = soup . findAll ( 'a', { 'class' : "JobLink" } )

recNo = 0
for link in links :
    target = link . contents [ 0 ]
    m = itemsRE . search ( target )
    employer = ''
    if m :
        jobTitle, employer, community = m . groups ( )
    else :
        jobTitle = target [ : target . find ( '- ' ) ]
        community = target [ target . rfind ( ' -' ) : ] [ 2 : ]
    jobTitle = jobTitle . strip ( )
    employer = employer . strip ( )
    community = community . strip ( )

    href = 'http://contactpoint.ca%s' % link . attrMap [ 'href' ]

    recNo += 1
    recId = '%s:%s' % ( datetime.datetime.now().strftime('%Y-%m-%d-%H.%M'), recNo, )

    record = {
            'salary': '',
            'jobTitle': jobTitle,
            'jurisdiction': '',
            'community': community,
            'employer': employer,
            'source': 'CP',
            'link': '<a href="%s">%s</a>' % ( href, target, ),
            'startedAt': startedAt,
            'conditions': '',
            'deadline': '',
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
            'link': 'CP',
            'startedAt': startedAt,
            'conditions': '-',
            'deadline': '-',
            'dateposted': '',
            }
scraperwiki.sqlite.save ( [ 'link' ], record )
    
