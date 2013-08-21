import scraperwiki
import requests
import lxml.html
import lxml.etree
from lxml.cssselect import CSSSelector
import time
from datetime import datetime

url = "http://www.wetter24.de/wetter/berlin/49X10168.html"        
html = requests.get(url, verify = False).text
#utf8_parser = etree.XMLParser(encoding='utf-8')

root = lxml.html.fromstring(html.encode("utf-8"))
time = datetime.now()


t_max_heute =  root.cssselect("p.one")[0].attrib['title']  
t_max_morgen =  root.cssselect("p.one")[1].attrib['title']  
t_max_ubermorgen =  root.cssselect("p.one")[2].attrib['title']  


t_min_heute =  root.cssselect("p.two")[0].attrib['title']
t_min_morgen =  root.cssselect("p.two")[1].attrib['title']
t_min_ubermorgen =  root.cssselect("p.two")[1].attrib['title']

data = {'time' : time,
        't_max_heute' : t_max_heute,
        't_max_morgen' : t_max_morgen,
        't_max_ubermorgen' : t_max_ubermorgen,
        't_min_heute' : t_min_heute,
        't_min_morgen' : t_min_morgen,
        't_min_ubermorgen' : t_min_ubermorgen
        }

scraperwiki.sqlite.save(unique_keys=['time'], data=data)
