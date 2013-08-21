# this is a scraper for Idox system planning applications for use by Openly Local

# there are 140 or so authorities using Idox systems, but this just implements the 12 London based scrapers

import scraperwiki
from datetime import timedelta
import random
import sys
import gc

util = scraperwiki.utils.swimport("utility_library")
idox = scraperwiki.utils.swimport("idox_system_planning_applications")

systems = [
    'WestminsterScraper'
]

class IdoxLondonScraper(idox.IdoxScraper):

    pass

class WestminsterScraper(IdoxLondonScraper):

    search_url = 'http://idoxpa.westminster.gov.uk/online-applications/search.do?action=advanced'
    TABLE_NAME = 'Westminster'
    # end date inclusive

if __name__ == 'scraper':

    #scraper = HammersmithScraper()
    #scraper.clear_all()
    #scraper.run()
    
    #scraper = BromleyScraper()
    #scraper.replace_all_with('idox_system_planning_applications')

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
    for k in systems: # get latest date scraped for each system
        try:
            scraper = eval(k + "()")
            latest_val = scraperwiki.sqlite.get_var('latest-' + scraper.TABLE_NAME)
            scraper = None
            gc.collect()
        except:
            latest_val = None
        sys_list.append( (k, latest_val) )
    sort_sys = sorted(sys_list, key=lambda system: system[1]) # sort so least recent are first
    for auth in sort_sys[:5]: # do max 5 per run
        strexec = auth[0] + "()"
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
    #scraper = BarkingScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/00728/FUL') # Barking
    #scraper = BarnetScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('F/03385/11') # Barnet
    #scraper = BexleyScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/01320/FUL') # Bexley
    #scraper = BromleyScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('12/02973/FULL6') # Bromley NOT WORKING AT THE MOMENT
    #scraper = CityScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/00590/FULL') # City
    #scraper = CroydonScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/01559/LE') # Croydon
    #scraper = GreenwichScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/1768/F') # Greenwich
    #scraper = HammersmithScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('2011/02554/FUL') # Hammersmith
    #scraper = LambethScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/02704/FUL') # Lambeth
    #scraper = LewishamScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('DC/11/78084/FT') # Lewisham
    #scraper = NewhamScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/01361/FUL') # Newham
    #scraper = WestminsterScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/07236/FULL') # Westminster

    #res = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('10/08/2011'))
    #print res, len(res)
    
    


