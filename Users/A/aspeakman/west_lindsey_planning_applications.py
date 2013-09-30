# this is a scraper of West Lindsey planning applications for use by Openly Local

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

class WestLindseyScraper(base.DateScraper):

    MAX_ID_BATCH = 150 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 100 # max application details to scrape in one go

    search_url = 'http://planning.west-lindsey.gov.uk/planning/'
    applic_url = 'http://planning.west-lindsey.gov.uk/planning/flarexmlDet.asp?LARef='
    date_from_field = {
        'day': 'StartDay',
        'month': 'StartMonth',
        'year': 'StartYear',
        }
    date_to_field = {
        'day': 'EndDay',
        'month': 'EndMonth',
        'year': 'EndYear',
        }
    request_date_format = '%-d/%-m/%Y'
    search_form = '1'
    scrape_ids = """
    <table id="listingtable">
    {* <tr> <td> <a href="{{ [records].url|abs }}">
    {{ [records].uid }} </a> </td> </tr> *}
    </table>
    """
    scrape_data_block = """
    <table id="table1"> {{ block|html }} </table>
    """
    scrape_min_data = """
    <td> <b> Planning Application No: </b> {{ reference }} </td>
    <td> <b> Application Date: </b> {{ date_validated }} </td>
    <td> <b> Description of Proposal: </b> {{ description }} </td>
    <td> <b> Location of Proposal: </b> {{ address }} </td>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<td> <b> Planning Officer: </b> {{ case_officer }} </td>',
    '<p> <b> Applicant Name: </b> {{ applicant_name }} </p>',
    '<p> <b> Ward: </b> {{ ward_name }} </p>',
    '<p> <b> Parish: </b> {{ parish }} </p>',
    '<td> <b> Status: </b> {{ status }} </td>',
    '<td> <b> Agent Name: </b> {{ agent_name }} <br> {{ agent_address }} </td>',
    """<td> <b> Date of Decision: </b> {{ decision_date }} </td>
    <td> <b> Decision: </b> {{ decision }} </td>""",
    '<td> <b> Appeal Date: </b> {{ appeal_date }} </td>',
    '<td> <b> Appeal Result: </b> {{ appeal_result }} </td>',
    ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)

        fields = { }
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

    scraper = WestLindseyScraper()
    scraper.run()

    # misc test calls
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('127688')
    #result = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('18/08/2011'))
    #print len(result), result

    



# this is a scraper of West Lindsey planning applications for use by Openly Local

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

class WestLindseyScraper(base.DateScraper):

    MAX_ID_BATCH = 150 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 100 # max application details to scrape in one go

    search_url = 'http://planning.west-lindsey.gov.uk/planning/'
    applic_url = 'http://planning.west-lindsey.gov.uk/planning/flarexmlDet.asp?LARef='
    date_from_field = {
        'day': 'StartDay',
        'month': 'StartMonth',
        'year': 'StartYear',
        }
    date_to_field = {
        'day': 'EndDay',
        'month': 'EndMonth',
        'year': 'EndYear',
        }
    request_date_format = '%-d/%-m/%Y'
    search_form = '1'
    scrape_ids = """
    <table id="listingtable">
    {* <tr> <td> <a href="{{ [records].url|abs }}">
    {{ [records].uid }} </a> </td> </tr> *}
    </table>
    """
    scrape_data_block = """
    <table id="table1"> {{ block|html }} </table>
    """
    scrape_min_data = """
    <td> <b> Planning Application No: </b> {{ reference }} </td>
    <td> <b> Application Date: </b> {{ date_validated }} </td>
    <td> <b> Description of Proposal: </b> {{ description }} </td>
    <td> <b> Location of Proposal: </b> {{ address }} </td>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<td> <b> Planning Officer: </b> {{ case_officer }} </td>',
    '<p> <b> Applicant Name: </b> {{ applicant_name }} </p>',
    '<p> <b> Ward: </b> {{ ward_name }} </p>',
    '<p> <b> Parish: </b> {{ parish }} </p>',
    '<td> <b> Status: </b> {{ status }} </td>',
    '<td> <b> Agent Name: </b> {{ agent_name }} <br> {{ agent_address }} </td>',
    """<td> <b> Date of Decision: </b> {{ decision_date }} </td>
    <td> <b> Decision: </b> {{ decision }} </td>""",
    '<td> <b> Appeal Date: </b> {{ appeal_date }} </td>',
    '<td> <b> Appeal Result: </b> {{ appeal_result }} </td>',
    ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)

        fields = { }
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

    scraper = WestLindseyScraper()
    scraper.run()

    # misc test calls
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('127688')
    #result = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('18/08/2011'))
    #print len(result), result

    



