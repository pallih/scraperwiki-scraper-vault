# this is a scraper for Idox system planning applications for use by Openly Local

# there are 140 or so authorities using Idox systems, but this just implements a sub-variant covering 9 Scottish authorities

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import random
import urllib
import urlparse
import sys
import gc

util = scraperwiki.utils.swimport("utility_library")
idox = scraperwiki.utils.swimport("idox_system_planning_applications")

systems = {
    'Clackmannanshire': 'ClackmannanshireScraper',
    'EastAyrshire': 'EastAyrshireScraper',
    'EastDunbartonshire': 'EastDunbartonshireScraper',
    'Inverclyde': 'InverclydeScraper',
    'Midlothian': 'MidlothianScraper',
    #'NorthAyrshire': 'NorthAyrshireScraper', # now normal Idox system
    'NorthLanarkshire': 'NorthLanarkshireScraper',
    #'Orkney': 'OrkneyScraper', # now normal Idox system
    'SouthAyrshire': 'SouthAyrshireScraper',
     }

class Idoxv2Scraper(idox.IdoxScraper):

    MAX_ID_BATCH = 300 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go

    date_from_field = 'dates(applicationReceivedStart)'
    date_to_field = 'dates(applicationReceivedEnd)'
    scrape_ids = """
    <div id="searchresults">
    {* <div>
    <a href="{{ [records].url|abs }}" />
    <p> No: {{ [records].uid }} <span />
    </div> *}
    </div>
    """
    scrape_dates_link = '<a id="dates" href="{{ dates_link|abs }}" />'
    scrape_info_link = '<a id="details" href="{{ info_link|abs }}" />'

class ClackmannanshireScraper(Idoxv2Scraper): # very slow

    search_url = 'https://eplanning.clacks.gov.uk/eplanning/search.do?action=application'

class EastAyrshireScraper(Idoxv2Scraper):

    search_url = 'http://eplanning.east-ayrshire.gov.uk/online/search.do?action=application'

class EastDunbartonshireScraper(Idoxv2Scraper):

    search_url = 'http://opis-web.eastdunbarton.gov.uk/bumblebee-web/search.do?action=application'

class InverclydeScraper(Idoxv2Scraper): # low numbers

    BATCH_DAYS = 28 # batch size for each scrape - number of days to gather to produce at least one result each time
    MIN_DAYS = 28 # min number of days to get when gathering current ids
    search_url = 'http://planning.inverclyde.gov.uk/Online/search.do?action=application'

class MidlothianScraper(Idoxv2Scraper):

    search_url = 'https://planning-applications.midlothian.gov.uk/OnlinePlanning/search.do?action=application'

class NorthAyrshireScraper(Idoxv2Scraper):

    search_url = 'http://www.eplanning.north-ayrshire.gov.uk/OnlinePlanning/search.do?action=application'

class NorthLanarkshireScraper(Idoxv2Scraper):

    search_url = 'https://eplanning.northlan.gov.uk/Online/search.do?action=application'

#class OrkneyScraper(Idoxv2Scraper):
#
#    search_url = 'http://opis.orkney.gov.uk/eplanning/search.do?action=application'

class SouthAyrshireScraper(Idoxv2Scraper):

    search_url = 'http://ww6.south-ayrshire.gov.uk:81/bumblebee-web/search.do?action=application'

    def __init__(self, table_name = None):
        self.br, self.handler, self.cj = util.get_browser(self.HEADERS, '', 'http://www.speakman.org.uk/glype/browse.php?u=%s') # use proxy to access port 81
        if table_name:
            self.TABLE_NAME = table_name
            self.DATA_START_MARKER = 'earliest-' + table_name
            self.DATA_END_MARKER = 'latest-' + table_name

if __name__ == 'scraper':

    #scraper = ClackmannanshireScraper('Clackmannanshire')
    #scraper.run()
    #sys.exit()

    sys_list = []
    for k, v in systems.items(): # get latest date scraped for each system
        sys_list.append( (k, v, scraperwiki.sqlite.get_var('latest-' + k)) )
    sort_sys = sorted(sys_list, key=lambda system: system[2]) # sort so least recent are first
    for auth in sort_sys[:4]: # do max 4 per run
        strexec = auth[1] + "('" + auth[0] + "')"
        print "Scraping from:", strexec
        try:
            scraper = eval(strexec)
            scraper.run()
            scraper = None
            gc.collect()
        except Exception as err:
            print "Error - skipping this authority -", str(err)
    print "Finished"

    # misc test calls
    #scraper = ClackmannanshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/00233/CLPUD') # Clackmannanshire OK
    #scraper = EastAyrshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/0689/AD') # EastAyrshire OK
    #scraper = EastDunbartonshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('TP/ED/11/0754') # EastDunbartonshire OK
    #scraper = InverclydeScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/0214/IC') # Inverclyde OK
    #scraper = MidlothianScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/00590/PNSP') # Midlothian OK
    #scraper = NorthAyrshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/00581/PP') # NorthAyrshire OK
    #scraper = NorthLanarkshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/00971/FUL') # NorthLanarkshire OK
    #scraper = OrkneyScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/439/PP') # Orkney OK
    #scraper = SouthAyrshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/01054/APP') # SouthAyrshire OK

    #res = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('28/08/2011'))
    #print res, len(res)




