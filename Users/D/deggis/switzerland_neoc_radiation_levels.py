# Testing parsing from nuclear radiation monitoring site in Switzerland,
# NEOC, National Emergency Operations Centre.
# import scraperwiki
import urllib
import json
import datetime
import scraperwiki

# {u'CH-AG-Beznau': (47.552106999999999, 8.2284919999999993),
# u'CH-AG-Buchs / Aarau': (47.383333, 8.0833329999999997),
# u'CH-BE-Adelboden': (46.5, 7.5666669999999998),
# u'CH-BE-Bern / Zollikofen': (47, 7.4500000000000002),
 #u'CH-BL-Basel / Binningen': (47.533332999999999, 7.5666669999999998),
# u'CH-LU-Egolzwil': (47.183332999999998, 8),
# u'CH-UR-Altdorf': (46.866667, 8.6333330000000004),
# u'CH-VD-Aigle': (46.316667000000002, 6.9666670000000002)}

#measurements_fields = ["radiation REAL", "station_id TEXT", "time TEXT", "PRIMARY KEY (station_id, time)"]
#scraperwiki.sqlite.execute("create table if not exists measurements (%s)" % ",".join(measurements_fields))

# Dataset comes in format of:
#   strDate='18.3.2011';
#   strHeight='400';
#   dataSet = (in JSON)
#   commentSet = [];
dataset_rows = urllib.urlopen("https://www.naz.ch/DAY/dataset_en.js").read().split("\n")
all_entries = json.loads(dataset_rows[2][10:-1])

def strip_vaduz(entry):
    return entry[0].find("Vaduz") == -1
def generate_id(city_str):
    return "CH-"+city_str[-2:]+"-"+city_str[:-3]

switzerland_entries = filter(strip_vaduz, all_entries)

measurements_fields = ["radiation REAL", "station_id TEXT", "time TEXT", "PRIMARY KEY (station_id, time)"]
scraperwiki.sqlite.execute("create table if not exists measurements (%s)" % ",".join(measurements_fields))

time_now = datetime.datetime.utcnow()
for entry in switzerland_entries:
  radiation = int(entry[2].split(" ")[0]) / 10e9 
  station_id = generate_id(entry[0])
  timestr = time_now.strftime("%Y-%m-%dT%H:%M:%S+00:00")
  scraperwiki.sqlite.execute("INSERT into 'measurements' values(?,?,?);",(radiation, station_id, timestr))
  scraperwiki.sqlite.commit()