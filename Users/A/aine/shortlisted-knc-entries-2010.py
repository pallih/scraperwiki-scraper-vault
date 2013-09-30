import scraperwiki
import mechanize 
import lxml.html
import urlparse
import urllib
import datetime
import re

url = "http://generalapp.newschallenge.org/SNC/GroupSearch.aspx?itemGUID=4751b3c2-3e9b-48ef-b201-71e76e1c4f52&pguid=6671c4e8-ddb2-4170-9b12-e864115cc5a3"

html = urllib.urlopen(url).read()
print html

# Julian - The main application page has a very long URL - it does not mean anything to me! :-)import scraperwiki
import mechanize 
import lxml.html
import urlparse
import urllib
import datetime
import re

url = "http://generalapp.newschallenge.org/SNC/GroupSearch.aspx?itemGUID=4751b3c2-3e9b-48ef-b201-71e76e1c4f52&pguid=6671c4e8-ddb2-4170-9b12-e864115cc5a3"

html = urllib.urlopen(url).read()
print html

# Julian - The main application page has a very long URL - it does not mean anything to me! :-)