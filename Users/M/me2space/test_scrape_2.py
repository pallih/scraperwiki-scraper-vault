# More airports available, http://www.weather.gov/xml/current_obs/

import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.weather.gov/xml/current_obs/KMCO.xml") 
root = lxml.html.fromstring(html)
print lxml.html.tostring(root)

#extract date and air temperature

el = lxml.html.fromstring(html)
location = el[5].text_content()
date = el[10].text_content()
temperature = el[13].text_content()
#print location, date, temperature

scraperwiki.sqlite.save_var(date, temperature)  

