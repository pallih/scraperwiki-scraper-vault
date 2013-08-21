import scraperwiki
import requests
import lxml.html
import lxml.etree
from lxml.cssselect import CSSSelector
import time
from datetime import datetime

url = "http://www.wetter.com/wetter_aktuell/wettervorhersage/3_tagesvorhersage/?id=DE0001020"        
html = requests.get(url, verify = False).text
root = lxml.html.fromstring(html)
time = datetime.now()


t_max_heute =  root.cssselect("div.forecast-day-overlay")#[1].text_content()
print t_max_heute

t_max_morgen =  root.cssselect("span.lower")[5].text_content()
t_max_ubermorgen =  root.cssselect("span.lower")[9].text_content()


t_min_heute =  root.cssselect("span.lower")[1].tail.split()[1]
t_min_morgen =  root.cssselect("span.lower")[5].tail.split()[1]
t_min_ubermorgen =  root.cssselect("span.lower")[9].tail.split()[1]

data = {'time' : time,
        't_max_heute' : t_max_heute,
        't_max_morgen' : t_max_morgen,
        't_max_ubermorgen' : t_max_ubermorgen,
        't_min_heute' : t_min_heute,
        't_min_morgen' : t_min_morgen,
        't_min_ubermorgen' : t_min_ubermorgen
        }

scraperwiki.sqlite.save(unique_keys=['time'], data=data)
