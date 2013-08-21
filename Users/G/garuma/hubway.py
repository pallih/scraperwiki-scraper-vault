import scraperwiki
import requests
from bs4 import BeautifulSoup

hubway_url = "http://thehubway.com/data/stations/bikeStations.xml"

content = requests.get(hubway_url)
doc = BeautifulSoup(content.text)

def station_to_dict(station):
    dict = {}
    for e in station:
        dict[str(e.name)] = str(e.string)
    dict['stationtimeid'] = station.id.string + '|' + station.latestupdatetime.string
    return dict

stations = doc.findAll('station')
result = map(station_to_dict, stations)
print result

scraperwiki.sqlite.save(['stationtimeid'], result)
