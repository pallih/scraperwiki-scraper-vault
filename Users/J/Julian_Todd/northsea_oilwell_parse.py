import scraperwiki
import urllib2, urllib, urlparse
import re
import datetime
import httplib
import time
import mechanize
import lxml.html

updatetime = datetime.datetime.now()

# this gets selected all in one lump.  better performance with generators and limit passed in as part of select statement
scraperwiki.sqlite.attach("northsea_oilwell_scrapedownload", "src")


wellkeys = ['Block No', 'Block Suffix', 'Bottom Hole Latitude', 'Bottom Hole Longtitude', 'Completion Date',
            'Completion Status', 
            'Coordinate System', 'Country Code', 'Date TD Reached', 'Datum Elevation', 'Datum Type', 'Deviated Well', 
            'Drilling Sequence No', 'Geodetic Datum', 'Ground Elevation', 'Onshore Offshore', 'Original Intent', 
            'Platform', 'Primary Target', 'Quadrant No', 'Slot No', 'Spud Date', 'TVDSS Driller', 
            'Top Hole Longtitude', 'Top hole Latitude', 'Total MD Driller', 'Total MD Logger', 'Water Depth', 
            'Well Registration No', 'Wellbore Type']


feetkeys = ['Datum Elevation', 'Ground Elevation', 'Total MD Driller', 'Total MD Logger', 'Water Depth' ]
datekeys = ['Completion Date', 'Date TD Reached', 'Spud Date' ]

monthnams = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]


def Main():
    #scraperwiki.sqlite.execute("drop table if exists swdata")
    offset, limit = 0, 300
    while True:
        qsel = "oilwellfields.quadrant as quadrant, oilwellfields.block as block, oilwellfields.wellno as wellno, contents, url, swdata.*"
        qsel = "*"
        qfrom = " from src.oilwellfields"
        qjoin = " left join swdata on oilwellfields.quadrant=swdata.quadrant and oilwellfields.block=swdata.block and oilwellfields.wellno=swdata.wellno"
        result = scraperwiki.sqlite.select("%s%s%s limit %d offset %d" % (qsel, qfrom, qjoin, limit, offset))
        ldata = [ ]
        for rdata in result:
            if re.search("403 = Request forbidden", rdata["contents"]):
                print rdata
                continue

            data = parsewell(rdata["contents"], rdata["url"])
            if not data:
                continue
            data['quadrant'], data['block'], data["wellno"] = rdata['quadrant'], rdata['block'], rdata["wellno"]

            data["lastupdatedate"] = rdata.get("lastupdatedate", "")
            data["lastupdatekey"] = rdata.get("lastupdatekey", "")
            for key in ['Datum Elevation','Total MD Driller','Total MD Logger','Water Depth','Completion Status']:
                if rdata.get(key) != data.get(key):
                    data["lastupdatedate"], data["lastupdatekey"] = updatetime, key
            ldata.append(data)

        # check if data has changed for the field and more 'Datum Elevation','Ground Elevation','Total MD Driller','Total MD Logger','Water Depth'
        # and save an update date, also check for 
        scraperwiki.sqlite.save(unique_keys=["quadrant", "block", "wellno"], data=ldata)
        if len(result) == limit:
            offset += limit
        else:
            break

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
    return lat, lng

