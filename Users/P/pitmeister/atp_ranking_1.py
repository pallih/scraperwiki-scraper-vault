import scraperwiki
import lxml.html

import datetime
now = datetime.datetime.now()

print now.strftime("%d.%m.%Y")
todaydate = now.strftime("%d.%m.%Y")

rooturl = "http://www.atpworldtour.com/Rankings/Singles.aspx?d="+str(todaydate)

print rooturl

for rank in range(0, 1):
    r=rank*100+1
    html = scraperwiki.scrape(rooturl+'&r='+str(r))
          
    root = lxml.html.fromstring(html)
    
    for tr in root.cssselect("table.bioTableAlt tr"):
        tds = tr.cssselect("td")
        key = str(todaydate)+","+tds[0].text_content().replace("u'", "").replace("\t", "").replace("\n", "").replace("\r", " ")
        rank = str(tr.cssselect("td.first .rank"))
        print rank
        data = {
            'key' : key,
            'date' : todaydate,
            'rank' : rank,
            'text' : tds[0].text_content().replace("u'", "").replace("\t", "").replace("\n", "").replace("\r", " "),
            'points': tds[1].text_content().replace(",", "")
        }
        scraperwiki.sqlite.save(unique_keys=['key'], data=data)