# this is a scraper for Idox system planning applications for use by Openly Local

# there are 140 or so authorities using Idox systems, but this just implements a sub-variant covering 9 Scottish authorities

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import random
import urllib
import urlparse
import sys
import gc

util = scraperwiki.utils.swimport("utility_library")
idox = scraperwiki.utils.swimport("idox_system_planning_applications")

systems = {
    'Clackmannanshire': 'ClackmannanshireScraper',
    'EastAyrshire': 'EastAyrshireScraper',
    'EastDunbartonshire': 'EastDunbartonshireScraper',
    'Inverclyde': 'InverclydeScraper',
    'Midlothian': 'MidlothianScraper',
    #'NorthAyrshire': 'NorthAyrshireScraper', # now normal Idox system
    'NorthLanarkshire': 'NorthLanarkshireScraper',
    #'Orkney': 'OrkneyScraper', # now normal Idox system
    'SouthAyrshire': 'SouthAyrshireScraper',
     }

class Idoxv2Scraper(idox.IdoxScraper):

    MAX_ID_BATCH = 300 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go

    date_from_field = 'dates(applicationReceivedStart)'
    date_to_field = 'dates(applicationReceivedEnd)'
    scrape_ids = """
    <div id="searchresults">
    {* <div>
    <a href="{{ [records].url|abs }}" />
    <p> No: {{ [records].uid }} <span />
    </div> *}
    </div>
    """
    scrape_dates_link = '<a id="dates" href="{{ dates_link|abs }}" />'
    scrape_info_link = '<a id="details" href="{{ info_link|abs }}" />'

class ClackmannanshireScraper(Idoxv2Scraper): # very slow

    search_url = 'https://eplanning.clacks.gov.uk/eplanning/search.do?action=application'

class EastAyrshireScraper(Idoxv2Scraper):

    search_url = 'http://eplanning.east-ayrshire.gov.uk/online/search.do?action=application'

class EastDunbartonshireScraper(Idoxv2Scraper):

    search_url = 'http://opis-web.eastdunbarton.gov.uk/bumblebee-web/search.do?action=application'

class InverclydeScraper(Idoxv2Scraper): # low numbers

    BATCH_DAYS = 28 # batch size for each scrape - number of days to gather to produce at least one result each time
    MIN_DAYS = 28 # min number of days to get when gathering current ids
    search_url = 'http://planning.inverclyde.gov.uk/Online/search.do?action=application'

class MidlothianScraper(Idoxv2Scraper):

    search_url = 'https://planning-applications.midlothian.gov.uk/OnlinePlanning/search.do?action=application'

class NorthAyrshireScraper(Idoxv2Scraper):

    search_url = 'http://www.eplanning.north-ayrshire.gov.uk/OnlinePlanning/search.do?action=application'

class NorthLanarkshireScraper(Idoxv2Scraper):

    search_url = 'https://eplanning.northlan.gov.uk/Online/search.do?action=application'

#class OrkneyScraper(Idoxv2Scraper):
#
#    search_url = 'http://opis.orkney.gov.uk/eplanning/search.do?action=application'

class SouthAyrshireScraper(Idoxv2Scraper):

    search_url = 'http://ww6.south-ayrshire.gov.uk:81/bumblebee-web/search.do?action=application'

    def __init__(self, table_name = None):
        self.br, self.handler, self.cj = util.get_browser(self.HEADERS, '', 'http://www.speakman.org.uk/glype/browse.php?u=%s') # use proxy to access port 81
        if table_name:
            self.TABLE_NAME = table_name
            self.DATA_START_MARKER = 'earliest-' + table_name
            self.DATA_END_MARKER = 'latest-' + table_name

if __name__ == 'scraper':

    #scraper = ClackmannanshireScraper('Clackmannanshire')
    #scraper.run()
    #sys.exit()

    sys_list = []
    for k, v in systems.items(): # get latest date scraped for each system
        sys_list.append( (k, v, scraperwiki.sqlite.get_var('latest-' + k)) )
    sort_sys = sorted(sys_list, key=lambda system: system[2]) # sort so least recent are first
    for auth in sort_sys[:4]: # do max 4 per run
        strexec = auth[1] + "('" + auth[0] + "')"
        print "Scraping from:", strexec
        try:
            scraper = eval(strexec)
            scraper.run()
            scraper = None
            gc.collect()
        except Exception as err:
            print "Error - skipping this authority -", str(err)
    print "Finished"

    # misc test calls
    #scraper = ClackmannanshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/00233/CLPUD') # Clackmannanshire OK
    #scraper = EastAyrshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/0689/AD') # EastAyrshire OK
    #scraper = EastDunbartonshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('TP/ED/11/0754') # EastDunbartonshire OK
    #scraper = InverclydeScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/0214/IC') # Inverclyde OK
    #scraper = MidlothianScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/00590/PNSP') # Midlothian OK
    #scraper = NorthAyrshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/00581/PP') # NorthAyrshire OK
    #scraper = NorthLanarkshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/00971/FUL') # NorthLanarkshire OK
    #scraper = OrkneyScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/439/PP') # Orkney OK
    #scraper = SouthAyrshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/01054/APP') # SouthAyrshire OK

    #res = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('28/08/2011'))
    #print res, len(res)




