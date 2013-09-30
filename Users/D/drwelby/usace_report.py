import scraperwiki
from BeautifulSoup import BeautifulSoup 
from urlparse import urlparse, parse_qs

html = scraperwiki.scrape("https://dl.dropbox.com/u/21330364/USACE%20%20Regulatory%20Permits%20Issued%20and%20Denied.html")

soup = BeautifulSoup(html)

table = soup.find('table', id='report_R12782901324074781')

for row in table('tr'):
    try:
        tds = row('td')
        district = tds[0].contents[0]
        DAnum = tds[1].contents[0]
        applicant = tds[2].contents[0]
        projname = tds[3].contents[0]
        permittype = tds[4].contents[0]
        pubdate = tds[5].contents[0]
        action = tds[6].contents[0]
        dateiss = tds[7].contents[0]
        mapurl = tds[8]
        
        if mapurl.a: 
            coords = parse_qs(urlparse(mapurl.a['href']).query)['q'][0].split(' ')
            lat = coords[0]
            lon = coords[1]
            scraperwiki.sqlite.save(unique_keys=["DAnum"], data={
                "DAnum":DAnum,
                "district":district,
                "applicant":applicant,
                "projname":projname,
                "permittype":permittype,
                "pubdate":pubdate,
                "action":action,
                "dateiss":dateiss,
                "lat":float(lat),
                "lon":float(lon)})

    except IndexError:
        pass

import scraperwiki
from BeautifulSoup import BeautifulSoup 
from urlparse import urlparse, parse_qs

html = scraperwiki.scrape("https://dl.dropbox.com/u/21330364/USACE%20%20Regulatory%20Permits%20Issued%20and%20Denied.html")

soup = BeautifulSoup(html)

table = soup.find('table', id='report_R12782901324074781')

for row in table('tr'):
    try:
        tds = row('td')
        district = tds[0].contents[0]
        DAnum = tds[1].contents[0]
        applicant = tds[2].contents[0]
        projname = tds[3].contents[0]
        permittype = tds[4].contents[0]
        pubdate = tds[5].contents[0]
        action = tds[6].contents[0]
        dateiss = tds[7].contents[0]
        mapurl = tds[8]
        
        if mapurl.a: 
            coords = parse_qs(urlparse(mapurl.a['href']).query)['q'][0].split(' ')
            lat = coords[0]
            lon = coords[1]
            scraperwiki.sqlite.save(unique_keys=["DAnum"], data={
                "DAnum":DAnum,
                "district":district,
                "applicant":applicant,
                "projname":projname,
                "permittype":permittype,
                "pubdate":pubdate,
                "action":action,
                "dateiss":dateiss,
                "lat":float(lat),
                "lon":float(lon)})

    except IndexError:
        pass

