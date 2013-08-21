# this is a scraper of Swale planning applications for use by Openly Local

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

class SwaleScraper(base.PeriodScraper):

    START_SEQUENCE = '2010-01-05'
    MAX_ID_BATCH = 250 # max application ids to fetch in one go
    PERIOD_TYPE = 'Monday'
    MIN_DAYS = 60 # min number of days to get when gathering current ids = matches number of update days because no other updating done

    search_url1 = 'http://www.swale.gov.uk/weekly-planning-list-%-d-%B-%Y/'
    search_url2 = 'http://archive.swale.gov.uk/weekly-planning-%-d-%B-%Y'
    search_url3 = 'http://archive.swale.gov.uk/assets/Planning-General/Planning-Applications-2010/%B-%-d-%Y.pdf'
    scrape_ids1 = """
    <div id="Content-Resident">
    {* <table>
    <tr> {{ [records].parish }} </tr>
    <tr> <td> Application Ref </td> <td> {{ [records].uid }} </td> <td> Case Officer </td> <td> {{ [records].case_officer }} </td> </tr>
    <tr> <td> Location </td> <td> {{ [records].address }} </td> </tr>
    <tr> <td> Proposal </td> <td> {{ [records].description }} </td> </tr>
    <tr> <td> Applicants Name </td> <td> {{ [records].applicant_name }} </td> </tr>
    <tr> <td /> <td /> <td> {{ [records].agent_name }} , {{ [records].agent_address }} </td> </tr>
    </table> *}
    </div>
    """
    scrape_ids1a = """
    <div id="Content-Resident">
    {* <table>
    <tr> {{ [records].parish }} </tr>
    <tr> <td> Application Ref </td> <td> {{ [records].uid }} </td> <td> Case Officer </td> <td> {{ [records].case_officer }} </td> </tr>
    <tr> <td> Location </td> <td> {{ [records].address }} </td> </tr>
    <tr> <td> Proposal </td> <td> {{ [records].description }} </td> </tr>
    <tr> <td> Applicants Name </td> <td> {{ [records].applicant_name }} </td> </tr>
    <tr> <td /> <td> {{ [records].agent_name }} , {{ [records].agent_address }} </td> </tr>
    </table> *}
    </div>
    """
    scrape_ids2 = """
    <div id="Content-Resident">
    {* 
    <h3> {{ [records].parish }} </h3> <table>
    <tr> <td> Application Ref </td> <td> {{ [records].uid }} </td> <td> Case Officer </td> <td> {{ [records].case_officer }} </td> </tr>
    <tr> <td> Location </td> <td> {{ [records].address }} </td> </tr>
    <tr> <td> Proposal </td> <td> {{ [records].description }} </td> </tr>
    <tr> <td> Applicants Name </td> <td> {{ [records].applicant_name }} </td> </tr>
    <tr> <td /> <td> {{ [records].agent_name }} , {{ [records].agent_address }} </td> </tr>
    </table> *}
    </div>
    """
    scrape_ids3 = """
    <b>Swale Borough Council </b>
    {*
    <text> <b> {{ [records].parish }} </b> </text>
    <text> Application Ref </text> <text> {{ [records].uid }} </text> 
    <text> Case Officer </text> <text> {{ [records].case_officer }} </text>
    <text> Location </text> <text> {{ [records].address }} </text>
    <text> Proposal </text> <text> {{ [records].description }} </text>
    <text> Applicants Name </text> <text> {{ [records].applicant_name }} </text>
    <text> Agent </text> <text> {{ [records].agent_name }} , {{ [records].agent1 }} </text> <text> {{ [records].agent2 }} </text>
    *}
    """

    def get_id_period (self, date):

        from_iso_dt, to_iso_dt = util.inc_dt(date.strftime(util.ISO8601_DATE), util.ISO8601_DATE, self.PERIOD_TYPE)
        from_dt = util.get_dt(from_iso_dt, util.ISO8601_DATE)
        to_dt = util.get_dt(to_iso_dt, util.ISO8601_DATE)

        url_date = to_dt.strftime(self.search_url1)
        if self.DEBUG: print url_date
        try:
            response = self.br.open(url_date)
        except:
            url_date = to_dt.strftime(self.search_url2)
            if self.DEBUG: print url_date
            try:
                response = self.br.open(url_date)
            except:
                url_date = to_dt.strftime(self.search_url3)
                if self.DEBUG: print url_date
                try:
                    response = self.br.open(url_date)
                except:
                    response = None

        final_result = []
        if response:
            html = response.read()
            if self.DEBUG: print html
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids1, html, url)
            if not result or not result.get('records'):
                result = scrapemark.scrape(self.scrape_ids1a, html, url)
            if not result or not result.get('records'):
                result = scrapemark.scrape(self.scrape_ids2, html, url)
            if not result or not result.get('records'):
                pdfxml = scraperwiki.pdftoxml(html)
                if self.DEBUG: print pdfxml
                result = scrapemark.scrape(self.scrape_ids3, pdfxml, url)     
            if result and result.get('records'):
                for rec in result['records']:
                    rec['url'] = url_date
                    rec['date_received'] = to_iso_dt
                    rec['start_date'] = to_iso_dt
                    if rec.get('agent1'):
                        if rec.get('agent2'):
                            rec['agent_address'] = rec['agent1'] + ' ' + rec['agent2']
                        else:
                            rec['agent_address'] = rec['agent1']
                        del rec['agent1']
                        if 'agent2' in rec: del rec['agent2']
                self.clean_ids(result['records'])
                for rec in result['records']: # note do this after record cleaning
                    rec['date_scraped'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
                final_result.extend(result['records'])
        #else:
        #    return [], None, None

        return final_result, from_dt, to_dt 

    # scrape detailed information on one record via its access URL
    def get_detail_from_url (self, url):
        return None

    # scrape detailed information on one record given its HTML and URL
    def get_detail (self, html, url, scrape_data_block = None, scrape_min_data = None, scrape_optional_data = []):
        return None

    # main run function - only do the ID update, cannot update individual records from source
    def run (self):
        self.gather_current_ids()
        self.gather_early_ids()

if __name__ == 'scraper':

    #util.rename_column('swdata', 'agent2', None)
    #sys.exit()

    scraper = SwaleScraper()
    scraper.run()

    #scraper.DEBUG = True
    # misc tests
    #result, dt1, dt2 = scraper.get_id_period(util.get_dt('01/03/2013'))
    #result, dt1, dt2 = scraper.get_id_period(util.get_dt('01/03/2010'))
    #print len(result), result, dt1, dt2
    
