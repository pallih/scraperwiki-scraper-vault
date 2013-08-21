import scraperwiki
import xlrd
import re
import urllib2
import datetime


def ConvertCell(cell):
    if cell.ctype == xlrd.XL_CELL_DATE:
        d = xlrd.xldate_as_tuple(cell.value, 0)
        return datetime.date(d[0], d[1], d[2])
    return cell.value

def extract_sheet(sheet, test_headings):
    result = { }
    
    headings = [ sheet.cell(0, i).value  for i in range(sheet.ncols) ]
    #print test_headings
    #print headings
    
    assert headings == test_headings, headings
    #print headings
    
    for irow in range(1, sheet.nrows):
        row = [ ConvertCell(sheet.cell(irow, i))  for i in range(sheet.ncols) ]
        data = dict(zip(headings, row))
        result[data['SEQNOS']] = data
    return result

def ExtractLatLng(data):
    latdeg, latmin, latsec, latquad = data.pop('LAT_DEG'), data.pop('LAT_MIN'), data.pop('LAT_SEC'), data.pop('LAT_QUAD')
    lngdeg, lngmin, lngsec, lngquad = data.pop('LONG_DEG'), data.pop('LONG_MIN'), data.pop('LONG_SEC'), data.pop('LONG_QUAD')
    if latdeg == '':
        if latsec == 0.0:
            latsec = ''
        assert (latdeg, latmin, latsec) == ('', '', ''), (latdeg, latmin, latsec, latquad, data)
        assert (lngdeg, lngmin, lngsec) == ('', '', ''), (lngdeg, lngmin, lngsec, lngquad, data)
        return None
    if lngquad != 'W':
        print "Bad lngquad!", lngquad, data
        lngquad = 'W'
    if latquad != 'N':
        print "Bad latquad!", latquad, data
        lngquad = 'W'
    try:
        lat = latdeg + latmin/60.0 + (latsec or 0)/3600.0
        lng = 360 - (lngdeg + lngmin/60.0 + (lngsec or 0)/3600.0)
    except TypeError:
        print "Typeerror on:", (latdeg, latmin, latsec), (lngdeg, lngmin, lngsec)
        return None
    return (lat, lng)

# make global due to problems with stack tracing
calls_data = None
commons_data = None
incident_data = None

def combine_data():

    seqnos = set(calls_data.keys())
    seqnos = seqnos.union(commons_data.keys())
    seqnos = seqnos.union(incident_data.keys())
    
    result = [ ]
    for i, seqno in enumerate(seqnos):
        #if i < 21000:
        #    continue
        data = calls_data.get(seqno, {})
        data.update(commons_data.get(seqno, {}))
        data.update(incident_data.get(seqno, {}))
        result.append(data)

        latlng = ExtractLatLng(data)
        if (i % 50) == 0:
            print i, latlng, data

        date = data.get('INCIDENT_DATE_TIME')
        scraperwiki.datastore.save(unique_keys=['SEQNOS'], data=data, date=date, latlng=latlng)

