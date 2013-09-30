##This is going to work
import scraperwiki  
from datetime import datetime,timedelta

def getHistoricalData(station, year, month, day):
    url = "http://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID=%s&month=%s&day=%s&year=%s&format=1" % (station, month, day, year) 
    csv = scraperwiki.scrape(url)
    csv = csv.replace("\n", "")

    rowNum = 0
    headers = []
    data = []
    for row in csv.split("<br>")[:-1]:
        columnNum = 0
        data.append({})
        data[rowNum]["station"] = station
        for column in row.split(","):
            if rowNum == 0:
                headers.append(column)
            else:
                if columnNum <= len(headers) - 1:
                    data[rowNum][headers[columnNum]] = column
            columnNum += 1
        rowNum += 1

    scraperwiki.sqlite.save(unique_keys=['station', 'DateUTC'], data=data[1:])

startt = datetime.fromtimestamp(1353646800)
endt = datetime.fromtimestamp(1357016400)
current = startt
while (current <= endt):
    print current
    getHistoricalData("KOHNORTO2", current.timetuple()[0], current.timetuple()[1], current.timetuple()[2])
    current = current+timedelta(1)
##This is going to work
import scraperwiki  
from datetime import datetime,timedelta

def getHistoricalData(station, year, month, day):
    url = "http://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID=%s&month=%s&day=%s&year=%s&format=1" % (station, month, day, year) 
    csv = scraperwiki.scrape(url)
    csv = csv.replace("\n", "")

    rowNum = 0
    headers = []
    data = []
    for row in csv.split("<br>")[:-1]:
        columnNum = 0
        data.append({})
        data[rowNum]["station"] = station
        for column in row.split(","):
            if rowNum == 0:
                headers.append(column)
            else:
                if columnNum <= len(headers) - 1:
                    data[rowNum][headers[columnNum]] = column
            columnNum += 1
        rowNum += 1

    scraperwiki.sqlite.save(unique_keys=['station', 'DateUTC'], data=data[1:])

startt = datetime.fromtimestamp(1353646800)
endt = datetime.fromtimestamp(1357016400)
current = startt
while (current <= endt):
    print current
    getHistoricalData("KOHNORTO2", current.timetuple()[0], current.timetuple()[1], current.timetuple()[2])
    current = current+timedelta(1)
