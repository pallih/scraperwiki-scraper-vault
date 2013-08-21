import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re
import datetime

# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['Time', 'Temperature', 'When'])


url = "http://www.weather.com/weather/today/USCA0993"

def num_only(temp):
    return re.sub("\D", "", temp)

def Main():
    root = lxml.html.parse(url).getroot()

    # Get the objects
    whens = root.cssselect('td.twc-forecast-when')
    temps = root.cssselect('td.twc-forecast-temperature')

    # Weather forecast has four times.  Now and 3 in the future.
    right_now = ['Right Now']
    whens = [when.text_content() for when in whens]
    times = right_now + whens

    # Four different temperatures
    temps = [num_only(temp.text_content()) for temp in temps]
    add_one_record(temps)

def add_one_record(temps):
    record = {'Temperature': temps[0], 'When': None, 'Time': datetime.datetime.now()}
    scraperwiki.datastore.save(["Time"], record)

def add_all_records(times, temps):
    record = {}
    i = 0
    while i < len(times):
        record['When'] = times[i]
        record['Temperature'] = temps[i]
        scraperwiki.datastore.save(["When"], record)
        i = i + 1
    
Main()

                        

