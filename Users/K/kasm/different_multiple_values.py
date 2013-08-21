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
        
#for k in root.cssselect("li .wx-temp"):
#    temPER = k.text
#    print k.text

for l in root.cssselect(".wx-timestamp .wx-value"):
    timeS = l.text
    print l.text

    if timeS is not None:
        data = {
            'Wind_Speed' : windSP,
            'Wind_Direction' : windDIR,
 #           'Temperature' : temPER,
            'Time Stamp' : timeS,
        }


   ## print data
    scraperwiki.sqlite.save(unique_keys=['Time Stamp'], data=data)
