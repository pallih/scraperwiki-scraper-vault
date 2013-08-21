# this is a scraper of Hounslow planning applications for use by Openly Local

# also see Kingston on Thames

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import random
import urllib
import urlparse
import copy

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

class HounslowScraper(base.DateScraper):

    ck = [{
        'name': 'LBHSupportCookies',
        'value': 'true',
        'domain': 'planning.hounslow.gov.uk',
        },
        {
        'name': 'LBHPlanningAccept',
        'value': 'true',
        'domain': 'planning.hounslow.gov.uk',
        }]
    date_from_field = 'txt_RecFrom'
    date_to_field = 'txt_RecTo'
    search_url = 'http://planning.hounslow.gov.uk/planning_search.aspx'
    applic_url = 'http://planning.hounslow.gov.uk/Planning_CaseNo.aspx'

    ref_field = 'txt_Alt_No'
    search_form = 'Form1'
    search_fields = { 'ddLimit': '500' } # max 500 records on one page
    search_submit = 'btn_Search'

    scrape_ids = """
    <form> <table />
    {* <table>
    <tr> </tr>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].reference }} </a> {{ [records].uid }} <br> </td>
    </table> *}
    </form>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <form id="Form1"> {{ block|html }} </form>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <span id="lbl_APPS"> System Reference: {{ reference }} Planning Reference: {{ uid }} <a /> </span>
    <span id="lbl_Site_description"> {{ address }} <a /> </span>
    <span id="lbl_Date_Rec"> {{ date_received }} </span>
    <span id="lbl_Proposal"> {{ description }} </span>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<span id="lbl_Date_Val"> {{ date_validated }} </span>',
    '<span id="lbl_App_Type"> {{ application_type }} </span>',
    '<span id="lbl_Ward"> {{ ward_name }} </span>',
    '<span id="lbl_Officer"> {{ case_officer }} </span>',
    '<span id="lbl_Status"> {{ decision }} </span>',
    '<span id="lbl_Dec_Level"> {{ decided_by }} </span>',
    '<span id="lbl_Target_Date"> {{ target_decision_date }} </span>',
    '<span id="lbl_Committee_Date"> {{ meeting_date }} </span>',
    '<span id="lbl_Applic_Name"> {{ applicant_name }} </span>',
    '<span id="lbl_Agent_Name"> {{ agent_name }} </span>',
    '<span id="lbl_Agent_Address"> {{ agent_address }} </span>',
    '<span id="lbl_Agent_Phone"> {{ agent_tel }} </span>',
    '<span id="lbl_Applic_Address"> {{ applicant_address }} </span>',
    '<span id="lbl_DECISIONNOTICESENTDATE"> {{ decision_issued_date }} </span>',
    '<span id="lbl_APPEAL_LODGED_DATE"> {{ appeal_date }} </span>',
    '<span id="lbl_P_APPEALS_DECISION"> {{ appeal_result }} </span>',
    '<span id="lbl_P_APPEALS_DECISIONDATE"> {{ appeal_decision_date }} </span>',
    ]

    def __init__(self, table_name = None):
        base.DateScraper.__init__(self, table_name)
        if self.ck:
            for tk in self.ck:
                util.set_cookie(self.cj, tk['name'], tk['value'], tk.get('domain'), tk.get('path', '/'))   

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)

        fields = {}
        fields.update(self.search_fields)
        fields [self.date_from_field] = date_from.strftime(self.request_date_format)
        fields [self.date_to_field] = date_to.strftime(self.request_date_format)
        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br, self.search_submit)

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
        
        try:
            response = self.br.open(self.search_url)
            fields = { self.ref_field: uid }
            util.setup_form(self.br, self.search_form, fields)
            if self.DEBUG: print self.br.form
            response = util.submit_form(self.br, self.search_submit)

            html = response.read()
            if self.DEBUG: print html
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            self.clean_ids(result['records'])
            url = result['records'][0]['url']
        except:
            return None

        return self.get_detail_from_url(url)

    def get_detail_from_reference (self, uid):
        url = self.applic_url + '?strCASENO=' + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    scraper = HounslowScraper()
    #scraper.DEBUG = True
    scraper.run()

    #print scraper.get_detail_from_reference ('P/2012/2353') # Hounslow OK
    #print scraper.get_detail_from_uid ('00248/480/P1')

    #result = scraper.get_id_batch(util.get_dt('08/08/2012'), util.get_dt('18/08/2012'))
    #print len(result), result

    


