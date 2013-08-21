# this is a scraper for PublicAccess system planning applications for use by Openly Local

# this implements a sub-variant covering Northern Ireland

# there are 26 authorities using this system, all 26 are defined but only 13 are scraped here (see Ulster 2 for the rest)

import scraperwiki
from datetime import timedelta
import random
import sys
import gc

util = scraperwiki.utils.swimport("utility_library")
pa = scraperwiki.utils.swimport("publicaccess_system_planning_applications")

systems = {
    'Antrim': 'AntrimScraper',
    'Ards': 'ArdsScraper',
    'Armagh': 'ArmaghScraper',
    'Ballymena': 'BallymenaScraper',
    'Ballymoney': 'BallymoneyScraper',
    'Banbridge': 'BanbridgeScraper',
    'Belfast': 'BelfastScraper',
    'Carrickfergus': 'CarrickfergusScraper',
    'Castlereagh': 'CastlereaghScraper',
    'Coleraine': 'ColeraineScraper',
    'Cookstown': 'CookstownScraper',
    'Craigavon': 'CraigavonScraper',
    'Derry': 'DerryScraper',
    #'Down': 'DownScraper',
    #'Dungannon': 'DungannonScraper',
    #'Fermanagh': 'FermanaghScraper',
    #'Larne': 'LarneScraper',
    #'Limavady': 'LimavadyScraper',
    #'Lisburn': 'LisburnScraper',
    #'Magherafelt': 'MagherafeltScraper',
    #'Moyle': 'MoyleScraper',
    #'NewryAndMourne': 'NewryAndMourneScraper',
    #'Newtownabbey': 'NewtownabbeyScraper',
    #'NorthDown': 'NorthDownScraper',
    #'Omagh': 'OmaghScraper',
    #'Strabane': 'StrabaneScraper',
}

class NorthernIrelandScraper(pa.PublicAccessScraper):

    search_url = 'http://epicpublic.planningni.gov.uk/PublicAccess/zd/zdApplication/application_searchform.aspx'

    def get_id_batch (self, date_from, date_to): # end date is exclusive, not inclusive
        date_to = date_to + timedelta(days=1) # increment end date by one day
        return pa.PublicAccessScraper.get_id_batch(self, date_from, date_to)

class AntrimScraper(NorthernIrelandScraper):

    query_fields =  { 'srchlgdcode': 'LGDANT|Antrim' }

class ArdsScraper(NorthernIrelandScraper):

    query_fields =  { 'srchlgdcode': 'LGDARD|Ards' }

class ArmaghScraper(NorthernIrelandScraper):

    query_fields =  { 'srchlgdcode': 'LGDARM|Armagh' }

class BallymenaScraper(NorthernIrelandScraper):

    query_fields =  { 'srchlgdcode': 'LGDBMA|Ballymena' }

class BallymoneyScraper(NorthernIrelandScraper):

    query_fields =  { 'srchlgdcode': 'LGDBMY|Ballymoney' }

class BanbridgeScraper(NorthernIrelandScraper):

    query_fields =  { 'srchlgdcode': 'LGDBAN|Banbridge' }

class BelfastScraper(NorthernIrelandScraper):

    query_fields =  { 'srchlgdcode': 'LGDBEL|Belfast' }

class CarrickfergusScraper(NorthernIrelandScraper):

    query_fields =  { 'srchlgdcode': 'LGDCAR|Carrickfergus' }

class CastlereaghScraper(NorthernIrelandScraper):

    query_fields =  { 'srchlgdcode': 'LGDCAS|Castlereagh' }

class ColeraineScraper(NorthernIrelandScraper):

    query_fields =  { 'srchlgdcode': 'LGDCOL|Coleraine' }

class CookstownScraper(NorthernIrelandScraper):

    query_fields =  { 'srchlgdcode': 'LGDCOO|Cookstown' }

class CraigavonScraper(NorthernIrelandScraper):

    query_fields =  { 'srchlgdcode': 'LGDCRA|Craigavon' }

class DerryScraper(NorthernIrelandScraper):

    query_fields =  { 'srchlgdcode': 'LGDDER|Derry' }

class DownScraper(NorthernIrelandScraper):

    query_fields =  { 'srchlgdcode': 'LGDDOW|Down' }

class DungannonScraper(NorthernIrelandScraper):

    query_fields =  { 'srchlgdcode': 'LGDDUN|Dungannon' }

class FermanaghScraper(NorthernIrelandScraper):

    query_fields =  { 'srchlgdcode': 'LGDFER|Fermanagh' }

class LarneScraper(NorthernIrelandScraper):

    query_fields =  { 'srchlgdcode': 'LGDLAR|Larne' }

class LimavadyScraper(NorthernIrelandScraper):

    query_fields =  { 'srchlgdcode': 'LGDLIM|Limavady' }

class LisburnScraper(NorthernIrelandScraper):

    query_fields =  { 'srchlgdcode': 'LGDLIS|Lisburn' }

class MagherafeltScraper(NorthernIrelandScraper):

    query_fields =  { 'srchlgdcode': 'LGDMAG|Magherafelt' }

class MoyleScraper(NorthernIrelandScraper):

    query_fields =  { 'srchlgdcode': 'LGDMOY|Moyle' }

class NewryAndMourneScraper(NorthernIrelandScraper):

    query_fields =  { 'srchlgdcode': 'LGDNM|Newry and Mourne' }

class NewtownabbeyScraper(NorthernIrelandScraper):

    query_fields =  { 'srchlgdcode': 'LGDNEW|Newtownabbey' }

class NorthDownScraper(NorthernIrelandScraper):

    query_fields =  { 'srchlgdcode': 'LGDND|North Down' }

class OmaghScraper(NorthernIrelandScraper):

    query_fields =  { 'srchlgdcode': 'LGDOMA|Omagh' }

class StrabaneScraper(NorthernIrelandScraper):

    query_fields =  { 'srchlgdcode': 'LGDSTR|Strabane' }

if __name__ == 'scraper':

    #scraper = FermanaghScraper('Fermanagh')
    #scraper.clear_all()
    #sys.exit()

    sys_list = []
    for k, v in systems.items(): # get latest date scraped for each system
        sys_list.append( (k, v, scraperwiki.sqlite.get_var('latest-' + k)) )
    sort_sys = sorted(sys_list, key=lambda system: system[2]) # sort so least recent are first
    for auth in sort_sys[:5]: # do max 5 per run
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
    #scraper = AntrimScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('T/2011/0326/F') # Antrim OK
    #scraper = ArdsScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('X/2011/0544/F') # Ards OK
    #scraper = ArmaghScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('O/2011/0387/F') # Armagh OK
    #scraper = BelfastScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('Z/2011/0975/F') # Belfast OK

    #res = scraper.get_id_batch(util.get_dt('10/08/2011'), util.get_dt('23/08/2011'))
    #print res, len(res)
