import scraperwiki
import lxml.html
import requests
import re
 
html = scraperwiki.scrape("http://www.nero.noaa.gov/hcd/STATES4/massri.htm") 
root = lxml.html.fromstring(html)

for el in root.cssselect('map area[href]'):
    altVal = el.get('alt')
    baseURL = "http://www.nero.noaa.gov/hcd/STATES4/"
    url1 = baseURL + str(el.get('href'))
    #print url1

    html2 = requests.get(url1).text
    sqtext = re.search('<P>(&nbsp;)??Square Description.+&#9;(</FONT><FONT\ SIZE=1>)??(.+?)</P>', html2).group(3)

    data = {
        'TMS' : altVal,
        'Square Description' : sqtext
    }

    scraperwiki.sqlite.save(unique_keys=['TMS'], data=data)





    



import scraperwiki
import lxml.html
import requests
import re
 
html = scraperwiki.scrape("http://www.nero.noaa.gov/hcd/STATES4/massri.htm") 
root = lxml.html.fromstring(html)

for el in root.cssselect('map area[href]'):
    altVal = el.get('alt')
    baseURL = "http://www.nero.noaa.gov/hcd/STATES4/"
    url1 = baseURL + str(el.get('href'))
    #print url1

    html2 = requests.get(url1).text
    sqtext = re.search('<P>(&nbsp;)??Square Description.+&#9;(</FONT><FONT\ SIZE=1>)??(.+?)</P>', html2).group(3)

    data = {
        'TMS' : altVal,
        'Square Description' : sqtext
    }

    scraperwiki.sqlite.save(unique_keys=['TMS'], data=data)





    



