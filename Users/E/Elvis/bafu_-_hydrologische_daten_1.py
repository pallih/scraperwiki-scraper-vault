import scraperwiki

# Blank Python

import lxml.html

station = 'http://www.meteoschweiz.admin.ch/web/de/wetter/aktuelles_wetter.par0010.html?allStations=1'

html = scraperwiki.scrape(station)
root = lxml.html.fromstring(html)
#messwerte = root.xpath('//div[@class="karte_text_hidden"]/span')
messwerte = root.xpath('//div[@id="karte_data_aktueller_wind_numerisch___WYN"]/span')
a,b,c = messwerte[0].text.split('|')
print c
print messwerte[0].textimport scraperwiki

# Blank Python

import lxml.html

station = 'http://www.meteoschweiz.admin.ch/web/de/wetter/aktuelles_wetter.par0010.html?allStations=1'

html = scraperwiki.scrape(station)
root = lxml.html.fromstring(html)
#messwerte = root.xpath('//div[@class="karte_text_hidden"]/span')
messwerte = root.xpath('//div[@id="karte_data_aktueller_wind_numerisch___WYN"]/span')
a,b,c = messwerte[0].text.split('|')
print c
print messwerte[0].text