import scraperwiki
import lxml.html
import urlparse

base = "http://www.nhs.uk/Scorecard/Pages/Results.aspx?OrgType=1&Coords=1799%%2c5148&SearchTerm=ub1+3hw&DistanceFrom=-1&PageCount=%s&PageNumber=%s"

# Hardcode, but should get from the original search really
totalpages = 1042
currentpage = scraperwiki.sqlite.get_var('currentpage', 1 )

for pagenum in range(currentpage, totalpages+1):
    html = scraperwiki.scrape( base % (str(totalpages), str(pagenum),))
    page = lxml.html.fromstring( html )
    pagelinks = []
    for x in page.cssselect('.organisation-header'):
        a = x.cssselect('h2 a')[0]
        name = a.attrib.get('title')
        link = a.attrib.get('href')
        link = urlparse.urljoin( base, link )
        pagelinks.append( {'name':name, 'link': link} )
    scraperwiki.sqlite.save(['name'], pagelinks, table_name='namelinkpairs' )
    scraperwiki.sqlite.save_var('currentpage', pagenum )import scraperwiki
import lxml.html
import urlparse

base = "http://www.nhs.uk/Scorecard/Pages/Results.aspx?OrgType=1&Coords=1799%%2c5148&SearchTerm=ub1+3hw&DistanceFrom=-1&PageCount=%s&PageNumber=%s"

# Hardcode, but should get from the original search really
totalpages = 1042
currentpage = scraperwiki.sqlite.get_var('currentpage', 1 )

for pagenum in range(currentpage, totalpages+1):
    html = scraperwiki.scrape( base % (str(totalpages), str(pagenum),))
    page = lxml.html.fromstring( html )
    pagelinks = []
    for x in page.cssselect('.organisation-header'):
        a = x.cssselect('h2 a')[0]
        name = a.attrib.get('title')
        link = a.attrib.get('href')
        link = urlparse.urljoin( base, link )
        pagelinks.append( {'name':name, 'link': link} )
    scraperwiki.sqlite.save(['name'], pagelinks, table_name='namelinkpairs' )
    scraperwiki.sqlite.save_var('currentpage', pagenum )import scraperwiki
import lxml.html
import urlparse

base = "http://www.nhs.uk/Scorecard/Pages/Results.aspx?OrgType=1&Coords=1799%%2c5148&SearchTerm=ub1+3hw&DistanceFrom=-1&PageCount=%s&PageNumber=%s"

# Hardcode, but should get from the original search really
totalpages = 1042
currentpage = scraperwiki.sqlite.get_var('currentpage', 1 )

for pagenum in range(currentpage, totalpages+1):
    html = scraperwiki.scrape( base % (str(totalpages), str(pagenum),))
    page = lxml.html.fromstring( html )
    pagelinks = []
    for x in page.cssselect('.organisation-header'):
        a = x.cssselect('h2 a')[0]
        name = a.attrib.get('title')
        link = a.attrib.get('href')
        link = urlparse.urljoin( base, link )
        pagelinks.append( {'name':name, 'link': link} )
    scraperwiki.sqlite.save(['name'], pagelinks, table_name='namelinkpairs' )
    scraperwiki.sqlite.save_var('currentpage', pagenum )