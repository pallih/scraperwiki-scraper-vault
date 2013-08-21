import time
import sqlite3
from datetime import datetime
import scraperwiki
from BeautifulSoup import BeautifulSoup as bs

now = datetime.now()
timestamp = int(time.time())


# http://cs.wikipedia.org/wiki/Dálnice_D1#P.C5.99ehled_.C3.BAsek.C5.AF
sensors = [ 
            469, # 96,23km směr Ostrava
            489, # 207,20km směr Ostrava
            507, # 96,23km směr Praha
            521, # 207,20km směr Praha
            1602, # 12,71km směr Ostrava
            1603, # 12,71km směr Praha
            1604, # 185,12km směr Ostrava
            1605, # 185,12km směr Praha
          ]

url = 'http://www.dopravniinfo.cz/public/data/traffic/%s.xml'



# data: sensor_id, date, hour, cars per hour, average speed
# fill out missing data.. or not?


for sensor_id in sensors:
    data = []
    html = scraperwiki.scrape(url % sensor_id)
    soup = bs(html)
    hour = int(soup.data['hour'])

    try:
        [last] = scraperwiki.sqlite.select('date, hour from data where sensor_id=? order by date desc, hour desc limit 1', sensor_id)
    except:
        print 'wait, what?'
    else:
        year, month, day =  map(int, last['date'].split('-'))
        print datetime(year, month, day, int(last['hour']))

    for cars, speed in zip(soup.left.fetch('dot'), soup.right.fetch('dot')):
        
        row = {
               'sensor_id': sensor_id, 'timestamp': timestamp,
               'car_count': cars['values'], 'avg_speed': speed['values'],
               'date': 1, 'hour': 2
              }
        data.append(row)
        hour -= 1

    scraperwiki.sqlite.save(unique_keys=['sensor_id', 'date', 'hour'], data=data, table_name='data')

    break;
    
    time.sleep(1/2)
