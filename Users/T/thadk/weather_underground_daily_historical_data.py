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

startt = datetime.fromtimestamp(1302930687)
endt = datetime.fromtimestamp(1308029504)
current = startt
while (current <= endt):
    print current
    getHistoricalData("KMASOMER8", current.timetuple()[0], current.timetuple()[1], current.timetuple()[2])
    current = current+timedelta(1)

getHistoricalData("KMASOMER8", 2011, 3, 17)
getHistoricalData("KMASOMER8", 2011, 3, 18)