import scraperwiki
import xlrd
import datetime
import re
import scraperwiki
import urllib
import urllib2
import simplejson


# A pattern used to replace address numbers of the for 123X with 1230
pattern = re.compile("^(\d+)(X+) (.*)")

# A function to convert an Excel cell value into a useful 
# python value.  Taken straight from the ScraperWiki Excel tutorial
def cellval(cell, datemode):
    if cell.ctype == xlrd.XL_CELL_DATE:
        try:
            datetuple = xlrd.xldate_as_tuple(cell.value, datemode)
        except Exception, e:
            print "BAD", cell, e
            return str(cell)
        try:
            if datetuple[3:] == (0, 0, 0):
                return datetime.date(datetuple[0], datetuple[1], datetuple[2])
            return datetime.datetime(datetuple[0], datetuple[1], datetuple[2], datetuple[3], datetuple[4], datetuple[5])
        except ValueError, e:
            print "BAD value", datetuple, cell, e
            return str(cell)
    if cell.ctype == xlrd.XL_CELL_EMPTY:    return None
    if cell.ctype == xlrd.XL_CELL_BOOLEAN:  return cell.value == 1
    return cell.value

# If we want to do the geocoding in the scraperwiki
def decodeData(data) :
    geocode_url = 'http://tasks.arcgisonline.com/ArcGIS/rest/services/Locators/TA_Streets_US_10/GeocodeServer/findAddressCandidates?Single+Line+Input='+urllib.quote_plus(address)+'&outFields=&outSR=&f=json'
    georeq = urllib2.Request(geocode_url)
    geo_response = urllib2.urlopen(georeq)
    geocode = simplejson.loads(geo_response.read())
    if len(geocode['candidates']):
        data['LAT'] = geocode['candidates'][0]['location']['y']
        data['LONG'] = geocode['candidates'][0]['location']['x']

# The crux of the work
# Read one spreadsheet, get the worksheet named 'INCIDENTS'
# read all the rows and clean up the address for each row
def getCrimeData(docId, url, folder) :

    # The URL for a week's data
    # We need to enhance this to get each week's spreadsheet
    url = "http://www.stpaul.gov/DocumentCenter/View/" + docId
    
    # Get the data from the spreadsheet
    xlbin = scraperwiki.scrape(url)
    book = xlrd.open_workbook(file_contents=xlbin)
    
    # There should be one sheet that we care about called INCIDENTS
    sheet = book.sheet_by_name('INCIDENTS')
    if not sheet :
        print "Not sheet named INCIDENTS"
        return
    # Get the column headers and turn them into valid key names by removing periods
    keys = sheet.row_values(0)
    for col in range(0, len(keys)) :
        keys[col] = keys[col].replace('.', '')
        keys[col] = keys[col].replace(' ', '_')
        keys[col] = keys[col].replace('#', '')
    
    #For each row
    recordCount = 0
    print "Reading " + str(sheet.nrows -1) + " rows" 
    for rownumber in range(1, sheet.nrows):
        try:
            # create dictionary of the row values
            values = [ cellval(c, book.datemode) for c in sheet.row(rownumber) ]
            data = dict(zip(keys, values))
            # The TIME columns is reduntant with the DATE column
            del data['TIME']
            # The address needs to be cleaned up
            # The report replaces the last numerals in the address with an 'X'
            address = data['ADDRESS']
            data['RAWADDRESS'] = address
            m = pattern.match(address)
            if (m) :
                xxx = m.group(2)
                zeros = "0" * len(xxx)
                address = m.group(1) + zeros + " " + m.group(3)
            address = address + ", St Paul, MN"
            data['ADDRESS'] = address
        
            # Now that we have the clean address, geocode it
            # geocodeData(data)
                
            # Save th data to the ScraperWiki data store
            scraperwiki.sqlite.save(unique_keys=['CN'], data=data)
            recordCount = recordCount +1
        except Exception as inst:
            print type(inst)     # the exception instance
            print inst.args      # arguments stored in .args
            print inst           # __str__ allows args to printed directly
            print "Failed to save row " + str(rownumber) + " of " + url
    print "Read " + str(recordCount)  + " incidents from " + url



## Main
def main () :
    scraperwiki.sqlite.attach("findstpaulpoliceincidentreports") 
    rows =  scraperwiki.sqlite.select('xlsid,  xlsurl, foldername from `findstpaulpoliceincidentreports`.swdata order by xlsid')
    for row in  rows :
        print "Getting data for " + str(row ['xlsid']) + " " + row ['xlsurl']
        getCrimeData(str(row ['xlsid']), row ['xlsurl'], row ['foldername'])

## Clean up the ADDRESS column because I had the string replacement wrong
## Should not need this again, but iit might be a handy code sample
def cleanup () :
    rows = scraperwiki.sqlite.execute("select * from swdata")
    print rows
    keys = rows['keys']
    for values in  rows['data'] :
        data = dict(zip(keys,values))
#        print data
        address = data['RAWADDRESS']
        m = pattern.match(address)
        if (m) :
            xxx = m.group(2)
            zeros = "0" * len(xxx)
            address = m.group(1) + zeros + " " + m.group(3)
        address = address + ", St Paul, MN"
#        print "Updating " + data['ADDRESS'] + " to " + address
        data['ADDRESS'] = address  
        scraperwiki.sqlite.save(unique_keys=['rowid'], data=data)


## To run this wiki, remove all the project's data, uncomment the next line
## and run the project.  It will take several hours to complete.
#main()


#cleanup()