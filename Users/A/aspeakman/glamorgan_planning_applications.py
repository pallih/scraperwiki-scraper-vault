# this is a scraper of Vale of Glamorgan planning applications for use by Openly Local

# also see Redcar and Cleveland

# currently designed to work backwards collecting applications from the current date to 1/1/2000

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

class GlamorganScraper(base.DateScraper):

    HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:8.0) Gecko/20100101 Firefox/8.0',
    'Accept-Charset': 'UTF-8,*',
    'Accept': 'text/html',
    'Accept-Language': 'en-gb,en',
    }

    date_from_field = 'ctl00$ContentPlaceHolder1$txtRecFrom'
    date_to_field = 'ctl00$ContentPlaceHolder1$txtRecTo'
    search_form = 'aspnetForm'
    submit_control = 'ctl00$ContentPlaceHolder1$Button1'
    request_date_format = '%d/%m/%Y'
    start_fields = { '__EVENTTARGET': 'ctl00$Header', '__EVENTARGUMENT': 'bSearch\\Pla Standard Search' }
    search_fields = { '__EVENTTARGET': '', '__EVENTARGUMENT': '' } 
    next_fields = { '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$gvPlanning', '__EVENTARGUMENT': 'Page$' }
    start_url = 'http://vogonline.planning-register.co.uk'
    applic_url = 'http://vogonline.planning-register.co.uk/PlaRecord.aspx'
    scrape_ids = """
    <table> <tr />
    {* <tr> <td />
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    </tr> *}
    </table>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="content"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <h1> Planning Application Details for : {{ reference }} </h1>
    <textarea id="ctl00_ContentPlaceHolder1_TabContainer1_tabDetails_txtLocation"> {{ address }} </textarea>
    <textarea id="ctl00_ContentPlaceHolder1_TabContainer1_tabDetails_txtProposal"> {{ description }} </textarea>
    <input id="ctl00_ContentPlaceHolder1_TabContainer1_tabOtherDetails_txtRec" value="{{ date_received }}">
    <input id="ctl00_ContentPlaceHolder1_TabContainer1_tabOtherDetails_txtComplete" value="{{ date_validated }}">
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<input id="ctl00_ContentPlaceHolder1_TabContainer1_tabDetails_txtEasting" value="{{ easting }}">',
    '<input id="ctl00_ContentPlaceHolder1_TabContainer1_tabDetails_txtNorthing" value="{{ northing }}">',
    '<input id="ctl00_ContentPlaceHolder1_TabContainer1_tabDetails_txtParish" value="{{ parish }}">',
    '<input id="ctl00_ContentPlaceHolder1_TabContainer1_tabDetails_txtAppType" value="{{ application_type }}">',
    '<input id="ctl00_ContentPlaceHolder1_TabContainer1_tabDetails_txtStatus" value="{{ status }}">',
    '<input id="ctl00_ContentPlaceHolder1_TabContainer1_tabDetails_txtAppName" value="{{ applicant_name }}">',
    '<input id="ctl00_ContentPlaceHolder1_TabContainer1_tabDetails_txtAgtName" value="{{ agent_name }}">',
    '<textarea id="ctl00_ContentPlaceHolder1_TabContainer1_tabDetails_txtAppAddress"> {{ applicant_address }} </textarea>',
    '<textarea id="ctl00_ContentPlaceHolder1_TabContainer1_tabDetails_txtAgtAddress"> {{ agent_address }} </textarea>',
    '<input id="ctl00_ContentPlaceHolder1_TabContainer1_tabOtherDetails_txtOffName" value="{{ case_officer }}">',
    '<input id="ctl00_ContentPlaceHolder1_TabContainer1_tabOtherDetails_txtDecisionType" value="{{ decided_by }}">',
    '<input id="ctl00_ContentPlaceHolder1_TabContainer1_tabOtherDetails_txtExpiry" value="{{ application_expires_date }}">',
    '<input id="ctl00_ContentPlaceHolder1_TabContainer1_tabDecision_txtDecision" value="{{ decision }}">',
    '<input id="ctl00_ContentPlaceHolder1_TabContainer1_tabDecision_txtDecDate" value="{{ decision_date }}">',
    '<div id="ctl00_ContentPlaceHolder1_TabContainer1_tabDecision_gvCondits"> <tr /> {{ conditions }} </div>',
    ]

    def get_id_batch (self, date_from, date_to):

        response = util.open_url(self.br, self.start_url)
        if self.DEBUG: print "start page:", response.read()

        form_ok = util.setup_form(self.br, self.search_form, self.start_fields)
        if self.DEBUG: print "form:", self.br.form
        response = util.submit_form(self.br)
        if self.DEBUG: print "search page:", response.read()

        fields = self.search_fields
        fields[self.date_from_field] = date_from.strftime(self.request_date_format)
        fields[self.date_to_field] = date_to.strftime(self.request_date_format)
        form_ok = util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print "form:", self.br.form
        response = util.submit_form(self.br, self.submit_control)
        
        final_result = []
        page_count = 1
        while response:
            html = response.read()
            url = response.geturl()
            if self.DEBUG: print "result page:", html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
                page_count += 1
                fields = self.next_fields
                fields['__EVENTARGUMENT'] = 'Page$' + str(page_count)
                form_ok = util.setup_form(self.br, self.search_form, fields)
                if self.DEBUG: print "form:", self.br.form
                response = util.submit_form(self.br)
            else:
                break

        return final_result

    def get_detail_from_uid (self, uid):
        url = self.applic_url + '?AppNo=' + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    scraper = GlamorganScraper()
    scraper.run()

    # misc tests
    #scraper.DEBUG = True
    #scraper.br.set_debug_http(True)
    #print scraper.get_detail_from_uid ('2011/00820/FUL')
    #res = scraper.get_id_batch(util.get_dt('17/05/2012'), util.get_dt('21/05/2012'))
    #print len(res), res
    #print scraper.gather_ids('2012-02-01')
    #print scraper.gather_ids('2011-02-01', '2012-01-18')

# this is a scraper of Vale of Glamorgan planning applications for use by Openly Local

# also see Redcar and Cleveland

# currently designed to work backwards collecting applications from the current date to 1/1/2000

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

class GlamorganScraper(base.DateScraper):

    HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:8.0) Gecko/20100101 Firefox/8.0',
    'Accept-Charset': 'UTF-8,*',
    'Accept': 'text/html',
    'Accept-Language': 'en-gb,en',
    }

    date_from_field = 'ctl00$ContentPlaceHolder1$txtRecFrom'
    date_to_field = 'ctl00$ContentPlaceHolder1$txtRecTo'
    search_form = 'aspnetForm'
    submit_control = 'ctl00$ContentPlaceHolder1$Button1'
    request_date_format = '%d/%m/%Y'
    start_fields = { '__EVENTTARGET': 'ctl00$Header', '__EVENTARGUMENT': 'bSearch\\Pla Standard Search' }
    search_fields = { '__EVENTTARGET': '', '__EVENTARGUMENT': '' } 
    next_fields = { '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$gvPlanning', '__EVENTARGUMENT': 'Page$' }
    start_url = 'http://vogonline.planning-register.co.uk'
    applic_url = 'http://vogonline.planning-register.co.uk/PlaRecord.aspx'
    scrape_ids = """
    <table> <tr />
    {* <tr> <td />
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    </tr> *}
    </table>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="content"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <h1> Planning Application Details for : {{ reference }} </h1>
    <textarea id="ctl00_ContentPlaceHolder1_TabContainer1_tabDetails_txtLocation"> {{ address }} </textarea>
    <textarea id="ctl00_ContentPlaceHolder1_TabContainer1_tabDetails_txtProposal"> {{ description }} </textarea>
    <input id="ctl00_ContentPlaceHolder1_TabContainer1_tabOtherDetails_txtRec" value="{{ date_received }}">
    <input id="ctl00_ContentPlaceHolder1_TabContainer1_tabOtherDetails_txtComplete" value="{{ date_validated }}">
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<input id="ctl00_ContentPlaceHolder1_TabContainer1_tabDetails_txtEasting" value="{{ easting }}">',
    '<input id="ctl00_ContentPlaceHolder1_TabContainer1_tabDetails_txtNorthing" value="{{ northing }}">',
    '<input id="ctl00_ContentPlaceHolder1_TabContainer1_tabDetails_txtParish" value="{{ parish }}">',
    '<input id="ctl00_ContentPlaceHolder1_TabContainer1_tabDetails_txtAppType" value="{{ application_type }}">',
    '<input id="ctl00_ContentPlaceHolder1_TabContainer1_tabDetails_txtStatus" value="{{ status }}">',
    '<input id="ctl00_ContentPlaceHolder1_TabContainer1_tabDetails_txtAppName" value="{{ applicant_name }}">',
    '<input id="ctl00_ContentPlaceHolder1_TabContainer1_tabDetails_txtAgtName" value="{{ agent_name }}">',
    '<textarea id="ctl00_ContentPlaceHolder1_TabContainer1_tabDetails_txtAppAddress"> {{ applicant_address }} </textarea>',
    '<textarea id="ctl00_ContentPlaceHolder1_TabContainer1_tabDetails_txtAgtAddress"> {{ agent_address }} </textarea>',
    '<input id="ctl00_ContentPlaceHolder1_TabContainer1_tabOtherDetails_txtOffName" value="{{ case_officer }}">',
    '<input id="ctl00_ContentPlaceHolder1_TabContainer1_tabOtherDetails_txtDecisionType" value="{{ decided_by }}">',
    '<input id="ctl00_ContentPlaceHolder1_TabContainer1_tabOtherDetails_txtExpiry" value="{{ application_expires_date }}">',
    '<input id="ctl00_ContentPlaceHolder1_TabContainer1_tabDecision_txtDecision" value="{{ decision }}">',
    '<input id="ctl00_ContentPlaceHolder1_TabContainer1_tabDecision_txtDecDate" value="{{ decision_date }}">',
    '<div id="ctl00_ContentPlaceHolder1_TabContainer1_tabDecision_gvCondits"> <tr /> {{ conditions }} </div>',
    ]

    def get_id_batch (self, date_from, date_to):

        response = util.open_url(self.br, self.start_url)
        if self.DEBUG: print "start page:", response.read()

        form_ok = util.setup_form(self.br, self.search_form, self.start_fields)
        if self.DEBUG: print "form:", self.br.form
        response = util.submit_form(self.br)
        if self.DEBUG: print "search page:", response.read()

        fields = self.search_fields
        fields[self.date_from_field] = date_from.strftime(self.request_date_format)
        fields[self.date_to_field] = date_to.strftime(self.request_date_format)
        form_ok = util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print "form:", self.br.form
        response = util.submit_form(self.br, self.submit_control)
        
        final_result = []
        page_count = 1
        while response:
            html = response.read()
            url = response.geturl()
            if self.DEBUG: print "result page:", html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
                page_count += 1
                fields = self.next_fields
                fields['__EVENTARGUMENT'] = 'Page$' + str(page_count)
                form_ok = util.setup_form(self.br, self.search_form, fields)
                if self.DEBUG: print "form:", self.br.form
                response = util.submit_form(self.br)
            else:
                break

        return final_result

    def get_detail_from_uid (self, uid):
        url = self.applic_url + '?AppNo=' + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    scraper = GlamorganScraper()
    scraper.run()

    # misc tests
    #scraper.DEBUG = True
    #scraper.br.set_debug_http(True)
    #print scraper.get_detail_from_uid ('2011/00820/FUL')
    #res = scraper.get_id_batch(util.get_dt('17/05/2012'), util.get_dt('21/05/2012'))
    #print len(res), res
    #print scraper.gather_ids('2012-02-01')
    #print scraper.gather_ids('2011-02-01', '2012-01-18')

