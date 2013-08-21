##This is going to work
import scraperwiki  
from datetime import datetime,timedelta

def getHistoricalData(station, year, month, day):
    url = "http://www.wunderground.com/wundermap/" % (station, month, day, year) 
    print url
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

startt = datetime.fromtimestamp(1309478400)
print startt
endt = datetime.fromtimestamp(1346284800)
print endt
current = startt
while (current <= endt):
    getHistoricalData("IZZBIRMI2", current.timetuple()[0], current.timetuple()[1], current.timetuple()[2])
    current = current+timedelta(1)