def parsewell(html, url):
    # extract the values and check complete
    data = dict(re.findall('<A HREF="/pls/wons/wdep0100.basicWellDataEpic.*">(.*?)\.?</A>\s*=\s*(.*?)\s*<BR>', html))

    for fkey in ['Datum Elevation','Ground Elevation','Total MD Driller','Total MD Logger','Water Depth' ]:
        fkeyfeet = data.pop(fkey + ' (feet)', None)
        fkeymetres = data.pop(fkey + ' (metres)', None)
        if fkeyfeet == 'NULL Value' or fkeymetres == 'NULL Value':
            data[fkey] = 'NULL Value'
        elif fkeymetres:
            data[fkey] = float(fkeymetres)
        elif fkeyfeet:
            data[fkey] = float(fkeyfeet) * 0.3048

    data['Onshore Offshore'] = data.pop('Onshore/Offshore')

    skeys = sorted(data.keys())
    if skeys != wellkeys:
        print (skeys, wellkeys, url, html), "\n\ntruncated?"
        return None

    # remove NULL Values and convert dates
    for key in data.keys():
        if data[key] == 'NULL Value' or data[key] == '':
            del data[key]
        elif key in datekeys:
            sdate = data[key]
            data[key] = datetime.date(int(sdate[7:]), monthnams.index(sdate[3:6])+1, int(sdate[:2])).isoformat()  
                    # 22-APR-1985

    # get coordinates
    coordsystem = data.pop('Coordinate System')
    assert coordsystem == data.pop('Geodetic Datum')
    assert coordsystem == 'ED50'

    latlngbottom = latlongconv('Bottom Hole Latitude', 'Bottom Hole Longtitude', data, coordsystem)
    if latlngbottom:
        data['bottomhole_lat'], data['bottomhole_lng'] = latlngbottom
    latlngtop = latlongconv('Top hole Latitude', 'Top Hole Longtitude', data, coordsystem)
    if latlngtop:
        data['tophole_lat'], data['tophole_lng'] = latlngtop

    assert data.get('Completion Status', None) in ['Completed', 'Suspended', 'Abandoned', None]

    if data.get("Datum Type") == "Kelly Bushing":
        data["Datum Type"] = "KB"

    return data


Main()

import scraperwiki
import urllib2, urllib, urlparse
import re
import datetime
import httplib
import time
import mechanize
import lxml.html

updatetime = datetime.datetime.now()

# this gets selected all in one lump.  better performance with generators and limit passed in as part of select statement
scraperwiki.sqlite.attach("northsea_oilwell_scrapedownload", "src")


wellkeys = ['Block No', 'Block Suffix', 'Bottom Hole Latitude', 'Bottom Hole Longtitude', 'Completion Date',
            'Completion Status', 
            'Coordinate System', 'Country Code', 'Date TD Reached', 'Datum Elevation', 'Datum Type', 'Deviated Well', 
            'Drilling Sequence No', 'Geodetic Datum', 'Ground Elevation', 'Onshore Offshore', 'Original Intent', 
            'Platform', 'Primary Target', 'Quadrant No', 'Slot No', 'Spud Date', 'TVDSS Driller', 
            'Top Hole Longtitude', 'Top hole Latitude', 'Total MD Driller', 'Total MD Logger', 'Water Depth', 
            'Well Registration No', 'Wellbore Type']


feetkeys = ['Datum Elevation', 'Ground Elevation', 'Total MD Driller', 'Total MD Logger', 'Water Depth' ]
datekeys = ['Completion Date', 'Date TD Reached', 'Spud Date' ]

monthnams = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]


def Main():
    #scraperwiki.sqlite.execute("drop table if exists swdata")
    offset, limit = 0, 300
    while True:
        qsel = "oilwellfields.quadrant as quadrant, oilwellfields.block as block, oilwellfields.wellno as wellno, contents, url, swdata.*"
        qsel = "*"
        qfrom = " from src.oilwellfields"
        qjoin = " left join swdata on oilwellfields.quadrant=swdata.quadrant and oilwellfields.block=swdata.block and oilwellfields.wellno=swdata.wellno"
        result = scraperwiki.sqlite.select("%s%s%s limit %d offset %d" % (qsel, qfrom, qjoin, limit, offset))
        ldata = [ ]
        for rdata in result:
            if re.search("403 = Request forbidden", rdata["contents"]):
                print rdata
                continue

            data = parsewell(rdata["contents"], rdata["url"])
            if not data:
                continue
            data['quadrant'], data['block'], data["wellno"] = rdata['quadrant'], rdata['block'], rdata["wellno"]

            data["lastupdatedate"] = rdata.get("lastupdatedate", "")
            data["lastupdatekey"] = rdata.get("lastupdatekey", "")
            for key in ['Datum Elevation','Total MD Driller','Total MD Logger','Water Depth','Completion Status']:
                if rdata.get(key) != data.get(key):
                    data["lastupdatedate"], data["lastupdatekey"] = updatetime, key
            ldata.append(data)

        # check if data has changed for the field and more 'Datum Elevation','Ground Elevation','Total MD Driller','Total MD Logger','Water Depth'
        # and save an update date, also check for 
        scraperwiki.sqlite.save(unique_keys=["quadrant", "block", "wellno"], data=ldata)
        if len(result) == limit:
            offset += limit
        else:
            break

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
    return lat, lng

