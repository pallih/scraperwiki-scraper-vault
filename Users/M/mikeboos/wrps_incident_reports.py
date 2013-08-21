import scraperwiki
import lxml.html
from lxml import etree
import re
from datetime import date, timedelta, datetime
from geopy import geocoders

months = '(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)'

def geocode(locString):
    geoUrl = 'http://geocoder.ca/?geoit=xml&location=' + locString
    xml = scraperwiki.scrape(geoUrl)
    root = etree.fromstring(xml)
    lat = root[0].text
    lon = root[0].text
    return lat, lon

def processIncident(incident, itype, location, text, reportdate):
    #print "%s \n%s \n%s \n%s" % (incident, itype, location, text)
    mdate = re.search(months + '\D{0,10}([0-9]{1,2})\D{1,10}(20[0-9]{2})', text)
    if mdate:
        day = mdate.group(2)
        month = mdate.group(1)[0:3]
        year = mdate.group(3)
    else:
        mdate = re.search('([0-9]{1,2})\D{0,8} ' + months + '\D{0,10}(20[0-9]{2})', text)
        if mdate:
            day = mdate.group(1)
            month = mdate.group(2)[0:3]
            year = mdate.group(3)
        else:
            mdate = re.search(months + '\D{0,10}([0-9]{1,2})', text)
            year = '20' + incident[0:2]
            if mdate:
                day = mdate.group(2)
                month = mdate.group(1)
            else:
                mdate = re.search('([0-9]{1,2})\D{0,8} ' + months, text)
                if mdate:
                    day = mdate.group(1)
                    month = mdate.group(2)
                else:
                    day = None
    mtime = re.search(' ([0-9]{1,2})[:.]?([0-5][0-9])[ ]?([apAP].*?),? ', text)
    if mtime and day is not None:
        hour = int(mtime.group(1))
        minute = mtime.group(2)
        if 'P' in mtime.group(3).capitalize() and hour < 12:
            hour += 12
        if 'A' in mtime.group(3).capitalize() and hour == 12:
            hour = 0
        dt = datetime.strptime(month + ' ' + day + ' ' + year + ' ' + str(hour) + ':' + minute, '%b %d %Y %H:%M')
    elif day is not None:
        dt = datetime.strptime(month + ' ' + day + ' ' + year, '%b %d %Y')
    else:
        dt = None
    #print dt
    #print coord
    fullloc = location.replace(' AT ', ' AND ')
    fullloc = fullloc.replace('EASTERN INTERSECTION', '')
    fullloc = fullloc.replace('SOUTHERN INTERSECTION', '')
    if fullloc.count('KITCHENER') > 1:
        fullloc = fullloc.replace('KITCHENER', '', 1)
    if fullloc.count('CAMBRIDGE') > 1:
        fullloc = fullloc.replace('CAMBRIDGE', '', 1)
    if ' AT ' not in fullloc or ' AND ' not in fullloc:
        street = fullloc.split(',')[0].lower()
        street = street.replace('street', 'st').replace('road', 'rd').replace('drive', 'dr')
        street = street.replace('.','')
        suffix = street.split()[-1]
        if 'north' == suffix:
            street = street.replace(' north', '')
        elif 'south' == suffix:
            street = street.replace(' south', '')
        elif 'east' == suffix:
            street = street.replace(' east', '')
        elif 'west' == suffix:
            street = street.replace(' west', '')
        elif 'w' == suffix or 's' == suffix or 'n' == suffix or 'e' == suffix:
            street = street[:-2]
        stxt = text.lower().replace('street', 'st').replace('road', 'rd').replace('drive', 'dr')
        stxt = stxt.replace('.', '')
        #print stxt
        rexp = '[0-9]+ ' + street + '( [nsew])?|\w+ (rd|st|dr|cr|bv|blvd|boulevard|pl|ave|way)\w*? ([nsew] |north |south |east |west )?(and|at|near|just \w+ of|between|towards|north of|south of|east of|west of) ' + street + '|' + street + '( north| south| east| west)?( [nsew])?' + '[.,]? (and|at|near|just \w+ of|between|past|towards|north of|south of|east of|west of) (\w+ ){1,2}(rd|st |street|dr|cr|bv|blvd|boulevard|pl|ave|way)'
        #print rexp
        match = re.search(rexp,stxt)
        if match:
            fullloc = match.group(0).replace('between', 'and').replace('near', 'and').replace('past', 'and').replace('towards', 'and')
            fullloc = fullloc.replace('just north of', 'and').replace('just south of', 'and').replace('just east of', 'and').replace('just west of', 'and')
            fullloc = fullloc.replace('north of', 'and').replace('south of', 'and').replace('east of', 'and').replace('west of', 'and')
            fullloc = fullloc.replace(',', '')
            fullloc += ', ' + ', '.join(location.split(',')[1:])
            print fullloc

    if 'IRA NEEDLES' in fullloc.upper() and 'UNIVERSITY' in fullloc.upper():
        fullloc = 'IRA NEEDLES AND UNIVERSITY, KITCHENER'
    fullloc = fullloc.replace('EASTERN INTERSECTION', '')
    fullloc = fullloc.replace('SOUTHERN INTERSECTION', '')
    try:
        #results = g.geocode(fullloc, exactly_one=False)
        #place, coord = results[0]
        print fulloc
        lat, lon = geocode(fulloc)
        coord = [lat, lon]
    except:
        coord = [None, None]
    
    scraperwiki.sqlite.save(["incident"], {'incident': incident, 'type': itype, 'location': location, 'text': text, 'date': dt, 'lat': coord[0], 'lon': coord[1], 'reportDate': reportdate, 'locationString': fullloc, 'url': report})