def scrape_year(year):
    global calls_data, commons_data, incident_data
    all_data = []

    # proper link which currently seems to download a fraction of the file
    url = "http://seagrass.goatchurch.org.uk/~julian/spills%d.xls" % year

    xldata = urllib2.urlopen(url).read()
    book = xlrd.open_workbook(file_contents=xldata)

    # We can find out information about the workbook
    print "Workbook has %s sheet(s)" % book.nsheets

    #grab the data from the 'calls' sheet
    calls_data = extract_sheet(book.sheet_by_index(0), ['SEQNOS', 'DATE_TIME_RECEIVED', 'DATE_TIME_COMPLETE', 'CALLTYPE', 'RESPONSIBLE_COMPANY', 'RESPONSIBLE_ORG_TYPE', 'RESPONSIBLE_CITY', 'RESPONSIBLE_STATE', 'RESPONSIBLE_ZIP', 'ON_BEHALF_OF', 'SOURCE'])
    
    #grab the data from the 'commons' sheet    
    commons_data = extract_sheet(book.sheet_by_index(1), ['SEQNOS', 'DESCRIPTION_OF_INCIDENT', 'TYPE_OF_INCIDENT', 'INCIDENT_CAUSE', 'INCIDENT_DATE_TIME', 'INCIDENT_DTG', 'INCIDENT_LOCATION', 'LOCATION_ADDRESS', 'LOCATION_STREET1', 'LOCATION_STREET2', 'LOCATION_NEAREST_CITY', 'LOCATION_STATE', 'LOCATION_COUNTY', 'LOCATION_ZIP', 'DISTANCE_FROM_CITY', 'DISTANCE_UNITS', 'DIRECTION_FROM_CITY', 'LAT_DEG', 'LAT_MIN', 'LAT_SEC', 'LAT_QUAD', 'LONG_DEG', 'LONG_MIN', 'LONG_SEC', 'LONG_QUAD', 'LOCATION_SECTION', 'LOCATION_TOWNSHIP', 'LOCATION_RANGE', 'POTENTIAL_FLAG'])    
    
    #grab the data from the 'incident details' sheet        
    incident_data = extract_sheet(book.sheet_by_index(2), ['SEQNOS', 'FIRE_INVOLVED', 'FIRE_EXTINGUISHED', 'ANY_EVACUATIONS', 'NUMBER_EVACUATED', 'WHO_EVACUATED', 'RADIUS_OF_EVACUATION', 'ANY_INJURIES', 'NUMBER_INJURED', 'NUMBER_HOSPITALIZED', 'ANY_FATALITIES', 'NUMBER_FATALITIES', 'ANY_DAMAGES', 'DAMAGE_AMOUNT', 'AIR_CORRIDOR_CLOSED', 'AIR_CORRIDOR_DESC', 'AIR_CLOSURE_TIME', 'WATERWAY_CLOSED', 'WATERWAY_DESC', 'WATERWAY_CLOSURE_TIME', 'ROAD_CLOSED', 'ROAD_DESC', 'ROAD_CLOSURE_TIME', 'CLOSURE_DIRECTION', 'MAJOR_ARTERY', 'TRACK_CLOSED', 'TRACK_DESC', 'TRACK_CLOSURE_TIME', 'MEDIA_INTEREST', 'MEDIUM_DESC', 'ADDITIONAL_MEDIUM_INFO', 'BODY_OF_WATER', 'TRIBUTARY_OF', 'RELEASE_SECURED', 'ESTIMATED_DURATION_OF_RELEASE', 'RELEASE_RATE', 'DESC_REMEDIAL_ACTION', 'STATE_AGENCY_ON_SCENE', 'STATE_AGENCY_REPORT_NUM', 'OTHER_AGENCY_NOTIFIED', 'WEATHER_CONDITIONS', 'AIR_TEMPERATURE', 'WIND_SPEED', 'WIND_DIRECTION', 'WATER_SUPPLY_CONTAMINATED', 'SHEEN_SIZE', 'SHEEN_COLOR', 'DIRECTION_OF_SHEEN_TRAVEL', 'SHEEN_ODOR_DESCRIPTION', 'WAVE_CONDITION', 'CURRENT_SPEED', 'CURRENT_DIRECTION', 'WATER_TEMPERATURE', 'TRACK_CLOSE_DIR', 'EMPL_FATALITY', 'PASS_FATALITY', 'COMMUNITY_IMPACT', 'WIND_SPEED_UNIT', 'EMPLOYEE_INJURIES', 'PASSENGER_INJURIES', 'OCCUPANT_FATALITY', 'CURRENT_SPEED_UNIT', 'ROAD_CLOSURE_UNITS', 'TRACK_CLOSURE_UNITS', 'SHEEN_SIZE_UNITS', 'ADDITIONAL_INFO', 'STATE_AGENCY_NOTIFIED', 'FEDERAL_AGENCY_NOTIFIED', 'NEAREST_RIVER_MILE_MARKER', 'SHEEN_SIZE_LENGTH', 'SHEEN_SIZE_LENGTH_UNITS', 'SHEEN_SIZE_WIDTH', 'SHEEN_SIZE_WIDTH_UNITS', 'OFFSHORE', 'DURATION_UNIT', 'RELEASE_RATE_UNIT', 'RELEASE_RATE_RATE', 'PASSENGERS_TRANSFERRED'])
    
    #finally, combine
    combine_data()


# run the scraper for the years we know we have data for
scrape_year(2009)
scrape_year(2008)
scrape_year(2007)
scrape_year(2006)
scrape_year(2005)

