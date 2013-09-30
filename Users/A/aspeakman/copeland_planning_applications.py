# this is a scraper of Copeland planning applications for use by Openly Local

# note the source data are weekly PDF lists

# records cannot be accessed or updated on an individual basis

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import urllib
import copy

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

class CopelandScraper(base.PeriodScraper):

    START_SEQUENCE = '2010-06-01'
    MAX_ID_BATCH = 200 # max application ids to fetch in one go
    PERIOD_TYPE = 'Friday'
    MIN_DAYS = 60 # min number of days to get when gathering current ids = matches number of update days because no other updating done

    #search_url = 'http://www.copelandbc.gov.uk/PDF/d_weekly_list_%d_%m_%y.pdf'
    search_url = 'http://www.copeland.gov.uk/sites/default/files/attachments/d_weekly_list_%d_%m_%y.pdf'
    scrape_ids1 = """
    {* 
    <text> App No </text> <text> {{ [records].uid }} </text>
    <text> Received </text> <text> {{ [records].date_received }} </text>
    <text> Proposal </text> <text> {{ [records].description }} </text>
    <text> Case Officer </text> <text> {{ [records].case_officer }} </text>
    <text> Site </text> <text> {{ [records].address }} </text>
    <text> Parish </text> <text> {{ [records].parish }} </text>
    <text> Applicant </text> <text> {{ [records].applicant_name }} </text>
    <text> Map Ref </text> <text> {{ [records].os_map_ref }} </text>
    <text> Address </text> <text> {{ [records].applicant_address }} </text>
    <text> Agent </text> <text> {{ [records].agent_name }} </text>
    <text> Address </text> <text> {{ [records].agent_address }} </text>
    *}
    """
    scrape_ids2 = """
    {*
    <text> App No </text> <text> {{ [records].uid }} </text>
    <text> Received </text> <text> {{ [records].date_received }} </text>
    <text> Proposal </text> <text> {{ [records].description }} </text>
    <text> Case Officer </text> <text> {{ [records].case_officer }} </text>
    <text> Site </text> <text> {{ [records].address }} </text>
    <text> Parish </text> <text> {{ [records].parish }} </text>
    <text> Applicant </text> <text> {{ [records].applicant_name }} </text>
    <text> Address </text> <text> {{ [records].applicant_address }} </text>
    <text> Agent </text> <text> {{ [records].agent_name }} </text>
    <text> Address </text> <text> {{ [records].agent_address }} </text>
    *}
    """

    def get_id_period (self, date):

        from_iso_dt, to_iso_dt = util.inc_dt(date.strftime(util.ISO8601_DATE), util.ISO8601_DATE, self.PERIOD_TYPE)
        from_dt = util.get_dt(from_iso_dt, util.ISO8601_DATE)
        to_dt = util.get_dt(to_iso_dt, util.ISO8601_DATE)

        url_date = to_dt.strftime(self.search_url)
        if self.DEBUG: print url_date
        try:
            response = self.br.open(url_date)
        except:
            response = None

        final_result = []
        if response:
            pdfxml = scraperwiki.pdftoxml(response.read())
            if self.DEBUG: print pdfxml
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids1, pdfxml, url)
            if not result or not result.get('records'):
                result = scrapemark.scrape(self.scrape_ids2, pdfxml, url)
            if result and result.get('records'):
                for rec in result['records']:
                    rec['url'] = url_date
                    rec['start_date'] = rec['date_received']
                    try:
                        map_ref_list = rec['os_map_ref'].split()
                        rec['easting'] = map_ref_list[0]
                        rec['northing'] = map_ref_list[1]
                        del rec['os_map_ref']
                    except:
                        pass
                self.clean_ids(result['records'])
                for rec in result['records']: # note do this after record cleaning
                    rec['date_scraped'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
                final_result.extend(result['records'])
        #else:
        #    return [], None, None

        return final_result, from_dt, to_dt # note weekly result might some times be legitimately empty

    # scrape detailed information on one record via its access URL
    def get_detail_from_url (self, url):
        return None

    # scrape detailed information on one record given its HTML and URL
    def get_detail (self, html, url, scrape_data_block = None, scrape_min_data = None, scrape_optional_data = []):
        return None

    # main run function - only do the ID update, cannot update individual records from PDF
    def run (self):
        self.gather_current_ids()
        self.gather_early_ids() 

if __name__ == 'scraper':

    scraper = CopelandScraper()
    scraper.run()

    #scraper.DEBUG = True
    # misc tests
    #result, dt1, dt2 = scraper.get_id_period(util.get_dt('03/01/2012'))
    #print len(result), result, dt1, dt2
    

# this is a scraper of Copeland planning applications for use by Openly Local

# note the source data are weekly PDF lists

# records cannot be accessed or updated on an individual basis

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import urllib
import copy

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

class CopelandScraper(base.PeriodScraper):

    START_SEQUENCE = '2010-06-01'
    MAX_ID_BATCH = 200 # max application ids to fetch in one go
    PERIOD_TYPE = 'Friday'
    MIN_DAYS = 60 # min number of days to get when gathering current ids = matches number of update days because no other updating done

    #search_url = 'http://www.copelandbc.gov.uk/PDF/d_weekly_list_%d_%m_%y.pdf'
    search_url = 'http://www.copeland.gov.uk/sites/default/files/attachments/d_weekly_list_%d_%m_%y.pdf'
    scrape_ids1 = """
    {* 
    <text> App No </text> <text> {{ [records].uid }} </text>
    <text> Received </text> <text> {{ [records].date_received }} </text>
    <text> Proposal </text> <text> {{ [records].description }} </text>
    <text> Case Officer </text> <text> {{ [records].case_officer }} </text>
    <text> Site </text> <text> {{ [records].address }} </text>
    <text> Parish </text> <text> {{ [records].parish }} </text>
    <text> Applicant </text> <text> {{ [records].applicant_name }} </text>
    <text> Map Ref </text> <text> {{ [records].os_map_ref }} </text>
    <text> Address </text> <text> {{ [records].applicant_address }} </text>
    <text> Agent </text> <text> {{ [records].agent_name }} </text>
    <text> Address </text> <text> {{ [records].agent_address }} </text>
    *}
    """
    scrape_ids2 = """
    {*
    <text> App No </text> <text> {{ [records].uid }} </text>
    <text> Received </text> <text> {{ [records].date_received }} </text>
    <text> Proposal </text> <text> {{ [records].description }} </text>
    <text> Case Officer </text> <text> {{ [records].case_officer }} </text>
    <text> Site </text> <text> {{ [records].address }} </text>
    <text> Parish </text> <text> {{ [records].parish }} </text>
    <text> Applicant </text> <text> {{ [records].applicant_name }} </text>
    <text> Address </text> <text> {{ [records].applicant_address }} </text>
    <text> Agent </text> <text> {{ [records].agent_name }} </text>
    <text> Address </text> <text> {{ [records].agent_address }} </text>
    *}
    """

    def get_id_period (self, date):

        from_iso_dt, to_iso_dt = util.inc_dt(date.strftime(util.ISO8601_DATE), util.ISO8601_DATE, self.PERIOD_TYPE)
        from_dt = util.get_dt(from_iso_dt, util.ISO8601_DATE)
        to_dt = util.get_dt(to_iso_dt, util.ISO8601_DATE)

        url_date = to_dt.strftime(self.search_url)
        if self.DEBUG: print url_date
        try:
            response = self.br.open(url_date)
        except:
            response = None

        final_result = []
        if response:
            pdfxml = scraperwiki.pdftoxml(response.read())
            if self.DEBUG: print pdfxml
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids1, pdfxml, url)
            if not result or not result.get('records'):
                result = scrapemark.scrape(self.scrape_ids2, pdfxml, url)
            if result and result.get('records'):
                for rec in result['records']:
                    rec['url'] = url_date
                    rec['start_date'] = rec['date_received']
                    try:
                        map_ref_list = rec['os_map_ref'].split()
                        rec['easting'] = map_ref_list[0]
                        rec['northing'] = map_ref_list[1]
                        del rec['os_map_ref']
                    except:
                        pass
                self.clean_ids(result['records'])
                for rec in result['records']: # note do this after record cleaning
                    rec['date_scraped'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
                final_result.extend(result['records'])
        #else:
        #    return [], None, None

        return final_result, from_dt, to_dt # note weekly result might some times be legitimately empty

    # scrape detailed information on one record via its access URL
    def get_detail_from_url (self, url):
        return None

    # scrape detailed information on one record given its HTML and URL
    def get_detail (self, html, url, scrape_data_block = None, scrape_min_data = None, scrape_optional_data = []):
        return None

    # main run function - only do the ID update, cannot update individual records from PDF
    def run (self):
        self.gather_current_ids()
        self.gather_early_ids() 

if __name__ == 'scraper':

    scraper = CopelandScraper()
    scraper.run()

    #scraper.DEBUG = True
    # misc tests
    #result, dt1, dt2 = scraper.get_id_period(util.get_dt('03/01/2012'))
    #print len(result), result, dt1, dt2
    

