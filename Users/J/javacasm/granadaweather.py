###############################################################################
# Based in Jaime de Aquino's Scraper
# Weather Granada - Hourly
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://www.eltiempo.es/granada.html?v=por_hora'
html = scraperwiki.scrape(starting_url)
#print html
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
trs = soup.findAll("tr")
i = 0
for tr in trs:
    trGood = tr.find("td", { "class" : "hour" })
    if trGood:
        record = {
                'n': None,
                'time': None,
                'weather': None,
                'temp': None,
                'windDirection': None,
                'precipitation': None,
                'cloudiness': None,
                'thunderProbability': None,
                'relativeMoist': None,
                'airPressure': None
            }
        #print tr
        tdTime = tr.find("td", { "class" : "hour" }) 
        tdWeather = tr.find("td", { "class" : "weather" })
        tdTemp = tr.find("td", { "class" : "temp" })
        tdWindDir = tr.find("td", { "class" : "wind-direction" })
        tdPrecip = tr.find("td", { "class" : "precipitation" })
        tdCloud = tr.find("td", { "class" : "cloudiness" })
        tdThunder = tr.find("td", { "class" : "thunder-probability" })
        tdRelative = tr.find("td", { "class" : "relative-moist" })
        tdAir = tr.find("td", { "class" : "air-pressure" })

        record['n'] = i
        
        try:
            record['time'] = tdTime.text
        except Exception: 
            pass
        try:
            record['weather'] = tdWeather.find("div")['title']
        except Exception: 
            pass
        try:
            record['temp'] = tdTemp.text
        except Exception: 
            pass
        try:
            record['windDirection'] = tdWindDir.find("div")['title']
        except Exception: 
            pass
        try:
            record['precipitation'] = tdPrecip.text
        except Exception: 
            pass
        try:
            record['cloudiness'] = tdCloud.text
        except Exception: 
            pass
        try:
            record['thunderProbability'] = tdThunder.text
        except Exception: 
            pass
        try:
            record['relativeMoist'] = tdRelative.text
        except Exception: 
            pass
        try:
            record['airPressure'] = tdAir.text
        except Exception: 
            pass
        

        #print record
        scraperwiki.sqlite.save(["n"], record)
        i = i + 1
###############################################################################
# Based in Jaime de Aquino's Scraper
# Weather Granada - Hourly
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://www.eltiempo.es/granada.html?v=por_hora'
html = scraperwiki.scrape(starting_url)
#print html
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
trs = soup.findAll("tr")
i = 0
for tr in trs:
    trGood = tr.find("td", { "class" : "hour" })
    if trGood:
        record = {
                'n': None,
                'time': None,
                'weather': None,
                'temp': None,
                'windDirection': None,
                'precipitation': None,
                'cloudiness': None,
                'thunderProbability': None,
                'relativeMoist': None,
                'airPressure': None
            }
        #print tr
        tdTime = tr.find("td", { "class" : "hour" }) 
        tdWeather = tr.find("td", { "class" : "weather" })
        tdTemp = tr.find("td", { "class" : "temp" })
        tdWindDir = tr.find("td", { "class" : "wind-direction" })
        tdPrecip = tr.find("td", { "class" : "precipitation" })
        tdCloud = tr.find("td", { "class" : "cloudiness" })
        tdThunder = tr.find("td", { "class" : "thunder-probability" })
        tdRelative = tr.find("td", { "class" : "relative-moist" })
        tdAir = tr.find("td", { "class" : "air-pressure" })

        record['n'] = i
        
        try:
            record['time'] = tdTime.text
        except Exception: 
            pass
        try:
            record['weather'] = tdWeather.find("div")['title']
        except Exception: 
            pass
        try:
            record['temp'] = tdTemp.text
        except Exception: 
            pass
        try:
            record['windDirection'] = tdWindDir.find("div")['title']
        except Exception: 
            pass
        try:
            record['precipitation'] = tdPrecip.text
        except Exception: 
            pass
        try:
            record['cloudiness'] = tdCloud.text
        except Exception: 
            pass
        try:
            record['thunderProbability'] = tdThunder.text
        except Exception: 
            pass
        try:
            record['relativeMoist'] = tdRelative.text
        except Exception: 
            pass
        try:
            record['airPressure'] = tdAir.text
        except Exception: 
            pass
        

        #print record
        scraperwiki.sqlite.save(["n"], record)
        i = i + 1
