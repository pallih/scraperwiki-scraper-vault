##This is going to work
import scraperwiki  

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

getHistoricalData("KCOCOLOR12", 2011, 7, 16)
getHistoricalData("KCOCOLOR12", 2011, 7, 15)
getHistoricalData("KCOCOLOR12", 2011, 7, 14)