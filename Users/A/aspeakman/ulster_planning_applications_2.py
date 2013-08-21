# this imports the main Ulster scraper (based on PublicAccess)

# there are 26 authorities using this system, they are all defined in the other scraper, but 13 are scraped here

import scraperwiki
from datetime import timedelta
import random
import sys
import gc

ulster = scraperwiki.utils.swimport("ulster_planning_applications")

systems = {
    #'Antrim': 'AntrimScraper',
    #'Ards': 'ArdsScraper',
    #'Armagh': 'ArmaghScraper',
    #'Ballymena': 'BallymenaScraper',
    #'Ballymoney': 'BallymoneyScraper',
    #'Banbridge': 'BanbridgeScraper',
    #'Belfast': 'BelfastScraper',
    #'Carrickfergus': 'CarrickfergusScraper',
    #'Castlereagh': 'CastlereaghScraper',
    #'Coleraine': 'ColeraineScraper',
    #'Cookstown': 'CookstownScraper',
    #'Craigavon': 'CraigavonScraper',
    #'Derry': 'DerryScraper',
    'Down': 'DownScraper',
    'Dungannon': 'DungannonScraper',
    'Fermanagh': 'FermanaghScraper',
    'Larne': 'LarneScraper',
    'Limavady': 'LimavadyScraper',
    'Lisburn': 'LisburnScraper',
    'Magherafelt': 'MagherafeltScraper',
    'Moyle': 'MoyleScraper',
    'NewryAndMourne': 'NewryAndMourneScraper',
    'Newtownabbey': 'NewtownabbeyScraper',
    'NorthDown': 'NorthDownScraper',
    'Omagh': 'OmaghScraper',
    'Strabane': 'StrabaneScraper',
}

if __name__ == 'scraper':

    #scraper = ulster.FermanaghScraper('Fermanagh')
    #scraper.replace_all_with('ulster_planning_applications', 'Fermanagh')
    #sys.exit()

    sys_list = []
    for k, v in systems.items(): # get latest date scraped for each system
        sys_list.append( (k, v, scraperwiki.sqlite.get_var('latest-' + k)) )
    sort_sys = sorted(sys_list, key=lambda system: system[2]) # sort so least recent are first
    for auth in sort_sys[:5]: # do max 5 per run
        strexec = 'ulster.' + auth[1] + "('" + auth[0] + "')"
        print "Scraping from:", strexec
        try:
            scraper = eval(strexec)
            scraper.run()
            scraper = None
            gc.collect()
        except Exception as err:
            print "Error - skipping this authority -", str(err)
    print "Finished"


