# Scrapping London headthrow airpot Arrival
import scraperwiki
import datetime as dt
import BeautifulSoup 


# Arrivals
url = "http://www.heathrowairport.com/flight-information/live-flight-arrivals"
html = scraperwiki.scrape(url)
soup = BeautifulSoup.BeautifulSoup(html)
tableFlight = soup.find('table', {"id": "timeTable"})
allTr = tableFlight.findAll('tr')[2:]
for itr in allTr:
    try:
        itd = itr.findAll("td")
        date = itd[0].getText().split(' ')[0]
        timeExpectedLand = itd[0].getText().split(' ')[1][:-5]+":00"
        timeLanded = itd[3].getText()[-5:]+":00"
        isLanded = itd[3].getText()[:-5].rstrip()
        FMT = '%H:%M:%S'
        tdelta = dt.datetime.strptime(timeLanded, FMT) -dt.datetime.strptime(timeExpectedLand, FMT)
        minutesDiff = divmod(tdelta.days * 86400 + tdelta.seconds, 60)[0]
        if minutesDiff>0:
            flightNumber = itd[1].getText()
            comingFrom = itd[2].getText()
            print "delayed minutes:"+str(minutesDiff)+","+flightNumber+","+comingFrom
            data = {"flight-id":flightNumber,"from":comingFrom,"date":date,"expected-Land-time":timeExpectedLand[:-3],"Landed-time":timeLanded[:-3],"delay":minutesDiff}
            scraperwiki.sqlite.save(unique_keys=['flight-id'],data=data)
    except: 
        pass
        
        



