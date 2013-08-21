# this is a scraper of Wokingham planning applications for use by Openly Local

#Seems to have 2 separate lists ->
#Status = 1 = current undecided applications
#Status = 2 = historical decided applications

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import urllib

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

class WokinghamScraper(base.PeriodScraper):

    MAX_ID_BATCH = 250 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go
    PERIOD_TYPE = 'Month' 

    date_field = { 'month': 'Month', 'year': 'Year' }
    query_fields = {  'pgid': '1813', 'tid': '147' }
    scrape_next_link = """
    <div class="PageNavBar"> <strong /> 
    <a href="{{ next_link }}" /> </div>
    """
    request_date_format = '%-d/%-m/%Y'
    search_url = 'http://www2.wokingham.gov.uk/sys_upl/templates/BT_WOK_PlanningApplication/BT_WOK_PlanningApplication_details.asp'
    applic_url = 'http://www2.wokingham.gov.uk/sys_upl/templates/BT_WOK_PlanningApplication/BT_WOK_PlanningApplication_details.asp?action=DocumentView&pgid=22472&tid=176'
    scrape_ids = """
    <div id="template-zone">
        {* <table summary="*"> 
        <tr> Application No: {{ [records].uid }} </tr>
        <tr> Plans and Documents: <a href="{{ [records].url|abs }}" /> </tr>
        </table>  *}
    </div>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="content-inner">  {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <table summary="*">
    <tr> Application No: {{ reference }} </tr>
    <tr> Location: {{ address }} </tr>
    <tr> Received Date: {{ date_received }} </tr>
    <tr> Valid Date: {{ date_validated }} </tr>
    <tr> Proposal: {{ description }} </tr>
    </table>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<table summary="*"> <tr> Consultation Start Date: {{ consultation_start_date }} </tr> </table>',
    '<table summary="*"> <tr> Deadline for Comments: {{ consultation_end_date }} </tr> </table>',
    '<table summary="*"> <tr> Planning Officer: {{ case_officer }} </tr> </table>',
    '<table summary="*"> <tr> Decision: {{ decision }} </tr> </table>',
    '<table summary="*"> <tr> Decision Date: {{ decision_date }} </tr> </table>',
    '<table summary="*"> <tr> Appeal Received Date: {{ appeal_date }} </tr> </table>',
    '<div class="SmallTitle"> {{ parish }} Parish </div>',
    ]

    def get_id_period (self, date):

        from_iso_dt, to_iso_dt = util.inc_dt(date.strftime(util.ISO8601_DATE), util.ISO8601_DATE, self.PERIOD_TYPE)
        from_dt = util.get_dt(from_iso_dt, util.ISO8601_DATE)
        to_dt = util.get_dt(to_iso_dt, util.ISO8601_DATE)

        fields = self.query_fields

        date = date.strftime(self.request_date_format)
        date_parts = date.split('/')
        #fields [self.date_from_field['day']] = date_parts[0]
        fields [self.date_field['month']] = date_parts[1]
        fields [self.date_field['year']] = date_parts[2]

        final_result = []
        
        fields['Status'] = '1'
        response = util.open_url(self.br, self.search_url, fields, 'GET')
        while response:
            html = response.read()
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            try:
                result = scrapemark.scrape(self.scrape_next_link, html, url)
                response = self.br.open(result['next_link'])
            except:
                response = None
        
        fields['Status'] = '2'
        response = util.open_url(self.br, self.search_url, fields, 'GET')
        while response:
            html = response.read()
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            try:
                result = scrapemark.scrape(self.scrape_next_link, html, url)
                response = self.br.open(result['next_link'])
            except:
                response = None

        if final_result:
            return final_result, from_dt, to_dt
        else:
            return [], None, None # monthly scraper - so empty result is always invalid

    def get_detail_from_uid (self, uid):
        url = self.applic_url + '&ApplicationCode=' + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    scraper = WokinghamScraper()
    scraper.run()

    #scraper.DEBUG = True
    # misc tests
    #print scraper.get_detail_from_uid ('F/2010/2048')
    #result = scraper.get_id_period(util.get_dt('01/03/2012'))
    #print result
    #print util.inc_dt('2010-02-01', util.ISO8601_DATE, 'Month')
    #print "Found " + str(len(result)) + " ids for Mar 2012"
    #print scraper.gather_ids('2010-02-01')
    #print scraper.gather_ids(None, None)
    #scraper.gather_current_ids()
