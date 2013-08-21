###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
import mechanize
import pytz
from datetime import datetime, date, timedelta
from BeautifulSoup import BeautifulSoup

# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['Date', 'Time', 'TimePeriod', 'Artist', 'Title'])

def save_current_page_songs(soup, time_period):
    songs = soup.findAll('div', {'class':'infoWrap'}) 
    for song in songs:
        
        if song.find('p') is not None:
            break
    
        record = {}    
    
        date_div = song.find('div', 'date')
        if date_div is not None:
            record['Date'] = date_div.text
        
        time_div = song.find('div', 'time')
        if time_div is not None:
            record['Time'] = time_div.text
    
        artist_div = song.find('div', 'artist') 
        if artist_div is not None:
            record['Artist'] = artist_div.text
    
        title_div = song.find('div', 'title')
        if title_div is not None:
            record['Title'] = title_div.text
        
        record['TimePeriod'] = time_period

        #print record
        scraperwiki.sqlite.save(unique_keys=["Date","Time"], data=record, table_name="songs")

def get_gold_time_period(hour):
    if hour >= 0 and hour <= 4:
        return '0'
    elif hour >= 4 and hour <= 8:
        return '1'
    elif hour >= 8 and hour <= 12:
        return '2'
    elif hour >= 12 and hour <= 16:
        return '3'
    elif hour >= 16 and hour <= 20:
        return '4'
    elif hour >= 20:
        return '5'

def scrape_songs_for_date_and_time_period(date, time_period):
    br = mechanize.Browser()
    br.open('http://www.mygoldmusic.co.uk/playlist.asp')
    br.select_form(name='form1')
    
    # Set the Start Date & Period
    br.set_value([date.strftime("%Y-%m-%d")], name="selDayList", kind="list")
    br.set_value([time_period], name="selHourList", kind="list")
    
    # and submit the form
    br.submit()
    soup = BeautifulSoup(br.response().read())
    save_current_page_songs(soup, time_period)

gold_time_periods = ['5','4','3','2','1','0']

tz_gmt = pytz.timezone("GMT")
now = datetime.now(tz_gmt)
current_gold_time_period = get_gold_time_period(now.hour)

#scrape_songs_for_date_and_time_period(now, current_gold_time_period)

for day in range(0,14):
    scrape_date = now - timedelta(days=day)
    print scrape_date
    for period in gold_time_periods:
        if day == 0:
            print 'day is 0, period is ' + period
            if int(period) < int(current_gold_time_period):
                result = scraperwiki.sqlite.select("count(*) from songs where TimePeriod='%s' and Date='%s'" % (period, scrape_date.strftime("%d/%m/%y")))
                if result[0]['count(*)'] < 10:
                    scrape_songs_for_date_and_time_period(scrape_date, period)
                else:
                    print result[0]['count(*)']
        else:
            print 'day is ' + str(day) + ', period is ' + period
            result = scraperwiki.sqlite.select("count(*) from songs where TimePeriod='%s' and Date='%s'" % (period, scrape_date.strftime("%d/%m/%y")))
            if result[0]['count(*)'] < 10:
                scrape_songs_for_date_and_time_period(scrape_date, period)
            else:
                print result[0]['count(*)']
