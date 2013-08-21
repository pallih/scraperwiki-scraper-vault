# this is a scraper of West Dunbartonshire planning applications for use by Openly Local

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import random
import urllib

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

class WestDunbartonshireScraper(base.DateScraper):

    MAX_ID_BATCH = 200 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 150 # max application details to scrape in one go
    BATCH_DAYS = 28 # batch size for each scrape - number of days to gather to produce at least one result each time
    MIN_DAYS = 28 # min number of days to get when gathering current ids

    search_url = 'http://www.west-dunbarton.gov.uk/uniform/dcsearch_app.asp'
    applic_url = 'http://www.west-dunbarton.gov.uk/uniform/dcdisplayfull.asp?vPassword=&View1=View&vUPRN='
    date_from_field = 'vDateRcvFr'
    date_to_field = 'vDateRcvTo'
    request_date_format = '%d/%m/%Y'
    search_form = 'publicdisplay'
    scrape_ids = """
    <h3>Property Search Results</h3>
    {* <table> <tr>
    <td /> <td> {{ [records].uid }} </td>
    </tr> </table> *}
    </div>
    """
    scrape_data_block = """
    <div class="document"> {{ block|html }} </div>
    """
    scrape_min_data = """
    <tr> <td> Reference Number </td> <td> {{ reference }} </td> </tr>
    <tr> <td> Address </td> <td> {{ address }} </td> </tr>
    <tr> <td> Proposal </td> <td> {{ description }} </td> </tr>
    <tr> <td> Date Received </td> <td> {{ date_received }} </td> </tr>
    <tr> <td> Date Valid </td> <td> {{ date_validated }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr> <td> Status </td> <td> {{ status }} </td> </tr>',
    '<tr> <td> Type of Application </td> <td> {{ application_type }} </td> </tr>',
    '<tr> <td> Development Type </td> <td> {{ development_type }} </td> </tr>',
    '<tr> <td> Officer </td> <td> {{ case_officer }} </td> </tr>',
    '<tr> <td> Decision Date </td> <td> {{ decision_date }} </td> </tr>',
    '<tr> <td> Committee Date </td> <td> {{ meeting_date }} </td> </tr>',
    '<tr> <td> Appeal Status </td> <td> {{ appeal_status }} </td> </tr>',
    '<tr> <td> Applicant Name </td> <td> {{ applicant_name }} </td> </tr>',
    '<tr> <td> Applicant Address </td> <td> {{ applicant_address }} </td> </tr>',
    '<tr> <td> Agent Name </td> <td> {{ agent_name }} </td> </tr>',
    '<tr> <td> Agent Address </td> <td> {{ agent_address }} </td> </tr>',
    '<tr> <td> Ward </td> <td> {{ ward_name }} </td> </tr>',
    '<tr> <td> Parish </td> <td> {{ parish }} </td> </tr>',
    ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)

        fields = {}
        fields [self.date_from_field] = date_from.strftime(self.request_date_format)
        fields [self.date_to_field] = date_to.strftime(self.request_date_format)
        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br)

        final_result = []
        if response:
            html = response.read()
            url = response.geturl()
            if self.DEBUG: print html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                for rec in result['records']:
                    rec['url'] = self.applic_url + urllib.quote_plus(rec['uid'])
                self.clean_ids(result['records'])
                final_result.extend(result['records'])

        return final_result

    def get_detail_from_uid (self, uid):
        url = self.applic_url + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    scraper = WestDunbartonshireScraper()
    scraper.run()

    # misc test calls
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('DC11/199')
    #result = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('18/09/2011'))
    #print len(result), result

    



