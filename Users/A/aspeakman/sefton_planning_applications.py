# this is a scraper of Sefton planning applications for use by Openly Local

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

class SeftonScraper(base.DateScraper):

    MAX_ID_BATCH = 250 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go

    search_url = 'http://forms.sefton.gov.uk/sefton.web.sefPlanningListsPDF/PlanningAppsListPDF.aspx'
    applic_url = 'http://www.sefton.gov.uk/default.aspx?page=5297'
    date_from_field = 'From'
    date_to_field = 'To'
    request_date_format = '%d/%m/%Y'
    ref_field = 'Template$ctl38$ctl00$TxtBoxAppRef'
    search_form = '0'
    ref_submit = 'Template$ctl38$ctl00$BtnFind'
    scrape_ids = """
    <body>
    {* <h3 />
    <p> <span> Ref No </span>
    <b> {{ [records].uid }} </b> </p>
    *}
    </body>
    """
    scrape_data_block = """
    <div id="content"> {{ block|html }} </div>
    """
    scrape_min_data = """
    <tr> <td> Application Ref </td> <td> {{ reference }} </td> </tr>
    <tr> <td> Valid Date </td> <td> {{ date_validated }} </td> </tr>
    <tr> <td> Address </td> <td> {{ address }} </td> </tr>
    <tr> <td> Proposal </td> <td> {{ description }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr> <td> Registered Date </td> <td> {{ consultation_start_date }} (start of notification period) </td> </tr>',
    '<tr> <td> Earliest Decision </td> <td> {{ consultation_end_date }} (end of notification period) </td> </tr>',
    '<tr> <td> Development Type </td> <td> {{ development_type }} </td> </tr>',
    '<tr> <td> Case Officer </td> <td> {{ case_officer }} </td> </tr>',
    '<tr> <td> Decision Level </td> <td> {{ decided_by }} </td> </tr>',
    '<tr> <td> Expiry Date </td> <td> {{ application_expires_date }} </td> </tr>',
    """<tr> <td> Decision Date </td> <td> {{ decision_date }} </td> </tr>
    <tr> <td> Decision </td> <td> {{ decision }} </td> </tr>""",
    '<tr> <td> Applicant </td> <td> {{ applicant_name }} </td> </tr>',
    '<tr> <td> Agent </td> <td> {{ agent_name }} - {{ agent_address }} </td> </tr>',
    '<tr> <td> Ward </td> <td> {{ ward_name }} </td> </tr>',
    ]

    def get_id_batch (self, date_from, date_to):

        fields = {}
        fields[self.date_from_field] = date_from.strftime(self.request_date_format)
        fields[self.date_to_field] = date_to.strftime(self.request_date_format)
        response = util.open_url(self.br, self.search_url, fields, 'GET')

        final_result = []
        if response:
            html = response.read()
            url = response.geturl()
            if self.DEBUG: print html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])

        return final_result

    def get_detail_from_uid (self, uid):

        response = self.br.open(self.applic_url)

        fields = { self.ref_field: uid}
        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br, self.ref_submit)

        if response:
            html = response.read()
            url = response.geturl()
            if self.DEBUG: print html
        else:
            return None

        return self.get_detail(html, url)

if __name__ == 'scraper':

    scraper = SeftonScraper()
    scraper.run()

    # misc test calls
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('S/2011/1013')
    #result = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('18/08/2011'))
    #print len(result), result

    



