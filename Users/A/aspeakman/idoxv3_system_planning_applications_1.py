# this is a scraper for Idox system planning applications for use by Openly Local

# there are 140 or so authorities using Idox systems, but this just implements a sub-variant covering systems where the search end date is exclusive

import scraperwiki
from datetime import timedelta
import random
import sys
import gc

util = scraperwiki.utils.swimport("utility_library")
idox = scraperwiki.utils.swimport("idox_system_planning_applications")

systems = {
    'Blackpool': 'BlackpoolScraper',
    'Bolton': 'BoltonScraper',
    'Cardiff': 'CardiffScraper',
    'Dover': 'DoverScraper',
    'Dumfries': 'DumfriesScraper',
    'EastHampshire': 'EastHampshireScraper',
    'EastLindsey': 'EastLindseyScraper',
    'Fylde': 'FyldeScraper',
    'Hastings': 'HastingsScraper',
    'MidSuffolk': 'MidSuffolkScraper',
    'NewForest': 'NewForestScraper',
    'Oldham': 'OldhamScraper',
    'Poole': 'PooleScraper',
    'Rhondda': 'RhonddaScraper',
    'WestSomerset': 'WestSomersetScraper',
    'Warwick': 'WarwickScraper',
}


class IdoxEndExcScraper(idox.IdoxScraper):

    def get_id_batch (self, date_from, date_to): # end date is exclusive, not inclusive
        date_to = date_to + timedelta(days=1) # increment end date by one day
        return idox.IdoxScraper.get_id_batch(self, date_from, date_to)

class BlackpoolScraper(IdoxEndExcScraper): 

    PROXY = 'http://www.speakman.org.uk/glype/browse.php?u=%s'
    search_url = 'http://publicaccess.blackpool.gov.uk:90/online-applications/search.do?action=advanced'

class BoltonScraper(IdoxEndExcScraper):

    search_url = 'http://www.planningpa.bolton.gov.uk/online-applications/search.do?action=advanced'

class CardiffScraper(IdoxEndExcScraper):

    search_url = 'http://planning.cardiff.gov.uk/online-applications/search.do?action=advanced'

class DoverScraper(IdoxEndExcScraper):

    search_url = 'http://planning.dover.gov.uk/online-applications/search.do?action=advanced'

class DumfriesScraper(IdoxEndExcScraper):

    search_url = 'http://eaccess.dumgal.gov.uk/online-applications/search.do?action=advanced'

class EastHampshireScraper(IdoxEndExcScraper):

    search_url = 'http://planningpublicaccess.easthants.gov.uk/online-applications/search.do?action=advanced'
    scrape_min_dates = "<th> Valid Date </th> <td> {{ date_validated }} </td>"

class EastLindseyScraper(IdoxEndExcScraper):

    search_url = 'http://publicaccess.e-lindsey.gov.uk/online-applications/search.do?action=advanced'

class FyldeScraper(IdoxEndExcScraper):

    search_url = 'http://www3.fylde.gov.uk/online-applications/search.do?action=advanced'

class HastingsScraper(IdoxEndExcScraper):

    search_url = 'http://publicaccess.hastings.gov.uk/online-applications/search.do?action=advanced'

class MidSuffolkScraper(IdoxEndExcScraper):

    search_url = 'http://planningpages.midsuffolk.gov.uk/online-applications/search.do?action=advanced'

class NewForestScraper(IdoxEndExcScraper):

    search_url = 'http://planweb3.newforest.gov.uk/online-applications/search.do?action=advanced'

class OldhamScraper(IdoxEndExcScraper):

    search_url = 'http://planningpa.oldham.gov.uk/online-applications/search.do?action=advanced'

class PooleScraper(IdoxEndExcScraper):

    search_url = 'https://boppa.boroughofpoole.com/online-applications/search.do?action=advanced'

class RhonddaScraper(IdoxEndExcScraper):

    search_url = 'http://planning.rctcbc.gov.uk/online-applications/search.do?action=advanced'
    scrape_min_dates = "<th> Received </th> <td> {{ date_received }} </td>"

class WestSomersetScraper(IdoxEndExcScraper):

    search_url = 'http://www.westsomerset.gov.uk/online-applications/search.do?action=advanced'

class WarwickScraper(IdoxEndExcScraper):

    search_url = 'http://planningdocuments.warwickdc.gov.uk/online-applications/search.do?action=advanced'

if __name__ == 'scraper':

    #scraper = MidSuffolkScraper('MidSuffolk')
    #scraper.run()
    #sys.exit()

    sys_list = []
    for k, v in systems.items(): # get latest date scraped for each system
        sys_list.append( (k, v, scraperwiki.sqlite.get_var('latest-' + k)) )
    sort_sys = sorted(sys_list, key=lambda system: system[2]) # sort so least recent are first
    for auth in sort_sys[:6]: # do max 6 per run
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
    #scraper = BlackpoolScraper()
    #scraper.DEBUG = True
    # print scraper.get_detail_from_uid ('11/0773') # Blackpool OK
    #scraper = BoltonScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('86677/11') # Bolton OK
    #scraper = CardiffScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/01366/DCH') # Cardiff OK
    #scraper = DoverScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/00702') # Dover OK
    #scraper = DumfriesScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/P/3/0348') # Dumfries OK
    #scraper = EastHampshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('23971/016') # EastHampshire OK
    #scraper = EastLindseyScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('N/173/01470/11') # EastLindsey OK
    #scraper = FyldeScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/0560') # Fylde OK
    #scraper = HastingsScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('HS/FA/11/00628') # Hastings OK
    #scraper = MidSuffolkScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('2705/11') # MidSuffolk OK
    #scraper = OldhamScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('PA/331003/11') # Oldham OK
    #scraper = PooleScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('APP/11/01050/F') # Poole OK
    #scraper = RhonddaScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/0969/10') # Rhondda OK
    #scraper = WestSomersetScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('3/21/11/106') # WestSomerset OK
    #scraper = WarwickScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('W/11/1024') # Warwick OK

    #res = scraper.get_id_batch(util.get_dt('09/08/2011'), util.get_dt('09/08/2011'))
    #print res, len(res)
    
    

