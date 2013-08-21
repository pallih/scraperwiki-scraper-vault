"""
Copied from http://scraperwiki.com/scrapers/show/oil-and-gas-wells-from-decc/
"""

import scraperwiki
import urllib2, urllib, urlparse
import re
import datetime
import httplib
import time
import mechanize


def main():
    # it only works with a new mechanize object per quadrant
    for i in range(70, 200):
        print "i=%d"%i, 
        quadranturl = getquadranturl(i)
        if not quadranturl:
            break
        welllinks = scrapequrl(quadranturl)
        print "Wells:", len(welllinks)
        for url in welllinks:
            scrapewell(url)


# scrapes the lookup data on a quadrant, which fails due to a bug in the https proxy
def scrapequrl(quadranturl):
    #qhtml = urllib2.urlopen("http://seagrass.goatchurch.org.uk/~julian/cgi-bin/aa.cgi", urllib.urlencode({'url':quadranturl})).read()
    qhtml = urllib2.urlopen(quadranturl).read()
    lurls = re.findall('<A HREF="(/pls/wons/wdep0100.wellHeaderData?.*?)">.*?</A>', qhtml)
    return [ urlparse.urljoin(quadranturl, lurl)  for lurl in lurls ]


# this would be a lot slicker without the bug that makes opening the wellhead data impossible

def getquadranturl(i):
    # set up the mechanize object
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open("https://www.og.decc.gov.uk/pls/wons/wdep0100.qryWell")

    # select the one form on the page
    br.form = list(br.forms())[0]

    # get the select list
    selectcontrol = br.form.find_control(name='f_quadNoList', type='select')

    # exceeded list of quadrants
    if i > len(selectcontrol.items):
        return None
    item = selectcontrol.items[i]
    itemlabel = item.get_labels()[0].text
    print "Selecting quadrant:", itemlabel
    selectcontrol.value = [itemlabel]
    response = br.submit()
    return br.geturl()



feetkeys = [ 'Datum Elevation', 'Ground Elevation', 'Total MD Driller', 'Total MD Logger', 'Water Depth' ]

wellkeys = ['Block No.', 'Block Suffix', 'Bottom Hole Latitude', 'Bottom Hole Longtitude', 'Completion Date', 'Completion Status', 
            'Coordinate System', 'Country Code', 'Date TD Reached', 'Datum Elevation', 'Datum Type', 'Deviated Well', 
            'Drilling Sequence No.', 'Geodetic Datum', 'Ground Elevation', 'Onshore/Offshore', 'Original Intent', 
            'Platform', 'Primary Target', 'Quadrant No.', 'Slot No.', 'Spud Date', 'TVDSS Driller', 
            'Top Hole Longtitude', 'Top hole Latitude', 'Total MD Driller', 'Total MD Logger', 'Water Depth', 
            'Well Registration No.', 'Wellbore Type']

datekeys = ['Completion Date', 'Date TD Reached', 'Spud Date' ]
monthnams = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]


def latlongconv(hnamelat, hnamelong, data, coordsystem):
    hlat = data.pop(hnamelat, "")
    hlng = data.pop(hnamelong, "")
    if not hlat or not hlng:
        return None
    if hlat == '000 00 00.000' and hlng == '000 00 00.000':
        return None
    
    mlat = re.match("(\d\d\d) (\d\d) (\d\d\.\d\d\d)N", hlat)
    mlng = re.match("(\d\d\d) (\d\d) (\d\d\.\d\d\d)([EW])", hlng)
    if not mlat or not mlng:
        return None
    
    # should convert the datum
    lat = int(mlat.group(1)) + int(mlat.group(2)) / 60.0 + float(mlat.group(3)) / 3600    
    lng = int(mlng.group(1)) + int(mlng.group(2)) / 60.0 + float(mlng.group(3)) / 3600
    if mlng.group(4) == "W":
        lng = -lng


    # should convert from ED50 here
    return [lat,lng]


