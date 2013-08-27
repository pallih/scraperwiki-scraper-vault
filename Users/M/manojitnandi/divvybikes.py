import scraperwiki
import pandas as pd
import json

url = "http://divvybikes.com/stations/json"
response = json.loads(scraperwiki.scrape(url))
executionTime, stationList = response.values()
date,time = executionTime[:10], executionTime[11:]
for station in stationList:
    data_values = {"Date":date,"Time":time}
    for key,value in station.iteritems():
        data_values[key] = value
    scraperwiki.sqlite.save(unique_keys=["id"], data = data_values)
import scraperwiki
import pandas as pd
import json

url = "http://divvybikes.com/stations/json"
response = json.loads(scraperwiki.scrape(url))
executionTime, stationList = response.values()
date,time = executionTime[:10], executionTime[11:]
for station in stationList:
    data_values = {"Date":date,"Time":time}
    for key,value in station.iteritems():
        data_values[key] = value
    scraperwiki.sqlite.save(unique_keys=["id"], data = data_values)
import scraperwiki
import pandas as pd
import json

url = "http://divvybikes.com/stations/json"
response = json.loads(scraperwiki.scrape(url))
executionTime, stationList = response.values()
date,time = executionTime[:10], executionTime[11:]
for station in stationList:
    data_values = {"Date":date,"Time":time}
    for key,value in station.iteritems():
        data_values[key] = value
    scraperwiki.sqlite.save(unique_keys=["id"], data = data_values)
