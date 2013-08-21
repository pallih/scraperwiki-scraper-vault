import scraperwiki
import lxml.html
import datetime
from datetime import date
year = date.today().year

country = 'India'
city = 'Bengaluru'
region = 'None' 

url = "http://spaceflight.nasa.gov/realdata/sightings/cities/view.cgi?country=%s&region=%s&city=%s" % (country,region,city)



html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)

table = root.cssselect('table') 

listing_table = table[4]

#print lxml.html.tostring(listing_table)

trs = listing_table.cssselect('tr')

for tr in trs:
    tds = tr.cssselect('td') 
    if tds[0].text_content() == "ISS":
        print tds[1].text_content()
        dateStr = tds[1].text_content() + " " +str(year)
        my_datetime =  datetime.datetime.strptime(dateStr, '%a %b %d/%I:%M %p %Y')
        scraperwiki.sqlite.save(unique_keys=["datetime"], data={"datetime":my_datetime, "satellite":tds[0].text_content(), "duration":tds[2].text_content(), "max_elevation":tds[3].text_content(), "approach":tds[4].text_content(),"departure":tds[5].text_content()})





