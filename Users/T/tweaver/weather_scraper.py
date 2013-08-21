import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://www.weather.com/weather/right-now/Denver+CO+80206") ##load site
root = lxml.html.fromstring(html)
for i in root.cssselect("div.wx-cc-wind-data .wx-cc-wind-dir-txt .wx-cc-wind-direction"): ##load css tag to parse
    windDIR = i.text
    print i.text    

for j in root.cssselect(".wx-cc-wind-speed .wx-temp"):
    windSP = j.text
    print j.text
        
for k in root.cssselect(".wx-temp .wx-value"):
    temp = k.text
    print k.text

for m in root.cssselect(".wx-cc-blocks .wx-cc-subblocks .wx-cc-blocks-2 .wx-temp"):
    presS = m.text
    print m.text

for l in root.cssselect(".wx-cc-blocks .wx-cc-blocks-2 [itemprop='humidity']"):
    humiD = l.text
    print l.text

for n in root.cssselect(".wx-timestamp .wx-value"):
    timeS = n.text
    print n.text

    if timeS is not None:
        data = {
            'Temperature' : temp,
            'Wind Speed' : windSP,
            'Wind Direction' : windDIR,
            'Humidity' : humiD,
            'Pressure' : presS,
            'Time Stamp' : timeS,
        }


   ## print data
    scraperwiki.sqlite.save(unique_keys=['Time Stamp'], data=data)
