# this is a scraper of West Devon planning applications for use by Openly Local

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

class WestDevonScraper(base.DateScraper):

    MAX_ID_BATCH = 200 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 150 # max application details to scrape in one go

    search_url = 'http://www.westdevon.gov.uk/PlanningApplicationSearch/PlanningSearch.aspx?doc=16265&cat=3185'
    applic_url = 'http://www.westdevon.gov.uk/PlanningApplicationSearch/ApplicationDetails.aspx?planningid='
    date_from_field = {
        'day': 'ctl00$mp_Application_Content$ValidationDateStartDay',
        'month': 'ctl00$mp_Application_Content$ValidationDateStartMonth',
        'year': 'ctl00$mp_Application_Content$ValidationDateStartYear',
        }
    date_to_field = {
        'day': 'ctl00$mp_Application_Content$ValidationDateEndDay',
        'month': 'ctl00$mp_Application_Content$ValidationDateEndMonth',
        'year': 'ctl00$mp_Application_Content$ValidationDateEndYear',
        }
    request_date_format = '%d/%B/%Y'
    search_form = 'aspnetForm'
    scrape_ids = """
    <form id="aspnetForm">
    {* <fieldset>
    <legend> Planning ID: {{ [records].uid }} </legend>
    <tr> <a href="{{ [records].url|abs }}"> </a> </tr>
    </fieldset> *}
    </form>
    """
    scrape_data_block = """
    <div id="content"> {{ block|html }} </div>
    """
    scrape_min_data = """
    <h1> Planning Application {{ reference }} </h1>
    <tr> <th> Site Address </th> <td> {{ address }} </td> </tr>
    <tr> <th> Proposal </th> <td> {{ description }} </td> </tr>
    <tr> <th> Date Received </th> <td> {{ date_received }} </td> </tr>
    <tr> <th> Date Registered </th> <td> {{ date_validated }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr> <th> Application Status </th> <td> {{ status }} </td> </tr>',
    '<tr> <th> Application Type </th> <td> {{ application_type }} </td> </tr>',
    """<tr> <th> Decision </th> <td> {{ decision }} </td> </tr>
    <tr> <th> Decision Date </th> <td> {{ decision_date }} </td> </tr>""",
    '<tr> <th> Case Officer </th> <td> {{ case_officer }} </td> </tr>',
    '<tr> <th> Target Date </th> <td> {{ target_decision_date }} </td> </tr>',
    '<tr> <td> Consultations Expire </th> <td> {{ consultation_end_date }} </td> </tr>',
    '<tr> <th> Applicant </th> <td> {{ applicant_name }} , {{ applicant_address }} </td> </tr>',
    '<tr> <th> Agent </th> <td> {{ agent_name }} , {{ agent_address }} </td> </tr>',
    '<a href="{{ comment_url|abs }}"> <strong> Click here if you wish to comment on this application </strong> </a>'
    ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)

        fields = {}
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
        response = util.submit_form(self.br)

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
        url = self.applic_url + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    scraper = WestDevonScraper()
    scraper.run()

    # misc test calls
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('03187/2012')
    #result = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('18/09/2011'))
    #print len(result), result

    



# this is a scraper of West Devon planning applications for use by Openly Local

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

class WestDevonScraper(base.DateScraper):

    MAX_ID_BATCH = 200 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 150 # max application details to scrape in one go

    search_url = 'http://www.westdevon.gov.uk/PlanningApplicationSearch/PlanningSearch.aspx?doc=16265&cat=3185'
    applic_url = 'http://www.westdevon.gov.uk/PlanningApplicationSearch/ApplicationDetails.aspx?planningid='
    date_from_field = {
        'day': 'ctl00$mp_Application_Content$ValidationDateStartDay',
        'month': 'ctl00$mp_Application_Content$ValidationDateStartMonth',
        'year': 'ctl00$mp_Application_Content$ValidationDateStartYear',
        }
    date_to_field = {
        'day': 'ctl00$mp_Application_Content$ValidationDateEndDay',
        'month': 'ctl00$mp_Application_Content$ValidationDateEndMonth',
        'year': 'ctl00$mp_Application_Content$ValidationDateEndYear',
        }
    request_date_format = '%d/%B/%Y'
    search_form = 'aspnetForm'
    scrape_ids = """
    <form id="aspnetForm">
    {* <fieldset>
    <legend> Planning ID: {{ [records].uid }} </legend>
    <tr> <a href="{{ [records].url|abs }}"> </a> </tr>
    </fieldset> *}
    </form>
    """
    scrape_data_block = """
    <div id="content"> {{ block|html }} </div>
    """
    scrape_min_data = """
    <h1> Planning Application {{ reference }} </h1>
    <tr> <th> Site Address </th> <td> {{ address }} </td> </tr>
    <tr> <th> Proposal </th> <td> {{ description }} </td> </tr>
    <tr> <th> Date Received </th> <td> {{ date_received }} </td> </tr>
    <tr> <th> Date Registered </th> <td> {{ date_validated }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr> <th> Application Status </th> <td> {{ status }} </td> </tr>',
    '<tr> <th> Application Type </th> <td> {{ application_type }} </td> </tr>',
    """<tr> <th> Decision </th> <td> {{ decision }} </td> </tr>
    <tr> <th> Decision Date </th> <td> {{ decision_date }} </td> </tr>""",
    '<tr> <th> Case Officer </th> <td> {{ case_officer }} </td> </tr>',
    '<tr> <th> Target Date </th> <td> {{ target_decision_date }} </td> </tr>',
    '<tr> <td> Consultations Expire </th> <td> {{ consultation_end_date }} </td> </tr>',
    '<tr> <th> Applicant </th> <td> {{ applicant_name }} , {{ applicant_address }} </td> </tr>',
    '<tr> <th> Agent </th> <td> {{ agent_name }} , {{ agent_address }} </td> </tr>',
    '<a href="{{ comment_url|abs }}"> <strong> Click here if you wish to comment on this application </strong> </a>'
    ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)

        fields = {}
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
        response = util.submit_form(self.br)

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
        url = self.applic_url + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    scraper = WestDevonScraper()
    scraper.run()

    # misc test calls
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('03187/2012')
    #result = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('18/09/2011'))
    #print len(result), result

    



