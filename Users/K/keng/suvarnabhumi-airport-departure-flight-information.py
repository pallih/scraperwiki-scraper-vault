#Suvarnabhumi Airport Departure Flight Information

import scraperwiki
from BeautifulSoup import BeautifulSoup

def scrape_table(soup):
    time_tables = soup.findAll("table", { "class" : "txt_tahoma_12" })
    record = {}

    for time_table in time_tables:
        flight_info = time_table.findAll("td")
        if flight_info and len(flight_info) >= 7:
            record['Time'] = flight_info[0].text
            record['Flight'] = flight_info[1].text
            record['Destination'] = flight_info[2].text
            record['Airline'] = flight_info[3].text
            record['Gate'] = flight_info[7].text
            record['Status'] = flight_info[8].text.replace("&nbsp;", "")
            
            #print record, '------------'
            scraperwiki.sqlite.save(["Flight"], record)

html = scraperwiki.scrape('http://www.suvarnabhumiairport.com/flight_schedule_passenger_departure_en.php')
soup = BeautifulSoup(html)

scrape_table(soup)
#Suvarnabhumi Airport Departure Flight Information

import scraperwiki
from BeautifulSoup import BeautifulSoup

def scrape_table(soup):
    time_tables = soup.findAll("table", { "class" : "txt_tahoma_12" })
    record = {}

    for time_table in time_tables:
        flight_info = time_table.findAll("td")
        if flight_info and len(flight_info) >= 7:
            record['Time'] = flight_info[0].text
            record['Flight'] = flight_info[1].text
            record['Destination'] = flight_info[2].text
            record['Airline'] = flight_info[3].text
            record['Gate'] = flight_info[7].text
            record['Status'] = flight_info[8].text.replace("&nbsp;", "")
            
            #print record, '------------'
            scraperwiki.sqlite.save(["Flight"], record)

html = scraperwiki.scrape('http://www.suvarnabhumiairport.com/flight_schedule_passenger_departure_en.php')
soup = BeautifulSoup(html)

scrape_table(soup)