def scrapewell(url):
    # extract the values and check complete
    html = urllib2.urlopen(url).read()
    data = dict(re.findall('<A HREF="/pls/wons/wdep0100.basicWellDataEpic.*">(.*?)</A>\s*=\s*(.*?)\s*<BR>', html))

    for fkey in ['Datum Elevation','Ground Elevation','Total MD Driller','Total MD Logger','Water Depth' ]:
        fkeyfeet = data.pop(fkey + ' (feet)', None)
        fkeymetres = data.pop(fkey + ' (metres)', None)
        if fkeyfeet == 'NULL Value' or fkeymetres == 'NULL Value':
            data[fkey] = 'NULL Value'
        elif fkeymetres:
            data[fkey] = float(fkeymetres)
        elif fkeyfeet:
            data[fkey] = float(fkeyfeet) * 0.3048
            
    skeys = sorted(data.keys())
    assert skeys == wellkeys, [url, skeys]

    # remove NULL Values and convert dates
    for key in data.keys():
        if data[key] == 'NULL Value' or data[key] == '':
            del data[key]
        elif key in datekeys:
            sdate = data[key]
            data[key] = datetime.date(int(sdate[7:]), monthnams.index(sdate[3:6])+1, int(sdate[:2]))  # 22-APR-1985

    # get coordinates
    coordsystem = data.pop('Coordinate System')
    assert coordsystem == data.pop('Geodetic Datum')
    assert coordsystem == 'ED50'

    latlngbottom = latlongconv('Bottom Hole Latitude', 'Bottom Hole Longtitude', data, coordsystem)
    latlngtop = latlongconv('Top hole Latitude', 'Top Hole Longtitude', data, coordsystem)
    if latlngtop:
        data['latlng'] = latlngtop

    assert data.get('Completion Status', None) in ['Completed', 'Suspended', 'Abandoned', None]

    if data.get("Datum Type") == "Kelly Bushing":
        data["Datum Type"] = "KB"

    data['url'] = url
    scraperwiki.datastore.save(unique_keys=["Well Registration No."], data=data, latlng=data.pop('latlng', None), silent=True)



#{u'date': u'None', u'date_scraped': u'2010-07-01 13:42:27', u'latlng': u'057.997105,-00.723548', u'data': {u'Spud_Date': u'2010-06-26', u'Drilling_Sequence_No.': u'10', u'Datum_Type': u'RT', u'Wellbore_Type': u'Initial', u'Block_Suffix': u'b', u'Primary_Target': u'G', u'Block_No.': u'2', u'Well_Registration_No.': u'20/02b- 10', u'Deviated_Well': u'Vertical', u'url': u'https://www.og.decc.gov.uk/pls/wons/wdep0100.wellHeaderData?p_quadNo=20&p_blockNo=2&p_block_suffix=b&p_platform=+&p_drilling_seq_no=10&p_well_suffix=+', u'Country_Code': u'United Kingdom', u'Onshore/Offshore': u'Offshore', u'Quadrant_No.': u'20', u'Water_Depth': u'107.2896', u'Original_Intent': u'Exploration', u'Datum_Elevation': u'24.9936'}}
import simplejson as json

def yearpoints(year):
    year = unicode(year)
    result = [ ]
    sd = "2010-06-26"
    sd = None # for all of them
    for fdata in scraperwiki.datastore.retrieve({"Spud_Date":sd}):
        data = fdata["data"]
        if data["Spud_Date"][:4] != year:
            continue
        latlng = fdata["latlng"].split(",")
        if len(latlng) != 2:
            continue
        lat, lng = map(float, latlng)
        rdata = { 'lat':lat, 'lng':lng }
        rdata['Water_Depth'] = float(data.get('Water_Depth', '0'))
        rdata['Spud_Date'] = data.get('Spud_Date')
        rdata['Original_Intent'] = data.get('Original_Intent')
        rdata['url'] = data.get('url')
        result.append(rdata)
    print "callback(%s)" % json.dumps(result)
    
#print yearpoints("2010")
main()
"""
Copied from http://scraperwiki.com/scrapers/show/oil-and-gas-wells-from-decc/
"""

import scraperwiki
import urllib2, urllib, urlparse
import re
import datetime
import httplib
import time
import mechanize


def main():
    # it only works with a new mechanize object per quadrant
    for i in range(70, 200):
        print "i=%d"%i, 
        quadranturl = getquadranturl(i)
        if not quadranturl:
            break
        welllinks = scrapequrl(quadranturl)
        print "Wells:", len(welllinks)
        for url in welllinks:
            scrapewell(url)


# scrapes the lookup data on a quadrant, which fails due to a bug in the https proxy
def scrapequrl(quadranturl):
    #qhtml = urllib2.urlopen("http://seagrass.goatchurch.org.uk/~julian/cgi-bin/aa.cgi", urllib.urlencode({'url':quadranturl})).read()
    qhtml = urllib2.urlopen(quadranturl).read()
    lurls = re.findall('<A HREF="(/pls/wons/wdep0100.wellHeaderData?.*?)">.*?</A>', qhtml)
    return [ urlparse.urljoin(quadranturl, lurl)  for lurl in lurls ]


# this would be a lot slicker without the bug that makes opening the wellhead data impossible

def getquadranturl(i):
    # set up the mechanize object
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open("https://www.og.decc.gov.uk/pls/wons/wdep0100.qryWell")

    # select the one form on the page
    br.form = list(br.forms())[0]

    # get the select list
    selectcontrol = br.form.find_control(name='f_quadNoList', type='select')

    # exceeded list of quadrants
    if i > len(selectcontrol.items):
        return None
    item = selectcontrol.items[i]
    itemlabel = item.get_labels()[0].text
    print "Selecting quadrant:", itemlabel
    selectcontrol.value = [itemlabel]
    response = br.submit()
    return br.geturl()



