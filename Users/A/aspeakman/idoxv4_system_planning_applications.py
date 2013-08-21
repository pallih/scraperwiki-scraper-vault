# this is a scraper for Idox system planning applications for use by Openly Local

# there are 140 or so authorities using Idox systems, but this just implements a sub-variant covering systems where the search is based on a plural 'dates' field

import scraperwiki
from datetime import timedelta
import random
import sys
import gc

util = scraperwiki.utils.swimport("utility_library")
idox = scraperwiki.utils.swimport("idox_system_planning_applications")

systems = {
    'Bedford': 'BedfordScraper',
    'Cambridge': 'CambridgeScraper',
    'DerbyshireDales': 'DerbyshireDalesScraper', # was Idox
    #'Cheltenham': 'CheltenhamScraper', # now Idox
    'Gloucester': 'GloucesterScraper',
    #'Hart': 'HartScraper', now Idox
    'Horsham': 'HorshamScraper',
    'Lancaster': 'LancasterScraper',
    'Lewes': 'LewesScraper',
    'Manchester': 'ManchesterScraper',
    'MidSussex': 'MidSussexScraper',
    'NorthKesteven': 'NorthKestevenScraper',
    'Peterborough': 'PeterboroughScraper',
    'Sunderland': 'SunderlandScraper',
    'Torbay': 'TorbayScraper', # now Idox
    'Wakefield': 'WakefieldScraper',
    'WestLancashire': 'WestLancashireScraper', # also see PublicAccess scraper
}

class IdoxDatesScraper(idox.IdoxScraper):

    date_from_field = 'dates(applicationReceivedStart)'
    date_to_field = 'dates(applicationReceivedEnd)'

class BedfordScraper(IdoxDatesScraper): 

    search_url = 'http://www.publicaccess.bedford.gov.uk/online-applications/search.do?action=advanced'

class CambridgeScraper(IdoxDatesScraper):

    search_url = 'http://idox.cambridge.gov.uk/online-applications/search.do?action=advanced'

class DerbyshireDalesScraper(IdoxDatesScraper): # note causes problems on OpenlyLocal with unsigned SSL certificate 

    search_url = 'https://planning.derbyshiredales.gov.uk/online-applications/search.do?action=advanced' 

#class CheltenhamScraper(IdoxDatesScraper):

#    search_url = 'http://publicaccess.cheltenham.gov.uk/idoxpa17/search.do?action=advanced'

class GloucesterScraper(IdoxDatesScraper):

    search_url = 'http://glcstrplnng12.co.uk/online-applications/search.do?action=advanced'

#class HartScraper(IdoxDatesScraper):

#    search_url = 'http://publicaccess.hart.gov.uk/online-applications/search.do?action=advanced'

class HorshamScraper(IdoxDatesScraper):

    search_url = 'http://public-access.horsham.gov.uk/public-access/search.do?action=advanced'

class LancasterScraper(IdoxDatesScraper):

    search_url = 'http://planning.lancaster.gov.uk/online-applications/search.do?action=advanced'

class LewesScraper(IdoxDatesScraper):

    search_url = 'http://planningpa.lewes.gov.uk/online-applications/search.do?action=advanced'

class ManchesterScraper(IdoxDatesScraper):

    search_url = 'http://pa.manchester.gov.uk/online-applications/search.do?action=advanced'

class MidSussexScraper(IdoxDatesScraper):

    search_url = 'http://pa.midsussex.gov.uk/online-applications/search.do?action=advanced'

class NorthKestevenScraper(IdoxDatesScraper):

    search_url = 'http://planningonline.n-kesteven.gov.uk/online-applications/search.do?action=advanced'

class PeterboroughScraper(IdoxDatesScraper):

    search_url = 'http://planpa.peterborough.gov.uk/online-applications/search.do?action=advanced'

class SunderlandScraper(IdoxDatesScraper):

    search_url = 'http://www.sunderland.gov.uk/online-applications/search.do?action=advanced'

class TorbayScraper(idox.IdoxScraper): # note now inherits from Idox + headers required to work

    HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
    'Accept-Charset': 'UTF-8,*',
    'Accept': 'text/html',
    'Accept-Language': 'en-gb,en'
    }
    search_url = 'http://www.torbay.gov.uk/newpublicaccess/search.do?action=advanced'

class WakefieldScraper(IdoxDatesScraper):# does not like delivering large nos - limit requests to 7 days

    BATCH_DAYS = 7 # batch size for each scrape - number of days to gather to produce at least one result each time
    MIN_DAYS = 10 # min number of days to get when gathering current ids
    search_url = 'https://planning.wakefield.gov.uk/online-applications/search.do?action=advanced'

class WestLancashireScraper(IdoxDatesScraper):

    search_url = 'https://pa.westlancs.gov.uk/online-applications/search.do?action=advanced'

if __name__ == 'scraper':

    #scraper = WakefieldScraper('Wakefield')
    #scraper.run()
    #scraper.clear_all()
    #scraper = TorbayScraper('Torbay')
    #scraper.replace_all_with('idox_system_planning_applications', 'Torbay')

    #sql = 'UPDATE DerbyshireDales SET application_expires_date = application_expiry_date WHERE application_expires_date is null'
    #print scraperwiki.sqlite.select("sql from sqlite_master where type='table' and name='Torbay'")
    #columns = util.get_table_columns('Torbay')
    #sql_new_schema = util.create_table_schema(columns, 'xxx')
    #print sql_new_schema
    #scraperwiki.sqlite.execute(sql)
    #scraperwiki.sqlite.commit()
    #util.rename_column('DerbyshireDales', 'application_expiry_date', None)
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
    #scraper = BedfordScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/01718/FUL') # Bedford OK
    #scraper = CambridgeScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/299/TTPO') # Cambridge OK
    #scraper = DerbyshireDalesScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/00627/FUL') # DerbyshireDales OK
    #scraper = CheltenhamScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/01122/CACN') # Cheltenham OK
    #scraper = GloucesterScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/00922/FUL') # Gloucester OK
    #scraper = HartScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/01717/FUL') # Hart OK
    #scraper = HorshamScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('DC/11/1597') # Horsham OK
    #scraper = LancasterScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/00748/FUL') # Lancaster OK
    #scraper = LewesScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('LW/11/0982') # Lewes OK
    #scraper = ManchesterScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('097035/AO/2011/N1') # Manchester OK
    #scraper = MidSussexScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/02484/FUL') # MidSussex OK
    #scraper = NorthKestevenScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/0901/FUL') # NorthKesteven OK
    #scraper = PeterboroughScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/01273/FUL') # Peterborough OK
    #scraper = SunderlandScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/02541/FUL') # Sunderland OK
    #scraper = TorbayScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('P/2011/0849') # Torbay OK
    #scraper = WakefieldScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/01618/ADV') # Wakefield OK
    #scraper = WestLancashireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('2011/0884/FUL') # WestLancashire OK

    #res = scraper.get_id_batch(util.get_dt('10/08/2011'), util.get_dt('10/08/2011'))
    #print res, len(res)
    
    


