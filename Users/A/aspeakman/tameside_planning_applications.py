# this is a scraper of Tameside planning applications for use by Openly Local

# note no URL for direct access to applications

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

class TamesideScraper(base.DateScraper):

    START_SEQUENCE = '2007-01-01'
    MAX_ID_BATCH = 350 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 250 # max application details to scrape in one go

    search_url = 'http://public.tameside.gov.uk/plan/f422planapp.asp'
    date_from_field = {
        'day': 'F08_Fdd',
        'month': 'F09_Fmm',
        'year': 'F10_Fyyyy',
        }
    date_to_field = {
        'day': 'F11_Tdd',
        'month': 'F12_Tmm',
        'year': 'F13_Tyyyy',
        }
    ref_field = 'F01_AppNo'
    search_fields = { 'F02_District': [ '99' ], }
    next_form = 'form3'
    next_fields = { 'submit': 'More' }
    request_date_format = '%d/%m/%Y'
    search_form = '1'
    search_submit = 'submit'
    scrape_ids = """
    <div class="content1">
    {* <table> <tr> <td> Application Number </td> <td> {{ [records].uid }} </td> </tr>
    </table> *}
    </div>
    """
    scrape_data_block = """
    <form action="f422planapp.asp"> {{ block|html }} </table>
    """
    scrape_min_data = """
    <tr> <td> Application Number </td> <td> {{ reference }} </td> <td> Date of Application </td> <td> {{ date_validated }} </td> </tr>
    <tr> <td> Proposal </td> <td> {{ description }} </td> </tr>
    <tr> <td> Site </td> <td> {{ address }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr> <td> Case Officer </td> <td> {{ case_officer }} </td> </tr>',
    '<tr> <td> Status </td> <td> {{ status }} </td> </tr>',
    '<tr> <td> Applicant </td> <td> {{ applicant_name }} </td> <td> {{ applicant_address|html }} </td> </tr>',
    '<input name="AgentName0" value ="{{ agent_name }}">',
    '<input name="AgentAddress0" value ="{{ agent_address }}">',
    '<input name="Decision0" value"{{ decision }}">',
    '<input name="DecisionDate0" value=" On {{ decision_date }}">',
    '<input name="AppRec0" value="{{ date_received }}">',
    '<input name="AppVal0" value="{{ date_validated }}">',
    '<input name="StartCons0" value="{{ consultation_start_date }}">',
    '<input name="TargetDec0" value="{{ target_decision_date }}">',
    '<input name="ExpiryDate0" value="{{ application_expires_date }}">',
    ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)

        fields = self.search_fields
        date_from = date_from.strftime(self.request_date_format)
        date_parts = date_from.split('/')
        fields [self.date_from_field['day']] = date_parts[0]
        fields [self.date_from_field['month']] = date_parts[1]
        fields [self.date_from_field['year']] = date_parts[2]
        date_to = date_to.strftime(self.request_date_format)
        date_parts = date_to.split('/')
        fields [self.date_to_field['day']] = date_parts[0]
        fields [self.date_to_field['month']] = date_parts[1]
        fields [self.date_to_field['year']] = date_parts[2]

        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br, self.search_submit)
        
        final_result = []
        while response:
            url = response.geturl()
            html = response.read()
            if self.DEBUG: print html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            else:
                break
            try:
                util.setup_form(self.br, self.next_form, self.next_fields)
                if self.DEBUG: print self.br.form
                response = util.submit_form(self.br)
            except:
                break
            
        return final_result

    def get_detail_from_uid (self, uid):
        try:
            response = self.br.open(self.search_url)
            fields = { self.ref_field: uid }
            util.setup_form(self.br, self.search_form, fields)
            if self.DEBUG: print self.br.form
            response = util.submit_form(self.br, self.search_submit)
            html = response.read()
            url = response.geturl()
            if self.DEBUG: print html
            return self.get_detail(html, url)
        except:
            return None

if __name__ == 'scraper':

    scraper = TamesideScraper()
    scraper.run()

    # misc test calls
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/00616/FUL')
    #result = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('08/09/2011'))
    #print len(result), result

    



