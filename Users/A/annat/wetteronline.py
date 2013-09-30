import scraperwiki
import requests
import lxml.html
import lxml.etree
from lxml.cssselect import CSSSelector
import time
from datetime import datetime

url = "http://www.wetteronline.de/Berlin/Berlin.htm"        
html = requests.get(url, verify = False).text

root = lxml.html.fromstring(html.encode("utf-8"))
time = datetime.now()


t_max_heute =  root.cssselect("td.tmax")[0].text_content()
t_max_morgen =  root.cssselect("td.tmax")[1].text_content() 
t_max_ubermorgen =  root.cssselect("td.tmax")[2].text_content()


t_min_heute =  root.cssselect("td.tmin")[0].text_content()
t_min_morgen =  root.cssselect("td.tmin")[1].text_content()
t_min_ubermorgen =  root.cssselect("td.tmin")[1].text_content()

data = {'time' : time,
        't_max_heute' : t_max_heute,
        't_max_morgen' : t_max_morgen,
        't_max_ubermorgen' : t_max_ubermorgen,
        't_min_heute' : t_min_heute,
        't_min_morgen' : t_min_morgen,
        't_min_ubermorgen' : t_min_ubermorgen
        }

scraperwiki.sqlite.save(unique_keys=['time'], data=data)
import scraperwiki
import requests
import lxml.html
import lxml.etree
from lxml.cssselect import CSSSelector
import time
from datetime import datetime

url = "http://www.wetteronline.de/Berlin/Berlin.htm"        
html = requests.get(url, verify = False).text

root = lxml.html.fromstring(html.encode("utf-8"))
time = datetime.now()


t_max_heute =  root.cssselect("td.tmax")[0].text_content()
t_max_morgen =  root.cssselect("td.tmax")[1].text_content() 
t_max_ubermorgen =  root.cssselect("td.tmax")[2].text_content()


t_min_heute =  root.cssselect("td.tmin")[0].text_content()
t_min_morgen =  root.cssselect("td.tmin")[1].text_content()
t_min_ubermorgen =  root.cssselect("td.tmin")[1].text_content()

data = {'time' : time,
        't_max_heute' : t_max_heute,
        't_max_morgen' : t_max_morgen,
        't_max_ubermorgen' : t_max_ubermorgen,
        't_min_heute' : t_min_heute,
        't_min_morgen' : t_min_morgen,
        't_min_ubermorgen' : t_min_ubermorgen
        }

scraperwiki.sqlite.save(unique_keys=['time'], data=data)
