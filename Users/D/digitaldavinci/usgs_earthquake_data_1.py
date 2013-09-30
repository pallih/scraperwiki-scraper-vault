import scraperwiki
import dateutil.parser
from datetime import date, timedelta
from bs4 import BeautifulSoup

ending_date = date.today() - timedelta(1)

for starting_year in range(1973, ending_date.year):

    ending_year = starting_year + 1

    # special case for ending day since data past today does not exist
    if ending_year == ending_date.year:
        ending_day = ending_date.day
    else:
        ending_day = 31

    page_url = "http://neic.usgs.gov/cgi-bin/epic/epic.cgi?SEARCHMETHOD=1&FILEFORMAT=6&SEARCHRANGE=HH&SYEAR=%d&SMONTH=1&SDAY=1&EYEAR=%d&EMONTH=12&EDAY=%d&LMAG=&UMAG=&NDEP1=&NDEP2=&IO1=&IO2=&CLAT=0.0&CLON=0.0&CRAD=0.0&SUBMIT=Submit+Search" % (starting_year, ending_year, ending_day)

    print 'Processing %d-%d' % (starting_year, ending_year)

    html = scraperwiki.scrape(page_url)
    
    soup = BeautifulSoup(html)
    
    data = soup.pre.string
    
    first_line = True
    
    for line in data.split('\n'):
    
        if line:
    
            if first_line: # first line is blank, second is headers
                first_line = False
                continue
    
            (year, month, day, time, lat, lng, magnitude, depth, catalog) = line.split(',')
    
            eq_datetime = '%s/%s/%s %s' % (day.strip(), month.strip(), year.strip(), time.strip())
    
            eq_date = dateutil.parser.parse(eq_datetime, dayfirst=True).date()

            eq_time = dateutil.parser.parse(eq_datetime, dayfirst=True).time()
    
            earthquake_info = {
                'Date': eq_date,
                'Time': eq_time,
                'Latitude': lat.strip(),
                'Longitude': lng.strip(),
                'Depth': depth.strip(),
                'Magnitude': magnitude,
                'Catalog': catalog.strip(),
            }
    
            scraperwiki.sqlite.save(unique_keys=['Date', 'Time', 'Latitude', 'Longitude', 'Depth', 'Magnitude'], data=earthquake_info)




import scraperwiki
import dateutil.parser
from datetime import date, timedelta
from bs4 import BeautifulSoup

ending_date = date.today() - timedelta(1)

for starting_year in range(1973, ending_date.year):

    ending_year = starting_year + 1

    # special case for ending day since data past today does not exist
    if ending_year == ending_date.year:
        ending_day = ending_date.day
    else:
        ending_day = 31

    page_url = "http://neic.usgs.gov/cgi-bin/epic/epic.cgi?SEARCHMETHOD=1&FILEFORMAT=6&SEARCHRANGE=HH&SYEAR=%d&SMONTH=1&SDAY=1&EYEAR=%d&EMONTH=12&EDAY=%d&LMAG=&UMAG=&NDEP1=&NDEP2=&IO1=&IO2=&CLAT=0.0&CLON=0.0&CRAD=0.0&SUBMIT=Submit+Search" % (starting_year, ending_year, ending_day)

    print 'Processing %d-%d' % (starting_year, ending_year)

    html = scraperwiki.scrape(page_url)
    
    soup = BeautifulSoup(html)
    
    data = soup.pre.string
    
    first_line = True
    
    for line in data.split('\n'):
    
        if line:
    
            if first_line: # first line is blank, second is headers
                first_line = False
                continue
    
            (year, month, day, time, lat, lng, magnitude, depth, catalog) = line.split(',')
    
            eq_datetime = '%s/%s/%s %s' % (day.strip(), month.strip(), year.strip(), time.strip())
    
            eq_date = dateutil.parser.parse(eq_datetime, dayfirst=True).date()

            eq_time = dateutil.parser.parse(eq_datetime, dayfirst=True).time()
    
            earthquake_info = {
                'Date': eq_date,
                'Time': eq_time,
                'Latitude': lat.strip(),
                'Longitude': lng.strip(),
                'Depth': depth.strip(),
                'Magnitude': magnitude,
                'Catalog': catalog.strip(),
            }
    
            scraperwiki.sqlite.save(unique_keys=['Date', 'Time', 'Latitude', 'Longitude', 'Depth', 'Magnitude'], data=earthquake_info)




