# this is a scraper of Kensington and Chelsea planning applications for use by Openly Local

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

class KensingtonScraper(base.PeriodScraper):

    MAX_ID_BATCH = 350 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 300 # max application details to scrape in one go
    PERIOD_TYPE = 'Friday'

    date_field = 'WeekEndDate'
    query_fields = {  'submit': 'search', 'order': 'Received Date' }
    request_date_format = '%-d/%-m/%Y'
    search_url = 'http://www.rbkc.gov.uk/Planning/scripts/weeklyresults.asp'
    applic_url = 'http://www.rbkc.gov.uk/planning/searches/details.aspx?batch=20&type=&tab='
    scrape_ids = """
    <table id="Table1"> <tr />
    {* <tr>
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
    <table id="property-details">
    <tr> Case reference: {{ reference }} </tr>
    <tr> Address: {{ address }} </tr>
    </table>
    <table id="proposal-details">
    <tr> Proposed development  {{ description }} </tr>
    <tr> Date received: {{ date_received }} </tr>
    <tr> Registration date: <br> (Statutory start date)  {{ date_validated }} </tr>
    </table>"""
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    "<tr> Applicant's name: {{ applicant_name }} </tr>",
    "<tr> Contact name: {{ agent_name }} </tr>", # note bug was agent_address
    "<tr> Contact address: {{ agent_address }} </tr>",
    "<tr> Contact telephone: {{ agent_tel }} </tr>",
    '<tr> Public consultation ends: {{ consultation_end_date }} </tr>',
    '<tr> Planning case officer: {{ case_officer }} </tr>',
    '<tr> <th> Target date for decision: </th> {{ target_decision_date }} </tr>',
    '<tr> <th> Decision date: </th> {{ decision_date }} </tr>',
    '<table id="decision-details"> <tr> <th> Decision: </th> {{ decision }} </tr> </table>',
    '<tr> Application type: {{ application_type }} </tr>',
    '<tr> Application status: {{ status }} </tr>',
    '<tr> Ward: {{ ward_name }} </tr>',
    '<tr> Conservation area: {{ district }} </tr>',
    '<tr> <th> Appeal start date: </th> {{ appeal_date }} </tr>',
    '<tr> <th> Appeal decision: </th> {{ appeal_result }} </tr> <tr> <th> Appeal decision date: </th> {{ appeal_decision_date }} </tr>',
    
    ]

    def get_id_period (self, date): 

        fields = self.query_fields
        from_iso_dt, to_iso_dt = util.inc_dt(date.strftime(util.ISO8601_DATE), util.ISO8601_DATE, self.PERIOD_TYPE)
        from_dt = util.get_dt(from_iso_dt, util.ISO8601_DATE)
        to_dt = util.get_dt(to_iso_dt, util.ISO8601_DATE)

        fields [self.date_field] = to_dt.strftime(self.request_date_format)

        final_result = []
        
        response = util.open_url(self.br, self.search_url, fields, 'POST')
        if response:
            html = response.read()
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
        else:
            return [], None, None

        return final_result, from_dt, to_dt # note weekly result might some times be legitimately empty
        
    def get_detail_from_uid (self, uid):
        url = self.applic_url + '&id=' + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    scraper = KensingtonScraper()
    scraper.run()

    #scraper.DEBUG = True
    # misc tests
    #print scraper.get_detail_from_uid ('CA/12/00942')
    #print scraper.get_detail_from_uid ('LB/11/00590')
    #result = scraper.get_id_period(util.get_dt('01/03/2011'))
    #print result
    #print scraper.gather_ids('2010-02-01')
    #print scraper.gather_ids(None, None)
    #scraper.gather_current_ids()
# this is a scraper of Kensington and Chelsea planning applications for use by Openly Local

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

class KensingtonScraper(base.PeriodScraper):

    MAX_ID_BATCH = 350 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 300 # max application details to scrape in one go
    PERIOD_TYPE = 'Friday'

    date_field = 'WeekEndDate'
    query_fields = {  'submit': 'search', 'order': 'Received Date' }
    request_date_format = '%-d/%-m/%Y'
    search_url = 'http://www.rbkc.gov.uk/Planning/scripts/weeklyresults.asp'
    applic_url = 'http://www.rbkc.gov.uk/planning/searches/details.aspx?batch=20&type=&tab='
    scrape_ids = """
    <table id="Table1"> <tr />
    {* <tr>
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
    <table id="property-details">
    <tr> Case reference: {{ reference }} </tr>
    <tr> Address: {{ address }} </tr>
    </table>
    <table id="proposal-details">
    <tr> Proposed development  {{ description }} </tr>
    <tr> Date received: {{ date_received }} </tr>
    <tr> Registration date: <br> (Statutory start date)  {{ date_validated }} </tr>
    </table>"""
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    "<tr> Applicant's name: {{ applicant_name }} </tr>",
    "<tr> Contact name: {{ agent_name }} </tr>", # note bug was agent_address
    "<tr> Contact address: {{ agent_address }} </tr>",
    "<tr> Contact telephone: {{ agent_tel }} </tr>",
    '<tr> Public consultation ends: {{ consultation_end_date }} </tr>',
    '<tr> Planning case officer: {{ case_officer }} </tr>',
    '<tr> <th> Target date for decision: </th> {{ target_decision_date }} </tr>',
    '<tr> <th> Decision date: </th> {{ decision_date }} </tr>',
    '<table id="decision-details"> <tr> <th> Decision: </th> {{ decision }} </tr> </table>',
    '<tr> Application type: {{ application_type }} </tr>',
    '<tr> Application status: {{ status }} </tr>',
    '<tr> Ward: {{ ward_name }} </tr>',
    '<tr> Conservation area: {{ district }} </tr>',
    '<tr> <th> Appeal start date: </th> {{ appeal_date }} </tr>',
    '<tr> <th> Appeal decision: </th> {{ appeal_result }} </tr> <tr> <th> Appeal decision date: </th> {{ appeal_decision_date }} </tr>',
    
    ]

    def get_id_period (self, date): 

        fields = self.query_fields
        from_iso_dt, to_iso_dt = util.inc_dt(date.strftime(util.ISO8601_DATE), util.ISO8601_DATE, self.PERIOD_TYPE)
        from_dt = util.get_dt(from_iso_dt, util.ISO8601_DATE)
        to_dt = util.get_dt(to_iso_dt, util.ISO8601_DATE)

        fields [self.date_field] = to_dt.strftime(self.request_date_format)

        final_result = []
        
        response = util.open_url(self.br, self.search_url, fields, 'POST')
        if response:
            html = response.read()
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
        else:
            return [], None, None

        return final_result, from_dt, to_dt # note weekly result might some times be legitimately empty
        
    def get_detail_from_uid (self, uid):
        url = self.applic_url + '&id=' + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    scraper = KensingtonScraper()
    scraper.run()

    #scraper.DEBUG = True
    # misc tests
    #print scraper.get_detail_from_uid ('CA/12/00942')
    #print scraper.get_detail_from_uid ('LB/11/00590')
    #result = scraper.get_id_period(util.get_dt('01/03/2011'))
    #print result
    #print scraper.gather_ids('2010-02-01')
    #print scraper.gather_ids(None, None)
    #scraper.gather_current_ids()
