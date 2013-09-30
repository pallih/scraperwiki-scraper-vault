# this is a scraper of Amber Valley planning applications for use by Openly Local

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

class AmberValleyScraper(base.DateScraper):

    MAX_ID_BATCH = 250 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go
    BATCH_DAYS = 14 # limited to single page of max 300 applications, but don't reduce days per batch as can cause problems around New Year 
    ID_ORDER = 'uid desc'

    search_url = 'http://www.ambervalley.gov.uk/environment-and-planning/planning/development-management/planning-applications/view-a-planning-application.aspx'
    date_from_field = {
        'day': 'ctl00$ctl00$ctl00$ContentPlaceHolderDefault$MasterTemplateBodyMainPlaceHolder$ctl01$PlanApps_3$lstDayStartCus',
        'month': 'ctl00$ctl00$ctl00$ContentPlaceHolderDefault$MasterTemplateBodyMainPlaceHolder$ctl01$PlanApps_3$lstMonthStartCus',
        'year': 'ctl00$ctl00$ctl00$ContentPlaceHolderDefault$MasterTemplateBodyMainPlaceHolder$ctl01$PlanApps_3$lstYearStartCus',
        }
    date_to_field = {
        'day': 'ctl00$ctl00$ctl00$ContentPlaceHolderDefault$MasterTemplateBodyMainPlaceHolder$ctl01$PlanApps_3$lstDayEndCus',
        'month': 'ctl00$ctl00$ctl00$ContentPlaceHolderDefault$MasterTemplateBodyMainPlaceHolder$ctl01$PlanApps_3$lstMonthEndCus',
        'year': 'ctl00$ctl00$ctl00$ContentPlaceHolderDefault$MasterTemplateBodyMainPlaceHolder$ctl01$PlanApps_3$lstYearEndCus',
        }
    search_fields = {
        'ctl00$ctl00$ctl00$ContentPlaceHolderDefault$MasterTemplateBodyMainPlaceHolder$ctl01$PlanApps_3$chkIncludeTPOCus': 'on', # include tree applications
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        }
    ref_field = 'ctl00$ctl00$ctl00$ContentPlaceHolderDefault$MasterTemplateBodyMainPlaceHolder$ctl01$PlanApps_3$txbAppRef'
    request_date_format = '%-d/%b/%Y'
    search_form = '0'
    search_submit = 'ctl00$ctl00$ctl00$ContentPlaceHolderDefault$MasterTemplateBodyMainPlaceHolder$ctl01$PlanApps_3$btnViewCustom'
    ref_submit = 'ctl00$ctl00$ctl00$ContentPlaceHolderDefault$MasterTemplateBodyMainPlaceHolder$ctl01$PlanApps_3$btnViewByAppRef'
    scrape_ids = """
    <div id="planAppList"> <table> <tr />
    {* <tr> <td>
    <a> {{ [records].uid }} </a>  </tr> *}
    </table> </div>
    """
    scrape_data_block = """
    <div id="dialogPlanAppDetails"> {{ block|html }} </div>
    """
    scrape_min_data = """
    <div class="detailName"> Application Reference </div> <div class="detailContent"> {{ reference }} </div>
    <div class="detailName"> Address </div> <div class="detailContent"> {{ address }} </div>
    <div class="detailName"> Proposal </div> <div class="detailContent"> {{ description }} </div>
    <div class="detailName"> Registered </div> <div class="detailContent"> {{ date_validated }} </div>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<div class="detailName"> Case Officer </div> <div class="detailContent"> {{ case_officer }} </div>',
    '<div class="detailName"> Status </div> <div class="detailContent"> {{ status }} </div>',
    '<div class="detailName"> Applicant </div> <div class="detailContent"> {{ applicant_name }} <br> {{ applicant_address }} </div>',
    '<div class="detailName"> Agent </div> <div class="detailContent"> {{ agent_name }} <br> {{ agent_address }} </div>',
    '<a href="{{ comment_url|abs }}">Comment on this Application</a>',
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
            response = util.submit_form(self.br, self.ref_submit)
            html = response.read()
            if self.DEBUG: print html
            url = response.geturl()
            return self.get_detail(html, url)
        except:
            return None

if __name__ == 'scraper':

    scraper = AmberValleyScraper()
    scraper.run()

    # misc test calls
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('AVA/2011/0742')
    #result = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('19/08/2011'))
    #print len(result), result

    



# this is a scraper of Amber Valley planning applications for use by Openly Local

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

class AmberValleyScraper(base.DateScraper):

    MAX_ID_BATCH = 250 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go
    BATCH_DAYS = 14 # limited to single page of max 300 applications, but don't reduce days per batch as can cause problems around New Year 
    ID_ORDER = 'uid desc'

    search_url = 'http://www.ambervalley.gov.uk/environment-and-planning/planning/development-management/planning-applications/view-a-planning-application.aspx'
    date_from_field = {
        'day': 'ctl00$ctl00$ctl00$ContentPlaceHolderDefault$MasterTemplateBodyMainPlaceHolder$ctl01$PlanApps_3$lstDayStartCus',
        'month': 'ctl00$ctl00$ctl00$ContentPlaceHolderDefault$MasterTemplateBodyMainPlaceHolder$ctl01$PlanApps_3$lstMonthStartCus',
        'year': 'ctl00$ctl00$ctl00$ContentPlaceHolderDefault$MasterTemplateBodyMainPlaceHolder$ctl01$PlanApps_3$lstYearStartCus',
        }
    date_to_field = {
        'day': 'ctl00$ctl00$ctl00$ContentPlaceHolderDefault$MasterTemplateBodyMainPlaceHolder$ctl01$PlanApps_3$lstDayEndCus',
        'month': 'ctl00$ctl00$ctl00$ContentPlaceHolderDefault$MasterTemplateBodyMainPlaceHolder$ctl01$PlanApps_3$lstMonthEndCus',
        'year': 'ctl00$ctl00$ctl00$ContentPlaceHolderDefault$MasterTemplateBodyMainPlaceHolder$ctl01$PlanApps_3$lstYearEndCus',
        }
    search_fields = {
        'ctl00$ctl00$ctl00$ContentPlaceHolderDefault$MasterTemplateBodyMainPlaceHolder$ctl01$PlanApps_3$chkIncludeTPOCus': 'on', # include tree applications
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        }
    ref_field = 'ctl00$ctl00$ctl00$ContentPlaceHolderDefault$MasterTemplateBodyMainPlaceHolder$ctl01$PlanApps_3$txbAppRef'
    request_date_format = '%-d/%b/%Y'
    search_form = '0'
    search_submit = 'ctl00$ctl00$ctl00$ContentPlaceHolderDefault$MasterTemplateBodyMainPlaceHolder$ctl01$PlanApps_3$btnViewCustom'
    ref_submit = 'ctl00$ctl00$ctl00$ContentPlaceHolderDefault$MasterTemplateBodyMainPlaceHolder$ctl01$PlanApps_3$btnViewByAppRef'
    scrape_ids = """
    <div id="planAppList"> <table> <tr />
    {* <tr> <td>
    <a> {{ [records].uid }} </a>  </tr> *}
    </table> </div>
    """
    scrape_data_block = """
    <div id="dialogPlanAppDetails"> {{ block|html }} </div>
    """
    scrape_min_data = """
    <div class="detailName"> Application Reference </div> <div class="detailContent"> {{ reference }} </div>
    <div class="detailName"> Address </div> <div class="detailContent"> {{ address }} </div>
    <div class="detailName"> Proposal </div> <div class="detailContent"> {{ description }} </div>
    <div class="detailName"> Registered </div> <div class="detailContent"> {{ date_validated }} </div>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<div class="detailName"> Case Officer </div> <div class="detailContent"> {{ case_officer }} </div>',
    '<div class="detailName"> Status </div> <div class="detailContent"> {{ status }} </div>',
    '<div class="detailName"> Applicant </div> <div class="detailContent"> {{ applicant_name }} <br> {{ applicant_address }} </div>',
    '<div class="detailName"> Agent </div> <div class="detailContent"> {{ agent_name }} <br> {{ agent_address }} </div>',
    '<a href="{{ comment_url|abs }}">Comment on this Application</a>',
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
            response = util.submit_form(self.br, self.ref_submit)
            html = response.read()
            if self.DEBUG: print html
            url = response.geturl()
            return self.get_detail(html, url)
        except:
            return None

if __name__ == 'scraper':

    scraper = AmberValleyScraper()
    scraper.run()

    # misc test calls
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('AVA/2011/0742')
    #result = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('19/08/2011'))
    #print len(result), result

    



