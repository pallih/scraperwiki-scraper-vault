#!/usr/bin/env python
# Scrape Auckland food ratings

import scraperwiki
from scrapemark import scrape
from datetime import datetime, timedelta
from dateutil import parser
import urllib
import json
import sys
from time import sleep
import mechanize
from random import randint

## FIX
#scraperwiki.sqlite.execute('CREATE TABLE `swdata2` (`name` text, `grade` text, `address` text, `inspection_date` text);')
#scraperwiki.sqlite.commit()
#print '1'
#scraperwiki.sqlite.execute('INSERT INTO swdata2 select distinct name, grade, address, inspection_date from swdata;')
#scraperwiki.sqlite.commit()
#print '1'
# scraperwiki.sqlite.execute('ALTER TABLE swdata ADD COLUMN `sin_lng` real;')
#scraperwiki.sqlite.execute('ALTER TABLE swdata ADD COLUMN `cos_lng` real;')
#scraperwiki.sqlite.execute('ALTER TABLE swdata ADD COLUMN `sin_lat` real;')
#scraperwiki.sqlite.execute('ALTER TABLE swdata ADD COLUMN `cos_lat` real;')
#scraperwiki.sqlite.commit()
#print '1'
#scraperwiki.sqlite.execute('ALTER TABLE swdata2 ADD COLUMN `lat` real;')
#scraperwiki.sqlite.commit()
# print '1'
#scraperwiki.sqlite.execute('UPDATE swdata2 SET lat = (SELECT lat FROM swdata WHERE swdata2.name = name AND swdata2.grade = grade AND swdata2.address = address AND swdata2.inspection_date = inspection_date AND lat IS NOT NULL);')
#scraperwiki.sqlite.commit()
#print '1'
#scraperwiki.sqlite.execute('UPDATE swdata2 SET lng = (SELECT lng FROM swdata WHERE swdata2.name = name AND swdata2.grade = grade AND swdata2.address = address #AND swdata2.inspection_date = inspection_date AND lng IS NOT NULL);')
#scraperwiki.sqlite.commit()
#print 'last'
#print 'starting'
#scraperwiki.sqlite.execute('ALTER TABLE swdata RENAME TO dupes;')
#scraperwiki.sqlite.commit()
#print 'ggg'
#scraperwiki.sqlite.execute('delete from swdata where name = "Primo Bar And Nightclub";')
#scraperwiki.sqlite.execute('delete from swdata where name = "The Corner Cafe";')
#scraperwiki.sqlite.commit()
#print 'EH?'
#sys.exit()
###

BASE_URL = 'http://www.aucklandcity.govt.nz/council/services/foodsearch'
LIST_URL = '%s/default.asp?pTradeName=%%25%%25%%25&pStreetName=&pSuburb=&pGrade=&status=go' %  BASE_URL
DETAIL_URL = '/detail.asp?pFoodGradeId='

PAGE_LIST_PATTERN="""
    <td valign="top" colspan="2" class="pageNumbers">
    {*
    <a>{{ []|int }}</a>
    *}
    </td>
"""

EST_PATTERN = """
        {*
           <a href="detail.asp?pFoodGradeId={{ []|int }}"></a>
        *}
"""

DETAIL_PATTERN = """
          <td valign="top" class="purple" colspan="3"><h3>{{ name }}</h3></td>
          <td valign="top" colspan="2">{{ address }}</td>
          <td valign="top"><h1>{{ grade }}</h1></td>
        <tr>
          <td valign="top" nowrap><b>Last inspection date</b></td>
          <td valign="top">{{ inspection_date }}</td>
        </tr>
          
"""
# !! Some dummy values below !! 
EXEMPT_PATTERN = """
          <td valign="top" class="purple" colspan="3"><h3>{{ name }}</h3></td>
        </tr>
        <tr>
          <td valign="top" nowrap><b>Address</b></td>
          <td valign="top" colspan="2">{{ address }}</td>
        </tr>
         <tr>
          <td valign="top" colspan="3">This premises has a registered food safety programme*{{ inspection_date }}in place&nbsp;<br>
            and is {{ grade }} from Auckland City's food grading programme.<br>
            <br>
            *More about <a href='grading.asp#programme'>food safety programmes</a> 
          </td>
        </tr>
"""

