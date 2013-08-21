import scraperwiki
from BeautifulSoup import BeautifulSoup
from datetime import datetime

#settings
date_time_pattern = "%I.%M%p %A %d %B %Y"
keys = ['opening',]

# retrieve a the bridge page
starting_url = 'http://www.gateshead.gov.uk/Leisure%20and%20Culture/attractions/bridge/Home.aspx'
html = scraperwiki.scrape(starting_url)

soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags in the table containing this month's times
# there's no id on the table, so we have to assume there is only one on the page
tables = soup.findAll('table')

if len(tables) == 0:
    raise RuntimeError("No table found listing opening times, page design changed?")
    
elif len(tables) > 1:
    raise RuntimeError("More than one table found in HTML, page design changed?")   

else:
    
    #get the month
    year_month = tables[0].find('caption').string.strip()
    
    for tr in tables[0].findAll('tr'):
        tds = tr.findAll('td')

        day = tds[0].string.strip().rstrip('st').rstrip('nd').rstrip('rd').rstrip('th')
        first_time =  tds[1].string.strip()
        second_time = tds[2].string.strip()

        if first_time != '':
            #convert the date to a proper datetime object
            string_of_opening_1 = first_time + ' ' + day + ' ' + year_month
            datetime_of_opening_1 = datetime.strptime(string_of_opening_1, "%I.%M%p %A %d %B %Y")
        
            #save the first time (string on date and datetime object)
            scraperwiki.datastore.save(keys, {'opening': datetime_of_opening_1, 'date': string_of_opening_1}) 


        if second_time != '':
            #convert the date to a proper datetime object
            string_of_opening_2 = second_time + ' ' + day + ' ' + year_month
            datetime_of_opening_2 = datetime.strptime(string_of_opening_1, "%I.%M%p %A %d %B %Y")
        
            #save the first time (string on date and datetime object)
            scraperwiki.datastore.save(keys, {'opening': datetime_of_opening_2, 'date': string_of_opening_2})         
