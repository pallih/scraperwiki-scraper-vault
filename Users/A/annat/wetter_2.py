import scraperwiki
import requests
import lxml.html
from lxml.cssselect import CSSSelector
import time
from datetime import datetime

url = "http://www2.wetterspiegel.de/de/europa/deutschland/berlin/13433x25.html"


        
html = requests.get(url, verify = False).text
root = lxml.html.fromstring(html)
time = datetime.now() 
t_max_heute =  root.cssselect("b")[7].text_content()
t_max_morgen =  root.cssselect("b")[8].text_content()
t_max_ubermorgen =  root.cssselect("b")[9].text_content()


t_min_heute =  root.cssselect("b")[10].text_content()
t_min_morgen =  root.cssselect("b")[11].text_content()
t_min_ubermorgen =  root.cssselect("b")[12].text_content()

data = {'time' : time,
        't_max_heute' : t_max_heute,
        't_max_morgen' : t_max_morgen,
        't_max_ubermorgen' : t_max_ubermorgen,
        't_min_heute' : t_min_heute,
        't_min_morgen' : t_min_morgen,
        't_min_ubermorgen' : t_min_ubermorgen
        }

scraperwiki.sqlite.save(unique_keys=['time'], data=data)


