try:
    from scraperwiki.utils import httpresponseheader
    from scraperwiki.sqlite import attach, select
except ImportError:
    def httpresponseheader(a, b):
        pass
from lxml.html import fromstring
from urllib2 import urlopen
from time import time

attach('combine_mix_scraper_spreadsheets_1')
httpresponseheader("Content-Type", "text/csv")
httpresponseheader("Content-Disposition", "attachment; filename=combined_spreadsheets.csv")
print select('spreadsheet from combined_spreadsheets where time = (select max(time) from combined_spreadsheets)')[0]['spreadsheet']try:
    from scraperwiki.utils import httpresponseheader
    from scraperwiki.sqlite import attach, select
except ImportError:
    def httpresponseheader(a, b):
        pass
from lxml.html import fromstring
from urllib2 import urlopen
from time import time

attach('combine_mix_scraper_spreadsheets_1')
httpresponseheader("Content-Type", "text/csv")
httpresponseheader("Content-Disposition", "attachment; filename=combined_spreadsheets.csv")
print select('spreadsheet from combined_spreadsheets where time = (select max(time) from combined_spreadsheets)')[0]['spreadsheet']