feetkeys = [ 'Datum Elevation', 'Ground Elevation', 'Total MD Driller', 'Total MD Logger', 'Water Depth' ]

wellkeys = ['Block No.', 'Block Suffix', 'Bottom Hole Latitude', 'Bottom Hole Longtitude', 'Completion Date', 'Completion Status', 
            'Coordinate System', 'Country Code', 'Date TD Reached', 'Datum Elevation', 'Datum Type', 'Deviated Well', 
            'Drilling Sequence No.', 'Geodetic Datum', 'Ground Elevation', 'Onshore/Offshore', 'Original Intent', 
            'Platform', 'Primary Target', 'Quadrant No.', 'Slot No.', 'Spud Date', 'TVDSS Driller', 
            'Top Hole Longtitude', 'Top hole Latitude', 'Total MD Driller', 'Total MD Logger', 'Water Depth', 
            'Well Registration No.', 'Wellbore Type']

datekeys = ['Completion Date', 'Date TD Reached', 'Spud Date' ]
monthnams = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]


def latlongconv(hnamelat, hnamelong, data, coordsystem):
    hlat = data.pop(hnamelat, "")
    hlng = data.pop(hnamelong, "")
    if not hlat or not hlng:
        return None
    if hlat == '000 00 00.000' and hlng == '000 00 00.000':
        return None
    
    mlat = re.match("(\d\d\d) (\d\d) (\d\d\.\d\d\d)N", hlat)
    mlng = re.match("(\d\d\d) (\d\d) (\d\d\.\d\d\d)([EW])", hlng)
    if not mlat or not mlng:
        return None
    
    # should convert the datum
    lat = int(mlat.group(1)) + int(mlat.group(2)) / 60.0 + float(mlat.group(3)) / 3600    
    lng = int(mlng.group(1)) + int(mlng.group(2)) / 60.0 + float(mlng.group(3)) / 3600
    if mlng.group(4) == "W":
        lng = -lng


    # should convert from ED50 here
    return [lat,lng]


def scrapewell(url):
    # extract the values and check complete
    html = urllib2.urlopen(url).read()
    data = dict(re.findall('<A HREF="/pls/wons/wdep0100.basicWellDataEpic.*">(.*?)</A>\s*=\s*(.*?)\s*<BR>', html))

    for fkey in ['Datum Elevation','Ground Elevation','Total MD Driller','Total MD Logger','Water Depth' ]:
        fkeyfeet = data.pop(fkey + ' (feet)', None)
        fkeymetres = data.pop(fkey + ' (metres)', None)
        if fkeyfeet == 'NULL Value' or fkeymetres == 'NULL Value':
            data[fkey] = 'NULL Value'
        elif fkeymetres:
            data[fkey] = float(fkeymetres)
        elif fkeyfeet:
            data[fkey] = float(fkeyfeet) * 0.3048
            
    skeys = sorted(data.keys())
    assert skeys == wellkeys, [url, skeys]

    # remove NULL Values and convert dates
    for key in data.keys():
        if data[key] == 'NULL Value' or data[key] == '':
            del data[key]
        elif key in datekeys:
            sdate = data[key]
            data[key] = datetime.date(int(sdate[7:]), monthnams.index(sdate[3:6])+1, int(sdate[:2]))  # 22-APR-1985

    # get coordinates
    coordsystem = data.pop('Coordinate System')
    assert coordsystem == data.pop('Geodetic Datum')
    assert coordsystem == 'ED50'

    latlngbottom = latlongconv('Bottom Hole Latitude', 'Bottom Hole Longtitude', data, coordsystem)
    latlngtop = latlongconv('Top hole Latitude', 'Top Hole Longtitude', data, coordsystem)
    if latlngtop:
        data['latlng'] = latlngtop

    assert data.get('Completion Status', None) in ['Completed', 'Suspended', 'Abandoned', None]

    if data.get("Datum Type") == "Kelly Bushing":
        data["Datum Type"] = "KB"

    data['url'] = url
    scraperwiki.datastore.save(unique_keys=["Well Registration No."], data=data, latlng=data.pop('latlng', None), silent=True)



#{u'date': u'None', u'date_scraped': u'2010-07-01 13:42:27', u'latlng': u'057.997105,-00.723548', u'data': {u'Spud_Date': u'2010-06-26', u'Drilling_Sequence_No.': u'10', u'Datum_Type': u'RT', u'Wellbore_Type': u'Initial', u'Block_Suffix': u'b', u'Primary_Target': u'G', u'Block_No.': u'2', u'Well_Registration_No.': u'20/02b- 10', u'Deviated_Well': u'Vertical', u'url': u'https://www.og.decc.gov.uk/pls/wons/wdep0100.wellHeaderData?p_quadNo=20&p_blockNo=2&p_block_suffix=b&p_platform=+&p_drilling_seq_no=10&p_well_suffix=+', u'Country_Code': u'United Kingdom', u'Onshore/Offshore': u'Offshore', u'Quadrant_No.': u'20', u'Water_Depth': u'107.2896', u'Original_Intent': u'Exploration', u'Datum_Elevation': u'24.9936'}}
import simplejson as json

