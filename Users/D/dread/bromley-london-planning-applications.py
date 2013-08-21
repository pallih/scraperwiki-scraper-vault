import scraperwiki
from BeautifulSoup import BeautifulSoup
import mechanize
import datetime
import re

#############################################################################################
# this executes an import from the code at http://scraperwiki.com/scrapers/ckanclient/edit/
# In the future there may be a slick way to overload __import__, but this does the job for now

caps = scraperwiki.utils.swimport('caps')
search_form_url = 'http://planning.bromley.gov.uk/PublicAccess/tdc/DcApplication/application_searchform.aspx'
scraper = caps.CapsScraper(search_form_url)
scraper.run()

import scraperwiki
from BeautifulSoup import BeautifulSoup
import mechanize
import datetime
import re

#############################################################################################
# this executes an import from the code at http://scraperwiki.com/scrapers/ckanclient/edit/
# In the future there may be a slick way to overload __import__, but this does the job for now

caps = scraperwiki.utils.swimport('caps')
search_form_url = 'http://planning.bromley.gov.uk/PublicAccess/tdc/DcApplication/application_searchform.aspx'
scraper = caps.CapsScraper(search_form_url)
scraper.run()