def parsewell(html, url):
    # extract the values and check complete
    data = dict(re.findall('<A HREF="/pls/wons/wdep0100.basicWellDataEpic.*">(.*?)\.?</A>\s*=\s*(.*?)\s*<BR>', html))

    for fkey in ['Datum Elevation','Ground Elevation','Total MD Driller','Total MD Logger','Water Depth' ]:
        fkeyfeet = data.pop(fkey + ' (feet)', None)
        fkeymetres = data.pop(fkey + ' (metres)', None)
        if fkeyfeet == 'NULL Value' or fkeymetres == 'NULL Value':
            data[fkey] = 'NULL Value'
        elif fkeymetres:
            data[fkey] = float(fkeymetres)
        elif fkeyfeet:
            data[fkey] = float(fkeyfeet) * 0.3048

    data['Onshore Offshore'] = data.pop('Onshore/Offshore')

    skeys = sorted(data.keys())
    if skeys != wellkeys:
        print (skeys, wellkeys, url, html), "\n\ntruncated?"
        return None

    # remove NULL Values and convert dates
    for key in data.keys():
        if data[key] == 'NULL Value' or data[key] == '':
            del data[key]
        elif key in datekeys:
            sdate = data[key]
            data[key] = datetime.date(int(sdate[7:]), monthnams.index(sdate[3:6])+1, int(sdate[:2])).isoformat()  
                    # 22-APR-1985

    # get coordinates
    coordsystem = data.pop('Coordinate System')
    assert coordsystem == data.pop('Geodetic Datum')
    assert coordsystem == 'ED50'

    latlngbottom = latlongconv('Bottom Hole Latitude', 'Bottom Hole Longtitude', data, coordsystem)
    if latlngbottom:
        data['bottomhole_lat'], data['bottomhole_lng'] = latlngbottom
    latlngtop = latlongconv('Top hole Latitude', 'Top Hole Longtitude', data, coordsystem)
    if latlngtop:
        data['tophole_lat'], data['tophole_lng'] = latlngtop

    assert data.get('Completion Status', None) in ['Completed', 'Suspended', 'Abandoned', None]

    if data.get("Datum Type") == "Kelly Bushing":
        data["Datum Type"] = "KB"

    return data


Main()

import scraperwiki
import urllib2, urllib, urlparse
import re
import datetime
import httplib
import time
import mechanize
import lxml.html

updatetime = datetime.datetime.now()

# this gets selected all in one lump.  better performance with generators and limit passed in as part of select statement
scraperwiki.sqlite.attach("northsea_oilwell_scrapedownload", "src")


wellkeys = ['Block No', 'Block Suffix', 'Bottom Hole Latitude', 'Bottom Hole Longtitude', 'Completion Date',
            'Completion Status', 
            'Coordinate System', 'Country Code', 'Date TD Reached', 'Datum Elevation', 'Datum Type', 'Deviated Well', 
            'Drilling Sequence No', 'Geodetic Datum', 'Ground Elevation', 'Onshore Offshore', 'Original Intent', 
            'Platform', 'Primary Target', 'Quadrant No', 'Slot No', 'Spud Date', 'TVDSS Driller', 
            'Top Hole Longtitude', 'Top hole Latitude', 'Total MD Driller', 'Total MD Logger', 'Water Depth', 
            'Well Registration No', 'Wellbore Type']


feetkeys = ['Datum Elevation', 'Ground Elevation', 'Total MD Driller', 'Total MD Logger', 'Water Depth' ]
datekeys = ['Completion Date', 'Date TD Reached', 'Spud Date' ]

monthnams = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]