def yearpoints(year):
    year = unicode(year)
    result = [ ]
    sd = "2010-06-26"
    sd = None # for all of them
    for fdata in scraperwiki.datastore.retrieve({"Spud_Date":sd}):
        data = fdata["data"]
        if data["Spud_Date"][:4] != year:
            continue
        latlng = fdata["latlng"].split(",")
        if len(latlng) != 2:
            continue
        lat, lng = map(float, latlng)
        rdata = { 'lat':lat, 'lng':lng }
        rdata['Water_Depth'] = float(data.get('Water_Depth', '0'))
        rdata['Spud_Date'] = data.get('Spud_Date')
        rdata['Original_Intent'] = data.get('Original_Intent')
        rdata['url'] = data.get('url')
        result.append(rdata)
    print "callback(%s)" % json.dumps(result)
    
#print yearpoints("2010")
main()
"""
Copied from http://scraperwiki.com/scrapers/show/oil-and-gas-wells-from-decc/
"""

import scraperwiki
import urllib2, urllib, urlparse
import re
import datetime
import httplib
import time
import mechanize


def main():
    # it only works with a new mechanize object per quadrant
    for i in range(70, 200):
        print "i=%d"%i, 
        quadranturl = getquadranturl(i)
        if not quadranturl:
            break
        welllinks = scrapequrl(quadranturl)
        print "Wells:", len(welllinks)
        for url in welllinks:
            scrapewell(url)


# scrapes the lookup data on a quadrant, which fails due to a bug in the https proxy
def scrapequrl(quadranturl):
    #qhtml = urllib2.urlopen("http://seagrass.goatchurch.org.uk/~julian/cgi-bin/aa.cgi", urllib.urlencode({'url':quadranturl})).read()
    qhtml = urllib2.urlopen(quadranturl).read()
    lurls = re.findall('<A HREF="(/pls/wons/wdep0100.wellHeaderData?.*?)">.*?</A>', qhtml)
    return [ urlparse.urljoin(quadranturl, lurl)  for lurl in lurls ]


# this would be a lot slicker without the bug that makes opening the wellhead data impossible

def getquadranturl(i):
    # set up the mechanize object
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open("https://www.og.decc.gov.uk/pls/wons/wdep0100.qryWell")

    # select the one form on the page
    br.form = list(br.forms())[0]

    # get the select list
    selectcontrol = br.form.find_control(name='f_quadNoList', type='select')

    # exceeded list of quadrants
    if i > len(selectcontrol.items):
        return None
    item = selectcontrol.items[i]
    itemlabel = item.get_labels()[0].text
    print "Selecting quadrant:", itemlabel
    selectcontrol.value = [itemlabel]
    response = br.submit()
    return br.geturl()



feetkeys = [ 'Datum Elevation', 'Ground Elevation', 'Total MD Driller', 'Total MD Logger', 'Water Depth' ]

wellkeys = ['Block No.', 'Block Suffix', 'Bottom Hole Latitude', 'Bottom Hole Longtitude', 'Completion Date', 'Completion Status', 
            'Coordinate System', 'Country Code', 'Date TD Reached', 'Datum Elevation', 'Datum Type', 'Deviated Well', 
            'Drilling Sequence No.', 'Geodetic Datum', 'Ground Elevation', 'Onshore/Offshore', 'Original Intent', 
            'Platform', 'Primary Target', 'Quadrant No.', 'Slot No.', 'Spud Date', 'TVDSS Driller', 
            'Top Hole Longtitude', 'Top hole Latitude', 'Total MD Driller', 'Total MD Logger', 'Water Depth', 
            'Well Registration No.', 'Wellbore Type']

datekeys = ['Completion Date', 'Date TD Reached', 'Spud Date' ]
monthnams = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]


def latlongconv(hnamelat, hnamelong, data, coordsystem):
    hlat = data.pop(hnamelat, "")
    hlng = data.pop(hnamelong, "")
    if not hlat or not hlng:
        return None
    if hlat == '000 00 00.000' and hlng == '000 00 00.000':
        return None
    
    mlat = re.match("(\d\d\d) (\d\d) (\d\d\.\d\d\d)N", hlat)
    mlng = re.match("(\d\d\d) (\d\d) (\d\d\.\d\d\d)([EW])", hlng)
    if not mlat or not mlng:
        return None
    
    # should convert the datum
    lat = int(mlat.group(1)) + int(mlat.group(2)) / 60.0 + float(mlat.group(3)) / 3600    
    lng = int(mlng.group(1)) + int(mlng.group(2)) / 60.0 + float(mlng.group(3)) / 3600
    if mlng.group(4) == "W":
        lng = -lng


    # should convert from ED50 here
    return [lat,lng]


