import scraperwiki           
import lxml.html
from lxml.html.clean import clean_html           

html = scraperwiki.scrape("http://www.bandonfloodwarning.ie/main.php")

root = lxml.html.fromstring(html)
roottext = root.text_content()
sentences = roottext.split('\r\n')

for j in sentences:
        if j.rfind('Water Level (m) at Bandon Bridge Gauge:') != -1:
            currenttext = j

level = currenttext.lstrip('Water Level (m) at Bandon Bridge Gauge:    ')
level = level.strip()
when = level
level = level.split(' ')
riverlevel = level[0]
when = when.split('Last Update:')
datetime = when[1]
data = {
      'level' : riverlevel,
      'datetime' : datetime
    }
scraperwiki.sqlite.save(unique_keys=['datetime'], data=data)