def Main():
    #scraperwiki.sqlite.execute("drop table if exists swdata")
    offset, limit = 0, 300
    while True:
        qsel = "oilwellfields.quadrant as quadrant, oilwellfields.block as block, oilwellfields.wellno as wellno, contents, url, swdata.*"
        qsel = "*"
        qfrom = " from src.oilwellfields"
        qjoin = " left join swdata on oilwellfields.quadrant=swdata.quadrant and oilwellfields.block=swdata.block and oilwellfields.wellno=swdata.wellno"
        result = scraperwiki.sqlite.select("%s%s%s limit %d offset %d" % (qsel, qfrom, qjoin, limit, offset))
        ldata = [ ]
        for rdata in result:
            if re.search("403 = Request forbidden", rdata["contents"]):
                print rdata
                continue

            data = parsewell(rdata["contents"], rdata["url"])
            if not data:
                continue
            data['quadrant'], data['block'], data["wellno"] = rdata['quadrant'], rdata['block'], rdata["wellno"]

            data["lastupdatedate"] = rdata.get("lastupdatedate", "")
            data["lastupdatekey"] = rdata.get("lastupdatekey", "")
            for key in ['Datum Elevation','Total MD Driller','Total MD Logger','Water Depth','Completion Status']:
                if rdata.get(key) != data.get(key):
                    data["lastupdatedate"], data["lastupdatekey"] = updatetime, key
            ldata.append(data)

        # check if data has changed for the field and more 'Datum Elevation','Ground Elevation','Total MD Driller','Total MD Logger','Water Depth'
        # and save an update date, also check for 
        scraperwiki.sqlite.save(unique_keys=["quadrant", "block", "wellno"], data=ldata)
        if len(result) == limit:
            offset += limit
        else:
            break

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
    return lat, lng

def parsewell(html, url):
    # extract the values and check complete
    data = dict(re.findall('<A HREF="/pls/wons/wdep0100.basicWellDataEpic.*">(.*?)\.?</A>\s*=\s*(.*?)\s*<BR>', html))

    for fkey in ['Datum Elevation','Ground Elevation','Total MD Driller','Total MD Logger','Water Depth' ]:
        fkeyfeet = data.pop(fkey + ' (feet)', None)
        fkeymetres = data.pop(fkey + ' (metres)', None)
        if fkeyfeet == 'NULL Value' or fkeymetres == 'NULL Value':
            data[fkey] = 'NULL Value'
        elif fkeymetres:
            data[fkey] = float(fkeymetres)
        elif fkeyfeet:
            data[fkey] = float(fkeyfeet) * 0.3048

    data['Onshore Offshore'] = data.pop('Onshore/Offshore')

    skeys = sorted(data.keys())
    if skeys != wellkeys:
        print (skeys, wellkeys, url, html), "\n\ntruncated?"
        return None

    # remove NULL Values and convert dates
    for key in data.keys():
        if data[key] == 'NULL Value' or data[key] == '':
            del data[key]
        elif key in datekeys:
            sdate = data[key]
            data[key] = datetime.date(int(sdate[7:]), monthnams.index(sdate[3:6])+1, int(sdate[:2])).isoformat()  
                    # 22-APR-1985

    # get coordinates
    coordsystem = data.pop('Coordinate System')
    assert coordsystem == data.pop('Geodetic Datum')
    assert coordsystem == 'ED50'

    latlngbottom = latlongconv('Bottom Hole Latitude', 'Bottom Hole Longtitude', data, coordsystem)
    if latlngbottom:
        data['bottomhole_lat'], data['bottomhole_lng'] = latlngbottom
    latlngtop = latlongconv('Top hole Latitude', 'Top Hole Longtitude', data, coordsystem)
    if latlngtop:
        data['tophole_lat'], data['tophole_lng'] = latlngtop

    assert data.get('Completion Status', None) in ['Completed', 'Suspended', 'Abandoned', None]

    if data.get("Datum Type") == "Kelly Bushing":
        data["Datum Type"] = "KB"

    return data


Main()

import scraperwiki
import urllib2, urllib, urlparse
import re
import datetime
import httplib
import time
import mechanize
import lxml.html

updatetime = datetime.datetime.now()

# this gets selected all in one lump.  better performance with generators and limit passed in as part of select statement
scraperwiki.sqlite.attach("northsea_oilwell_scrapedownload", "src")


wellkeys = ['Block No', 'Block Suffix', 'Bottom Hole Latitude', 'Bottom Hole Longtitude', 'Completion Date',
            'Completion Status', 
            'Coordinate System', 'Country Code', 'Date TD Reached', 'Datum Elevation', 'Datum Type', 'Deviated Well', 
            'Drilling Sequence No', 'Geodetic Datum', 'Ground Elevation', 'Onshore Offshore', 'Original Intent', 
            'Platform', 'Primary Target', 'Quadrant No', 'Slot No', 'Spud Date', 'TVDSS Driller', 
            'Top Hole Longtitude', 'Top hole Latitude', 'Total MD Driller', 'Total MD Logger', 'Water Depth', 
            'Well Registration No', 'Wellbore Type']


