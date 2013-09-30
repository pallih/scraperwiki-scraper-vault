"""
This scraper is designed to extract all of the data from the New South Wales
Air Quality Index <http://www.environment.nsw.gov.au/AQMS/aqi.htm>
"""

import dateutil
import random
from time import sleep

import scraperwiki
import lxml.html

ROOT = "http://airquality.environment.nsw.gov.au/aquisnetnswphp/"
START = "http://airquality.environment.nsw.gov.au/aquisnetnswphp/getPage.php?reportid=2"

def get_page(url):
    return lxml.html.parse(url).getroot()

def get_page_rawdata(page):
    data = page.cssselect('table.aqi')[0]
    rows = data.cssselect('tr')
    date = page.cssselect('td.date')[0] 

    region = ''
    for row in rows[2:-4]:
        row = row.text_content().split('\n')
        if len(row) > 10:
            if len(row) == 13:
                region = row[0]
            else:
                row = [region] + row

            if row[1] in row[0]:
                row[0] = row[0].split(' - ')[0]

            yield  dict(region=row[0],
                        suburb=row[1],
                        ozone_1h_hour_average=row[2],
                        ozone_h4_average=row[3],
                        nitrous_dioxide_1h_average=row[4],
                        nitrous_dioxide_4h_average=row[5],
                        visibility_1h_average=row[6],
                        carbon_monoxide_rolling_8h_average=row[7],
                        sulphur_dioxide_1h_average=row[8],
                        particles_PM10_rolling_24h_average=row[8],
                        particles_PM25_rolling_24h_average=row[9],
                        date = ', '.join([date.text, date[0].tail, date[1].tail]))

def next_page(page):
    for link in page.iterlinks():
        if 'previous' in link[2]:
            return ROOT + link[2]

def main():
    url = START
    while 1:
        page = get_page(url)
        for row in get_page_rawdata(page):
            scraperwiki.sqlite.save(['date', 'region', 'suburb'], row)
        next = next_page(page)
        if next:
            url = next
        else:
            break

main()
    
"""
This scraper is designed to extract all of the data from the New South Wales
Air Quality Index <http://www.environment.nsw.gov.au/AQMS/aqi.htm>
"""

import dateutil
import random
from time import sleep

import scraperwiki
import lxml.html

ROOT = "http://airquality.environment.nsw.gov.au/aquisnetnswphp/"
START = "http://airquality.environment.nsw.gov.au/aquisnetnswphp/getPage.php?reportid=2"

def get_page(url):
    return lxml.html.parse(url).getroot()

def get_page_rawdata(page):
    data = page.cssselect('table.aqi')[0]
    rows = data.cssselect('tr')
    date = page.cssselect('td.date')[0] 

    region = ''
    for row in rows[2:-4]:
        row = row.text_content().split('\n')
        if len(row) > 10:
            if len(row) == 13:
                region = row[0]
            else:
                row = [region] + row

            if row[1] in row[0]:
                row[0] = row[0].split(' - ')[0]

            yield  dict(region=row[0],
                        suburb=row[1],
                        ozone_1h_hour_average=row[2],
                        ozone_h4_average=row[3],
                        nitrous_dioxide_1h_average=row[4],
                        nitrous_dioxide_4h_average=row[5],
                        visibility_1h_average=row[6],
                        carbon_monoxide_rolling_8h_average=row[7],
                        sulphur_dioxide_1h_average=row[8],
                        particles_PM10_rolling_24h_average=row[8],
                        particles_PM25_rolling_24h_average=row[9],
                        date = ', '.join([date.text, date[0].tail, date[1].tail]))

def next_page(page):
    for link in page.iterlinks():
        if 'previous' in link[2]:
            return ROOT + link[2]

def main():
    url = START
    while 1:
        page = get_page(url)
        for row in get_page_rawdata(page):
            scraperwiki.sqlite.save(['date', 'region', 'suburb'], row)
        next = next_page(page)
        if next:
            url = next
        else:
            break

main()
    