def scrapewell(url):
    # extract the values and check complete
    html = urllib2.urlopen(url).read()
    data = dict(re.findall('<A HREF="/pls/wons/wdep0100.basicWellDataEpic.*">(.*?)</A>\s*=\s*(.*?)\s*<BR>', html))

    for fkey in ['Datum Elevation','Ground Elevation','Total MD Driller','Total MD Logger','Water Depth' ]:
        fkeyfeet = data.pop(fkey + ' (feet)', None)
        fkeymetres = data.pop(fkey + ' (metres)', None)
        if fkeyfeet == 'NULL Value' or fkeymetres == 'NULL Value':
            data[fkey] = 'NULL Value'
        elif fkeymetres:
            data[fkey] = float(fkeymetres)
        elif fkeyfeet:
            data[fkey] = float(fkeyfeet) * 0.3048
            
    skeys = sorted(data.keys())
    assert skeys == wellkeys, [url, skeys]

    # remove NULL Values and convert dates
    for key in data.keys():
        if data[key] == 'NULL Value' or data[key] == '':
            del data[key]
        elif key in datekeys:
            sdate = data[key]
            data[key] = datetime.date(int(sdate[7:]), monthnams.index(sdate[3:6])+1, int(sdate[:2]))  # 22-APR-1985

    # get coordinates
    coordsystem = data.pop('Coordinate System')
    assert coordsystem == data.pop('Geodetic Datum')
    assert coordsystem == 'ED50'

    latlngbottom = latlongconv('Bottom Hole Latitude', 'Bottom Hole Longtitude', data, coordsystem)
    latlngtop = latlongconv('Top hole Latitude', 'Top Hole Longtitude', data, coordsystem)
    if latlngtop:
        data['latlng'] = latlngtop

    assert data.get('Completion Status', None) in ['Completed', 'Suspended', 'Abandoned', None]

    if data.get("Datum Type") == "Kelly Bushing":
        data["Datum Type"] = "KB"

    data['url'] = url
    scraperwiki.datastore.save(unique_keys=["Well Registration No."], data=data, latlng=data.pop('latlng', None), silent=True)



#{u'date': u'None', u'date_scraped': u'2010-07-01 13:42:27', u'latlng': u'057.997105,-00.723548', u'data': {u'Spud_Date': u'2010-06-26', u'Drilling_Sequence_No.': u'10', u'Datum_Type': u'RT', u'Wellbore_Type': u'Initial', u'Block_Suffix': u'b', u'Primary_Target': u'G', u'Block_No.': u'2', u'Well_Registration_No.': u'20/02b- 10', u'Deviated_Well': u'Vertical', u'url': u'https://www.og.decc.gov.uk/pls/wons/wdep0100.wellHeaderData?p_quadNo=20&p_blockNo=2&p_block_suffix=b&p_platform=+&p_drilling_seq_no=10&p_well_suffix=+', u'Country_Code': u'United Kingdom', u'Onshore/Offshore': u'Offshore', u'Quadrant_No.': u'20', u'Water_Depth': u'107.2896', u'Original_Intent': u'Exploration', u'Datum_Elevation': u'24.9936'}}
import simplejson as json

def yearpoints(year):
    year = unicode(year)
    result = [ ]
    sd = "2010-06-26"
    sd = None # for all of them
    for fdata in scraperwiki.datastore.retrieve({"Spud_Date":sd}):
        data = fdata["data"]
        if data["Spud_Date"][:4] != year:
            continue
        latlng = fdata["latlng"].split(",")
        if len(latlng) != 2:
            continue
        lat, lng = map(float, latlng)
        rdata = { 'lat':lat, 'lng':lng }
        rdata['Water_Depth'] = float(data.get('Water_Depth', '0'))
        rdata['Spud_Date'] = data.get('Spud_Date')
        rdata['Original_Intent'] = data.get('Original_Intent')
        rdata['url'] = data.get('url')
        result.append(rdata)
    print "callback(%s)" % json.dumps(result)
    
#print yearpoints("2010")
main()
"""
Copied from http://scraperwiki.com/scrapers/show/oil-and-gas-wells-from-decc/
"""

import scraperwiki
import urllib2, urllib, urlparse
import re
import datetime
import httplib
import time
import mechanize


def main():
    # it only works with a new mechanize object per quadrant
    for i in range(70, 200):
        print "i=%d"%i, 
        quadranturl = getquadranturl(i)
        if not quadranturl:
            break
        welllinks = scrapequrl(quadranturl)
        print "Wells:", len(welllinks)
        for url in welllinks:
            scrapewell(url)


# scrapes the lookup data on a quadrant, which fails due to a bug in the https proxy
def scrapequrl(quadranturl):
    #qhtml = urllib2.urlopen("http://seagrass.goatchurch.org.uk/~julian/cgi-bin/aa.cgi", urllib.urlencode({'url':quadranturl})).read()
    qhtml = urllib2.urlopen(quadranturl).read()
    lurls = re.findall('<A HREF="(/pls/wons/wdep0100.wellHeaderData?.*?)">.*?</A>', qhtml)
    return [ urlparse.urljoin(quadranturl, lurl)  for lurl in lurls ]


