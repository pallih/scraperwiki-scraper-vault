import scraperwiki
import urllib2
import re
from scrapemark import scrape

Daten = scraperwiki.scrape("http://www.lidl.de/de/Filialsuche")

urls = re.findall(r'href=[\'"]?([^\'" >]+)', Daten)

print ' '.join(urls)

import scraperwiki
import urllib2
import re
from scrapemark import scrape

Daten = scraperwiki.scrape("http://www.lidl.de/de/Filialsuche")

urls = re.findall(r'href=[\'"]?([^\'" >]+)', Daten)

print ' '.join(urls)

