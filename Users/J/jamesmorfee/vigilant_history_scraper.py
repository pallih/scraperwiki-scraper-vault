import scraperwiki
import lxml.html

lastday = 0
page_number = 1
max_page_number = 1
MMSI = "311963000"
web_address = "http://www.marinetraffic.com/ais/datasheet.aspx?MMSI=" + MMSI + "&TIMESTAMP=1&menuid=&datasource=POS&app=&mode=&B1=Search&orderby=TIMESTAMP&sort_order=DESC&var_page="

def gethtml(web_location): #scrape the webpage and return parsed data
    html = scraperwiki.scrape(web_location)
    root = lxml.html.fromstring(html)
    return root

def getpn(root): #get the number of pages of data available, return int
    el = root.cssselect("div#datasheet b")
    pagestring = el[0].text_content()
    max_page_number = int(pagestring.split("/")[1])
    return max_page_number

def store_data(latlong, timestampstr): #format data and store
    latitude = latlong.split()[0]
    longitude = latlong.split()[1]
    if latitude.startswith('-'): #format the latlong from + and - to N,S,E and W
        latitude = latitude.strip('-') + "S"
    else:
        latitude = latitude + "N"
    if longitude.startswith('-'):
        longitude = longitude.strip('-') + "W"
    else:
        longitude = longitude + "E"
    data = { #setup the data object
        'timestamp' : timestampstr,
        'position' : latitude + " " + longitude
        }
    scraperwiki.sqlite.save(unique_keys=['timestamp'], data=data) #store it!
    return
while page_number < max_page_number + 1: #while we still have a valid page
    root = gethtml(web_address + str(page_number)) #get the page
    if page_number == 1:
        max_page_number = getpn(root) #get the maximum number of pages
    for tr in root.cssselect("div#datasheet tr"):
        tds = tr.cssselect("td")
        if tds[0].text_content() != "MMSI": #ignore first line
            latlong = tds[2].text_content()
            timestampstr = tds[4].text_content()
            day = int(timestampstr[8:10]) #get the day in the timestamp
            if lastday > day: #check for cahnge
                store_data(old_latlong, old_timestampstr)
            lastday = day
            old_latlong = latlong
            old_timestampstr = timestampstr
    page_number = page_number + 1
print str(page_number - 1) + " of " + str(max_page_number) + " scraped"
import scraperwiki
import lxml.html

lastday = 0
page_number = 1
max_page_number = 1
MMSI = "311963000"
web_address = "http://www.marinetraffic.com/ais/datasheet.aspx?MMSI=" + MMSI + "&TIMESTAMP=1&menuid=&datasource=POS&app=&mode=&B1=Search&orderby=TIMESTAMP&sort_order=DESC&var_page="

def gethtml(web_location): #scrape the webpage and return parsed data
    html = scraperwiki.scrape(web_location)
    root = lxml.html.fromstring(html)
    return root

def getpn(root): #get the number of pages of data available, return int
    el = root.cssselect("div#datasheet b")
    pagestring = el[0].text_content()
    max_page_number = int(pagestring.split("/")[1])
    return max_page_number

def store_data(latlong, timestampstr): #format data and store
    latitude = latlong.split()[0]
    longitude = latlong.split()[1]
    if latitude.startswith('-'): #format the latlong from + and - to N,S,E and W
        latitude = latitude.strip('-') + "S"
    else:
        latitude = latitude + "N"
    if longitude.startswith('-'):
        longitude = longitude.strip('-') + "W"
    else:
        longitude = longitude + "E"
    data = { #setup the data object
        'timestamp' : timestampstr,
        'position' : latitude + " " + longitude
        }
    scraperwiki.sqlite.save(unique_keys=['timestamp'], data=data) #store it!
    return
while page_number < max_page_number + 1: #while we still have a valid page
    root = gethtml(web_address + str(page_number)) #get the page
    if page_number == 1:
        max_page_number = getpn(root) #get the maximum number of pages
    for tr in root.cssselect("div#datasheet tr"):
        tds = tr.cssselect("td")
        if tds[0].text_content() != "MMSI": #ignore first line
            latlong = tds[2].text_content()
            timestampstr = tds[4].text_content()
            day = int(timestampstr[8:10]) #get the day in the timestamp
            if lastday > day: #check for cahnge
                store_data(old_latlong, old_timestampstr)
            lastday = day
            old_latlong = latlong
            old_timestampstr = timestampstr
    page_number = page_number + 1
print str(page_number - 1) + " of " + str(max_page_number) + " scraped"
