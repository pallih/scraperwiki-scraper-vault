# this is a scraper of South Northamptonshire planning applications for use by Openly Local

# also see Bournemouth

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

class SouthNorthamptonshireScraper(base.DateScraper):

    MAX_ID_BATCH = 250 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go

    search_url = 'http://snc.planning-register.co.uk/planappsrch.aspx?pageprefix=plan'
    date_from_field = 'ctl00$ctl00$MainContent$MainContent$txtDateReceivedFrom$dateInput'
    date_to_field = 'ctl00$ctl00$MainContent$MainContent$txtDateReceivedTo$dateInput'
    ref_field = 'ctl00$ctl00$MainContent$MainContent$txtAppNumber'
    search_fields = { '__EVENTTARGET': '', '__EVENTARGUMENT': '',  }
    next_target = 'ctl00$Mainpage$gridMain'
    request_date_format = '%Y-%m-%d-00-00-00'
    search_form = 'aspnetForm'
    search_submit = 'ctl00$ctl00$MainContent$MainContent$btnSearch'
    scrape_ids = """
    <table id="ctl00_ctl00_MainContent_MainContent_grdResults_ctl00"> <tbody>
    {* <tr> <td> <a href="{{ [records].url|abs }}">
    {{ [records].uid }} </a> </td>
    </tr> *}
    </tbody> </table>
    """
    scrape_max_recs = '<p> Your search returned the following results (a total of <b> {{ max_recs }} </b>).'
    scrape_next_submit = '<input class="rgPageNext" name="{{ next_submit }}">'
    scrape_data_block = """
    <div id="contenttext"> {{ block|html }} </div>
    """
    scrape_min_data = """
    <input name="ctl00$ctl00$MainContent$MainContent$txtAppNo" value="{{ reference }}">
    <textarea name="ctl00$ctl00$MainContent$MainContent$txtLocation"> {{ address }} </textarea>
    <textarea name="ctl00$ctl00$MainContent$MainContent$txtProposal"> {{ description }} </textarea>
    <input name="ctl00$ctl00$MainContent$MainContent$txtReceivedDate" value="{{ date_received }}">
    <input name="ctl00$ctl00$MainContent$MainContent$txtValidDate" value="{{ date_validated }}">
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<input name="ctl00$ctl00$MainContent$MainContent$txtParish" value="{{ parish }}">',
    '<input name="ctl00$ctl00$MainContent$MainContent$txtEasting" value="{{ easting }}">',
    '<input name="ctl00$ctl00$MainContent$MainContent$txtNorthing" value="{{ northing }}">',
    '<input name="ctl00$ctl00$MainContent$MainContent$txtStatus" value="{{ status }}">',
    '<input name="ctl00$ctl00$MainContent$MainContent$txtDecisionDate" value="{{ decision_date }}">',
    '<input name="ctl00$ctl00$MainContent$MainContent$txtCommitteeDate" value="{{ meeting_date }}">',
    '<input name="ctl00$ctl00$MainContent$MainContent$txtExpiryDate" value="{{ application_expires_date }}">',
    '<input name="ctl00$ctl00$MainContent$MainContent$txtType" value="{{ application_type }}">',
    '<input name="ctl00$ctl00$MainContent$MainContent$txtCaseOfficer" value="{{ case_officer }}">',
    '<input name="ctl00$ctl00$MainContent$MainContent$txtAgentName" value="{{ agent_name }}">',
    '<input name="ctl00$ctl00$MainContent$MainContent$txtAppName" value="{{ applicant_name }}">',
    '<textarea name="ctl00$ctl00$MainContent$MainContent$txtAgentsAddress"> {{ agent_address }} </textarea>',
    '<textarea name="ctl00$ctl00$MainContent$MainContent$txtApplicantsAddress"> {{ applicant_address }} </textarea>',
    '<input name="ctl00$ctl00$MainContent$MainContent$txtAgentTelephone" value="{{ agent_tel }}">',
    '<input name="ctl00$ctl00$MainContent$MainContent$txtDecisionLevel" value="{{ decided_by }}">',
    '<input name="ctl00$ctl00$MainContent$MainContent$txtDecisionDate2" value="{{ decision_date }}">',
    '<input name="ctl00$ctl00$MainContent$MainContent$txtDecision" value="{{ decision }}">',
    '<input name="ctl00$ctl00$MainContent$MainContent$txtApplicationCategory" value="{{ development_type }}">',
    '<input name="ctl00$ctl00$MainContent$MainContent$txtPublicNoticeDate" value="{{ consultation_start_date }}">',
    '<input name="ctl00$ctl00$MainContent$MainContent$txtPublicNoticeExpiryDate" value="{{ consultation_end_date }}">',
    '<input name="ctl00$ctl00$MainContent$MainContent$txtNeighbourLetterDate" value="{{ neighbour_consultation_start_date }}">',
    '<input name="ctl00$ctl00$MainContent$MainContent$txtNeighbourLetterExpiryDate" value="{{ neighbour_consultation_end_date }}">',
    '<input name="ctl00$ctl00$MainContent$MainContent$txtSiteNoticeDisplayDate" value="{{ site_notice_start_date }}">',
    '<input name="ctl00$ctl00$MainContent$MainContent$txtSiteNoticeExpiryDate" value="{{ site_notice_end_date }}">',
    ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)

        fields = self.search_fields
        fields [self.date_from_field] = date_from.strftime(self.request_date_format)
        fields [self.date_to_field] = date_to.strftime(self.request_date_format)

        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br, self.search_submit)
        html = response.read()

        try:
            result = scrapemark.scrape(self.scrape_max_recs, html)
            max_recs = int(result['max_recs']) 
        except:
            max_recs = 0
        if self.DEBUG: print max_recs
        
        final_result = []
        while response and len(final_result) < max_recs:
            url = response.geturl()
            if self.DEBUG: print html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            if len(final_result) >= max_recs: 
                break
            try:
                result = scrapemark.scrape(self.scrape_next_submit, html, url)
                util.setup_form(self.br, self.search_form)
                if self.DEBUG: print self.br.form
                response = util.submit_form(self.br, result['next_submit'])
                html = response.read()
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
            result = scrapemark.scrape(self.scrape_ids, html, url)
            return self.get_detail_from_url(result['records'][0]['url'])
        except:
            return None
        
if __name__ == 'scraper':

    scraper = SouthNorthamptonshireScraper()
    scraper.run()

    # misc test calls
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('S/2011/1043/CAC')
    #result = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('18/08/2011'))
    #print len(result), result

    



# this is a scraper of South Northamptonshire planning applications for use by Openly Local

# also see Bournemouth

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

class SouthNorthamptonshireScraper(base.DateScraper):

    MAX_ID_BATCH = 250 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go

    search_url = 'http://snc.planning-register.co.uk/planappsrch.aspx?pageprefix=plan'
    date_from_field = 'ctl00$ctl00$MainContent$MainContent$txtDateReceivedFrom$dateInput'
    date_to_field = 'ctl00$ctl00$MainContent$MainContent$txtDateReceivedTo$dateInput'
    ref_field = 'ctl00$ctl00$MainContent$MainContent$txtAppNumber'
    search_fields = { '__EVENTTARGET': '', '__EVENTARGUMENT': '',  }
    next_target = 'ctl00$Mainpage$gridMain'
    request_date_format = '%Y-%m-%d-00-00-00'
    search_form = 'aspnetForm'
    search_submit = 'ctl00$ctl00$MainContent$MainContent$btnSearch'
    scrape_ids = """
    <table id="ctl00_ctl00_MainContent_MainContent_grdResults_ctl00"> <tbody>
    {* <tr> <td> <a href="{{ [records].url|abs }}">
    {{ [records].uid }} </a> </td>
    </tr> *}
    </tbody> </table>
    """
    scrape_max_recs = '<p> Your search returned the following results (a total of <b> {{ max_recs }} </b>).'
    scrape_next_submit = '<input class="rgPageNext" name="{{ next_submit }}">'
    scrape_data_block = """
    <div id="contenttext"> {{ block|html }} </div>
    """
    scrape_min_data = """
    <input name="ctl00$ctl00$MainContent$MainContent$txtAppNo" value="{{ reference }}">
    <textarea name="ctl00$ctl00$MainContent$MainContent$txtLocation"> {{ address }} </textarea>
    <textarea name="ctl00$ctl00$MainContent$MainContent$txtProposal"> {{ description }} </textarea>
    <input name="ctl00$ctl00$MainContent$MainContent$txtReceivedDate" value="{{ date_received }}">
    <input name="ctl00$ctl00$MainContent$MainContent$txtValidDate" value="{{ date_validated }}">
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<input name="ctl00$ctl00$MainContent$MainContent$txtParish" value="{{ parish }}">',
    '<input name="ctl00$ctl00$MainContent$MainContent$txtEasting" value="{{ easting }}">',
    '<input name="ctl00$ctl00$MainContent$MainContent$txtNorthing" value="{{ northing }}">',
    '<input name="ctl00$ctl00$MainContent$MainContent$txtStatus" value="{{ status }}">',
    '<input name="ctl00$ctl00$MainContent$MainContent$txtDecisionDate" value="{{ decision_date }}">',
    '<input name="ctl00$ctl00$MainContent$MainContent$txtCommitteeDate" value="{{ meeting_date }}">',
    '<input name="ctl00$ctl00$MainContent$MainContent$txtExpiryDate" value="{{ application_expires_date }}">',
    '<input name="ctl00$ctl00$MainContent$MainContent$txtType" value="{{ application_type }}">',
    '<input name="ctl00$ctl00$MainContent$MainContent$txtCaseOfficer" value="{{ case_officer }}">',
    '<input name="ctl00$ctl00$MainContent$MainContent$txtAgentName" value="{{ agent_name }}">',
    '<input name="ctl00$ctl00$MainContent$MainContent$txtAppName" value="{{ applicant_name }}">',
    '<textarea name="ctl00$ctl00$MainContent$MainContent$txtAgentsAddress"> {{ agent_address }} </textarea>',
    '<textarea name="ctl00$ctl00$MainContent$MainContent$txtApplicantsAddress"> {{ applicant_address }} </textarea>',
    '<input name="ctl00$ctl00$MainContent$MainContent$txtAgentTelephone" value="{{ agent_tel }}">',
    '<input name="ctl00$ctl00$MainContent$MainContent$txtDecisionLevel" value="{{ decided_by }}">',
    '<input name="ctl00$ctl00$MainContent$MainContent$txtDecisionDate2" value="{{ decision_date }}">',
    '<input name="ctl00$ctl00$MainContent$MainContent$txtDecision" value="{{ decision }}">',
    '<input name="ctl00$ctl00$MainContent$MainContent$txtApplicationCategory" value="{{ development_type }}">',
    '<input name="ctl00$ctl00$MainContent$MainContent$txtPublicNoticeDate" value="{{ consultation_start_date }}">',
    '<input name="ctl00$ctl00$MainContent$MainContent$txtPublicNoticeExpiryDate" value="{{ consultation_end_date }}">',
    '<input name="ctl00$ctl00$MainContent$MainContent$txtNeighbourLetterDate" value="{{ neighbour_consultation_start_date }}">',
    '<input name="ctl00$ctl00$MainContent$MainContent$txtNeighbourLetterExpiryDate" value="{{ neighbour_consultation_end_date }}">',
    '<input name="ctl00$ctl00$MainContent$MainContent$txtSiteNoticeDisplayDate" value="{{ site_notice_start_date }}">',
    '<input name="ctl00$ctl00$MainContent$MainContent$txtSiteNoticeExpiryDate" value="{{ site_notice_end_date }}">',
    ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)

        fields = self.search_fields
        fields [self.date_from_field] = date_from.strftime(self.request_date_format)
        fields [self.date_to_field] = date_to.strftime(self.request_date_format)

        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br, self.search_submit)
        html = response.read()

        try:
            result = scrapemark.scrape(self.scrape_max_recs, html)
            max_recs = int(result['max_recs']) 
        except:
            max_recs = 0
        if self.DEBUG: print max_recs
        
        final_result = []
        while response and len(final_result) < max_recs:
            url = response.geturl()
            if self.DEBUG: print html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            if len(final_result) >= max_recs: 
                break
            try:
                result = scrapemark.scrape(self.scrape_next_submit, html, url)
                util.setup_form(self.br, self.search_form)
                if self.DEBUG: print self.br.form
                response = util.submit_form(self.br, result['next_submit'])
                html = response.read()
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
            result = scrapemark.scrape(self.scrape_ids, html, url)
            return self.get_detail_from_url(result['records'][0]['url'])
        except:
            return None
        
if __name__ == 'scraper':

    scraper = SouthNorthamptonshireScraper()
    scraper.run()

    # misc test calls
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('S/2011/1043/CAC')
    #result = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('18/08/2011'))
    #print len(result), result

    



