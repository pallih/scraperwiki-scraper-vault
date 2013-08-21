import lxml.html
import urllib2
import re, sys
from BeautifulSoup import BeautifulSoup
import scraperwiki
import math
import time
import random
from datetime import datetime

def isTimeFormat(input):     
    try:         
        time.strptime(input, '%H:%M')         
        return True     
    except ValueError:
         return False 

# scrape the weeks list of economic events from the forex pros website
# save results to a database or file

def calendar_scrapper(url, sec_type):

    data = []
#    record = {'date': None,'time':None,'currency':None, 'impact':None, 'eventname':None, 'actual_val':None, 'forecast_val':None, 'previous_val':None }
    record = {}
    release_date =''
    d    = datetime.now()
    yr = str(d.year)


    # read the forex pros URL 
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(url,headers=hdr)
    html = urllib2.urlopen(req)
    
    
    soup = BeautifulSoup(html)
    # print soup.prettify()

    # find the table with the econ data - table 6
    htm_tables = soup.findAll('table')
    # print htm_tables
        
    table = htm_tables[0]
    econ_data = table.findAll('tr')
    
    # for each release data loop through rows in econ table to extract releases
    for row in econ_data:
       
        rowstr = str(row)
        # find the release dates available    
        if rowstr.find('event_timestamp')>0:
            release_date = row.get('event_timestamp', 'nothing')
            release_date = re.sub('&nbsp;',' ',release_date)
            release_date = re.sub(',','',release_date)
            release_date = re.sub('  ',' ',release_date)

            # print release_date
            cell = row.findAll('td')
            # print cell

            for item in cell:     

                # print item.get('class','nothing')
                cellstr = str(item.get('class','nothing'))
                cellstr2 = str(item.get('id','nothing'))
               # print cellstr

                if cellstr.find('center time') > -1:
                    date_object = datetime.strptime(release_date, '%Y-%m-%d %H:%M:%S') 
                    record['datetime'] = date_object.strftime('%Y-%m-%d %H:%M:%S')

                elif cellstr.find('flagCur') > -1:
                    currency = currency = re.sub('&nbsp;',' ',item.text)
                    record['currency'] = currency

                    record['country'] = item.span.get('title')
                
                elif cellstr.find('sentiment') > -1:
                    impact = str(item.get('title','nothing'))    
                    record['impact'] = impact

                elif cellstr.find('left event') > -1:

                    eventname = re.sub('&nbsp;',' ',item.text)    
                    record['eventname'] = eventname

                if cellstr2.find('eventActual') > -1:
                    actual_val = re.sub('&nbsp;',' ',item.text)   
                    record['actual_val'] = actual_val
                    record['better_worse'] = item.get('title')
                    
                elif cellstr2.find('eventForecast') > -1:
                    forecast_val = re.sub('&nbsp;',' ',item.text)   
                    record['forecast_val'] = forecast_val

                elif cellstr2.find('eventPrevious') > 0:
                    previous_val= re.sub('&nbsp;',' ',item.text)    
                    record['previous_val'] = previous_val

    #    print record    

        if len(record)>0:
            record['key'] = str(record['datetime']) + str(eventname)
            scraperwiki.sqlite.save(["key"], record)
            data.append(record)
    return data              

def main():
    
    calendar_list =[]
    base_url = 'http://www.investing.com/'
    cal_page_dict = {'calendar':'economic-calendar/'}
    cal_type = cal_page_dict.keys()

    i = 0   
    for typ in cal_type:

        url = base_url+str(cal_page_dict[typ])
        print url 
        calendar_list = calendar_scrapper(url, typ)
        i +=1     
#    print len(calendar_list)
#    print calendar_list
    return calendar_list
    

#if __name__ == "__main__":
     
main()