listUrls = []
reportUrls = []

for year in range(date.today().year, date.today().year+1):
    for month in range(date.today().month,date.today().month+1):
        listUrls.append("http://www.wrps.on.ca/news/archive/%d%02d" % (year, month))

while len(listUrls) > 0:
    html = scraperwiki.scrape(listUrls.pop())
    root = lxml.html.fromstring(html)
    links = root.cssselect('div.left-col * a')
    
    for link in links:
        url = link.get('href')
        if url is not None and 'incident-reports' in url and 'read more' not in link.text:
            reportUrls.append('http://www.wrps.on.ca' + url)
        elif url is not None and 'next' in link.text:
            listUrls.append('http://www.wrps.on.ca' + url)

g = geocoders.Google(domain='maps.google.ca')

#scraperwiki.sqlite.execute('drop table swdata')
#scraperwiki.sqlite.commit()

reportUrls.reverse()
for report in reportUrls:
    print report
    html = scraperwiki.scrape(report)
    lines = html.split('\n')
    itype = None
    for line in lines:
        match = re.search('<h1 class="title">.*eports( for)? (.*?)( ?- ?[Uu][Pp][Dd][Aa][Tt][Ee].*)?</h1>', line)
        if match:
            try:
                reportdate = datetime.strptime(match.group(2), '%B %d, %Y')
            except:
                reportdate = datetime.strptime(match.group(2), '%B%d, %Y')
            continue
        match = re.search('^<p>.*?Incident # ([0-9]{2}-[0-9]{6}).*?Type : ([^&]*)&?.*?<br />(.*?)<br />(.*?)</p>', line.strip())
        if match:
            if itype != None:
                processIncident(incident, itype, location, text, reportdate)
                #
    
            incident = match.group(1)
            itype = match.group(2)
            if '<strong>' in itype:
                m2 = re.search('<strong>([^<]*)', itype)
                itype = m2.group(1)
            location = match.group(3).split('(')[0].replace('/', ' AT ')
            location = location.split('>')[-1]
            if ',' in location and location.split(',')[1] == '':
                location += ' WATERLOO, ON'
            text = match.group(4)
            
        elif itype != None:
            match = re.search('^<p>(.*)</p>', line)
            if match:
                text += " " + match.group(1)
    if itype != None:
        processIncident(incident, itype, location, text, reportdate)

