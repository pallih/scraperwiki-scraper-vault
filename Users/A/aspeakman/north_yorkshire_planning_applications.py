# this is a scraper of North Yorkshire planning applications for use by Openly Local

# also see Lancashire

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

class NorthYorkshireScraper(base.DateScraper):

    MAX_ID_BATCH = 200 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 150 # max application details to scrape in one go
    ID_ORDER = 'uid desc'

    search_url = 'https://onlineplanningregister.northyorks.gov.uk/register/PlanAppSrch.aspx'
    date_from_field = 'ctl00$MainContent$txtValidatedDateFrom$dateInput'
    date_to_field = 'ctl00$MainContent$txtValidatedDateTo$dateInput'
    scrape_next_submit = '<input class="rdpPageNext" name="{{ next_submit }}">'
    ref_field = 'ctl00$MainContent$txtApplNum'
    request_date_format = '%Y-%m-%d-00-00-00'
    search_form = '0'
    scrape_max_pages = '<div class="rdpWrap"> Page 1 of {{ max_pages }} </div>'
    scrape_ids = """
    <div id="news_results_list">
    {* <div>
    <td> Application Number: <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    </div> *}
    </div>
    """
    scrape_data_block = """
    <body> {{ block|html }} </body>
    """
    scrape_min_data = """
    <input name="ctl00$MainContent$txtApplNum" value="{{ reference }}" />
    <textarea name="ctl00$MainContent$txtLocation"> {{ address }} </textarea>
    <textarea name="ctl00$MainContent$txtProposal"> {{ description }} </textarea>
    <input name="ctl00$MainContent$txtReceivedDate" value="{{ date_received }}" />
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<input name="ctl00$MainContent$txtCurrentStatus" value="{{ status }}" />',
    '<input name="ctl00$MainContent$txtDistrict" value="{{ district }}" />',
    '<input name="ctl00$MainContent$txtParish" value="{{ parish }}" />',
    '<input name="ctl00$MainContent$txtElecDiv" value="{{ ward_name }}" />',
    '<input name="ctl00$MainContent$txtEasting" value="{{ easting }}" />',
    '<input name="ctl00$MainContent$txtNorthing" value="{{ northing }}" />',
    '<input name="ctl00$MainContent$txtApplName" value="{{ applicant_name }}" />',
    '<input name="ctl00$MainContent$txtAgentsName" value="{{ agent_name }}" />',
    '<textarea name="ctl00$MainContent$txtApplicantsAddr"> {{ applicant_address }} </textarea>',
    '<textarea name="ctl00$MainContent$txtAgentsAddress"> {{ agent_address }} </textarea>',
    '<input name="ctl00$MainContent$txtSiteNoticeDate" value="{{ site_notice_start_date }}" />',
    '<input name="ctl00$MainContent$txtTargetDecisionDate" value="{{ target_decision_date }}" />',
    '<input name="ctl00$MainContent$txtPressNoticeDate" value="{{ consultation_start_date }}" />',
    '<a id="MainContent_hypComment" href="{{ comment_url|abs }}" />',
    '<input name="ctl00$MainContent$txtDelegatedTo" value="{{ decided_by }}" />',
    '<input name="ctl00$MainContent$txtCommitteeDate" value="{{ meeting_date }}" />',
    '<input name="ctl00$MainContent$txtDecisionDate" value="{{ decision_date }}" />',
    '<input name="ctl00$MainContent$txtDecision" value="{{ decision }}" />',
    '<input name="ctl00$MainContent$txtAppealDate" value="{{ appeal_date }}" />',
    '<input name="ctl00$MainContent$txtAppealDecision" value="{{ appeal_result }}" />',
    '<textarea name="ctl00$MainContent$txtPlanningOfficer"> {{ case_officer }}" </textarea>',
    ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)

        fields = {}
        fields [self.date_from_field] = date_from.strftime(self.request_date_format)
        fields [self.date_to_field] = date_to.strftime(self.request_date_format)
        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br)
        html = response.read()

        try:
            result = scrapemark.scrape(self.scrape_max_pages, html)
            max_pages = int(result['max_pages'])
        except:
            max_pages = 0
        if self.DEBUG: print max_pages

        current_page = 0
        final_result = []
        while response and current_page < max_pages:
            url = response.geturl()
            if self.DEBUG: print html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            else:
                break
            current_page += 1
            if current_page >= max_pages: break
            try:
                result = scrapemark.scrape(self.scrape_next_submit, html)
                next_submit = result['next_submit']
                util.setup_form(self.br, self.search_form)
                if self.DEBUG: print self.br.form
                response = util.submit_form(self.br, next_submit)
                html = response.read()
            except:
                response = None

        return final_result

    def get_detail_from_uid (self, uid):
        
        response = self.br.open(self.search_url)
        fields = { self.ref_field: uid }
        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br)

        try:
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

    scraper = NorthYorkshireScraper()
    scraper.run()

    # misc test calls
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('NY/2011/0305/A30')
    #result = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('18/09/2011'))
    #print len(result), result

    



# this is a scraper of North Yorkshire planning applications for use by Openly Local

# also see Lancashire

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

class NorthYorkshireScraper(base.DateScraper):

    MAX_ID_BATCH = 200 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 150 # max application details to scrape in one go
    ID_ORDER = 'uid desc'

    search_url = 'https://onlineplanningregister.northyorks.gov.uk/register/PlanAppSrch.aspx'
    date_from_field = 'ctl00$MainContent$txtValidatedDateFrom$dateInput'
    date_to_field = 'ctl00$MainContent$txtValidatedDateTo$dateInput'
    scrape_next_submit = '<input class="rdpPageNext" name="{{ next_submit }}">'
    ref_field = 'ctl00$MainContent$txtApplNum'
    request_date_format = '%Y-%m-%d-00-00-00'
    search_form = '0'
    scrape_max_pages = '<div class="rdpWrap"> Page 1 of {{ max_pages }} </div>'
    scrape_ids = """
    <div id="news_results_list">
    {* <div>
    <td> Application Number: <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    </div> *}
    </div>
    """
    scrape_data_block = """
    <body> {{ block|html }} </body>
    """
    scrape_min_data = """
    <input name="ctl00$MainContent$txtApplNum" value="{{ reference }}" />
    <textarea name="ctl00$MainContent$txtLocation"> {{ address }} </textarea>
    <textarea name="ctl00$MainContent$txtProposal"> {{ description }} </textarea>
    <input name="ctl00$MainContent$txtReceivedDate" value="{{ date_received }}" />
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<input name="ctl00$MainContent$txtCurrentStatus" value="{{ status }}" />',
    '<input name="ctl00$MainContent$txtDistrict" value="{{ district }}" />',
    '<input name="ctl00$MainContent$txtParish" value="{{ parish }}" />',
    '<input name="ctl00$MainContent$txtElecDiv" value="{{ ward_name }}" />',
    '<input name="ctl00$MainContent$txtEasting" value="{{ easting }}" />',
    '<input name="ctl00$MainContent$txtNorthing" value="{{ northing }}" />',
    '<input name="ctl00$MainContent$txtApplName" value="{{ applicant_name }}" />',
    '<input name="ctl00$MainContent$txtAgentsName" value="{{ agent_name }}" />',
    '<textarea name="ctl00$MainContent$txtApplicantsAddr"> {{ applicant_address }} </textarea>',
    '<textarea name="ctl00$MainContent$txtAgentsAddress"> {{ agent_address }} </textarea>',
    '<input name="ctl00$MainContent$txtSiteNoticeDate" value="{{ site_notice_start_date }}" />',
    '<input name="ctl00$MainContent$txtTargetDecisionDate" value="{{ target_decision_date }}" />',
    '<input name="ctl00$MainContent$txtPressNoticeDate" value="{{ consultation_start_date }}" />',
    '<a id="MainContent_hypComment" href="{{ comment_url|abs }}" />',
    '<input name="ctl00$MainContent$txtDelegatedTo" value="{{ decided_by }}" />',
    '<input name="ctl00$MainContent$txtCommitteeDate" value="{{ meeting_date }}" />',
    '<input name="ctl00$MainContent$txtDecisionDate" value="{{ decision_date }}" />',
    '<input name="ctl00$MainContent$txtDecision" value="{{ decision }}" />',
    '<input name="ctl00$MainContent$txtAppealDate" value="{{ appeal_date }}" />',
    '<input name="ctl00$MainContent$txtAppealDecision" value="{{ appeal_result }}" />',
    '<textarea name="ctl00$MainContent$txtPlanningOfficer"> {{ case_officer }}" </textarea>',
    ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)

        fields = {}
        fields [self.date_from_field] = date_from.strftime(self.request_date_format)
        fields [self.date_to_field] = date_to.strftime(self.request_date_format)
        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br)
        html = response.read()

        try:
            result = scrapemark.scrape(self.scrape_max_pages, html)
            max_pages = int(result['max_pages'])
        except:
            max_pages = 0
        if self.DEBUG: print max_pages

        current_page = 0
        final_result = []
        while response and current_page < max_pages:
            url = response.geturl()
            if self.DEBUG: print html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            else:
                break
            current_page += 1
            if current_page >= max_pages: break
            try:
                result = scrapemark.scrape(self.scrape_next_submit, html)
                next_submit = result['next_submit']
                util.setup_form(self.br, self.search_form)
                if self.DEBUG: print self.br.form
                response = util.submit_form(self.br, next_submit)
                html = response.read()
            except:
                response = None

        return final_result

    def get_detail_from_uid (self, uid):
        
        response = self.br.open(self.search_url)
        fields = { self.ref_field: uid }
        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br)

        try:
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

    scraper = NorthYorkshireScraper()
    scraper.run()

    # misc test calls
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('NY/2011/0305/A30')
    #result = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('18/09/2011'))
    #print len(result), result

    



