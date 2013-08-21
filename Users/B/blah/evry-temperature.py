import datetime
import scraperwiki
import re
import time
from BeautifulSoup import BeautifulSoup

evryWeatherUri = 'http://www.weather.com/weather/today/Evry+France+FRBO0405'

temperaF = \
(re.sub("[^0-9]", "",
  BeautifulSoup(scraperwiki.scrape(evryWeatherUri))
  .findAll('td',{"class": "twc-col-1 twc-forecast-temperature"})[0]
  .findAll('strong')[0].text))

def far2cel(f):
  return (( f - 32 ) * 5 ) / 9.

scraperwiki.sqlite.save(["time"], {"time": time.time(), "tempera": far2cel(int(temperaF))})

