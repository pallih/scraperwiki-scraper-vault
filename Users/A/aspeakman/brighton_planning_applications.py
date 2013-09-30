# this is a scraper of Brighton planning applications for use by Openly Local

# currently designed to work backwards collecting applications from the current date to 1/1/2000

# note currently excludes enforcement notices = development control only

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import urllib
import urlparse

base = scraperwiki.utils.swimport("openlylocal_base_scraper")
scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")

class BrightonScraper(base.DateScraper):

    date_from_field = 'date_from'
    date_to_field = 'date_to'
    search_form = '0'
    start_fields = { 'accept': '1', }
    search_fields = { 'dateFilterCol': 'Received', }
    request_date_format = '%d/%m/%Y'
    start_url = 'http://www.brighton-hove.gov.uk/index.cfm?request=c1199915&action=showform'
    applic_url = 'http://www.brighton-hove.gov.uk/index.cfm?request=c1199915&action=showDetail'
    next_form = '0'
    next_submit = 'next'
    scrape_ids = """
    <div class="base-layer2">
    {* <div class="pl-listTop-row"> <h4> {{ [records].uid }} </h4> </div>
    <div class="pl-table-row "> <form action="{{ [records].url|abs }}" /> </div>
     *}
    </div>
    """

    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="centreColumn"> <div class="base-layer"> {{ block|html }} </div> </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <div class="pl-listTop-row"> <h2> Details for application number: {{ reference }} </h2> </div>
    <div class="pl-table-row-noline"> address: {{ address }} </div>
    <div class="pl-table-row-noline"> description: {{ description }} </div>
    <div class="pl-table-row-noline"> received date: {{ date_received }} </div>
    <div class="pl-table-row-noline"> valid date: {{ date_validated }} </div>
    """ 
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<div class="pl-table-row-noline"> application type: {{ application_type }} </div>', # OK
    
    '<div class="pl-table-row-noline"> ward: {{ ward_name }} </div>', # OK
    '<div class="pl-table-row-noline"> status: {{ status }} </div>', # OK
    '<div class="pl-table-row-noline"> decision: {{ decision }} </div>', # OK
    '<div class="pl-table-row-noline"> target decision date: {{ target_decision_date }} </div>', # OK
    '<div class="pl-table-row-noline"> decision date: {{ decision_date }} </div>', # OK
    '<div class="pl-table-row-noline"> officer: {{ case_officer }} </div>', # OK
    '<div class="pl-table-row-noline"> agent: {{ agent_name }} <br> {{ agent_address }} </div>', # OK
    '<div class="pl-table-row-noline"> applicant: {{ applicant_name }} <br> {{ applicant_address }} </div>', #OK
    '<div class="pl-table-row-noline"> development type: {{ development_type }} </div>', # OK
    '<div class="pl-table-row-noline"> development types: {{ development_type }} </div>', # OK
    '<div class="pl-table-row-noline"> conservation area: {{ district }} </div>', # OK
    ]


    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.start_url, urllib.urlencode(self.start_fields))

        self.search_fields[self.date_from_field] = date_from.strftime(self.request_date_format)
        self.search_fields[self.date_to_field] = date_to.strftime(self.request_date_format)
        #print self.search_fields
        form_ok = util.setup_form(self.br, self.search_form, self.search_fields )
        
        response = util.submit_form(self.br)

        final_result = []
        while response:
            html = response.read()
            url = response.geturl()
            #print html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            try:
                next_form_ok = util.setup_form(self.br, self.next_form )
                response = util.submit_form(self.br, self.next_submit)
            except:
                response = None
        return final_result

    def get_detail_from_uid (self, uid):
        url = self.applic_url + '&APPLICATION_NUMBER=' + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    scraper = BrightonScraper()
    scraper.run()

    #scraper.DEBUG = True

    # misc test calls
    #print scraper.get_detail_from_uid ('BH2011/02336')
    #result = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('08/08/2011')) 
    #print len(result), result
    #print scraper.get_id_batch(util.get_dt('23/03/2012'), util.get_dt('25/03/2012'))


# this is a scraper of Brighton planning applications for use by Openly Local

# currently designed to work backwards collecting applications from the current date to 1/1/2000

# note currently excludes enforcement notices = development control only

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import urllib
import urlparse

base = scraperwiki.utils.swimport("openlylocal_base_scraper")
scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")

class BrightonScraper(base.DateScraper):

    date_from_field = 'date_from'
    date_to_field = 'date_to'
    search_form = '0'
    start_fields = { 'accept': '1', }
    search_fields = { 'dateFilterCol': 'Received', }
    request_date_format = '%d/%m/%Y'
    start_url = 'http://www.brighton-hove.gov.uk/index.cfm?request=c1199915&action=showform'
    applic_url = 'http://www.brighton-hove.gov.uk/index.cfm?request=c1199915&action=showDetail'
    next_form = '0'
    next_submit = 'next'
    scrape_ids = """
    <div class="base-layer2">
    {* <div class="pl-listTop-row"> <h4> {{ [records].uid }} </h4> </div>
    <div class="pl-table-row "> <form action="{{ [records].url|abs }}" /> </div>
     *}
    </div>
    """

    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="centreColumn"> <div class="base-layer"> {{ block|html }} </div> </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <div class="pl-listTop-row"> <h2> Details for application number: {{ reference }} </h2> </div>
    <div class="pl-table-row-noline"> address: {{ address }} </div>
    <div class="pl-table-row-noline"> description: {{ description }} </div>
    <div class="pl-table-row-noline"> received date: {{ date_received }} </div>
    <div class="pl-table-row-noline"> valid date: {{ date_validated }} </div>
    """ 
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<div class="pl-table-row-noline"> application type: {{ application_type }} </div>', # OK
    
    '<div class="pl-table-row-noline"> ward: {{ ward_name }} </div>', # OK
    '<div class="pl-table-row-noline"> status: {{ status }} </div>', # OK
    '<div class="pl-table-row-noline"> decision: {{ decision }} </div>', # OK
    '<div class="pl-table-row-noline"> target decision date: {{ target_decision_date }} </div>', # OK
    '<div class="pl-table-row-noline"> decision date: {{ decision_date }} </div>', # OK
    '<div class="pl-table-row-noline"> officer: {{ case_officer }} </div>', # OK
    '<div class="pl-table-row-noline"> agent: {{ agent_name }} <br> {{ agent_address }} </div>', # OK
    '<div class="pl-table-row-noline"> applicant: {{ applicant_name }} <br> {{ applicant_address }} </div>', #OK
    '<div class="pl-table-row-noline"> development type: {{ development_type }} </div>', # OK
    '<div class="pl-table-row-noline"> development types: {{ development_type }} </div>', # OK
    '<div class="pl-table-row-noline"> conservation area: {{ district }} </div>', # OK
    ]


    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.start_url, urllib.urlencode(self.start_fields))

        self.search_fields[self.date_from_field] = date_from.strftime(self.request_date_format)
        self.search_fields[self.date_to_field] = date_to.strftime(self.request_date_format)
        #print self.search_fields
        form_ok = util.setup_form(self.br, self.search_form, self.search_fields )
        
        response = util.submit_form(self.br)

        final_result = []
        while response:
            html = response.read()
            url = response.geturl()
            #print html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            try:
                next_form_ok = util.setup_form(self.br, self.next_form )
                response = util.submit_form(self.br, self.next_submit)
            except:
                response = None
        return final_result

    def get_detail_from_uid (self, uid):
        url = self.applic_url + '&APPLICATION_NUMBER=' + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    scraper = BrightonScraper()
    scraper.run()

    #scraper.DEBUG = True

    # misc test calls
    #print scraper.get_detail_from_uid ('BH2011/02336')
    #result = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('08/08/2011')) 
    #print len(result), result
    #print scraper.get_id_batch(util.get_dt('23/03/2012'), util.get_dt('25/03/2012'))


