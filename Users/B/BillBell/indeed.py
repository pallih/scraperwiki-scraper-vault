from string import split
from urllib import urlopen, quote
from BeautifulSoup import BeautifulSoup, NavigableString
from datetime import datetime, date
import scraperwiki

data = scraperwiki.sqlite.select('datetime()')
startedAt = data [ 0 ] [ 'datetime()' ]

scraperwiki.sqlite.execute("drop table if exists swdata")
scraperwiki.sqlite.commit()

URL_template = 'http://www.indeed.ca/jobs?q=title%3A%28counsellor%29&l=&radius=50&fromage=15'


titles = '''\
career consultant
career counsellor
career counselor
career coach
career development 
career group 
career resource 
employment consultant
employment counsellor
employment counselor
employment rehabilitation 
employment services 
employment specialist
intake coordinator
job coach
job developer
job finding 
job skills 
language training 
outplacement consultant
vocational program 
vocational rehabilitation 
vocational support'''

shortNames = [ 'NS', 'NB', 'NL', 'QC', 'BC', 'AB', 'SK', 'MB', 'ON', 'PE', 'YT', 'NU', 'NT', ]

titles = [ title . strip ( ) for title in split ( titles, '\n' ) ];


def getInnerText ( item ) :
    result = ''
    if type ( item ) is NavigableString :
        return unicode ( item )
    else :
        try :
            for content in item . contents :
                result += ' %s' % getInnerText ( content ) 
        except :
            pass
    return result
            
for title in titles :
    URL = URL_template . replace ( 'counsellor', quote ( title ) )
    while URL :
        print URL
        HTML = urlopen ( URL ) . read ( )
        if HTML . find ( 'did not match any jobs' ) != -1 : break
        soup = BeautifulSoup ( HTML )
        jobTitles = soup . findAll ( 'h2', { 'class': 'jobtitle' } )
        for jobTitle in jobTitles :
            for attr in jobTitle . find ( 'a' ) . attrs :
                if attr [ 0 ] == 'href' :
                    link = attr [ 1 ]
                elif attr [ 0 ] == 'title' :
                    theJobTitle = attr [ 1 ] . strip ( )
            link = '<a href="http://www.indeed.com%s">%s</a>' % ( link, theJobTitle, )
            employer = getInnerText ( jobTitle . findNext ( 'span', { 'class': 'company' } ) )
            location = getInnerText ( jobTitle . findNext ( 'span', { 'class': 'location' } ) )

            jurisdiction = location [ -2 : ]
            community = location [ : -4 ] . strip ( )
            if not jurisdiction in shortNames :
                break
            record = {
                'salary': '',
                'jobTitle': theJobTitle,
                'jurisdiction': jurisdiction,
                'community': community,
                'employer': employer,
                'source': 'IN',
                'link': link,
                'startedAt': startedAt,
                'conditions': '',
                'deadline': '',
                'dateposted': '',
                }
            scraperwiki.sqlite.save ( [ 'link' ], record )
        URL = ''
        possibleNexts = soup . findAll ( 'span', { 'class': 'np' } )
        breakLoop = possibleNexts == [ ]
        for possibleNext in possibleNexts :
            breakLoop = getInnerText ( possibleNext ) . find ( 'Next' ) == -1
            if not breakLoop :
                nextLink = possibleNext . findParent ( 'a' )
                for attr in nextLink . attrs :
                    if attr [ 0 ] == 'href' :
                        URL = 'http://www.indeed.com%s' % attr [ 1 ]
                        found = True
                        break
        if breakLoop :
            break

