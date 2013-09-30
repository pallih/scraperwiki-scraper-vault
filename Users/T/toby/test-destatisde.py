import urllib
import scraperwiki
import BeautifulSoup

# data
htmlurl = "http://www.destatis.de/jetspeed/portal/cms/Sites/destatis/Internet/EN/Content/Statistics/VolkswirtschaftlicheGesamtrechnungen/Inlandsprodukt/Tabellen/Content75/Gesamtwirtschaft,templateId=renderPrint.psml"

# load
htmldata = scraperwiki.scrape(htmlurl)
page = BeautifulSoup.BeautifulSoup(htmldata)

# parse
print page

import urllib
import scraperwiki
import BeautifulSoup

# data
htmlurl = "http://www.destatis.de/jetspeed/portal/cms/Sites/destatis/Internet/EN/Content/Statistics/VolkswirtschaftlicheGesamtrechnungen/Inlandsprodukt/Tabellen/Content75/Gesamtwirtschaft,templateId=renderPrint.psml"

# load
htmldata = scraperwiki.scrape(htmlurl)
page = BeautifulSoup.BeautifulSoup(htmldata)

# parse
print page

