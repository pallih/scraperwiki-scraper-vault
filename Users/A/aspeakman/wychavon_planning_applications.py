# this is a scraper of Wychavon planning applications for use by Openly Local

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import urllib

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

class WychavonScraper(base.PeriodScraper):

    MAX_ID_BATCH = 250 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go
    PERIOD_TYPE = 'Month'
    #ID_ORDER = 'uid desc'
    ID_ORDER = "CASE uid WHEN substr(uid, 1, 2) < '50' THEN '20' || uid ELSE '19' || uid END desc"

    search_form = 'FrmSearchGeneral2'
    applic_form = 'FrmSearchGeneral'
    date_field_from = { 'month': 'EdtMonthStart1', 'year': 'EdtYearStart' }
    date_field_to = { 'month': 'EdtMonthEnd', 'year': 'EdtYearEnd' }
    ref_field1 = 'EdtYearNo'
    ref_field2 = 'EdtCaseNo'
    request_date_format = '%-d/%-m/%Y'
    search_url = 'http://www.e-wychavon.org.uk/wychavon/plan_search/search.html'
    # fix bad html
    html_subs = {
        r'<optgroup label="Month" value="1" selected>Jan': r'<optgroup label="Month"> <option value="1" selected="selected">Jan</option>',
        r'<optgroup label="Month" value="1">Jan': r'<optgroup label="Month"> <option value="1">Jan</option>',
        r'<option value="2012" selected>2012</option>\s*</optgroup>': '<option value="2012" selected="selected">2012</option> <option value="2013">2013</option> </optgroup>',
    }
    scrape_ids = """
    <div id="wccContentPane">
    {* <table>
    <tr> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </tr>
    </table> *}
    </div>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="wccContentPane"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <div align="center"> <b> PLANNING INFORMATION FOR </b> {{ reference }} <br /> </div>
    <tr> <td> Location: </td> <td> {{ address }} </td> </tr>
    <tr> <td> Proposal: </td> <td> {{ description }} </td> </tr>
    <tr> <td> Received Date: </td> <td> {{ date_received }} </td>
         <td> Statutory Start Date: </td> <td> {{ date_validated }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr> <td> Application Type: </td> <td> {{ application_type }} </td> </tr>',
    '<tr> <td> Status: </td> <td> {{ status }} </td> </tr>',
    '<tr> <td> Statutory Expiry Date: </td> <td> {{ application_expires_date }} </td> </tr>',
    '<a href="{{ comment_url }}"> <font> Comment on this application </font> </a>',
    '<tr> <td> Ward: </td> <td> {{ ward_name }} </td> </tr>',
    '<tr> <td> Parish: </td> <td> {{ parish }} </td> </tr>',
    '<tr> <td> Consultation Period From: </td> <td> {{ consultation_start_date }} </td> </tr>',
    '<tr> <td> Consultation Period End Date: </td> <td> {{ consultation_end_date }} </td> </tr>',
    '<tr> <td> Case Officer: </td> <td> {{ case_officer }} </td> </tr>',
    '<tr> <td> Committee Date (if applicable): </td> <td> {{ meeting_date }} </td> </tr>',
    """<tr> <td> Decision: </td> <td> {{ decision }} </td> </tr>
    <tr> <td> Decision Date: </td> <td> {{ decision_date }} </td> </tr>""",
    '<b> Conditions and Reasons applicable to the decision of this application </b> <p /> {{ conditions }} <p />',
    """<tr> <td> Applicant: </td> <td> Agent: </td> </tr> <tr> <td> {{ applicant_name }} <br> {{ applicant_address }} </td> </tr> """,
    """<tr> <td> Applicant: </td> <td> Agent: </td> </tr> <tr> <td /> <td> {{ agent_name }} <br> {{ agent_address }} </td> </tr> """,
    ]

    def get_id_period (self, date):

        from_iso_dt, to_iso_dt = util.inc_dt(date.strftime(util.ISO8601_DATE), util.ISO8601_DATE, self.PERIOD_TYPE)
        from_dt = util.get_dt(from_iso_dt, util.ISO8601_DATE)
        to_dt = util.get_dt(to_iso_dt, util.ISO8601_DATE)

        response = self.br.open(self.search_url)
        html = response.get_data()
        for k, v in self.html_subs.items():
            html = re.sub(k, v, html, 0, re.U|re.S|re.I) # unicode|dot matches new line|ignore case
        response.set_data(html)
        self.br.set_response(response)
        if self.DEBUG: print response.read()

        fields = {}
        date = date.strftime(self.request_date_format)
        date_parts = date.split('/')
        #fields [self.date_from_field['day']] = date_parts[0]
        fields [self.date_field_from['month']] = date_parts[1]
        fields [self.date_field_from['year']] = date_parts[2]
        fields [self.date_field_to['month']] = date_parts[1]
        fields [self.date_field_to['year']] = date_parts[2]

        form_ok = util.setup_form(self.br, self.search_form, fields )
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br)

        final_result = []
        if response:
            html = response.read()
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
        
        if final_result:
            return final_result, from_dt, to_dt
        else:
            return [], None, None # monthly scraper - so empty result is always invalid

    def get_detail_from_uid (self, uid):

        try:
            response = self.br.open(self.search_url)
            
            fields = { self.ref_field1: uid[0:2], self.ref_field2: uid[3:8] }
            if self.DEBUG: print fields
            form_ok = util.setup_form(self.br, self.applic_form, fields )
            if self.DEBUG: print self.br.form
            response = util.submit_form(self.br)

            html = response.read()
            url = response.geturl()
            if self.DEBUG: print html

            result = scrapemark.scrape(self.scrape_ids, html, url)
            url = result['records'][0]['url']
            
        except:
            if self.DEBUG: raise
            else: return None

        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    scraper = WychavonScraper()
    scraper.run()

    #scraper.DEBUG = True
    # misc tests
    #print scraper.get_detail_from_uid ('12/00570')
    #print scraper.get_detail_from_uid ('09/00733')
    #result = scraper.get_id_period(util.get_dt('01/01/2012'))
    #print result, len(result)
    #print util.inc_dt('2010-02-01', util.ISO8601_DATE, 'Month')
    #print "Found " + str(len(result)) + " ids for Mar 2012"
    #print scraper.gather_ids('2010-02-01')
    #print scraper.gather_ids(None, None)
    #scraper.gather_current_ids()
# this is a scraper of Wychavon planning applications for use by Openly Local

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import urllib

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

class WychavonScraper(base.PeriodScraper):

    MAX_ID_BATCH = 250 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go
    PERIOD_TYPE = 'Month'
    #ID_ORDER = 'uid desc'
    ID_ORDER = "CASE uid WHEN substr(uid, 1, 2) < '50' THEN '20' || uid ELSE '19' || uid END desc"

    search_form = 'FrmSearchGeneral2'
    applic_form = 'FrmSearchGeneral'
    date_field_from = { 'month': 'EdtMonthStart1', 'year': 'EdtYearStart' }
    date_field_to = { 'month': 'EdtMonthEnd', 'year': 'EdtYearEnd' }
    ref_field1 = 'EdtYearNo'
    ref_field2 = 'EdtCaseNo'
    request_date_format = '%-d/%-m/%Y'
    search_url = 'http://www.e-wychavon.org.uk/wychavon/plan_search/search.html'
    # fix bad html
    html_subs = {
        r'<optgroup label="Month" value="1" selected>Jan': r'<optgroup label="Month"> <option value="1" selected="selected">Jan</option>',
        r'<optgroup label="Month" value="1">Jan': r'<optgroup label="Month"> <option value="1">Jan</option>',
        r'<option value="2012" selected>2012</option>\s*</optgroup>': '<option value="2012" selected="selected">2012</option> <option value="2013">2013</option> </optgroup>',
    }
    scrape_ids = """
    <div id="wccContentPane">
    {* <table>
    <tr> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </tr>
    </table> *}
    </div>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="wccContentPane"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <div align="center"> <b> PLANNING INFORMATION FOR </b> {{ reference }} <br /> </div>
    <tr> <td> Location: </td> <td> {{ address }} </td> </tr>
    <tr> <td> Proposal: </td> <td> {{ description }} </td> </tr>
    <tr> <td> Received Date: </td> <td> {{ date_received }} </td>
         <td> Statutory Start Date: </td> <td> {{ date_validated }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr> <td> Application Type: </td> <td> {{ application_type }} </td> </tr>',
    '<tr> <td> Status: </td> <td> {{ status }} </td> </tr>',
    '<tr> <td> Statutory Expiry Date: </td> <td> {{ application_expires_date }} </td> </tr>',
    '<a href="{{ comment_url }}"> <font> Comment on this application </font> </a>',
    '<tr> <td> Ward: </td> <td> {{ ward_name }} </td> </tr>',
    '<tr> <td> Parish: </td> <td> {{ parish }} </td> </tr>',
    '<tr> <td> Consultation Period From: </td> <td> {{ consultation_start_date }} </td> </tr>',
    '<tr> <td> Consultation Period End Date: </td> <td> {{ consultation_end_date }} </td> </tr>',
    '<tr> <td> Case Officer: </td> <td> {{ case_officer }} </td> </tr>',
    '<tr> <td> Committee Date (if applicable): </td> <td> {{ meeting_date }} </td> </tr>',
    """<tr> <td> Decision: </td> <td> {{ decision }} </td> </tr>
    <tr> <td> Decision Date: </td> <td> {{ decision_date }} </td> </tr>""",
    '<b> Conditions and Reasons applicable to the decision of this application </b> <p /> {{ conditions }} <p />',
    """<tr> <td> Applicant: </td> <td> Agent: </td> </tr> <tr> <td> {{ applicant_name }} <br> {{ applicant_address }} </td> </tr> """,
    """<tr> <td> Applicant: </td> <td> Agent: </td> </tr> <tr> <td /> <td> {{ agent_name }} <br> {{ agent_address }} </td> </tr> """,
    ]

    def get_id_period (self, date):

        from_iso_dt, to_iso_dt = util.inc_dt(date.strftime(util.ISO8601_DATE), util.ISO8601_DATE, self.PERIOD_TYPE)
        from_dt = util.get_dt(from_iso_dt, util.ISO8601_DATE)
        to_dt = util.get_dt(to_iso_dt, util.ISO8601_DATE)

        response = self.br.open(self.search_url)
        html = response.get_data()
        for k, v in self.html_subs.items():
            html = re.sub(k, v, html, 0, re.U|re.S|re.I) # unicode|dot matches new line|ignore case
        response.set_data(html)
        self.br.set_response(response)
        if self.DEBUG: print response.read()

        fields = {}
        date = date.strftime(self.request_date_format)
        date_parts = date.split('/')
        #fields [self.date_from_field['day']] = date_parts[0]
        fields [self.date_field_from['month']] = date_parts[1]
        fields [self.date_field_from['year']] = date_parts[2]
        fields [self.date_field_to['month']] = date_parts[1]
        fields [self.date_field_to['year']] = date_parts[2]

        form_ok = util.setup_form(self.br, self.search_form, fields )
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br)

        final_result = []
        if response:
            html = response.read()
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
        
        if final_result:
            return final_result, from_dt, to_dt
        else:
            return [], None, None # monthly scraper - so empty result is always invalid

    def get_detail_from_uid (self, uid):

        try:
            response = self.br.open(self.search_url)
            
            fields = { self.ref_field1: uid[0:2], self.ref_field2: uid[3:8] }
            if self.DEBUG: print fields
            form_ok = util.setup_form(self.br, self.applic_form, fields )
            if self.DEBUG: print self.br.form
            response = util.submit_form(self.br)

            html = response.read()
            url = response.geturl()
            if self.DEBUG: print html

            result = scrapemark.scrape(self.scrape_ids, html, url)
            url = result['records'][0]['url']
            
        except:
            if self.DEBUG: raise
            else: return None

        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    scraper = WychavonScraper()
    scraper.run()

    #scraper.DEBUG = True
    # misc tests
    #print scraper.get_detail_from_uid ('12/00570')
    #print scraper.get_detail_from_uid ('09/00733')
    #result = scraper.get_id_period(util.get_dt('01/01/2012'))
    #print result, len(result)
    #print util.inc_dt('2010-02-01', util.ISO8601_DATE, 'Month')
    #print "Found " + str(len(result)) + " ids for Mar 2012"
    #print scraper.gather_ids('2010-02-01')
    #print scraper.gather_ids(None, None)
    #scraper.gather_current_ids()
