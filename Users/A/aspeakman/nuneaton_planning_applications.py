# this is a scraper of Nuneaton and Bedworth planning applications for use by Openly Local

# currently designed to work backwards collecting applications from the current date to 1/1/2000

import scraperwiki
from datetime import timedelta 
from datetime import date
from datetime import datetime
import re
import dateutil.parser

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library") 
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

class NuneatonScraper(base.DateScraper):

    MAX_ID_BATCH = 400 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 600 # max application details to scrape in one go
    ID_ORDER = 'uid desc'

    date_from_field = { 'day': 'intFromDay', 'month': 'strFromMonth', 'year': 'intFromYear', }
    date_to_field = { 'day': 'intToDay', 'month': 'strToMonth', 'year': 'intToYear', }
    search_form = 'frmSearchByLocationDate'
    request_date_format = '%-d/%B/%Y'
    search_url = 'http://apps.nuneatonandbedworth.gov.uk/bt_nbbc_planning/bt_nbbc_planning_disp.asp'
    applic_url = 'http://apps.nuneatonandbedworth.gov.uk/BT_NBBC_Planning/BT_NBBC_Planning_application.asp'
    scrape_ids = """
    <body>
         {* <tr> <td> <a href="{{ [records].url|abs }}">
             Ref: {{ [records].uid }} - accepted
            </a> </td> </tr>
           *}
    </body> """ # note first table is paging control - but does not appear if only one page
    link_next = 'Next >'

    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <table class="nbbcTable"> {{ block|html }} </table>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <tr> Application reference: {{ reference }} </tr>
    <tr> Date accepted: {{ date_validated }} </tr>
    <tr> Location: {{ address }} </tr>
    <tr> Description: {{ description }} </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    "<tr> Application type: {{ application_type }} </tr>", # OK
    "<tr> Application status: {{ status }} </tr>", # OK
    "<tr> Date received: {{ date_received }} </tr>", # OK
    "<tr> Officer: {{ case_officer }} </tr>", # OK
    "<tr> Applicant: {{ applicant_name }} </tr>", #OK
    "<tr> Applicant's address: {{ applicant_address }} </tr>", # OK
    "<tr> Agent: {{ agent_name }} </tr>", # OK
    "<tr> Agent's address: {{ agent_address }} </tr>", # OK
    "<tr> Recommendation: {{ decision }} </tr>", # OK
    "<tr> Target decision date: {{ target_decision_date }} </tr>", # OK
    "<tr> Decided on: {{ decision_date }} </tr>", # OK
    "<tr> Decided by: {{ decided_by }} </tr>", # OK
    "<tr> Appeal made on: {{ appeal_date }} </tr>", # OK
    "<tr> Appeal result: {{ appeal_result }} </tr>", # OK
    "<tr> Appeal decided on: {{ appeal_decision_date }} </tr>", # OK
    ]

    def get_id_batch (self, date_from, date_to):
        response = self.br.open(self.search_url)
        self.br.select_form(name=self.search_form)
        date_from = date_from.strftime(self.request_date_format)
        date_parts = date_from.split('/')
        self.br[self.date_from_field['day']] = [ date_parts[0] ]
        self.br[self.date_from_field['month']] = [ date_parts[1] ]
        self.br[self.date_from_field['year']] = [ date_parts[2] ]
        date_to = date_to.strftime(self.request_date_format)
        date_parts = date_to.split('/')
        self.br[self.date_to_field['day']] = [ date_parts[0] ]
        self.br[self.date_to_field['month']] = [ date_parts[1] ]
        self.br[self.date_to_field['year']] = [ date_parts[2] ]
        response = self.br.submit()
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
                response = self.br.follow_link(text=self.link_next)
            except:
                response = None
        return final_result

    # post process a set of uid/url records: strips spaces in the uid and converts the reference to 'number_type' format
    def clean_ids (self, records):
        for record in records:
            if record.get('uid'):
                uid = record['uid'].upper()
                record['uid'] = re.sub(r'\s*(\d+)\s*\(\s*([PB]).*', r'\1_\2', record['uid'], 1, re.U)

    def get_detail_from_uid (self, uid):
        part = uid.split('_') # no need to quote the url query values, as letters/ numbers exclusively
        url = self.applic_url + '?strApplicationReference=' + part[0] + '&strRecordType=' + part[1]
        return self.get_detail_from_url(url)

if __name__ == 'scraper': 

    scraper = NuneatonScraper()
    scraper.run()
    #scraper.DEBUG = True

    # misc test calls
    #print scraper.get_detail_from_uid ('030654_P')
    #res = scraper.get_id_batch(util.get_dt('10/05/2012'), util.get_dt('25/05/2012'))
    #print res, len(res)
    #print scraper.get_id_batch(util.get_dt('23/03/2012'), util.get_dt('25/03/2012'))

    #util.list_url_prefixes(scraper.TABLE_NAME, 'url')
    #util.replace_vals(scraper.TABLE_NAME, 'url', 'http://www.nuneatonandbedworth.gov.uk/sys_upl/templates/', 'http://apps.nuneatonandbedworth.gov.uk/', 'prefix', 'yes')
    


