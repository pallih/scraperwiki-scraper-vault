"""Weather Observation Data collected from http://www.imd.gov.in/section/nhac/dynamic/current.htm
"""

import scraperwiki
import lxml.html
import dateutil.parser

utils = scraperwiki.utils.swimport("utils")
utils.save.unique_keys = ['observed_date', 'station_name']

scraperwiki.sqlite.execute("create index if not exists idx1 on swdata (observed_date, station_name)")


def get_current_weather():
    url = 'http://www.imd.gov.in/section/nhac/dynamic/current.htm'
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    assert 'CURRENT WEATHER OBSERVATIONS' in html

    date = root.xpath("//p[contains(text(), 'Date :')]")[0]
    date = date.text_content().split(':')[1]
    time = root.xpath("//p[contains(text(), 'Time :')]")[0]
    time = time.text_content().split(':')[1].strip()
    time = time[:2] + ':' + time[2:] #insert : after hour
    observed_date = dateutil.parser.parse(date + ' ' + time)

    table = root.cssselect('table')[0]
    rows = table.cssselect('tr')
    del rows[0] # Header
    for row in rows:
        cells = [td.text_content() for td in row]
        rec = dict()
        rec['station_name'] = cells[0]
        rec['temperature_in_celcius'] = cells[1]
        rec['relative_humidity_percentage'] = cells[2]
        rec['mean_sea_level_pressure_in_hpa'] = cells[3].replace('*', '')
        rec['wind_in_kts'] = cells[4]
        rec['weather'] = cells[5]
        rec['observed_date'] = observed_date
        utils.save(rec)


get_current_weather()
"""Weather Observation Data collected from http://www.imd.gov.in/section/nhac/dynamic/current.htm
"""

import scraperwiki
import lxml.html
import dateutil.parser

utils = scraperwiki.utils.swimport("utils")
utils.save.unique_keys = ['observed_date', 'station_name']

scraperwiki.sqlite.execute("create index if not exists idx1 on swdata (observed_date, station_name)")


def get_current_weather():
    url = 'http://www.imd.gov.in/section/nhac/dynamic/current.htm'
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    assert 'CURRENT WEATHER OBSERVATIONS' in html

    date = root.xpath("//p[contains(text(), 'Date :')]")[0]
    date = date.text_content().split(':')[1]
    time = root.xpath("//p[contains(text(), 'Time :')]")[0]
    time = time.text_content().split(':')[1].strip()
    time = time[:2] + ':' + time[2:] #insert : after hour
    observed_date = dateutil.parser.parse(date + ' ' + time)

    table = root.cssselect('table')[0]
    rows = table.cssselect('tr')
    del rows[0] # Header
    for row in rows:
        cells = [td.text_content() for td in row]
        rec = dict()
        rec['station_name'] = cells[0]
        rec['temperature_in_celcius'] = cells[1]
        rec['relative_humidity_percentage'] = cells[2]
        rec['mean_sea_level_pressure_in_hpa'] = cells[3].replace('*', '')
        rec['wind_in_kts'] = cells[4]
        rec['weather'] = cells[5]
        rec['observed_date'] = observed_date
        utils.save(rec)


get_current_weather()