def locate(address):
    """ 
    Wrapper for google geocoder
    Returns (lat,lng) tuple or None 
    """
    url = "http://maps.googleapis.com/maps/api/geocode/json?%s" % \
        urllib.urlencode({ 'address':address, 'sensor':'false' })
    jd = json.loads(scraperwiki.scrape(url))

    sleep(randint(1,3))

    if jd['status'] == 'OK':
        return (float(jd['results'][0]['geometry']['location']['lat']),\
            float(jd['results'][0]['geometry']['location']['lng']))
    else: 
        return None

def main():
    #  Fetch last page index
    last_page = scraperwiki.sqlite.get_var('last_page', default=0)
    #Scrape initial list
    p = scrape(PAGE_LIST_PATTERN, url=LIST_URL)
    # print p
    print 'starting from ' + str(last_page)
    
    # 
    if last_page == 0:
        print 'first page? '
        # Scrape the first list page
        scrape_list(LIST_URL)
    
    # slice from last index
    p = p[last_page:]
    # print p
        
    # Scrape each list page
    for page in p:
        # print 'scraping page : ' + str(page)
        url = "%s&intPageNumber=%d" % (LIST_URL, page)
        # print url
        scrape_list(url)
        # save page index
        scraperwiki.sqlite.save_var('last_page', page-1)
        
    # reset page index to 0
    scraperwiki.sqlite.save_var('last_page', 0)


def mech_scrape(url):
    br = mechanize.Browser()
    # sometimes the server is sensitive to this information
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')] 
    return br.open(url).read()

def scrape_list(url):
    #html = mech_scrape(url)
    p = scrape(EST_PATTERN, url=url)
    print p
    for e in p:
        est_url = "%s%s%d" % (BASE_URL, DETAIL_URL, e)
        print 'scraping: ' + est_url
        print 'scraping id: ' + str(e)
        scrape_detail(est_url, e)
    
def scrape_detail(est_url, id):
    
    html = scraperwiki.scrape(est_url)
    est_details = scrape(DETAIL_PATTERN, html)

    if not est_details:
        #Try the exempt pattern
        est_details = scrape(EXEMPT_PATTERN, html)
        
        if not est_details:
            # it's either changed hands and will turn up soon, or it's new
            return
    else:
        # print est_details['inspection_date']
        est_details['inspection_date'] =  datetime.strftime(datetime.strptime(est_details['inspection_date'], '%d/%m/%Y'), '%Y-%m-%d')
        # parser.parse(est_details['inspection_date'])
        # print est_details['inspection_date']        

    # Locate
    # Attempt to find
    sql = 'lat, lng FROM swdata WHERE address = "%s" AND lat IS NOT NULL LIMIT 0,1' % est_details['address']
    latlng = scraperwiki.sqlite.select(sql)
    
    #Avoid multiple google lookups
    if latlng:
        # print 'DB Geo'
        # print latlng
        est_details['lat'] = latlng[0]['lat']
        est_details['lng'] = latlng[0]['lng']
        # print est_details['lat']
    else:
        # print 'Goog lookup'
        location = locate(est_details['address'] + ', Auckland, NZ')
        if location:
            est_details['lat'], est_details['lng'] = location 
        

    #est_details['fg_id'] = id  # Gah! id aint unique??
    #est_details['url'] = est_url # URLs are useless - the IDs float!!?? WTF!?
    
    
    # Save
    scraperwiki.sqlite.save(unique_keys=['name','address','grade','inspection_date'], data=est_details)
    print 'saved'
    
main()


