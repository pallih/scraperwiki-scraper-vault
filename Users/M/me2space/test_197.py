# More airports available, http://www.weather.gov/xml/current_obs/

import requests
import lxml
from lxml import html

# To grab the URL and convert into an lxml object ...
r = requests.get('http://www.weather.gov/data/obhistory/KMCO.html')
root = lxml.html.fromstring(r.content)
for tr in root.cssselect("td[align='left'] tr")[1:]:
    tds = tr.cssselect("td")
    start = tds[1].text_content().strip()
    end = tds[2].text_content().strip()
    description = tds[3].text_content().strip()




# More airports available, http://www.weather.gov/xml/current_obs/

import requests
import lxml
from lxml import html

# To grab the URL and convert into an lxml object ...
r = requests.get('http://www.weather.gov/data/obhistory/KMCO.html')
root = lxml.html.fromstring(r.content)
for tr in root.cssselect("td[align='left'] tr")[1:]:
    tds = tr.cssselect("td")
    start = tds[1].text_content().strip()
    end = tds[2].text_content().strip()
    description = tds[3].text_content().strip()




