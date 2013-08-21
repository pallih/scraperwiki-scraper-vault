import re
import dateutil.parser
import scraperwiki
html = scraperwiki.scrape('http://www.cityofmadison.com/parkingUtility/calendar/index.cfm')

import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
cal = root.get_element_by_id('calendar')
rows = cal.cssselect('tr')

# skip over the two header rows. The first header is boring, the second is more useful:
#   0  <th width="13%">Date</th> 
#   1  <th width="24%">Locations with $4 Pay-on-Entry (Cash or Coupon only)&nbsp;</th>
#   2  <th width="19%">Time</th>
#   3  <th width="18%">Event</th>
#   4  <th width="12%">Venue</th>
#   5  <th width="14%">Time</th>
extracted = []



for row in rows[2:]:
    tds = row.cssselect('td') # get all the <td> tags

    # this is a little more interesting - if an event is at say Overture, it affects two ramps
    # 'Overture Center Garage, State Street Capitol v' 

    
    ramps = re.split(',', tds[1].text)
    for ramp in ramps:
        
        # normally the time the ramp is in special event mode is an 2 hours and 5 minutes
        # '5:00 pm - 7:05 pm' 
        # but sometimes it's different - again, events at the Overture often have two showings
        # '12:00 pm & 6:00 pm - 2:05 pm & 8:05 pm'
        times = re.split('-', tds[2].text)
        starttimes = re.split('&', times[0])
        endtimes = re.split('&', times[1])
        eventtimes = re.split('&', tds[5].text)
        if len(eventtimes) == len(starttimes):
            actualtimes = zip(starttimes, endtimes, eventtimes)
        else:
            actualtimes = zip(starttimes, endtimes, list('Unknown' for n in range(len(starttimes))))
        for actualtime in actualtimes:
            data = {}
            data['ParkingLocation'] = ramp.strip()
            data['Event'] = tds[3].text.strip()
            data['ParkingStartTime'] = dateutil.parser.parse(tds[0].text + " " + actualtime[0])
            data['ParkingEndTime'] = dateutil.parser.parse(tds[0].text + " " + actualtime[1])
            if actualtime[2] == 'Unknown':
                data['EventTime'] = dateutil.parser.parse(tds[0].text)
            else:
                # Ugh sometimes the events are weird-looking. Consider this one:
                # 2/23/2012     State Street Campus Garage    4:15 pm - 7:15 pm    WIAA State Wrestling Tournament    Kohl Center    3:00 pm - 10:00 pm
                # time is a duration, so just take the first thing we find in the string. Consider someday scrapping the 'starttime' field and
                # making it free-form
                m = re.search("(\d+:\d+\s{0,1}[a,p]m)", actualtime[2]);
                data['EventTime'] = dateutil.parser.parse(tds[0].text + " " + m.group(0))
            data['EventVenue'] = tds[4].text.strip()
            extracted.append(data)

#for x in extracted:
#   print x

from datetime import datetime
from datetime import timedelta

# OK, if we actually extracted data, let's save it
if len(extracted) > 0:

    # First, save when we ran this scrape
    scraperwiki.sqlite.execute("drop table if exists scraperstats")
    scraperwiki.sqlite.execute("create table scraperstats (lastupdated date, cacheuntil date)")

    now = datetime.now()
    oneday = timedelta(days=+1,minutes=+10)
    tomorrow = now+oneday
    sql = "insert into scraperstats values( datetime('" + now.strftime("%Y-%m-%d %H:%M:%S") + "'), datetime('" + tomorrow.strftime("%Y-%m-%d %H:%M:%S") + "'))" 
    #scraperwiki.sqlite.execute("insert into scraperstats values(datetime('now'))")
    scraperwiki.sqlite.execute(sql)
    
    # now, delete all of the old data and write new data in its place
    # SW has an 'save or update if new', but we don't know what's new and whats changed
    # so this is safer
    scraperwiki.sqlite.execute("drop table if exists'swdata'")
    scraperwiki.sqlite.save([], extracted)

    # I don't think we need this - we have to commit the changes to scraperstats
    # but the save() above includes a commit - but I don't know if that commits only
    # changes to swdata or to all outstand xtns
    scraperwiki.sqlite.commit()


   
    