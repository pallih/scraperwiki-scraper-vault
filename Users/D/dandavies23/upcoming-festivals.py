import scraperwiki
from BeautifulSoup import BeautifulSoup
import re
# scraperwiki.cache(True)  # can be used during development

html = scraperwiki.scrape('http://www.ents24.com/web/festivalguide.html?tab=all')

soup = BeautifulSoup(html)
trs = soup.findAll('tr')



for tr in trs:
    tds = tr.findAll('td')
    if len(tds) == 3:
        record = {}
        record['date'] = tds[0].text
        #print eventname summary
        record['status'] = 'Tickets for sale'  # this sets the default
        if tds[1].find('span', {'class': 'alert'}): # this finds an exception
            status = tds[1].find('span', {'class': 'alert'}).text
            record['status'] = status
        record['name'] = tds[1].find('span', {'class': 'eventname summary'}).text 
        #record['locality'] = tds[2].text
        locality = tds[2].find('span', {'class': 'locality'}).text
        record['locality'] = locality
        latlng = tds[2].find('abbr', {'class': 'geo adr'})['title']
        # split latlng at the semi-colon to make separate latitude & longitude fields (python function split())
        latlng_array = re.split(';', latlng)
        record['lat'] = latlng_array[0]
        record['lng'] = latlng_array[1]
        # record['lat'] = ...
        print record
        scraperwiki.datastore.save(["date"], record)               
              
# for tr in trs:
#     record = { "tr" : tr.text } # column name and value
#     scraperwiki.datastore.save(["tr"], record) # save the records one by one THIS WORKED!
              
# for abbr in trs[0].findall('date'):
#     record['date'] = date.text
#     print record ['date'] 
      
# if tds = tr.findAll

             
                  

# WHAT I WANT TO DO 
# <tr class="vevent event_style row0"> - make it recognise this table and rows starting here DONE
# Group according to <td class="date"> DONE
# Pull out name <span class="eventname summary">Larmer Tree Festival<br /></span> DONE -
# Pull <span class="locality">  DONE              
# If present pull out any alerts: <span class="alert">CANCELLED</span><br /> DONE
# change ENTS weblink by mashing with another table that has official websites on Wikipedia - Might try Google Q instead
# Get Geo location featured in <abbr class="geo adr" title="50.969872;-2.063424"> GOT
# output to CSV
# Plot it on a map!
      import scraperwiki
from BeautifulSoup import BeautifulSoup
import re
# scraperwiki.cache(True)  # can be used during development

html = scraperwiki.scrape('http://www.ents24.com/web/festivalguide.html?tab=all')

soup = BeautifulSoup(html)
trs = soup.findAll('tr')



for tr in trs:
    tds = tr.findAll('td')
    if len(tds) == 3:
        record = {}
        record['date'] = tds[0].text
        #print eventname summary
        record['status'] = 'Tickets for sale'  # this sets the default
        if tds[1].find('span', {'class': 'alert'}): # this finds an exception
            status = tds[1].find('span', {'class': 'alert'}).text
            record['status'] = status
        record['name'] = tds[1].find('span', {'class': 'eventname summary'}).text 
        #record['locality'] = tds[2].text
        locality = tds[2].find('span', {'class': 'locality'}).text
        record['locality'] = locality
        latlng = tds[2].find('abbr', {'class': 'geo adr'})['title']
        # split latlng at the semi-colon to make separate latitude & longitude fields (python function split())
        latlng_array = re.split(';', latlng)
        record['lat'] = latlng_array[0]
        record['lng'] = latlng_array[1]
        # record['lat'] = ...
        print record
        scraperwiki.datastore.save(["date"], record)               
              
# for tr in trs:
#     record = { "tr" : tr.text } # column name and value
#     scraperwiki.datastore.save(["tr"], record) # save the records one by one THIS WORKED!
              
# for abbr in trs[0].findall('date'):
#     record['date'] = date.text
#     print record ['date'] 
      
# if tds = tr.findAll

             
                  

# WHAT I WANT TO DO 
# <tr class="vevent event_style row0"> - make it recognise this table and rows starting here DONE
# Group according to <td class="date"> DONE
# Pull out name <span class="eventname summary">Larmer Tree Festival<br /></span> DONE -
# Pull <span class="locality">  DONE              
# If present pull out any alerts: <span class="alert">CANCELLED</span><br /> DONE
# change ENTS weblink by mashing with another table that has official websites on Wikipedia - Might try Google Q instead
# Get Geo location featured in <abbr class="geo adr" title="50.969872;-2.063424"> GOT
# output to CSV
# Plot it on a map!
      