# this would be a lot slicker without the bug that makes opening the wellhead data impossible

def getquadranturl(i):
    # set up the mechanize object
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open("https://www.og.decc.gov.uk/pls/wons/wdep0100.qryWell")

    # select the one form on the page
    br.form = list(br.forms())[0]

    # get the select list
    selectcontrol = br.form.find_control(name='f_quadNoList', type='select')

    # exceeded list of quadrants
    if i > len(selectcontrol.items):
        return None
    item = selectcontrol.items[i]
    itemlabel = item.get_labels()[0].text
    print "Selecting quadrant:", itemlabel
    selectcontrol.value = [itemlabel]
    response = br.submit()
    return br.geturl()



feetkeys = [ 'Datum Elevation', 'Ground Elevation', 'Total MD Driller', 'Total MD Logger', 'Water Depth' ]

wellkeys = ['Block No.', 'Block Suffix', 'Bottom Hole Latitude', 'Bottom Hole Longtitude', 'Completion Date', 'Completion Status', 
            'Coordinate System', 'Country Code', 'Date TD Reached', 'Datum Elevation', 'Datum Type', 'Deviated Well', 
            'Drilling Sequence No.', 'Geodetic Datum', 'Ground Elevation', 'Onshore/Offshore', 'Original Intent', 
            'Platform', 'Primary Target', 'Quadrant No.', 'Slot No.', 'Spud Date', 'TVDSS Driller', 
            'Top Hole Longtitude', 'Top hole Latitude', 'Total MD Driller', 'Total MD Logger', 'Water Depth', 
            'Well Registration No.', 'Wellbore Type']

datekeys = ['Completion Date', 'Date TD Reached', 'Spud Date' ]
monthnams = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]


def latlongconv(hnamelat, hnamelong, data, coordsystem):
    hlat = data.pop(hnamelat, "")
    hlng = data.pop(hnamelong, "")
    if not hlat or not hlng:
        return None
    if hlat == '000 00 00.000' and hlng == '000 00 00.000':
        return None
    
    mlat = re.match("(\d\d\d) (\d\d) (\d\d\.\d\d\d)N", hlat)
    mlng = re.match("(\d\d\d) (\d\d) (\d\d\.\d\d\d)([EW])", hlng)
    if not mlat or not mlng:
        return None
    
    # should convert the datum
    lat = int(mlat.group(1)) + int(mlat.group(2)) / 60.0 + float(mlat.group(3)) / 3600    
    lng = int(mlng.group(1)) + int(mlng.group(2)) / 60.0 + float(mlng.group(3)) / 3600
    if mlng.group(4) == "W":
        lng = -lng


    # should convert from ED50 here
    return [lat,lng]


def scrapewell(url):
    # extract the values and check complete
    html = urllib2.urlopen(url).read()
    data = dict(re.findall('<A HREF="/pls/wons/wdep0100.basicWellDataEpic.*">(.*?)</A>\s*=\s*(.*?)\s*<BR>', html))

    for fkey in ['Datum Elevation','Ground Elevation','Total MD Driller','Total MD Logger','Water Depth' ]:
        fkeyfeet = data.pop(fkey + ' (feet)', None)
        fkeymetres = data.pop(fkey + ' (metres)', None)
        if fkeyfeet == 'NULL Value' or fkeymetres == 'NULL Value':
            data[fkey] = 'NULL Value'
        elif fkeymetres:
            data[fkey] = float(fkeymetres)
        elif fkeyfeet:
            data[fkey] = float(fkeyfeet) * 0.3048
            
    skeys = sorted(data.keys())
    assert skeys == wellkeys, [url, skeys]

    # remove NULL Values and convert dates
    for key in data.keys():
        if data[key] == 'NULL Value' or data[key] == '':
            del data[key]
        elif key in datekeys:
            sdate = data[key]
            data[key] = datetime.date(int(sdate[7:]), monthnams.index(sdate[3:6])+1, int(sdate[:2]))  # 22-APR-1985

    # get coordinates
    coordsystem = data.pop('Coordinate System')
    assert coordsystem == data.pop('Geodetic Datum')
    assert coordsystem == 'ED50'

    latlngbottom = latlongconv('Bottom Hole Latitude', 'Bottom Hole Longtitude', data, coordsystem)
    latlngtop = latlongconv('Top hole Latitude', 'Top Hole Longtitude', data, coordsystem)
    if latlngtop:
        data['latlng'] = latlngtop

    assert data.get('Completion Status', None) in ['Completed', 'Suspended', 'Abandoned', None]

    if data.get("Datum Type") == "Kelly Bushing":
        data["Datum Type"] = "KB"

    data['url'] = url
    scraperwiki.datastore.save(unique_keys=["Well Registration No."], data=data, latlng=data.pop('latlng', None), silent=True)



