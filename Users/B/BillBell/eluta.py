from urllib import urlopen, quote
from BeautifulSoup import BeautifulSoup, NavigableString
from string import split
import scraperwiki

data = scraperwiki.sqlite.select('datetime()')
startedAt = data [ 0 ] [ 'datetime()' ]

scraperwiki.sqlite.execute("drop table if exists swdata")
scraperwiki.sqlite.commit()

kws = { 
'career' : [
set ( [ 'career', 'advisor', ] ),
set ( [ 'career', 'consultant', ] ),
set ( [ 'career', 'counsellor', ] ),
set ( [ 'career', 'counselor', ] ),
set ( [ 'career', 'coach', ] ),
set ( [ 'career', 'development', 'officer', ] ),
set ( [ 'career', 'development', 'facillitator', ] ),
set ( [ 'career', 'development', 'facilitator', ] ),
set ( [ 'career', 'group', 'facillitator', ] ),
set ( [ 'career', 'group', 'facilitator', ] ),
set ( [ 'career', 'resource', 'centre', 'coordinator', ] ),
set ( [ 'career', 'resource', 'center', 'coordinator', ] ),
],
'employment' : [
set ( [ 'employment', 'advisor', ] ),
set ( [ 'employment', 'consultant', ] ),
set ( [ 'employment', 'coordinator', ] ),
set ( [ 'employment', 'counsellor', ] ),
set ( [ 'employment', 'counselor', ] ),
set ( [ 'employment', 'officer', ] ),
set ( [ 'employment', 'rehabilitation', 'worker', ] ),
set ( [ 'employment', 'services', 'assessment', 'officer', ] ),
set ( [ 'employment', 'specialist', ] ),
set ( [ 'employment', 'support', ] ),
],
'intake' : [
set ( [ 'intake', 'coordinator', ] ),
],
'job' : [
set ( [ 'job', 'coach', ] ),
set ( [ 'job', 'developer', ] ),
set ( [ 'job', 'finding', 'club', ] ),
set ( [ 'job', 'counsellor', ] ),
set ( [ 'job', 'counselor', ] ),
], 
'language' : [
set ( [ 'language', 'training', 'instructor', ] ),
],
'outplacement' : [
set ( [ 'outplacement', ] ),
],
'vocational' : [
set ( [ 'vocational', 'program', 'facillitator', ] ),
set ( [ 'vocational', 'program', 'facilitator', ] ),
set ( [ 'vocational', 'rehabilitation', 'consultant', ] ),
set ( [ 'vocational', 'support', 'worker', ] ),
],
}

def getInnerText ( item ) :
    result = ''
    if type ( item ) is NavigableString :
        return unicode ( item )
    elif item :
        for content in item . contents :
            result += ' %s' % getInnerText ( content ) 
    else :
        result = ''
    return result
            
for kw in kws :
    
    URL = 'http://www.eluta.ca/search?field=&q=&xq=&tq=%s&eq=&city=&province=&pcode=&radius=50&advanced=1' % quote ( kw )

    while URL :
        print URL
        
        try :
            HTML = scraperwiki . scrape ( URL )
        except :
            break

        soup = BeautifulSoup ( HTML )
        
        jobRows = soup . findAll ( 'h2' )
        for jobRow in jobRows :
            jobTitle = getInnerText ( jobRow . findChild ( 'span' ) ) . strip ( )
            
            jobTitleWords = split ( jobTitle . lower ( ), ' ' )
            acceptable = False
            for kwSet in kws [ kw ] :
                if kwSet . issubset ( set ( jobTitleWords ) ) :
                    acceptable = True
                    break
            if not acceptable :
                continue
            
            location = jobRow. findNextSibling ( 'span', { 'class' : 'resultContent' } ).findChild('span',{'itemprop':"addressLocality"}).string
            jurisdiction = location [ -2 : ]
            community = location [ : -3 ] . strip ( )
            employer = jobRow. findNextSibling ( 'span', { 'class' : 'resultContent' } ).findChild('a').string
            source = 'EL'
            attrs = jobRow. findChild ( 'a' ) . attrs
            for attr in attrs :
                if attr [ 0 ] == 'href' :
                    link = attr [ 1 ]
                    break
            link = '<a href="http://www.eluta.ca%s">%s</a>' % ( link, jobTitle, )
            
            record = {
                'salary':  '',
                'jobTitle': jobTitle,
                'jurisdiction': jurisdiction,
                'community': community,
                'employer': employer,
                'source': source,
                'link': link,
                'startedAt': startedAt,
                'conditions': '',
                'deadline': '',
                'dateposted': '',
                }

            scraperwiki.sqlite.save ( [ 'link' ], record )

                
        #~ continue

        URL = ''

        input = soup . find ( 'input', { 'name': 'pg' } )
        if input :
            inputParent = input . findParent ( 'span' )
            if inputParent . previousSibling ( ) and getInnerText ( inputParent . previousSibling ( ) [ 0 ] ) . find ( 'Next' ) != -1 :
                for attr in inputParent . previousSibling ( ) [ 0 ] . attrs :
                    if attr [ 0 ] == 'href' :
                        URL = attr [ 1 ]
                        break
        if URL :
            URL = 'http://www.eluta.ca%s' % URL 
            
    #~ break

