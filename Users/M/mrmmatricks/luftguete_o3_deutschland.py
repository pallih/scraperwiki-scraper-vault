import scraperwiki 
import datetime         
stations = scraperwiki.scrape("http://www.env-it.de/stationen/public/download.do?event=euMetaStation")
stationParameters = scraperwiki.scrape("http://www.env-it.de/stationen/public/download.do?event=euMetaStationparameter")


def toFraction(position):
    parts1 = position.split(u"\xb0")
    degree = float(parts1[0])
    parts2 = parts1[1].split(u"'")
    degree += float(parts2[0]) / 60
    parts3 = parts2[1].split(u'"') 
    degree += float(parts3[0]) / (60 * 60)
    return degree


def addArea(areaCode):
    now = datetime.datetime.now()
    datestr = datetime.datetime.now().strftime('%G%m%d') 
    print datestr 
    url ='http://www.env-it.de/luftdaten/statedata.csv?comp=O3&version=v1&type=1SMW&date=' + datestr + '&time=900&state=' + areaCode
    print url
    areaCSV = scraperwiki.scrape(url)
    areaData = {}
    
    areaCSV = areaCSV.partition("\n")[2]
    reader = csv.reader(areaCSV.splitlines(),delimiter=';') 
    for row in reader: 
        areaData[row[0]] = row[2]
    areas[areaCode] = areaData


stations = stations.partition("\n")[2]
stationParameters = stationParameters.partition("\n")[2]
import csv           

areas = {}
reader = csv.DictReader(stationParameters.splitlines(),delimiter=';') 
#print reader.next()['component_code']
towerIDList = []
i = 0
for row in reader:           
    if row['parameter'] == 'Ozone':
        towerIDList.append(row['station_code'])
        i = i+1
print towerIDList

towers = {}
reader = csv.DictReader(stations .splitlines(),delimiter=';') 
for row in reader:           
    if towerIDList.count(row['station_code']) > 0 and row['station_end_date'] == '':
        areacode = row['station_code'][2:4]
        if areas.keys().count(areacode) == 0:
            addArea(areacode)

        if areas[areacode].keys().count(row['station_code']) == 0:
            continue
        unicodeName = unicode(row['station_name'], errors='replace')
        data = {
            'id' : row['station_code'],
            'name' : unicodeName  ,
            'ozon1h' : areas[areacode][row['station_code']],
            'lon' : row['station_longitude_d'],
            'lat' : row['station_latitude_d']
        }
        scraperwiki.sqlite.save(unique_keys=['id'], data=data)
        towers[row['station_code']] = data

print len(towers.keys())
                
            
