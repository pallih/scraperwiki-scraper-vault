import scraperwiki
import re
import time
import codecs
import chardet
from scraperwiki.sqlite import save

columns = [
    'Name', 'Address','latlong','Phone'
]

homeurl = "http://www.edu.gov.on.ca/eng/sift/index.asp"
homescrape = scraperwiki.scrape(homeurl)
relevanthomeportion = re.search('129674">Fallingbrook(.+?)<\/select>', homescrape, re.DOTALL|re.S)

for each_school in re.finditer('<option value="(.+?)"', relevanthomeportion.group(1)):
    schoolnumber = each_school.group(1)
    schoolurl = "http://www.edu.gov.on.ca/eng/sift/schoolProfileSec.asp?SCH_NUMBER=" + schoolnumber + "&x=29&y=20"
    schoolscrape = scraperwiki.scrape(schoolurl)
    latlong = "none"
    schoolscrape = schoolscrape.decode('Latin-1').encode('utf-8','replace')
    if re.search('var point = new GLatLng\((.+?)\)', schoolscrape):
        latlong = re.search('var point = new GLatLng\((.+?)\)', schoolscrape)
        latlong = latlong.group(1)
    name = re.search('<h2>(.+?)\(', schoolscrape)
    name = name.group(1)
    address = re.search('<strong>Address:<\/strong>(.+?)<', schoolscrape)
    address = re.sub('&nbsp;', ' ', address.group(1))
    phone = re.search('<strong>Phone Number:<\/strong>(.+?)<', schoolscrape)
    phone = re.sub('&nbsp;', ' ', phone.group(1))
    row_data = {'Name': name, 'Address': address, 'latlong': latlong, 'Phone': phone}
    save([],row_data)
    time.sleep(1)
    import scraperwiki
import re
import time
import codecs
import chardet
from scraperwiki.sqlite import save

columns = [
    'Name', 'Address','latlong','Phone'
]

homeurl = "http://www.edu.gov.on.ca/eng/sift/index.asp"
homescrape = scraperwiki.scrape(homeurl)
relevanthomeportion = re.search('129674">Fallingbrook(.+?)<\/select>', homescrape, re.DOTALL|re.S)

for each_school in re.finditer('<option value="(.+?)"', relevanthomeportion.group(1)):
    schoolnumber = each_school.group(1)
    schoolurl = "http://www.edu.gov.on.ca/eng/sift/schoolProfileSec.asp?SCH_NUMBER=" + schoolnumber + "&x=29&y=20"
    schoolscrape = scraperwiki.scrape(schoolurl)
    latlong = "none"
    schoolscrape = schoolscrape.decode('Latin-1').encode('utf-8','replace')
    if re.search('var point = new GLatLng\((.+?)\)', schoolscrape):
        latlong = re.search('var point = new GLatLng\((.+?)\)', schoolscrape)
        latlong = latlong.group(1)
    name = re.search('<h2>(.+?)\(', schoolscrape)
    name = name.group(1)
    address = re.search('<strong>Address:<\/strong>(.+?)<', schoolscrape)
    address = re.sub('&nbsp;', ' ', address.group(1))
    phone = re.search('<strong>Phone Number:<\/strong>(.+?)<', schoolscrape)
    phone = re.sub('&nbsp;', ' ', phone.group(1))
    row_data = {'Name': name, 'Address': address, 'latlong': latlong, 'Phone': phone}
    save([],row_data)
    time.sleep(1)
    