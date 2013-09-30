import  urllib2
import datetime
import scraperwiki 


url = 'http://forecast.weather.gov/MapClick.php?CityName=Bloomsburg&state=PA&site=CTP&textField1=41.0023&textField2=-76.4569'
html = urllib2.urlopen(url).read() 
ia = html.find("\n<b>Today: </b>")
ib = html.find("<br><br></td>\n<td")
html = html[ia:ib].replace("<br>","").replace("\n", "")
htmllist = html.split("<b>")[1:] 
titles = []
content = []
for entry in htmllist:
    temp = entry.split("</b>")
    titles.append(temp[0])
    content.append(temp[1])

today = datetime.date.today()
day = datetime.timedelta(days = 1)

for i in range(len(titles)):
    titles[i] =  (today + i * day ).isoformat()

dataarr = []
for i in range(len(titles)) :
    dataarr.append({ "Date":titles[i] , "Forecast":content[i] })

for dataa in dataarr :
     scraperwiki.sqlite.save(unique_keys=["Date"], data=dataa) 
import  urllib2
import datetime
import scraperwiki 


url = 'http://forecast.weather.gov/MapClick.php?CityName=Bloomsburg&state=PA&site=CTP&textField1=41.0023&textField2=-76.4569'
html = urllib2.urlopen(url).read() 
ia = html.find("\n<b>Today: </b>")
ib = html.find("<br><br></td>\n<td")
html = html[ia:ib].replace("<br>","").replace("\n", "")
htmllist = html.split("<b>")[1:] 
titles = []
content = []
for entry in htmllist:
    temp = entry.split("</b>")
    titles.append(temp[0])
    content.append(temp[1])

today = datetime.date.today()
day = datetime.timedelta(days = 1)

for i in range(len(titles)):
    titles[i] =  (today + i * day ).isoformat()

dataarr = []
for i in range(len(titles)) :
    dataarr.append({ "Date":titles[i] , "Forecast":content[i] })

for dataa in dataarr :
     scraperwiki.sqlite.save(unique_keys=["Date"], data=dataa) 
