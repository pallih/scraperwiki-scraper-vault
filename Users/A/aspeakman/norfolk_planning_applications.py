# this is a scraper of Norfolk planning applications for use by Openly Local

# no dates in result, so we search on "Complete" date one day at a time and add the dates on each iteration

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

class NorfolkScraper(base.DateScraper):

    MAX_ID_BATCH = 150 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 100 # max application details to scrape in one go

    search_url = 'http://eplanning.norfolk.gov.uk/PlanAppSearch.aspx'
    applic_url = 'http://eplanning.norfolk.gov.uk/PlanAppDisp.aspx?AppNo='
    date_from_field = 'ctl00$ContentPlaceHolder1$txtCompleteDateFrom$dateInput'
    date_to_field = 'ctl00$ContentPlaceHolder1$txtCompleteDateTo$dateInput'
    scrape_next_submit = '<input class="rgPageNext" name="{{ next_submit }}">'
    request_date_format = '%Y-%m-%d-00-00-00'
    search_form = 'aspnetForm'
    scrape_max_recs = 'Back to Search Page {{ max_recs }} record(s) found.'
    date_type = 'date_validated'

    scrape_ids = """
    <table id="ctl00_ContentPlaceHolder1_gridResults_ctl00"> <tbody>
    {* <tr>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td> 
    <td> {{ [records].site_notice_start_date }} </td> 
    <td> {{ [records].consultation_end_date }} </td> 
    </tr> *}
    </tbody> </table>
    """
    scrape_data_block = """
    <div id="formContent"> {{ block|html }} </div>
    """
    scrape_min_data = """
    <input name="ctl00$ContentPlaceHolder1$txtAppNumber" value="{{ reference }}">
    <textarea name="ctl00$ContentPlaceHolder1$txtLocation"> {{ address }} </textarea>
    <textarea name="ctl00$ContentPlaceHolder1$txtProposal"> {{ description }} </textarea>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<input name="ctl00$ContentPlaceHolder1$txtStatus" value="{{ status }}">',
    '<input name="ctl00$ContentPlaceHolder1$txtDistrict" value="{{ district }}">',
    '<input name="ctl00$ContentPlaceHolder1$txtParish" value="{{ parish }}">',
    '<input name="ctl00$ContentPlaceHolder1$txtElecDiv" value="{{ ward_name }}">',
    '<input name="ctl00$ContentPlaceHolder1$txtEasting" value="{{ easting }}">',
    '<input name="ctl00$ContentPlaceHolder1$txtNorthing" value="{{ northing }}">',
    '<input name="ctl00$ContentPlaceHolder1$txtApplicantsName" value="{{ applicant_name }}">',
    '<input name="ctl00$ContentPlaceHolder1$txtAgentsName" value="{{ agent_name }}">',
    '<textarea name="ctl00$ContentPlaceHolder1$txtApplicantsAddress"> {{ applicant_address }} </textarea>',
    '<textarea name="ctl00$ContentPlaceHolder1$txtAgentAddress"> {{ agent_address }} </textarea>',
    '<input name="ctl00$ContentPlaceHolder1$txtCommitteDeleagated" value="{{ decided_by }}">',
    '<input name="ctl00$ContentPlaceHolder1$txtCommitteeDate" value="{{ meeting_date }}">',
    '<input name="ctl00$ContentPlaceHolder1$txtDecisionDate" value="{{ decision_date }}">',
    '<input name="ctl00$ContentPlaceHolder1$txtDecision" value="{{ decision }}">',
    '<input name="ctl00$ContentPlaceHolder1$txtAppealDate" value="{{ appeal_date }}">',
    '<input name="ctl00$ContentPlaceHolder1$txtAppealDecision" value="{{ appeal_result }}">',
    '<input name="ctl00$ContentPlaceHolder1$txtPlanningOfficer" value="{{ case_officer }}">',
    ]

    def get_id_batch (self, date_from, date_to):

        this_dt = date_from
        final_result = []

        while this_dt <= date_to:
    
            response = self.br.open(self.search_url)
    
            fields = {}
            fields [self.date_from_field] = this_dt.strftime(self.request_date_format)
            fields [self.date_to_field] = this_dt.strftime(self.request_date_format)
            util.setup_form(self.br, self.search_form, fields)
            if self.DEBUG: print self.br.form
            response = util.submit_form(self.br)
            html = response.read()
    
            try:
                result = scrapemark.scrape(self.scrape_max_recs, html)
                max_recs = int(result['max_recs'])
            except:
                max_recs = 0
            if self.DEBUG: print max_recs
    
            interim_result = []
            while response and len(interim_result) < max_recs:
                url = response.geturl()
                if self.DEBUG: print html
                result = scrapemark.scrape(self.scrape_ids, html, url)
                if result and result.get('records'):
                    for rec in result['records']:
                        rec[self.date_type] = fields[self.date_to_field]
                    self.clean_ids(result['records'])
                    interim_result.extend(result['records'])
                else:
                    break
                if len(interim_result) >= max_recs: break
                try:
                    result = scrapemark.scrape(self.scrape_next_submit, html)
                    next_submit = result['next_submit']
                    util.setup_form(self.br, self.search_form)
                    if self.DEBUG: print self.br.form
                    response = util.submit_form(self.br, next_submit)
                    html = response.read()
                except:
                    response = None

            final_result.extend(interim_result)
            this_dt += timedelta(days=1)

        return final_result

    def get_detail_from_uid (self, uid):
        url = self.applic_url + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    scraper = NorfolkScraper()
    scraper.run()

    # misc test calls
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('C/7/2011/7006')
    #result = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('19/09/2011'))
    #print len(result), result

    



# this is a scraper of Norfolk planning applications for use by Openly Local

# no dates in result, so we search on "Complete" date one day at a time and add the dates on each iteration

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

class NorfolkScraper(base.DateScraper):

    MAX_ID_BATCH = 150 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 100 # max application details to scrape in one go

    search_url = 'http://eplanning.norfolk.gov.uk/PlanAppSearch.aspx'
    applic_url = 'http://eplanning.norfolk.gov.uk/PlanAppDisp.aspx?AppNo='
    date_from_field = 'ctl00$ContentPlaceHolder1$txtCompleteDateFrom$dateInput'
    date_to_field = 'ctl00$ContentPlaceHolder1$txtCompleteDateTo$dateInput'
    scrape_next_submit = '<input class="rgPageNext" name="{{ next_submit }}">'
    request_date_format = '%Y-%m-%d-00-00-00'
    search_form = 'aspnetForm'
    scrape_max_recs = 'Back to Search Page {{ max_recs }} record(s) found.'
    date_type = 'date_validated'

    scrape_ids = """
    <table id="ctl00_ContentPlaceHolder1_gridResults_ctl00"> <tbody>
    {* <tr>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td> 
    <td> {{ [records].site_notice_start_date }} </td> 
    <td> {{ [records].consultation_end_date }} </td> 
    </tr> *}
    </tbody> </table>
    """
    scrape_data_block = """
    <div id="formContent"> {{ block|html }} </div>
    """
    scrape_min_data = """
    <input name="ctl00$ContentPlaceHolder1$txtAppNumber" value="{{ reference }}">
    <textarea name="ctl00$ContentPlaceHolder1$txtLocation"> {{ address }} </textarea>
    <textarea name="ctl00$ContentPlaceHolder1$txtProposal"> {{ description }} </textarea>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<input name="ctl00$ContentPlaceHolder1$txtStatus" value="{{ status }}">',
    '<input name="ctl00$ContentPlaceHolder1$txtDistrict" value="{{ district }}">',
    '<input name="ctl00$ContentPlaceHolder1$txtParish" value="{{ parish }}">',
    '<input name="ctl00$ContentPlaceHolder1$txtElecDiv" value="{{ ward_name }}">',
    '<input name="ctl00$ContentPlaceHolder1$txtEasting" value="{{ easting }}">',
    '<input name="ctl00$ContentPlaceHolder1$txtNorthing" value="{{ northing }}">',
    '<input name="ctl00$ContentPlaceHolder1$txtApplicantsName" value="{{ applicant_name }}">',
    '<input name="ctl00$ContentPlaceHolder1$txtAgentsName" value="{{ agent_name }}">',
    '<textarea name="ctl00$ContentPlaceHolder1$txtApplicantsAddress"> {{ applicant_address }} </textarea>',
    '<textarea name="ctl00$ContentPlaceHolder1$txtAgentAddress"> {{ agent_address }} </textarea>',
    '<input name="ctl00$ContentPlaceHolder1$txtCommitteDeleagated" value="{{ decided_by }}">',
    '<input name="ctl00$ContentPlaceHolder1$txtCommitteeDate" value="{{ meeting_date }}">',
    '<input name="ctl00$ContentPlaceHolder1$txtDecisionDate" value="{{ decision_date }}">',
    '<input name="ctl00$ContentPlaceHolder1$txtDecision" value="{{ decision }}">',
    '<input name="ctl00$ContentPlaceHolder1$txtAppealDate" value="{{ appeal_date }}">',
    '<input name="ctl00$ContentPlaceHolder1$txtAppealDecision" value="{{ appeal_result }}">',
    '<input name="ctl00$ContentPlaceHolder1$txtPlanningOfficer" value="{{ case_officer }}">',
    ]

    def get_id_batch (self, date_from, date_to):

        this_dt = date_from
        final_result = []

        while this_dt <= date_to:
    
            response = self.br.open(self.search_url)
    
            fields = {}
            fields [self.date_from_field] = this_dt.strftime(self.request_date_format)
            fields [self.date_to_field] = this_dt.strftime(self.request_date_format)
            util.setup_form(self.br, self.search_form, fields)
            if self.DEBUG: print self.br.form
            response = util.submit_form(self.br)
            html = response.read()
    
            try:
                result = scrapemark.scrape(self.scrape_max_recs, html)
                max_recs = int(result['max_recs'])
            except:
                max_recs = 0
            if self.DEBUG: print max_recs
    
            interim_result = []
            while response and len(interim_result) < max_recs:
                url = response.geturl()
                if self.DEBUG: print html
                result = scrapemark.scrape(self.scrape_ids, html, url)
                if result and result.get('records'):
                    for rec in result['records']:
                        rec[self.date_type] = fields[self.date_to_field]
                    self.clean_ids(result['records'])
                    interim_result.extend(result['records'])
                else:
                    break
                if len(interim_result) >= max_recs: break
                try:
                    result = scrapemark.scrape(self.scrape_next_submit, html)
                    next_submit = result['next_submit']
                    util.setup_form(self.br, self.search_form)
                    if self.DEBUG: print self.br.form
                    response = util.submit_form(self.br, next_submit)
                    html = response.read()
                except:
                    response = None

            final_result.extend(interim_result)
            this_dt += timedelta(days=1)

        return final_result

    def get_detail_from_uid (self, uid):
        url = self.applic_url + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    scraper = NorfolkScraper()
    scraper.run()

    # misc test calls
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('C/7/2011/7006')
    #result = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('19/09/2011'))
    #print len(result), result

    



