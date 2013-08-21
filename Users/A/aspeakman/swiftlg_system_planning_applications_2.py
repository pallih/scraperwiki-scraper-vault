# this imports the main SwiftLG system scraper

# there are 20 authorities using this system, they are all defined in the other scraper, but 10 are scraped here

import scraperwiki
import random
import sys

plan = scraperwiki.utils.swimport("swiftlg_system_planning_applications")

systems = {
    'MoleValley': 'MoleValleyScraper',
    'Newport': 'NewportScraper',
    'NorthDorset': 'NorthDorsetScraper',
    'Oxfordshire': 'OxfordshireScraper',
    'Pembrokeshire': 'PembrokeshireScraper',
    'Redbridge': 'RedbridgeScraper',
    #'Rochdale': 'RochdaleScraper', # now Idox
    'Rutland': 'RutlandScraper', # new
    'Slough': 'SloughScraper',
    'Snowdonia': 'SnowdoniaScraper', # National Park
    'SouthCambridgeshire': 'SouthCambridgeshireScraper',
    'Warrington': 'WarringtonScraper',
    'Warwickshire': 'WarwickshireScraper',
}

if __name__ == 'scraper':

    #scraperwiki.sqlite.execute("update Slough set date_scraped = null, start_date = null, address = null, status = null where length(status) > 255")
    #scraperwiki.sqlite.commit()
    #sys.exit()

    #scraperwiki.sqlite.execute("drop table if exists Rochdale")
    #scraperwiki.sqlite.commit()
    #scraper = plan.RochdaleScraper('Rochdale')
    #scraper.reset()
    #scraper.run()
    #sys.exit()
    #scraper = plan.WarwickshireScraper('Warwickshire')
    #scraper.reset()
    #scraper.run()
    #sys.exit()

    #scraperwiki.sqlite.execute("delete from swvariables where name like '%-Rochdale'")
    #scraperwiki.sqlite.commit()

    #scraper = plan.SloughScraper('Slough')
    #scraper.run()
    #sys.exit()

    sys_list = []
    for k, v in systems.items(): # get latest date scraped for each system
        sys_list.append( (k, v, scraperwiki.sqlite.get_var('latest-' + k)) )
    sort_sys = sorted(sys_list, key=lambda system: system[2]) # sort so least recent are first
    for auth in sort_sys[:6]: # do max 6 per run
        strexec = 'plan.' + auth[1] + "('" + auth[0] + "')"
        print "Scraping from:", strexec
        try:
            scraper = eval(strexec)
            scraper.run()
        except Exception as err:
            print "Error - skipping this authority -", str(err)
    print "Finished"

    #scraperwiki.sqlite.execute("drop table if exists xxx")
    #scraperwiki.sqlite.commit()
    #scraper = plan.RedbridgeScraper('xxx')
    #scraper.reset()
    #scraper = plan.WarwickshireScraper('Warwickshire')
    #scraper.reset()
    #scraper.DEBUG = True
    #scraper.gather_current_ids()
    
    #scraper = plan.WarwickshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('NBB/13CM001') # Warwickshire (low numbers)

    #res = scraper.get_id_batch(util.get_dt('01/01/2012'), util.get_dt('02/02/2013'))
    #print res, len(res)
    
