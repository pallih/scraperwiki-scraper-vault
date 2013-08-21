import scraperwiki
import requests
import lxml.html
import lxml.etree
from lxml.cssselect import CSSSelector
import time
from datetime import datetime

url = "http://www.proplanta.de/Agrar-Wetter/Berlin-AgrarWetter.html"        
html = requests.get(url, verify = False).text
root = lxml.html.fromstring(html)
time = datetime.now()


t_max_heute =  root.cssselect("span.SCHRIFT_FORMULAR_WERTE_MITTE ")#[1].text_content()
print t_max_heute[19].text_content()
#for item in t_max_heute:
#    print item.text_content()

t_max_morgen =  root.cssselect("span.lower")[5].text_content()
t_max_ubermorgen =  root.cssselect("span.lower")[9].text_content()


t_min_heute =  root.cssselect("span.lower")[1].tail.split()[1]
t_min_morgen =  root.cssselect("span.lower")[5].tail.split()[1]
t_min_ubermorgen =  root.cssselect("span.lower")[9].tail.split()[1]

