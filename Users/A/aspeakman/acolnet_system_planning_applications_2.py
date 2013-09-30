# this imports the main AcolNet system scraper

# there are 29 authorities using this system, they are all defined in the other scraper, but 15 are scraped here

import scraperwiki
import random
import sys
import gc

plan = scraperwiki.utils.swimport("acolnet_system_planning_applications")

systems = {
    'Harlow': 'HarlowScraper',
    'Havant': 'HavantScraper',
    'Hertsmere': 'HertsmereScraper',
    #'Lewisham': 'LewishamScraper', # now Idox
    'Medway': 'MedwayScraper',
    #'NewForest': 'NewForestScraper', now Idox
    'NewForestPark': 'NewForestParkScraper', # National Park
    'NorthHertfordshire': 'NorthHertfordshireScraper',
    'NorthNorfolk': 'NorthNorfolkScraper',
    'NorthWiltshire': 'NorthWiltshireScraper', 
    'Renfrewshire': 'RenfrewshireScraper',
    'Southwark': 'SouthwarkScraper',
    'Stockport': 'StockportScraper',
    'StokeOnTrent': 'StokeOnTrentScraper',
    'SuffolkCoastal': 'SuffolkCoastalScraper',
    'Wirral': 'WirralScraper',
     }

if __name__ == 'scraper':

    #scraper = plan.StokeOnTrentScraper('StokeOnTrent') 
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
            scraper = None
            gc.collect()
        except Exception as err:
            print "Error - skipping this authority -", str(err)
    print "Finished"


# this imports the main AcolNet system scraper

# there are 29 authorities using this system, they are all defined in the other scraper, but 15 are scraped here

import scraperwiki
import random
import sys
import gc

plan = scraperwiki.utils.swimport("acolnet_system_planning_applications")

systems = {
    'Harlow': 'HarlowScraper',
    'Havant': 'HavantScraper',
    'Hertsmere': 'HertsmereScraper',
    #'Lewisham': 'LewishamScraper', # now Idox
    'Medway': 'MedwayScraper',
    #'NewForest': 'NewForestScraper', now Idox
    'NewForestPark': 'NewForestParkScraper', # National Park
    'NorthHertfordshire': 'NorthHertfordshireScraper',
    'NorthNorfolk': 'NorthNorfolkScraper',
    'NorthWiltshire': 'NorthWiltshireScraper', 
    'Renfrewshire': 'RenfrewshireScraper',
    'Southwark': 'SouthwarkScraper',
    'Stockport': 'StockportScraper',
    'StokeOnTrent': 'StokeOnTrentScraper',
    'SuffolkCoastal': 'SuffolkCoastalScraper',
    'Wirral': 'WirralScraper',
     }

if __name__ == 'scraper':

    #scraper = plan.StokeOnTrentScraper('StokeOnTrent') 
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
            scraper = None
            gc.collect()
        except Exception as err:
            print "Error - skipping this authority -", str(err)
    print "Finished"


