from datetime import datetime, timedelta
import dateutil.parser, string, re
import requests
from lxml import html
import scraperwiki

# http://www.guardian.co.uk/theguardian/2012/may/16/corrections-and-clarifications
URL = 'http://www.guardian.co.uk/theguardian/%Y/%b/%d/corrections-and-clarifications'
# Matches: http://www.guardian.co.uk/money/shortcuts/2012/may/15/what-can-you-buy-just-with-1p-and-2p
PATTERN = 'http://www.guardian.co.uk/(?:.*)/(?P<year>\d{4})/(?P<month>.+)\/(?P<day>\d{2})/'

# For each correction page, save every corrected article link into the datastore