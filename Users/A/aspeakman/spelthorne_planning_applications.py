# this is a scraper of Spelthorne planning applications for use by Openly Local

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

class SpelthorneScraper(base.DateScraper):

    ck = { 'name': 'astun:readTerms', 'value': 'true', 'domain': 'my.spelthorne.gov.uk', 'path': '/' }
    date_from_field = 'DATEAPRECV:FROM:DATE'
    date_to_field = 'DATEAPRECV:TO:DATE'
    search_form = '1'
    request_date_format = '%d/%m/%Y'
    next_link = 'Next >'
    start_url = 'http://my.spelthorne.gov.uk/planning/?requesttype=parsetemplate&template=DCSearchAdv.tmplt'
    applic_url = 'http://my.spelthorne.gov.uk/planning/default.aspx'
    applic_fields = { 'basepage': 'default.aspx', 'requesttype': 'parsetemplate', 'template': 'DCApplication.tmplt' }
    scrape_ids = """
    <div id="atResultsList">
    {* <div>
    <p> <a href="{{ [records].url|abs }}" /> </p>
    <p> Reference: {{ [records].uid }} | </p>
    </div> *}
    </div>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="atTabs"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <dl> <dt> Application Reference: </dt> <dd> {{ reference }} </dd>
    <dt> Address of Proposal: </dt> <dd> {{ address }} </dd>
    <dt> Proposal: </dt> <dd> {{ description }} </dd> </dl>
    <dl> <dt> Date Application Received: </dt> <dd> {{ date_received }} </dd>
    <dt> Date Application Validated: </dt> <dd> {{ date_validated }} </dd> </dl>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<dt> Planning Portal Reference Number: </dt> <dd> {{ planning_portal_id }} </dd>',
    '<dt> Type of Application: </dt> <dd> {{ application_type }} </dd>',
    '<dt> Status: </dt> <dd> {{ status }} </dd>',
    '<dt> Decision: </dt> <dd> {{ decision }} </dd>',
    '<dt> Decision Type: </dt> <dd> {{ decided_by }} </dd>',
    '<dt> Ward: </dt> <dd> {{ ward_name }} </dd>',
    '<dt> Case Officer: </dt> <dd> {{ case_officer }} </dd>',
    '<dt> Appeal Reference: </dt> <dd> {{ appeal_reference }} </dd>',
    '<dt> Appeal Status: </dt> <dd> {{ appeal_status }} </dd>',
    '<h4> Applicant </h4> <dt> Name: </dt> <dd> {{ applicant_name }} </dd> <dt> Address: </dt> <dd> {{ applicant_address }} </dd>',
    '<h4> Agent </h4> <dt> Name: </dt> <dd> {{ agent_name }} </dd> <dt> Address: </dt> <dd> {{ agent_address }} </dd>',
    '<dt> Target Determination Date: </dt> <dd> {{ target_decision_date }} </dd>',
    '<dt> Actual Committee Date: </dt> <dd> {{ meeting_date }} </dd>',
    '<dt> Neighbourhood Consultations sent on: </dt> <dd>{{ consultation_start_date }} </dd>',
    '<dt> Expiry Date for Neighbour Consultations: </dt><dd> {{ neighbour_consultation_end_date }} </dd>',
    '<dt> Standard Consultations sent on: </dt> <dd> {{ neighbour_consultation_start_date }} </dd>',
    '<dt> Expiry Date for Standard Consultations: </dt> <dd> {{ consultation_end_date }} </dd>',
    '<dt> Last Advertised on: </dt> <dd> {{ last_advertised_date }} </dd>',
    '<dt> Expiry Date for Latest Advertisement: </dt> <dd> {{ latest_advertisement_expiry_date }} </dd>',
    '<dt> Latest Site Notice posted on: </dt> <dd> {{ site_notice_start_date }} </dd>',
    '<dt> Expiry Date for Latest Site Notice: </dt> <dd>{{ site_notice_end_date }} </dd>',
    '<dt> Date Decision Made: </dt> <dd> {{ decision_date }} </dd>',
    '<dt> Date Decision Issued: </dt> <dd> {{ decision_issued_date }} </dd>',
    '<dt> Permission Expiry Date: </dt> <dd> {{ permission_expires_date }} </dd>',
    '<dt> Date Decision Printed: </dt> <dd> {{ decision_published_date }} </dd>',
    '<a class="atComments forwardlink" href="{{ comment_url|abs }}"> Comment on this application </a>',
    ]

    def __init__(self):
        self.br, self.handler, self.cj = util.get_browser(self.HEADERS)
        util.set_cookie(self.cj, self.ck['name'], self.ck['value'], self.ck.get('domain'), self.ck.get('path', '/'))   

    def get_id_batch (self, date_from, date_to):

        response = util.open_url(self.br, self.start_url)
        if self.DEBUG: print "start page:", response.read()

        fields = { }
        fields[self.date_from_field] = date_from.strftime(self.request_date_format)
        fields[self.date_to_field] = date_to.strftime(self.request_date_format)
        form_ok = util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print "form:", self.br.form
        response = util.submit_form(self.br)

        html = response.read()
        url = response.geturl()
        if self.DEBUG: print "result page:", url, html

        final_result = []
        while response:
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
                try:
                    response = self.br.follow_link(text=self.next_link)
                except:
                    break
                html = response.read()
                url = response.geturl()
                if self.DEBUG: print "next page:", html
            else:
                break

        return final_result

    def get_detail_from_uid (self, uid):
        self.applic_fields['Filter'] = "^REFVAL^='" + uid + "'"
        url = self.applic_url + '?' + urllib.urlencode(self.applic_fields)
        if self.DEBUG: print url
        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    scraper = SpelthorneScraper()
    scraper.run()

    # misc tests
    #scraper.DEBUG = True
    #scraper.br.set_debug_http(True)
    #print scraper.get_detail_from_uid ('12/00779/ADV')
    #res = scraper.get_id_batch(util.get_dt('11/06/2012'), util.get_dt('19/07/2012'))
    #print len(res), res
    #print scraper.gather_ids('2012-02-01')
    #print scraper.gather_ids('2011-02-01', '2012-01-18')

# this is a scraper of Spelthorne planning applications for use by Openly Local

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

class SpelthorneScraper(base.DateScraper):

    ck = { 'name': 'astun:readTerms', 'value': 'true', 'domain': 'my.spelthorne.gov.uk', 'path': '/' }
    date_from_field = 'DATEAPRECV:FROM:DATE'
    date_to_field = 'DATEAPRECV:TO:DATE'
    search_form = '1'
    request_date_format = '%d/%m/%Y'
    next_link = 'Next >'
    start_url = 'http://my.spelthorne.gov.uk/planning/?requesttype=parsetemplate&template=DCSearchAdv.tmplt'
    applic_url = 'http://my.spelthorne.gov.uk/planning/default.aspx'
    applic_fields = { 'basepage': 'default.aspx', 'requesttype': 'parsetemplate', 'template': 'DCApplication.tmplt' }
    scrape_ids = """
    <div id="atResultsList">
    {* <div>
    <p> <a href="{{ [records].url|abs }}" /> </p>
    <p> Reference: {{ [records].uid }} | </p>
    </div> *}
    </div>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="atTabs"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <dl> <dt> Application Reference: </dt> <dd> {{ reference }} </dd>
    <dt> Address of Proposal: </dt> <dd> {{ address }} </dd>
    <dt> Proposal: </dt> <dd> {{ description }} </dd> </dl>
    <dl> <dt> Date Application Received: </dt> <dd> {{ date_received }} </dd>
    <dt> Date Application Validated: </dt> <dd> {{ date_validated }} </dd> </dl>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<dt> Planning Portal Reference Number: </dt> <dd> {{ planning_portal_id }} </dd>',
    '<dt> Type of Application: </dt> <dd> {{ application_type }} </dd>',
    '<dt> Status: </dt> <dd> {{ status }} </dd>',
    '<dt> Decision: </dt> <dd> {{ decision }} </dd>',
    '<dt> Decision Type: </dt> <dd> {{ decided_by }} </dd>',
    '<dt> Ward: </dt> <dd> {{ ward_name }} </dd>',
    '<dt> Case Officer: </dt> <dd> {{ case_officer }} </dd>',
    '<dt> Appeal Reference: </dt> <dd> {{ appeal_reference }} </dd>',
    '<dt> Appeal Status: </dt> <dd> {{ appeal_status }} </dd>',
    '<h4> Applicant </h4> <dt> Name: </dt> <dd> {{ applicant_name }} </dd> <dt> Address: </dt> <dd> {{ applicant_address }} </dd>',
    '<h4> Agent </h4> <dt> Name: </dt> <dd> {{ agent_name }} </dd> <dt> Address: </dt> <dd> {{ agent_address }} </dd>',
    '<dt> Target Determination Date: </dt> <dd> {{ target_decision_date }} </dd>',
    '<dt> Actual Committee Date: </dt> <dd> {{ meeting_date }} </dd>',
    '<dt> Neighbourhood Consultations sent on: </dt> <dd>{{ consultation_start_date }} </dd>',
    '<dt> Expiry Date for Neighbour Consultations: </dt><dd> {{ neighbour_consultation_end_date }} </dd>',
    '<dt> Standard Consultations sent on: </dt> <dd> {{ neighbour_consultation_start_date }} </dd>',
    '<dt> Expiry Date for Standard Consultations: </dt> <dd> {{ consultation_end_date }} </dd>',
    '<dt> Last Advertised on: </dt> <dd> {{ last_advertised_date }} </dd>',
    '<dt> Expiry Date for Latest Advertisement: </dt> <dd> {{ latest_advertisement_expiry_date }} </dd>',
    '<dt> Latest Site Notice posted on: </dt> <dd> {{ site_notice_start_date }} </dd>',
    '<dt> Expiry Date for Latest Site Notice: </dt> <dd>{{ site_notice_end_date }} </dd>',
    '<dt> Date Decision Made: </dt> <dd> {{ decision_date }} </dd>',
    '<dt> Date Decision Issued: </dt> <dd> {{ decision_issued_date }} </dd>',
    '<dt> Permission Expiry Date: </dt> <dd> {{ permission_expires_date }} </dd>',
    '<dt> Date Decision Printed: </dt> <dd> {{ decision_published_date }} </dd>',
    '<a class="atComments forwardlink" href="{{ comment_url|abs }}"> Comment on this application </a>',
    ]

    def __init__(self):
        self.br, self.handler, self.cj = util.get_browser(self.HEADERS)
        util.set_cookie(self.cj, self.ck['name'], self.ck['value'], self.ck.get('domain'), self.ck.get('path', '/'))   

    def get_id_batch (self, date_from, date_to):

        response = util.open_url(self.br, self.start_url)
        if self.DEBUG: print "start page:", response.read()

        fields = { }
        fields[self.date_from_field] = date_from.strftime(self.request_date_format)
        fields[self.date_to_field] = date_to.strftime(self.request_date_format)
        form_ok = util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print "form:", self.br.form
        response = util.submit_form(self.br)

        html = response.read()
        url = response.geturl()
        if self.DEBUG: print "result page:", url, html

        final_result = []
        while response:
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
                try:
                    response = self.br.follow_link(text=self.next_link)
                except:
                    break
                html = response.read()
                url = response.geturl()
                if self.DEBUG: print "next page:", html
            else:
                break

        return final_result

    def get_detail_from_uid (self, uid):
        self.applic_fields['Filter'] = "^REFVAL^='" + uid + "'"
        url = self.applic_url + '?' + urllib.urlencode(self.applic_fields)
        if self.DEBUG: print url
        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    scraper = SpelthorneScraper()
    scraper.run()

    # misc tests
    #scraper.DEBUG = True
    #scraper.br.set_debug_http(True)
    #print scraper.get_detail_from_uid ('12/00779/ADV')
    #res = scraper.get_id_batch(util.get_dt('11/06/2012'), util.get_dt('19/07/2012'))
    #print len(res), res
    #print scraper.gather_ids('2012-02-01')
    #print scraper.gather_ids('2011-02-01', '2012-01-18')

