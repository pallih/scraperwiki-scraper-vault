import scraperwiki
import BeautifulSoup
import re
from datetime import datetime

from scraperwiki import datastore

# Hello World Example #

#scrape page
html = scraperwiki.scrape('http://www.direct.gov.uk/en/Governmentcitizensandrights/LivingintheUK/DG_073741')
page = BeautifulSoup.BeautifulSoup(html)

#find rows
for table in page.findAll('table', { 'class':'markuptable' } ):

    rows = table.findAll('tr')[:-2]
    country = rows[0].th.string

    years = [cell.string.strip()
             for cell in rows[0].findAll('th')[1:]]
    
    # Confirm correct parsing
    print years
    
    for row in rows[1:]:
        holiday_name = row.td.string
        for cell, year in zip(row.findAll('td')[1:], years):
            #save to datastore
            cell = re.sub('(\d+)',r'\1 ', cell.string.strip().replace('*','').strip())
            if cell == '-':
                continue
            
            date_str = cell + " " + year
            # Remove non-breaking spaces (\xa0), and join up with single spaces
            date_str = ' '.join(date_str.split())
            print repr(date_str)
            
            #convert date to date object
            date_of_holiday = datetime.strptime(date_str, "%d %B %Y")
            print date_of_holiday

            
            #save to datastore
            data = { 'country' : country, 'date' : date_of_holiday, 'holiday_name' : holiday_name}
            datastore.save(unique_keys=['country','date'], data=data, date=date_of_holiday)

