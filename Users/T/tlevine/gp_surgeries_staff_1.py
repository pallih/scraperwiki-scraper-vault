# Scrapes the URL and name of GP surgeries
# eg: Grove House Surgery, http://www.nhs.uk/ServiceDirectories/Pages/GP.aspx?pid=71243E73-BB80-417D-A817-E776017854B9

# Basic surgery info (address, phone, opening hours) can be found at that URL
# Detailed staff info (including name and GMC number of doctors) can be found by appending '&TopicId=9' to the URL

import scraperwiki
import lxml.html
import urlparse
import re

# scraperwiki.sqlite.save_var('currentpage', 0 )

base = "http://www.nhs.uk/Scorecard/Pages/Results.aspx?OrgType=1&Coords=1799%%2c5148&SearchTerm=ub1+3hw&DistanceFrom=-1&TabId=30&SortType=2"
html = scraperwiki.scrape(base)
page = lxml.html.fromstring(html)
link = page.cssselect('.scorecard-header .pagination a')[0].attrib.get('href')
totalpages = re.search("PageCount=([0-9]+)",link).group(1)

scraperwiki.sqlite.save_var('totalpages', totalpages )

currentpage = scraperwiki.sqlite.get_var('currentpage', 1)

base = base + "&PageCount=%s&PageNumber=%s"

for pagenum in range(int(currentpage), int(totalpages) + 1):
    html = scraperwiki.scrape( base % (str(totalpages), str(pagenum),))
    page = lxml.html.fromstring( html )
    d=[]
    for o in page.cssselect('div.organisation'):
        name = o.cssselect('.organisation-header h2 a')[0].attrib.get('title')
        address = o.cssselect('.address li')[0].text
        id = re.search("([^=]+)$", o.cssselect('.organisation-header h2 a')[0].attrib.get('href')).group(1)
        scraperwiki.sqlite.save(['id'], {'id': id, 'name': name, 'address': address}, table_name='surgeries' )
        html2 = scraperwiki.scrape('http://www.nhs.uk/ServiceDirectories/Pages/GP.aspx?Pid=%s&TopicId=9' % id)
        page2 = lxml.html.fromstring(html2)
        for s in page2.cssselect('.staff-details'):
            name = s.cssselect('h3')[0].text
            try:
                jobtitle = s.xpath('//h4[text()="Job Title:"]/following-sibling::*')[0].text
            except:
                jobtitle = None
            try:
                gmcnumber = s.xpath('//h4[text()="GMC Number:"]/following-sibling::*')[0].text
            except:
                gmcnumber = 'unavailable: ' + name
            try:
                qualifications = s.xpath('//h4[text()="Other qualifications:"]/following-sibling::*')[0].text
            except:
                qualifications = None
            d.append({'gmcnumber': gmcnumber, 'name': name, 'jobtitle': jobtitle, 'qualifications': qualifications, 'surgery': id,'pagenum':pagenum})
    scraperwiki.sqlite.save_var('currentpage', pagenum )
    scraperwiki.sqlite.save(['gmcnumber'], d, table_name='staff' )


