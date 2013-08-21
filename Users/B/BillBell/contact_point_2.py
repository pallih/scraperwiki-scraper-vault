from BeautifulSoup import BeautifulSoup, NavigableString 
from string import split
import scraperwiki
import datetime
from itertools import chain

def get_href ( attrs ) :
    return [ attrs [ i ] [ 1 ]  for i in range ( len ( attrs ) ) if attrs [ i ] [ 0 ] == 'href' ] [ 0 ]

provinces = [ 'NS', 'NB', 'NL', 'QC', 'BC', 'AB', 'SK', 'MB', 'ON', 'PE', 'YT', 'NU', 'NT', ]

scraperwiki.sqlite.execute("drop table if exists swdata")
scraperwiki.sqlite.commit()

data = scraperwiki.sqlite.select('datetime()')
startedAt = data [ 0 ] [ 'datetime()' ]

long_provs = {
    'Alberta' : 'AB',
    'British Columbia' : 'BC',
    'New Brunswick' : 'NB',
    'Newfoundland and Labrador' : 'NL',
    'Newfoundland': 'NL',
    'Northwest Territories' : 'NT',
    'Nova Scotia' : 'NS',
    'Nunavut' : 'NU',
    'Ontario' : 'ON' ,
    'Prince Edward Island' : 'PE',
    'Quebec' : 'QC',
    'Saskatchewan': 'SK',
    'Yukon': 'YT',
    }

pageNo = 0
while True :
    pageNo += 1
    HTML = scraperwiki . scrape ( 'http://contactpoint.ca/jobs/page/%s' % pageNo ) 
    if 'No job listings found.' in HTML :
        break
    page = BeautifulSoup ( HTML )
    
    complete_link_cells = page . findAll ( 'td', { 'class' : 'wpjb-column-title' } )
    for complete_link_cell in complete_link_cells :
        joblink = complete_link_cell . find ( 'a' )
        jobTitle = joblink . contents [ 0 ]
        jobURL = joblink . attrs [ 0 ] [ 1 ]
        jobLocationSibling = complete_link_cell.findNextSibling()
        jobLocation = jobLocationSibling . contents [ 0 ] . strip ( ) . replace ( '  ', ' ' )
        if jobLocation . endswith ( ', Canada' ) :
            jobLocation = jobLocation [ : -8 ]
        province_part = ''
        for long_prov in long_provs :
            if long_prov in jobLocation :
                province_part = long_provs [ long_prov] 
                break
        if ',' in jobLocation :
            location_part = jobLocation [ : jobLocation . find ( ',' ) ]
        if not province_part :
            if 'Calgary' in location_part :
                province_part = 'AB'
            if 'Edmonton' in location_part :
                province_part = 'AB'
            if 'High Prairie' in location_part :
                province_part = 'AB'
            if 'Kentville' in location_part :
                province_part = 'NS'
            if 'Scarborough' in location_part :
                province_part = 'ON'
            if 'Picton' in location_part :
                province_part = 'ON'
            if 'Napanee' in location_part :
                province_part = 'ON'
            if 'Richmond Hill' in location_part :
                province_part = 'ON'
            if 'Sudbury' in location_part :
                province_part = 'ON'
            if 'Hamilton' in location_part :
                province_part = 'ON'
            elif 'Toronto' in location_part :
                province_part = 'ON'
            elif 'Mississauga' in location_part :
                province_part = 'ON'
            elif 'Brampton' in location_part :
                province_part = 'ON'
            elif 'North York' in location_part :
                province_part = 'ON'
            elif 'Courtice' in location_part :
                province_part = 'ON'
            elif 'Ajax' in location_part :
                province_part = 'ON'
            elif 'Pickering' in location_part :
                province_part = 'ON'
            elif 'Winnipeg' in location_part :
                province_part = 'MB'
            elif 'Langley' in location_part :
                province_part = 'BC'
            elif 'Surrey' in location_part :
                province_part = 'BC'
            elif 'Vancouver' in location_part :
                province_part = 'BC'
            elif 'St. Laurent' in location_part :
                province_part = 'QC'
            else :
                pass
        dateSibling = jobLocationSibling.findNextSibling()
        dateInfo = dateSibling . contents [ 0 ] . strip ( )
        datePosted = dateSibling . contents [ 0 ] . strip ( )
        if datePosted == 'Today' :
            datePosted = datetime.datetime.now()
        else :
            datePosted = datetime.datetime.strptime('2013%s' % datePosted, '%Y%b, %d')
        datePosted = datePosted.strftime('%Y-%m-%d')
        record = {
            'salary': '',
            'jobTitle': jobTitle,
            'jurisdiction': province_part,
            'community': location_part,
            'employer': '',
            'source': 'CP',
            'link': joblink,
            'startedAt': startedAt,
            'conditions': dateSibling.contents[1].contents[0].strip(),
            'deadline': '_',
            'dateposted': datePosted,
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
scraperwiki.sqlite.save ( [ 'link' ], record )
    