#{u'date': u'None', u'date_scraped': u'2010-07-01 13:42:27', u'latlng': u'057.997105,-00.723548', u'data': {u'Spud_Date': u'2010-06-26', u'Drilling_Sequence_No.': u'10', u'Datum_Type': u'RT', u'Wellbore_Type': u'Initial', u'Block_Suffix': u'b', u'Primary_Target': u'G', u'Block_No.': u'2', u'Well_Registration_No.': u'20/02b- 10', u'Deviated_Well': u'Vertical', u'url': u'https://www.og.decc.gov.uk/pls/wons/wdep0100.wellHeaderData?p_quadNo=20&p_blockNo=2&p_block_suffix=b&p_platform=+&p_drilling_seq_no=10&p_well_suffix=+', u'Country_Code': u'United Kingdom', u'Onshore/Offshore': u'Offshore', u'Quadrant_No.': u'20', u'Water_Depth': u'107.2896', u'Original_Intent': u'Exploration', u'Datum_Elevation': u'24.9936'}}
import simplejson as json

def yearpoints(year):
    year = unicode(year)
    result = [ ]
    sd = "2010-06-26"
    sd = None # for all of them
    for fdata in scraperwiki.datastore.retrieve({"Spud_Date":sd}):
        data = fdata["data"]
        if data["Spud_Date"][:4] != year:
            continue
        latlng = fdata["latlng"].split(",")
        if len(latlng) != 2:
            continue
        lat, lng = map(float, latlng)
        rdata = { 'lat':lat, 'lng':lng }
        rdata['Water_Depth'] = float(data.get('Water_Depth', '0'))
        rdata['Spud_Date'] = data.get('Spud_Date')
        rdata['Original_Intent'] = data.get('Original_Intent')
        rdata['url'] = data.get('url')
        result.append(rdata)
    print "callback(%s)" % json.dumps(result)
    
#print yearpoints("2010")
main()
"""
Copied from http://scraperwiki.com/scrapers/show/oil-and-gas-wells-from-decc/
"""

import scraperwiki
import urllib2, urllib, urlparse
import re
import datetime
import httplib
import time
import mechanize


def main():
    # it only works with a new mechanize object per quadrant
    for i in range(70, 200):
        print "i=%d"%i, 
        quadranturl = getquadranturl(i)
        if not quadranturl:
            break
        welllinks = scrapequrl(quadranturl)
        print "Wells:", len(welllinks)
        for url in welllinks:
            scrapewell(url)


# scrapes the lookup data on a quadrant, which fails due to a bug in the https proxy
def scrapequrl(quadranturl):
    #qhtml = urllib2.urlopen("http://seagrass.goatchurch.org.uk/~julian/cgi-bin/aa.cgi", urllib.urlencode({'url':quadranturl})).read()
    qhtml = urllib2.urlopen(quadranturl).read()
    lurls = re.findall('<A HREF="(/pls/wons/wdep0100.wellHeaderData?.*?)">.*?</A>', qhtml)
    return [ urlparse.urljoin(quadranturl, lurl)  for lurl in lurls ]


# this would be a lot slicker without the bug that makes opening the wellhead data impossible

def getquadranturl(i):
    # set up the mechanize object
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open("https://www.og.decc.gov.uk/pls/wons/wdep0100.qryWell")

    # select the one form on the page
    br.form = list(br.forms())[0]

    # get the select list
    selectcontrol = br.form.find_control(name='f_quadNoList', type='select')

    # exceeded list of quadrants
    if i > len(selectcontrol.items):
        return None
    item = selectcontrol.items[i]
    itemlabel = item.get_labels()[0].text
    print "Selecting quadrant:", itemlabel
    selectcontrol.value = [itemlabel]
    response = br.submit()
    return br.geturl()



feetkeys = [ 'Datum Elevation', 'Ground Elevation', 'Total MD Driller', 'Total MD Logger', 'Water Depth' ]

wellkeys = ['Block No.', 'Block Suffix', 'Bottom Hole Latitude', 'Bottom Hole Longtitude', 'Completion Date', 'Completion Status', 
            'Coordinate System', 'Country Code', 'Date TD Reached', 'Datum Elevation', 'Datum Type', 'Deviated Well', 
            'Drilling Sequence No.', 'Geodetic Datum', 'Ground Elevation', 'Onshore/Offshore', 'Original Intent', 
            'Platform', 'Primary Target', 'Quadrant No.', 'Slot No.', 'Spud Date', 'TVDSS Driller', 
            'Top Hole Longtitude', 'Top hole Latitude', 'Total MD Driller', 'Total MD Logger', 'Water Depth', 
            'Well Registration No.', 'Wellbore Type']

datekeys = ['Completion Date', 'Date TD Reached', 'Spud Date' ]
monthnams = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]


