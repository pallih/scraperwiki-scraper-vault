import scraperwiki
import BeautifulSoup
import re
import datetime

from scraperwiki import datastore
from datetime import datetime

WARDS = {"Ainsdale": "G+", "Birkdale": "F+", "Blundellsands": "P+", "Cambridge": "A+", "Church": "S+",
         "Derby": "Z+", "Dukes": "B+", "Ford": "O+", "Harington": "H+", "Kew": "E+", "Linacre": "Y+",
         "Litherland": "N+", "Manor": "R+", "Meols": "C+", "Molyneux": "M+", "Netherton & Orrell": "W+",
         "Norwood": "D+", "Park": "K+", "Ravenmeols": "J+", "St Oswald": "V+", "Sudell": "L+", "Victoria": "T+"}

def Main():
    year = datetime.today().year
    #ScrapeWard(WARDS["Ainsdale"], year)
    for ward_id in WARDS.values():
        ScrapeWard(ward_id, year)
    
def ScrapeWard(ward_id, year):
    url_format_string = "http://breathingspace.sefton.gov.uk/Default.aspx?bsPage=road_safety&option=4&step=2&WardId={0}&StartMonth=1&StartYear={1}&EndMonth=12&EndYear={1}"
    url = str.format(url_format_string, ward_id, year)
    html = scraperwiki.scrape(url)
    page = BeautifulSoup.BeautifulSoup(html)
    table = page.findAll('table', {'class': 'Grid'})[1]
    for row in table.findAll('tr')[1:]:
        cells = row.findAll('td')
        time = ExtractTime(cells[0].string, cells[1].string)
        location_description = cells[2].string
        latlng = ConvertLocationToLatLng(cells[3].string)
        details_url = 'http://breathingspace.sefton.gov.uk/' + cells[4].find('a')['href']
        data = {"date": time, "location_description": location_description, "url": details_url }
        data.update(ScrapeAccidentDetails(details_url))        
        datastore.save(unique_keys = ['date', 'location_description'], latlng = latlng, data = data)

def ExtractTime(date, time):
    date_match = re.match('(\d{2})-(\d{2})-(\d{4})', date.string)
    time_match = re.match('(\d{1,2}):00', time.string)
    return datetime(int(date_match.group(3)), int(date_match.group(2)), int(date_match.group(1)), int(time_match.group(1)))
     
def ConvertLocationToLatLng(easting_northing):
    easting, northing = easting_northing.split('/')
    latlng = scraperwiki.geo.os_easting_northing_to_latlng(int(easting), int(northing))
    return (latlng[0], latlng[1])
        
def ScrapeAccidentDetails(details_url):
    html = scraperwiki.scrape(details_url)
    page = BeautifulSoup.BeautifulSoup(html)
    casualty_details_table = page.findAll('table', {'class': 'Grid'})[1]
    casualty_details = BuildFullAccidentDetails(casualty_details_table)
    details = page.find('h3').string
    match = re.match('Collision Details \(Vehicles Involved: (\d+), Casualties: (\d+)\)', details)
    return {"vehicles_involved": match.group(1), "casualties": match.group(2), "casualty_details": casualty_details}

def BuildFullAccidentDetails(casualties_table):
    "An accident can have many casualties so I have to build up a string of all of them and put it in a single field."
    casualty_details = []
    for casualty_row in casualties_table.findAll('tr')[1:]:
        casualty = casualty_row.findAll('td')
        user_class = casualty[0].string.rstrip(' ') # this string has a trailing space
        vehicle_type = casualty[1].string
        age_class = casualty[2].string
        level_of_injury = casualty[3].string
        casualty_details.append(str.format("Vehicle: {0} - Injury: {1} - {2} {3}", vehicle_type, level_of_injury, age_class, user_class))
    return ', '.join(casualty_details)
        
Main()
import scraperwiki
import BeautifulSoup
import re
import datetime

from scraperwiki import datastore
from datetime import datetime

WARDS = {"Ainsdale": "G+", "Birkdale": "F+", "Blundellsands": "P+", "Cambridge": "A+", "Church": "S+",
         "Derby": "Z+", "Dukes": "B+", "Ford": "O+", "Harington": "H+", "Kew": "E+", "Linacre": "Y+",
         "Litherland": "N+", "Manor": "R+", "Meols": "C+", "Molyneux": "M+", "Netherton & Orrell": "W+",
         "Norwood": "D+", "Park": "K+", "Ravenmeols": "J+", "St Oswald": "V+", "Sudell": "L+", "Victoria": "T+"}

def Main():
    year = datetime.today().year
    #ScrapeWard(WARDS["Ainsdale"], year)
    for ward_id in WARDS.values():
        ScrapeWard(ward_id, year)
    
def ScrapeWard(ward_id, year):
    url_format_string = "http://breathingspace.sefton.gov.uk/Default.aspx?bsPage=road_safety&option=4&step=2&WardId={0}&StartMonth=1&StartYear={1}&EndMonth=12&EndYear={1}"
    url = str.format(url_format_string, ward_id, year)
    html = scraperwiki.scrape(url)
    page = BeautifulSoup.BeautifulSoup(html)
    table = page.findAll('table', {'class': 'Grid'})[1]
    for row in table.findAll('tr')[1:]:
        cells = row.findAll('td')
        time = ExtractTime(cells[0].string, cells[1].string)
        location_description = cells[2].string
        latlng = ConvertLocationToLatLng(cells[3].string)
        details_url = 'http://breathingspace.sefton.gov.uk/' + cells[4].find('a')['href']
        data = {"date": time, "location_description": location_description, "url": details_url }
        data.update(ScrapeAccidentDetails(details_url))        
        datastore.save(unique_keys = ['date', 'location_description'], latlng = latlng, data = data)

def ExtractTime(date, time):
    date_match = re.match('(\d{2})-(\d{2})-(\d{4})', date.string)
    time_match = re.match('(\d{1,2}):00', time.string)
    return datetime(int(date_match.group(3)), int(date_match.group(2)), int(date_match.group(1)), int(time_match.group(1)))
     
def ConvertLocationToLatLng(easting_northing):
    easting, northing = easting_northing.split('/')
    latlng = scraperwiki.geo.os_easting_northing_to_latlng(int(easting), int(northing))
    return (latlng[0], latlng[1])
        
def ScrapeAccidentDetails(details_url):
    html = scraperwiki.scrape(details_url)
    page = BeautifulSoup.BeautifulSoup(html)
    casualty_details_table = page.findAll('table', {'class': 'Grid'})[1]
    casualty_details = BuildFullAccidentDetails(casualty_details_table)
    details = page.find('h3').string
    match = re.match('Collision Details \(Vehicles Involved: (\d+), Casualties: (\d+)\)', details)
    return {"vehicles_involved": match.group(1), "casualties": match.group(2), "casualty_details": casualty_details}

def BuildFullAccidentDetails(casualties_table):
    "An accident can have many casualties so I have to build up a string of all of them and put it in a single field."
    casualty_details = []
    for casualty_row in casualties_table.findAll('tr')[1:]:
        casualty = casualty_row.findAll('td')
        user_class = casualty[0].string.rstrip(' ') # this string has a trailing space
        vehicle_type = casualty[1].string
        age_class = casualty[2].string
        level_of_injury = casualty[3].string
        casualty_details.append(str.format("Vehicle: {0} - Injury: {1} - {2} {3}", vehicle_type, level_of_injury, age_class, user_class))
    return ', '.join(casualty_details)
        
Main()
