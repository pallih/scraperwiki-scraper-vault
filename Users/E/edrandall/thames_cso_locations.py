# Scrape Thames CSO data

import scraperwiki
import xlrd
import datetime
import re
from collections import OrderedDict

TABLENAME = "cso_locations";

# Normalised version of "discharge_type"
DISCHARGE_TYPES = {
    'Sewage Pumping Station': re.compile('(sps|sewage\s+pumping\s+station)', re.I),
    'Storm Sewer Overflow':   re.compile('(sewer\s+storm\s+overflow|storm\s+sewer\s+overflow)', re.I),
    'Storm Tank Overflow':    re.compile('(storm\s+tank)', re.I),
};

def cellval(cell, datemode):
    if cell.ctype == xlrd.XL_CELL_DATE:
        datetuple = xlrd.xldate_as_tuple(cell.value, datemode)
        if datetuple[3:] == (0, 0, 0):
            return datetime.date(datetuple[0], datetuple[1], datetuple[2])
        return datetime.date(datetuple[0], datetuple[1], datetuple[2], datetuple[3], datetuple[4], datetuple[5])
    if cell.ctype == xlrd.XL_CELL_EMPTY:    return None
    if cell.ctype == xlrd.XL_CELL_BOOLEAN:  return cell.value == 1
    return cell.value


def scrapeData(dataSetId, srcUrl):
    print "Scraping dataset: ",dataSetId+" from: "+srcUrl

    xlbin = scraperwiki.scrape(srcUrl)
    book = xlrd.open_workbook(file_contents=xlbin)
    sheet = book.sheet_by_index(0) 

    keys = sheet.row_values(0)
    for i in range(len(keys)):
        keys[i] = keys[i].replace(' ','_').lower()

    rowsSaved= 0
    for rownumber in range(1, sheet.nrows):

        # create dictionary of the row values
        values = [ cellval(c, book.datemode) for c in sheet.row(rownumber) ]
        data = dict(zip(keys, values))
        data['rownumber'] = rownumber
        data['datasetid'] = dataSetId

        if data.get('eastings') != None and data.get('northings') != None :
            location = scraperwiki.geo.os_easting_northing_to_latlng(data['eastings'], data['northings'])
            #print "east:",data['eastings']," north:",data['northings']," location:",location
            data['lat'] = location[0];
            data['lng'] = location[1];

        elif data.get('grid_ref') != None :
            location = scraperwiki.geo.osgb_to_lonlat(data['grid_ref'])
            #print "grid_ref:",data['grid_ref']," location:",location
            data['lat'] = location[1];
            data['lng'] = location[0];

        elif data.get('grid_reference') != None :
            location = scraperwiki.geo.osgb_to_lonlat(data['grid_reference'])
            data['lat'] = location[1];
            data['lng'] = location[0];

        # Find normalised version of "discharge_type"
        if (data['discharge_type'] != None):
            for ndt in DISCHARGE_TYPES:
                if (DISCHARGE_TYPES[ndt].search(data['discharge_type']) != None):
                    data['ndt'] = ndt;
                    break;

        # only save if it is a full row (rather than a blank line or a note)
        if data['site_name'] != None:
            scraperwiki.sqlite.save(unique_keys=['datasetid', 'rownumber'], data=data, table_name=TABLENAME);
            rowsSaved = rowsSaved + 1

    print "Dataset: ",dataSetId," saved: ",rowsSaved," rows"


def createTable():
    sql = "DROP TABLE `"+TABLENAME+"`";
    scraperwiki.sqlite.execute(sql);
    scraperwiki.sqlite.commit();

    sql = "CREATE TABLE `"+TABLENAME+"` ("+\
            "`datasetid` text, "+\
            "`rownumber` integer, "+\
            "`site_name` text, "+\
            "`ndt` text, "+\
            "`discharge_type` text, "+\
            "`receiving_water` text, "+\
            "`receiving_watercourse` text, "+\
            "`site_id` text, "+\
            "`consent_reference` text, "+\
            "`lat` real, "+\
            "`lng` real, "+\
            "`eastings` real, "+\
            "`northings` real, "+\
            "`grid_ref` text, "+\
            "`grid_reference` text"+\
            " )";
    scraperwiki.sqlite.execute(sql);
    scraperwiki.sqlite.commit();

# Main program

#createTable();
#scrapeData("DEP2009-2983", "http://www.parliament.uk/deposits/depositedpapers/2009/DEP2009-2983.xls")
#scrapeData("Xl0000007",    "http://www.cassilis.plus.com/TAC/Xl0000007.xls")
#scrapeData("Crane-CSOs",   "http://www.cassilis.plus.com/TAC/crane-cso-locations.xls")
scrapeData("Tributary-CSOs",   "http://www.cassilis.plus.com/TAC/tributary-cso-locations.xls")