feetkeys = ['Datum Elevation', 'Ground Elevation', 'Total MD Driller', 'Total MD Logger', 'Water Depth' ]
datekeys = ['Completion Date', 'Date TD Reached', 'Spud Date' ]

monthnams = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]


def Main():
    #scraperwiki.sqlite.execute("drop table if exists swdata")
    offset, limit = 0, 300
    while True:
        qsel = "oilwellfields.quadrant as quadrant, oilwellfields.block as block, oilwellfields.wellno as wellno, contents, url, swdata.*"
        qsel = "*"
        qfrom = " from src.oilwellfields"
        qjoin = " left join swdata on oilwellfields.quadrant=swdata.quadrant and oilwellfields.block=swdata.block and oilwellfields.wellno=swdata.wellno"
        result = scraperwiki.sqlite.select("%s%s%s limit %d offset %d" % (qsel, qfrom, qjoin, limit, offset))
        ldata = [ ]
        for rdata in result:
            if re.search("403 = Request forbidden", rdata["contents"]):
                print rdata
                continue

            data = parsewell(rdata["contents"], rdata["url"])
            if not data:
                continue
            data['quadrant'], data['block'], data["wellno"] = rdata['quadrant'], rdata['block'], rdata["wellno"]

            data["lastupdatedate"] = rdata.get("lastupdatedate", "")
            data["lastupdatekey"] = rdata.get("lastupdatekey", "")
            for key in ['Datum Elevation','Total MD Driller','Total MD Logger','Water Depth','Completion Status']:
                if rdata.get(key) != data.get(key):
                    data["lastupdatedate"], data["lastupdatekey"] = updatetime, key
            ldata.append(data)

        # check if data has changed for the field and more 'Datum Elevation','Ground Elevation','Total MD Driller','Total MD Logger','Water Depth'
        # and save an update date, also check for 
        scraperwiki.sqlite.save(unique_keys=["quadrant", "block", "wellno"], data=ldata)
        if len(result) == limit:
            offset += limit
        else:
            break

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
    return lat, lng

def parsewell(html, url):
    # extract the values and check complete
    data = dict(re.findall('<A HREF="/pls/wons/wdep0100.basicWellDataEpic.*">(.*?)\.?</A>\s*=\s*(.*?)\s*<BR>', html))

    for fkey in ['Datum Elevation','Ground Elevation','Total MD Driller','Total MD Logger','Water Depth' ]:
        fkeyfeet = data.pop(fkey + ' (feet)', None)
        fkeymetres = data.pop(fkey + ' (metres)', None)
        if fkeyfeet == 'NULL Value' or fkeymetres == 'NULL Value':
            data[fkey] = 'NULL Value'
        elif fkeymetres:
            data[fkey] = float(fkeymetres)
        elif fkeyfeet:
            data[fkey] = float(fkeyfeet) * 0.3048

    data['Onshore Offshore'] = data.pop('Onshore/Offshore')

    skeys = sorted(data.keys())
    if skeys != wellkeys:
        print (skeys, wellkeys, url, html), "\n\ntruncated?"
        return None

    # remove NULL Values and convert dates
    for key in data.keys():
        if data[key] == 'NULL Value' or data[key] == '':
            del data[key]
        elif key in datekeys:
            sdate = data[key]
            data[key] = datetime.date(int(sdate[7:]), monthnams.index(sdate[3:6])+1, int(sdate[:2])).isoformat()  
                    # 22-APR-1985

    # get coordinates
    coordsystem = data.pop('Coordinate System')
    assert coordsystem == data.pop('Geodetic Datum')
    assert coordsystem == 'ED50'

    latlngbottom = latlongconv('Bottom Hole Latitude', 'Bottom Hole Longtitude', data, coordsystem)
    if latlngbottom:
        data['bottomhole_lat'], data['bottomhole_lng'] = latlngbottom
    latlngtop = latlongconv('Top hole Latitude', 'Top Hole Longtitude', data, coordsystem)
    if latlngtop:
        data['tophole_lat'], data['tophole_lng'] = latlngtop

    assert data.get('Completion Status', None) in ['Completed', 'Suspended', 'Abandoned', None]

    if data.get("Datum Type") == "Kelly Bushing":
        data["Datum Type"] = "KB"

    return data


Main()

