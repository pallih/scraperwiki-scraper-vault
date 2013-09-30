import scraperwiki
import lxml.html
import datetime
import string

index = 0

now  = datetime.datetime.now()
date = now.date()
day      = now.day
year     = now.year
month    = now.month
monthTxt = now.strftime("%B")

param1 = str(year) + "/" + str(month) + "/" + str(day)
param2 = str(monthTxt) + "-" + str(day) + "-" + str(year)

urlToday = "http://vicksburgdailynews.com/"+ param1 + "/this-day-in-history-" + param2 + "/"
print urlToday

index = 0

html = scraperwiki.scrape(urlToday)
root = lxml.html.fromstring(html)

his_nodes = root.cssselect("div[class = 'entry'] > p")
 
for node in his_nodes:
    root2 = lxml.html.fromstring(lxml.html.tostring(node));
    his_year = root2.cssselect("p > strong")
    his_data = root2.xpath("//p/text()")
    if his_year:        
        
        index = index + 1
        data = {
                "index" : index,
                "date" : param1,
                "eventYear" : his_year[0].text,
                "eventInfo" : his_data[0][2:]
               }
        print data
        
        scraperwiki.sqlite.save(unique_keys=['index'], table_name="history", data=data)
        
        import scraperwiki
import lxml.html
import datetime
import string

index = 0

now  = datetime.datetime.now()
date = now.date()
day      = now.day
year     = now.year
month    = now.month
monthTxt = now.strftime("%B")

param1 = str(year) + "/" + str(month) + "/" + str(day)
param2 = str(monthTxt) + "-" + str(day) + "-" + str(year)

urlToday = "http://vicksburgdailynews.com/"+ param1 + "/this-day-in-history-" + param2 + "/"
print urlToday

index = 0

html = scraperwiki.scrape(urlToday)
root = lxml.html.fromstring(html)

his_nodes = root.cssselect("div[class = 'entry'] > p")
 
for node in his_nodes:
    root2 = lxml.html.fromstring(lxml.html.tostring(node));
    his_year = root2.cssselect("p > strong")
    his_data = root2.xpath("//p/text()")
    if his_year:        
        
        index = index + 1
        data = {
                "index" : index,
                "date" : param1,
                "eventYear" : his_year[0].text,
                "eventInfo" : his_data[0][2:]
               }
        print data
        
        scraperwiki.sqlite.save(unique_keys=['index'], table_name="history", data=data)
        
        