def latlongconv(hnamelat, hnamelong, data, coordsystem):
    hlat = data.pop(hnamelat, "")
    hlng = data.pop(hnamelong, "")
    if not hlat or not hlng:
        return None
    if hlat == '000 00 00.000' and hlng == '000 00 00.000':
        return None
    
    mlat = re.match("(\d\d\d) (\d\d) (\d\d\.\d\d\d)N", hlat)
    mlng = re.match("(\d\d\d) (\d\d) (\d\d\.\d\d\d)([EW])", hlng)
    if not mlat or not mlng:
        return None
    
    # should convert the datum
    lat = int(mlat.group(1)) + int(mlat.group(2)) / 60.0 + float(mlat.group(3)) / 3600    
    lng = int(mlng.group(1)) + int(mlng.group(2)) / 60.0 + float(mlng.group(3)) / 3600
    if mlng.group(4) == "W":
        lng = -lng


    # should convert from ED50 here
    return [lat,lng]


def scrapewell(url):
    # extract the values and check complete
    html = urllib2.urlopen(url).read()
    data = dict(re.findall('<A HREF="/pls/wons/wdep0100.basicWellDataEpic.*">(.*?)</A>\s*=\s*(.*?)\s*<BR>', html))

    for fkey in ['Datum Elevation','Ground Elevation','Total MD Driller','Total MD Logger','Water Depth' ]:
        fkeyfeet = data.pop(fkey + ' (feet)', None)
        fkeymetres = data.pop(fkey + ' (metres)', None)
        if fkeyfeet == 'NULL Value' or fkeymetres == 'NULL Value':
            data[fkey] = 'NULL Value'
        elif fkeymetres:
            data[fkey] = float(fkeymetres)
        elif fkeyfeet:
            data[fkey] = float(fkeyfeet) * 0.3048
            
    skeys = sorted(data.keys())
    assert skeys == wellkeys, [url, skeys]

    # remove NULL Values and convert dates
    for key in data.keys():
        if data[key] == 'NULL Value' or data[key] == '':
            del data[key]
        elif key in datekeys:
            sdate = data[key]
            data[key] = datetime.date(int(sdate[7:]), monthnams.index(sdate[3:6])+1, int(sdate[:2]))  # 22-APR-1985

    # get coordinates
    coordsystem = data.pop('Coordinate System')
    assert coordsystem == data.pop('Geodetic Datum')
    assert coordsystem == 'ED50'

    latlngbottom = latlongconv('Bottom Hole Latitude', 'Bottom Hole Longtitude', data, coordsystem)
    latlngtop = latlongconv('Top hole Latitude', 'Top Hole Longtitude', data, coordsystem)
    if latlngtop:
        data['latlng'] = latlngtop

    assert data.get('Completion Status', None) in ['Completed', 'Suspended', 'Abandoned', None]

    if data.get("Datum Type") == "Kelly Bushing":
        data["Datum Type"] = "KB"

    data['url'] = url
    scraperwiki.datastore.save(unique_keys=["Well Registration No."], data=data, latlng=data.pop('latlng', None), silent=True)



#{u'date': u'None', u'date_scraped': u'2010-07-01 13:42:27', u'latlng': u'057.997105,-00.723548', u'data': {u'Spud_Date': u'2010-06-26', u'Drilling_Sequence_No.': u'10', u'Datum_Type': u'RT', u'Wellbore_Type': u'Initial', u'Block_Suffix': u'b', u'Primary_Target': u'G', u'Block_No.': u'2', u'Well_Registration_No.': u'20/02b- 10', u'Deviated_Well': u'Vertical', u'url': u'https://www.og.decc.gov.uk/pls/wons/wdep0100.wellHeaderData?p_quadNo=20&p_blockNo=2&p_block_suffix=b&p_platform=+&p_drilling_seq_no=10&p_well_suffix=+', u'Country_Code': u'United Kingdom', u'Onshore/Offshore': u'Offshore', u'Quadrant_No.': u'20', u'Water_Depth': u'107.2896', u'Original_Intent': u'Exploration', u'Datum_Elevation': u'24.9936'}}
import simplejson as json

def yearpoints(year):
    year = unicode(year)
    result = [ ]
    sd = "2010-06-26"
    sd = None # for all of them
    for fdata in scraperwiki.datastore.retrieve({"Spud_Date":sd}):
        data = fdata["data"]
        if data["Spud_Date"][:4] != year:
            continue
        latlng = fdata["latlng"].split(",")
        if len(latlng) != 2:
            continue
        lat, lng = map(float, latlng)
        rdata = { 'lat':lat, 'lng':lng }
        rdata['Water_Depth'] = float(data.get('Water_Depth', '0'))
        rdata['Spud_Date'] = data.get('Spud_Date')
        rdata['Original_Intent'] = data.get('Original_Intent')
        rdata['url'] = data.get('url')
        result.append(rdata)
    print "callback(%s)" % json.dumps(result)
    
#print yearpoints("2010")
main()
