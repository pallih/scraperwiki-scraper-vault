# this is a scraper of Kingston on Thames planning applications for use by Openly Local

# also see Hounslow

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

class KingstonOnThamesScraper(base.DateScraper):

    MAX_ID_BATCH = 350 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 250 # max application details to scrape in one go
    ID_ORDER = "CASE uid WHEN substr(uid, 1, 2) < '50' THEN '20' || uid ELSE '19' || uid END desc"

    date_from_field = 'wdDateValidFrom_input'
    date_to_field = 'wdDateValidTo_input'
    ref_field = 'txt_App_No'
    search_form = 'Form1'
    search_fields = { 'ddLimit': '500' } # max 500 records on one page
    search_submit = 'btn_Search'
    request_date_format = '%m/%d/%Y'
    search_url = 'http://maps.kingston.gov.uk/isis_main/Planning/Planning_Search.aspx'

    scrape_ids = """
    <form> <table />
    {* <table>
    <tr> </tr>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    </table> *}
    </form>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <form id="Form1"> {{ block|html }} </form>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <span id="lbl_APPS"> {{ reference }} </span>
    <span id="lbl_Address"> {{ address }} </span>
    <span id="lbl_Date_Rec"> {{ date_received }} </span>
    <span id="lbl_Date_Val"> {{ date_validated }} </span>
    <span id="lbl_Proposal"> {{ description }} </span>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<span id="lbl_App_Type"> {{ application_type }} </span>',
    '<span id="lbl_Neighbourhood"> {{ district }} </span>',
    '<span id="lbl_Ward"> {{ ward_name }} </span>',
    '<span id="lbl_Officer"> {{ case_officer }} </span>',
    '<span id="lbl_Officer"> {{ case_officer }} </span>',
    '<span id="lbl_Status"> {{ status }} </span>',
    '<span id="lbl_Dec_Level"> {{ decided_by }} </span>',
    '<span id="lbl_Target_Date"> {{ target_decision_date }} </span>',
    '<span id="lbl_Committee_Date"> {{ meeting_date }} </span>',
    '<span id="lbl_Applic_Name"> {{ applicant_name }} </span>',
    '<span id="lbl_Agent_Name"> {{ agent_name }} </span>',
    '<span id="lbl_Agent_Address"> {{ agent_address }} </span>',
    '<span id="lbl_Agent_Phone"> {{ agent_tel }} </span>',
    '<span id="lbl_Applic_Address"> {{ applicant_address }} </span>',
    ]

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
            fields = { self.ref_field: uid[0:8] } # strip out last part of non-numeric part of uid
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

if __name__ == 'scraper':

    scraper = KingstonOnThamesScraper()
    scraper.run()

    # misc test calls
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('12/10213/FUL') # KingstonOnThames OK
    #result = scraper.get_id_batch(util.get_dt('08/08/2012'), util.get_dt('18/08/2012'))
    #print len(result), result

    


