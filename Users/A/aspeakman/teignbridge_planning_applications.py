# this is a scraper of Teignbridge planning applications for use by Openly Local

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import urllib

base = scraperwiki.utils.swimport("openlylocal_base_scraper")
scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")

class TeignbridgeScraper(base.DateScraper):

    date_from_field = 'ctl00$MainContent$AdvancedValidStartFromDateValueTextBox' 
    date_to_field = 'ctl00$MainContent$AdvancedValidStartToDateValueTextBox'
    search_form = 'aspnetForm'
    request_date_format = '%d/%m/%Y'
    submit_control = 'ctl00$MainContent$AdvancedButton'
    #select_fields = { 'ctl00$MainContent$AddressCase': 'CaseDetailsRadioButton', '__EVENTTARGET': 'ctl00$MainContent$CaseDetailsRadioButton', '__EVENTARGUMENT': '', } 
    # select address search
    #search_fields = { '__EVENTTARGET': 'ctl00$MainContent$SearchButton', '__EVENTARGUMENT': '', 'ctl00$MainContent$AddressMapSearchTextBox': None,
    #        'ctl00$MainContent$AddressMapImageButton': None }
    start_url = 'http://gis.teignbridge.gov.uk/TeignbridgePlanningOnline/Search.aspx'
    applic_url = 'http://gis.teignbridge.gov.uk/TeignbridgePlanningOnline/Results.aspx'
    #subs = {
    #    r' disabled ': r' ',
    #    }
    scrape_ids = """
    <div id="ctl00_ctl00_MainContent_ChildContentTabsAddress_divSearchResults">
    {* <table>
    <tr> <td /> <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td> </tr>
    </table> *}
    </div>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="divResultDetails"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <tr> <td> Reference: </td> <td> {{ reference }} </td> </tr>
    <tr> <td> Address: </td> <td> {{ address }} </td> </tr>
    <tr> <td> Proposal: </td> <td> {{ description }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr> <td> Date Application Received: </td> <td> {{ date_received }} </td> </tr>',
    '<tr> <td> Date Application Validated: </td> <td> {{ date_validated }} </td> </tr>',
    '<tr> <td> Date Appeal Started: </td> <td> {{ date_validated }}{{ appeal_date }} </td> </tr>',
    """<tr> <td> Decision: </td> <td> {{ appeal_result }} </td> </tr>
    <tr> <td> Date Appeal Decided: </td> <td> {{ appeal_decision_date }} </td> </tr>""",
    '<tr> <td> Status: </td> <td> {{ status }} </td> </tr>',
    '<tr> <td> Parish: </td> <td> {{ parish }} </td> </tr>',
    '<tr> <td> Ward: </td> <td> {{ ward_name }} </td> </tr>',
    '<tr> <td> Type of Application: </td> <td> {{ application_type }} </td> </tr>',
    '<tr> <td> Type: </td> <td> {{ application_type }} </td> </tr>',
    '<tr> <td> Decision: </td> <td> {{ decision }} </td> </tr>',
    '<tr> <td> Case Officer: </td> <td> {{ case_officer }} </td> </tr>',
    '<tr> <td> Decision Level: </td> <td> {{ decided_by }} </td> </tr>',
    '<tr> <td> Applicant Name: </td> <td> {{ applicant_name }} </td> </tr>',
    '<tr> <td> Applicant Address: </td> <td> {{ applicant_address }} </td> </tr>',
    '<tr> <td> Agent Name: </td> <td> {{ agent_name }} </td> </tr>',
    '<tr> <td> Agent Address: </td> <td> {{ agent_address }} </td> </tr>',
    '<tr> <td> Conditional: </td> <td> {{ conditions }} </td> </tr>',
    '<tr> <td> Publicity Expiry Date: </td> <td> {{ latest_advertisement_expiry_date }} </td> </tr>',
    '<tr> <td> Target Date: </td> <td> {{ target_decision_date }} </td> </tr>',
    '<tr> <td> Date Decision Issued: </td> <td> {{ decision_date }} </td> </tr>',
    ]

    def get_id_batch (self, date_from, date_to):

        response = util.open_url(self.br, self.start_url)
        html = response.get_data()
        if self.DEBUG: print "Start html:", html

        #for k, v in self.subs.items():
        #    html = re.sub(k, v, html, 0, re.U|re.S|re.I) # unicode|dot matches new line|ignore case
        #if self.DEBUG: print "html post sub:", html
        #response.set_data(html)
        #self.br.set_response(response)

        #fields = self.select_fields
        #form_ok = util.setup_form(self.br, self.search_form, fields)
        #if self.DEBUG: print "form:", self.br.form
        #response = util.submit_form(self.br)
        #html = response.get_data()
        #if self.DEBUG: print "html pre sub:", html
        #for k, v in self.subs.items():
        #    html = re.sub(k, v, html, 0, re.U|re.S|re.I) # unicode|dot matches new line|ignore case
        #if self.DEBUG: print "html post sub:", html
        #response.set_data(html)
        #self.br.set_response(response)

        #fields = self.search_fields
        fields = {}
        fields[self.date_from_field] = date_from.strftime(self.request_date_format)
        fields[self.date_to_field] = date_to.strftime(self.request_date_format)
        form_ok = util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print "form:", self.br.form
        response = util.submit_form(self.br, self.submit_control)

        html = response.read()
        url = response.geturl()
        if self.DEBUG: print "result page:", url, html

        final_result = []
        if response:
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])

        return final_result

    def get_detail_from_uid (self, uid):
        url = self.applic_url + '?Type=Application&Refval=' + urllib.quote_plus(uid)
        result = self.get_detail_from_url(url)
        if not result:
            url = self.applic_url + '?Type=Appeal&Refval=' + urllib.quote_plus(uid)
            return self.get_detail_from_url(url)
        else:
            return result

if __name__ == 'scraper':

    scraper = TeignbridgeScraper()
    scraper.run()

    # misc tests
    #scraper.DEBUG = True
    #scraper.br.set_debug_http(True)
    #print scraper.get_detail_from_uid ('11/00030/REF')
    #print scraper.get_detail_from_uid ('11/02646/FUL')
    #res = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('09/08/2011'))
    #print len(res), res
    #print scraper.gather_ids('2012-02-01')
    #print scraper.gather_ids('2011-02-01', '2012-01-18')

# this is a scraper of Teignbridge planning applications for use by Openly Local

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import urllib

base = scraperwiki.utils.swimport("openlylocal_base_scraper")
scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")

class TeignbridgeScraper(base.DateScraper):

    date_from_field = 'ctl00$MainContent$AdvancedValidStartFromDateValueTextBox' 
    date_to_field = 'ctl00$MainContent$AdvancedValidStartToDateValueTextBox'
    search_form = 'aspnetForm'
    request_date_format = '%d/%m/%Y'
    submit_control = 'ctl00$MainContent$AdvancedButton'
    #select_fields = { 'ctl00$MainContent$AddressCase': 'CaseDetailsRadioButton', '__EVENTTARGET': 'ctl00$MainContent$CaseDetailsRadioButton', '__EVENTARGUMENT': '', } 
    # select address search
    #search_fields = { '__EVENTTARGET': 'ctl00$MainContent$SearchButton', '__EVENTARGUMENT': '', 'ctl00$MainContent$AddressMapSearchTextBox': None,
    #        'ctl00$MainContent$AddressMapImageButton': None }
    start_url = 'http://gis.teignbridge.gov.uk/TeignbridgePlanningOnline/Search.aspx'
    applic_url = 'http://gis.teignbridge.gov.uk/TeignbridgePlanningOnline/Results.aspx'
    #subs = {
    #    r' disabled ': r' ',
    #    }
    scrape_ids = """
    <div id="ctl00_ctl00_MainContent_ChildContentTabsAddress_divSearchResults">
    {* <table>
    <tr> <td /> <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td> </tr>
    </table> *}
    </div>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="divResultDetails"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <tr> <td> Reference: </td> <td> {{ reference }} </td> </tr>
    <tr> <td> Address: </td> <td> {{ address }} </td> </tr>
    <tr> <td> Proposal: </td> <td> {{ description }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr> <td> Date Application Received: </td> <td> {{ date_received }} </td> </tr>',
    '<tr> <td> Date Application Validated: </td> <td> {{ date_validated }} </td> </tr>',
    '<tr> <td> Date Appeal Started: </td> <td> {{ date_validated }}{{ appeal_date }} </td> </tr>',
    """<tr> <td> Decision: </td> <td> {{ appeal_result }} </td> </tr>
    <tr> <td> Date Appeal Decided: </td> <td> {{ appeal_decision_date }} </td> </tr>""",
    '<tr> <td> Status: </td> <td> {{ status }} </td> </tr>',
    '<tr> <td> Parish: </td> <td> {{ parish }} </td> </tr>',
    '<tr> <td> Ward: </td> <td> {{ ward_name }} </td> </tr>',
    '<tr> <td> Type of Application: </td> <td> {{ application_type }} </td> </tr>',
    '<tr> <td> Type: </td> <td> {{ application_type }} </td> </tr>',
    '<tr> <td> Decision: </td> <td> {{ decision }} </td> </tr>',
    '<tr> <td> Case Officer: </td> <td> {{ case_officer }} </td> </tr>',
    '<tr> <td> Decision Level: </td> <td> {{ decided_by }} </td> </tr>',
    '<tr> <td> Applicant Name: </td> <td> {{ applicant_name }} </td> </tr>',
    '<tr> <td> Applicant Address: </td> <td> {{ applicant_address }} </td> </tr>',
    '<tr> <td> Agent Name: </td> <td> {{ agent_name }} </td> </tr>',
    '<tr> <td> Agent Address: </td> <td> {{ agent_address }} </td> </tr>',
    '<tr> <td> Conditional: </td> <td> {{ conditions }} </td> </tr>',
    '<tr> <td> Publicity Expiry Date: </td> <td> {{ latest_advertisement_expiry_date }} </td> </tr>',
    '<tr> <td> Target Date: </td> <td> {{ target_decision_date }} </td> </tr>',
    '<tr> <td> Date Decision Issued: </td> <td> {{ decision_date }} </td> </tr>',
    ]

    def get_id_batch (self, date_from, date_to):

        response = util.open_url(self.br, self.start_url)
        html = response.get_data()
        if self.DEBUG: print "Start html:", html

        #for k, v in self.subs.items():
        #    html = re.sub(k, v, html, 0, re.U|re.S|re.I) # unicode|dot matches new line|ignore case
        #if self.DEBUG: print "html post sub:", html
        #response.set_data(html)
        #self.br.set_response(response)

        #fields = self.select_fields
        #form_ok = util.setup_form(self.br, self.search_form, fields)
        #if self.DEBUG: print "form:", self.br.form
        #response = util.submit_form(self.br)
        #html = response.get_data()
        #if self.DEBUG: print "html pre sub:", html
        #for k, v in self.subs.items():
        #    html = re.sub(k, v, html, 0, re.U|re.S|re.I) # unicode|dot matches new line|ignore case
        #if self.DEBUG: print "html post sub:", html
        #response.set_data(html)
        #self.br.set_response(response)

        #fields = self.search_fields
        fields = {}
        fields[self.date_from_field] = date_from.strftime(self.request_date_format)
        fields[self.date_to_field] = date_to.strftime(self.request_date_format)
        form_ok = util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print "form:", self.br.form
        response = util.submit_form(self.br, self.submit_control)

        html = response.read()
        url = response.geturl()
        if self.DEBUG: print "result page:", url, html

        final_result = []
        if response:
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])

        return final_result

    def get_detail_from_uid (self, uid):
        url = self.applic_url + '?Type=Application&Refval=' + urllib.quote_plus(uid)
        result = self.get_detail_from_url(url)
        if not result:
            url = self.applic_url + '?Type=Appeal&Refval=' + urllib.quote_plus(uid)
            return self.get_detail_from_url(url)
        else:
            return result

if __name__ == 'scraper':

    scraper = TeignbridgeScraper()
    scraper.run()

    # misc tests
    #scraper.DEBUG = True
    #scraper.br.set_debug_http(True)
    #print scraper.get_detail_from_uid ('11/00030/REF')
    #print scraper.get_detail_from_uid ('11/02646/FUL')
    #res = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('09/08/2011'))
    #print len(res), res
    #print scraper.gather_ids('2012-02-01')
    #print scraper.gather_ids('2011-02-01', '2012-01-18')

