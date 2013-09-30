# this is a scraper of Halton planning applications for use by Openly Local

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

class HaltonScraper(base.DateScraper):

    MAX_ID_BATCH = 350 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 250 # max application details to scrape in one go

    search_url = 'http://www.halton.gov.uk/planningapps/'
    date_from_field = 'DateApValFrom'
    date_to_field = 'DateApValTo'
    ref_field = 'CaseNo'
    next_form = 'formNext'
    search_submit = 'Action'
    request_date_format = '%d/%m/%Y'
    search_form = '3'
    scrape_ids = """
    <div id="maincontentContainer">
    {* <table class="tab"> <table />
    <tr> Case No: {{ [records].uid }} Officer name: </tr>
    </table> *}
    </div>
    """
    address_regex = re.compile(r'\s+AT\s+(.+?)$', re.I) # matches AT address at the end of the proposal (ignoring case)
    scrape_data_block = """
    <table id="Details0"> {{ block|html }} </table>
    """
    scrape_min_data = """
    <tr> <td> Case No </td> <td> {{ reference }} </td> </tr>
    <tr> <td> Details of Proposal </td> <td> {{ description }} </td> </tr>
    <tr> <td> Date Received </td> <td> {{ date_received }} </td> </tr>
    <tr> <td> Date Valid </td> <td> {{ date_validated }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr> <td> Officer Name </td> <td> {{ case_officer }} </td> </tr>',
    '<tr> <td> Status </td> <td> {{ status }} </td> </tr>',
    '<tr> <td> Ward </td> <td> {{ ward_name }} </td> </tr>',
    '<tr> <td> Applicants Name </td> <td> {{ applicant_name }} </td> <td> Applicants Address </td> <td> {{ applicant_address }} </td> </tr>',
    '<tr> <td> Agents Name </td> <td> {{ agent_name }} </td> <td> Agents Address </td> <td> {{ agent_address }} </td> </tr>',
    '<tr> <td> Comment Between </td> <td> {{ consultation_start_date }} and {{ consultation_end_date }} </td> </tr>',
    '<tr> <td> 8 Week Target Date </td> <td> {{ application_expires_date }} </td> </tr>',
    '<tr> <td> Decision Date </td> <td> {{ decision_date }} </td> </tr>',
    ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)

        fields = { }
        date_to = date_to + timedelta(days=1) # end date is exclusive
        fields [self.date_from_field] = date_from.strftime(self.request_date_format)
        fields [self.date_to_field] = date_to.strftime(self.request_date_format)

        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br)
        
        final_result = []
        while response:
            url = response.geturl()
            html = response.read()
            if self.DEBUG: print html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            else:
                break
            try:
                util.setup_form(self.br, self.next_form)
                if self.DEBUG: print self.br.form
                response = util.submit_form(self.br, self.search_submit)
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
            return self.get_detail(html, url)
        except:
            return None

    # scrape detailed information on one record given its HTML and URL
    def get_detail (self, html, url, scrape_data_block = None, scrape_min_data = None, scrape_optional_data = []):
        result = base.DateScraper.get_detail(self, html, url, scrape_data_block, scrape_min_data, scrape_optional_data)
        if not result: return None
        if result.get('description'):
            address_match = self.address_regex.search(result['description'])
            if address_match and address_match.group(1):
                address = address_match.group(1)
                result['address'] = address
            else:
                result['address'] = result['description']
        return result

if __name__ == 'scraper':

    scraper = HaltonScraper()
    scraper.run()

    # misc test calls
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/00342/FUL')
    #result = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('08/09/2011'))
    #print len(result), result

    




# this is a scraper of Halton planning applications for use by Openly Local

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

class HaltonScraper(base.DateScraper):

    MAX_ID_BATCH = 350 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 250 # max application details to scrape in one go

    search_url = 'http://www.halton.gov.uk/planningapps/'
    date_from_field = 'DateApValFrom'
    date_to_field = 'DateApValTo'
    ref_field = 'CaseNo'
    next_form = 'formNext'
    search_submit = 'Action'
    request_date_format = '%d/%m/%Y'
    search_form = '3'
    scrape_ids = """
    <div id="maincontentContainer">
    {* <table class="tab"> <table />
    <tr> Case No: {{ [records].uid }} Officer name: </tr>
    </table> *}
    </div>
    """
    address_regex = re.compile(r'\s+AT\s+(.+?)$', re.I) # matches AT address at the end of the proposal (ignoring case)
    scrape_data_block = """
    <table id="Details0"> {{ block|html }} </table>
    """
    scrape_min_data = """
    <tr> <td> Case No </td> <td> {{ reference }} </td> </tr>
    <tr> <td> Details of Proposal </td> <td> {{ description }} </td> </tr>
    <tr> <td> Date Received </td> <td> {{ date_received }} </td> </tr>
    <tr> <td> Date Valid </td> <td> {{ date_validated }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr> <td> Officer Name </td> <td> {{ case_officer }} </td> </tr>',
    '<tr> <td> Status </td> <td> {{ status }} </td> </tr>',
    '<tr> <td> Ward </td> <td> {{ ward_name }} </td> </tr>',
    '<tr> <td> Applicants Name </td> <td> {{ applicant_name }} </td> <td> Applicants Address </td> <td> {{ applicant_address }} </td> </tr>',
    '<tr> <td> Agents Name </td> <td> {{ agent_name }} </td> <td> Agents Address </td> <td> {{ agent_address }} </td> </tr>',
    '<tr> <td> Comment Between </td> <td> {{ consultation_start_date }} and {{ consultation_end_date }} </td> </tr>',
    '<tr> <td> 8 Week Target Date </td> <td> {{ application_expires_date }} </td> </tr>',
    '<tr> <td> Decision Date </td> <td> {{ decision_date }} </td> </tr>',
    ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)

        fields = { }
        date_to = date_to + timedelta(days=1) # end date is exclusive
        fields [self.date_from_field] = date_from.strftime(self.request_date_format)
        fields [self.date_to_field] = date_to.strftime(self.request_date_format)

        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br)
        
        final_result = []
        while response:
            url = response.geturl()
            html = response.read()
            if self.DEBUG: print html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            else:
                break
            try:
                util.setup_form(self.br, self.next_form)
                if self.DEBUG: print self.br.form
                response = util.submit_form(self.br, self.search_submit)
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
            return self.get_detail(html, url)
        except:
            return None

    # scrape detailed information on one record given its HTML and URL
    def get_detail (self, html, url, scrape_data_block = None, scrape_min_data = None, scrape_optional_data = []):
        result = base.DateScraper.get_detail(self, html, url, scrape_data_block, scrape_min_data, scrape_optional_data)
        if not result: return None
        if result.get('description'):
            address_match = self.address_regex.search(result['description'])
            if address_match and address_match.group(1):
                address = address_match.group(1)
                result['address'] = address
            else:
                result['address'] = result['description']
        return result

if __name__ == 'scraper':

    scraper = HaltonScraper()
    scraper.run()

    # misc test calls
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/00342/FUL')
    #result = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('08/09/2011'))
    #print len(result), result

    




