# this imports the main PlanningExplorer system scraper

# there are 24 authorities using this system, they are all defined in the other scraper, but 12 are scraped here

import scraperwiki
import random
import sys

plan = scraperwiki.utils.swimport("planningexplorer_system_planning_applications")

systems = {
    'Mendip': 'MendipScraper',
    'Merton': 'MertonScraper',
    'NorthYorkMoors': 'NorthYorkMoorsScraper', # National Park
    'Runnymede': 'RunnymedeScraper',
    'SouthLanarkshire': 'SouthLanarkshireScraper',
    #'SouthNorfolk': 'SouthNorfolkScraper', # now Idox
    'SouthTyneside': 'SouthTynesideScraper',
    'Swansea': 'SwanseaScraper',
    'Tamworth': 'TamworthScraper',
    'Trafford': 'TraffordScraper',
    'WalthamForest': 'WalthamForestScraper',
    'Wandsworth': 'WandsworthScraper',
    'Wiltshire': 'WiltshireScraper',
     }


if __name__ == 'scraper':

    #scraper = plan.WiltshireScraper()
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
