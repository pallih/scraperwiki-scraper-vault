import scraperwiki
import BeautifulSoup

from scraperwiki import datastore

# Port of London Arrivals #

#test10
#scrape page
html = scraperwiki.scrape('http://www.pla.co.uk/Ships/index.cfm/site/navigation/flag/2/print/yes')
page = BeautifulSoup.BeautifulSoup(html)

#find vessels
for row in page.find('table').find('table').findAll('tr')[1:]:
    cells = row.findAll('td')
    time = cells[0].string.replace('&nbsp;', '')
    vessel_name = cells[1].string.title()
    vessel_number = cells[2].string    
    country_code = cells[3].string    
    port_from = cells[4].string.title()    
    port_to = cells[5].string.title()        
    
    print "Found a vessel called: " + vessel_name
    
    #save to datastore
    data = {'time' : time,
                'vessel_name' : vessel_name,
                'vessel_number' : vessel_number,           
                'country_code' : country_code,
                'port_from' : port_from,
                'port_to' : port_to,
                }
    
    datastore.save(unique_keys=['time', 'vessel_number'], data=data)



