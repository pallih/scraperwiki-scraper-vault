# this is a scraper of Lancashire planning applications for use by Openly Local

# also see North Yorkshire

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

class LancashireScraper(base.DateScraper):

    BATCH_DAYS = 28 # batch size for each scrape - number of days to gather to produce at least one result each time
    MIN_DAYS = 28 # min number of days to get when gathering current ids
    MAX_ID_BATCH = 250 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go

    HEADERS = { 'User-agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1', }

    search_url = 'http://planningregister.lancashire.gov.uk/planappsearch.aspx'
    date_from_field = 'ctl00$ContentPlaceHolder1$txtAppValFrom$dateInput'
    date_to_field = 'ctl00$ContentPlaceHolder1$txtAppValTo$dateInput'
    next_base_fields = { '__EVENTARGUMENT': '', '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$ddlPager', 
            'ctl00$ContentPlaceHolder1$btnNewSearch': None, 'ctl00$ContentPlaceHolder1$Button1': None }
    next_field = 'ctl00$ContentPlaceHolder1$ddlPager'
    ref_field = 'ctl00$ContentPlaceHolder1$txtAppNum'
    request_date_format = '%Y-%m-%d-00-00-00'
    search_form = 'aspnetForm'
    scrape_max_pages = '<p> Currently showing page 1 of {{ max_pages }} (10 applications per page). </p>'
    scrape_ids = """
    <table id="ctl00_ContentPlaceHolder1_grdResults_ctl00">
    {* <table>
    Application Number: <a href="{{ [records].url|abs }}">
    {{ [records].uid }} </a>
    </table> *}
    </table>
    """
    scrape_data_block = """
    <div id="ctl00_ContentPlaceHolder1_RadMultiPage1"> {{ block|html }} </div>
    """
    scrape_min_data = """
    <input name="txtAppNum" value="{{ reference }}">
    <textarea name="Location"> {{ address }} </textarea>
    <textarea name="Proposal"> {{ description }} </textarea>
    <input name="RecvDate" value="{{ date_received }}">
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<input name="SiteNot" value="{{ date_validated }}">',
    '<input name="txtAppStatus" value="{{ status }}">',
    '<input name="ctl00$ContentPlaceHolder1$RadLVProperty$ctrl0$txtDistrict" value="{{ district }}">',
    '<input name="ctl00$ContentPlaceHolder1$RadLVProperty$ctrl0$txtParish" value="{{ parish }}">',
    '<input name="ctl00$ContentPlaceHolder1$RadLVProperty$ctrl0$txtWard" value="{{ ward_name }}">',
    '<input name="Easting" value="{{ easting }}">',
    '<input name="Northing" value="{{ northing }}">',
    '<input name="AppName" value="{{ applicant_name }}">',
    '<input name="agentName" value="{{ agent_name }}">',
    '<textarea name="ctl00$ContentPlaceHolder1$RadLVApplicants$ctrl0$txtAppAddress"> {{ applicant_address }} </textarea>',
    '<textarea name="ctl00$ContentPlaceHolder1$RadLVApplicants$ctrl0$txtAgentAddress"> {{ agent_address }} </textarea>',
    '<input name="delegComm" value="{{ decided_by }}">',
    '<input name="commDate" value="{{ meeting_date }}">',
    '<input name="decDate" value="{{ decision_issued_date }}">',
    '<input name="dec" value="{{ decision }}">',
    '<input name="aplDate" value="{{ appeal_date }}">',
    '<input name="aplDec" value="{{ appeal_result }}">',
    '<input name="planOff" value="{{ case_officer }}">',
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
                fields = self.next_base_fields
                fields [self.next_field] = str(current_page)
                util.setup_form(self.br, self.search_form, fields)
                if self.DEBUG: print self.br.form
                response = util.submit_form(self.br)
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

    scraper = LancashireScraper()
    scraper.run()

    # misc test calls
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('06/11/0713') 
    #result = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('18/09/2011'))
    #print len(result), result

    



# this is a scraper of Lancashire planning applications for use by Openly Local

# also see North Yorkshire

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

class LancashireScraper(base.DateScraper):

    BATCH_DAYS = 28 # batch size for each scrape - number of days to gather to produce at least one result each time
    MIN_DAYS = 28 # min number of days to get when gathering current ids
    MAX_ID_BATCH = 250 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go

    HEADERS = { 'User-agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1', }

    search_url = 'http://planningregister.lancashire.gov.uk/planappsearch.aspx'
    date_from_field = 'ctl00$ContentPlaceHolder1$txtAppValFrom$dateInput'
    date_to_field = 'ctl00$ContentPlaceHolder1$txtAppValTo$dateInput'
    next_base_fields = { '__EVENTARGUMENT': '', '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$ddlPager', 
            'ctl00$ContentPlaceHolder1$btnNewSearch': None, 'ctl00$ContentPlaceHolder1$Button1': None }
    next_field = 'ctl00$ContentPlaceHolder1$ddlPager'
    ref_field = 'ctl00$ContentPlaceHolder1$txtAppNum'
    request_date_format = '%Y-%m-%d-00-00-00'
    search_form = 'aspnetForm'
    scrape_max_pages = '<p> Currently showing page 1 of {{ max_pages }} (10 applications per page). </p>'
    scrape_ids = """
    <table id="ctl00_ContentPlaceHolder1_grdResults_ctl00">
    {* <table>
    Application Number: <a href="{{ [records].url|abs }}">
    {{ [records].uid }} </a>
    </table> *}
    </table>
    """
    scrape_data_block = """
    <div id="ctl00_ContentPlaceHolder1_RadMultiPage1"> {{ block|html }} </div>
    """
    scrape_min_data = """
    <input name="txtAppNum" value="{{ reference }}">
    <textarea name="Location"> {{ address }} </textarea>
    <textarea name="Proposal"> {{ description }} </textarea>
    <input name="RecvDate" value="{{ date_received }}">
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<input name="SiteNot" value="{{ date_validated }}">',
    '<input name="txtAppStatus" value="{{ status }}">',
    '<input name="ctl00$ContentPlaceHolder1$RadLVProperty$ctrl0$txtDistrict" value="{{ district }}">',
    '<input name="ctl00$ContentPlaceHolder1$RadLVProperty$ctrl0$txtParish" value="{{ parish }}">',
    '<input name="ctl00$ContentPlaceHolder1$RadLVProperty$ctrl0$txtWard" value="{{ ward_name }}">',
    '<input name="Easting" value="{{ easting }}">',
    '<input name="Northing" value="{{ northing }}">',
    '<input name="AppName" value="{{ applicant_name }}">',
    '<input name="agentName" value="{{ agent_name }}">',
    '<textarea name="ctl00$ContentPlaceHolder1$RadLVApplicants$ctrl0$txtAppAddress"> {{ applicant_address }} </textarea>',
    '<textarea name="ctl00$ContentPlaceHolder1$RadLVApplicants$ctrl0$txtAgentAddress"> {{ agent_address }} </textarea>',
    '<input name="delegComm" value="{{ decided_by }}">',
    '<input name="commDate" value="{{ meeting_date }}">',
    '<input name="decDate" value="{{ decision_issued_date }}">',
    '<input name="dec" value="{{ decision }}">',
    '<input name="aplDate" value="{{ appeal_date }}">',
    '<input name="aplDec" value="{{ appeal_result }}">',
    '<input name="planOff" value="{{ case_officer }}">',
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
                fields = self.next_base_fields
                fields [self.next_field] = str(current_page)
                util.setup_form(self.br, self.search_form, fields)
                if self.DEBUG: print self.br.form
                response = util.submit_form(self.br)
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

    scraper = LancashireScraper()
    scraper.run()

    # misc test calls
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('06/11/0713') 
    #result = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('18/09/2011'))
    #print len(result), result

    



