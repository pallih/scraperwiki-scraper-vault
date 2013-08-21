# this imports the main AcolNet system scraper

# there are 28 authorities using this system, they are all defined in the other scraper, but 14 are scraped here

import scraperwiki
import random
import sys

plan = scraperwiki.utils.swimport("acolnet_system_planning_applications")

systems = {
    'Harlow': 'HarlowScraper',
    'Havant': 'HavantScraper',
    'Hertsmere': 'HertsmereScraper',
    'Lewisham': 'LewishamScraper',
    'Medway': 'MedwayScraper',
    'NewForest': 'NewForestScraper',
    'NorthHertfordshire': 'NorthHertfordshireScraper',
    'NorthNorfolk': 'NorthNorfolkScraper',
    'Renfrewshire': 'RenfrewshireScraper',
    'Southwark': 'SouthwarkScraper',
    'Stockport': 'StockportScraper',
    'StokeOnTrent': 'StokeOnTrentScraper',
    'SuffolkCoastal': 'SuffolkCoastalScraper',
    'Wirral': 'WirralScraper',
     }

if __name__ == 'scraper':

    alist = systems.keys()
    random.shuffle(alist)
    for auth in alist[:7]: # do max 7 per run
        strexec = 'plan.' + systems[auth] + "('" + auth + "')"
        print "Authority:", auth, strexec
        try:
            scraper = eval(strexec)
            scraper.run()
        except Exception as err:
            print "Error - skipping this authority -", str(err)
    print "Finished"

    #scraperwiki.sqlite.execute("drop table if exists xxx")
    #scraperwiki.sqlite.commit()
    #scraper = plan.xxxScraper('xxx')
    #scraper.reset()
    #scraper = plan.yyyScraper('yyy')
    #scraper.reset()
    #scraper.DEBUG = True
    #scraper.gather_current_ids()

