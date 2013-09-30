# this is a scraper of Isle of Man planning applications

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import urllib
import copy

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

class IsleOfManScraper(base.PeriodScraper):

    MAX_ID_BATCH = 200 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 150 # max application details to scrape in one go
    PERIOD_TYPE = 'Friday'
    MIN_DAYS = 28 # min number of days to get when gathering current ids

    search_form = '0'
    date_field = 'PressListDate'
    query_fields =  { 'Question': '2', 'search': 'Search' }
    ref_field = 'ctl00$mainContent$appnum'
    request_date_format = '%Y-%m-%dT00:00:00.000'
    detail_submit = 'ctl00$mainContent$butAppnum'
    search_url = 'https://www.gov.im/planningapplication/services/planning/search.iom'
    applic_url = 'https://www.gov.im/planningapplication/services/planning/planningapplicationdetails.iom?ApplicationReferenceNumber='
    scrape_next_link = '<div class="pagesearchbuttons"> | <a href="{{ next_link }}"> Next </a> </div>'
    junk_regex = re.compile(r'&#xD;|&#xA;') 
    scrape_ids = """
    <table class="results"> <tr />
    {* <tr>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td> </tr>
    <tr /> *}
    </table>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div class="subsection"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <h2> Planning Application: {{ reference }} </h2>
    <th> Address </th> <td> {{ address }} </td>
    <th> Proposal </th> <td> {{ description }} </td>
    <th> Application Date </th> <td> {{ date_received }} </td>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<th> Parish </th> <td> {{ parish }} </td>',
    '<th> Status </th> <td> {{ status }} </td>',
    '<th> Date the decision was issued </th> <td> {{ decision_issued_date }} </td>',
    '<th> Status of the appeal </th> <td> {{ appeal_status }} </td>',
    '<th> Date an appeal was lodged </th> <td> {{ appeal_date }} </td>',
    '<th> Date the appeal was determined </th> <td> {{ appeal_decision_date }} </td>',
    ]

    def get_id_period (self, date):

        from_iso_dt, to_iso_dt = util.inc_dt(date.strftime(util.ISO8601_DATE), util.ISO8601_DATE, self.PERIOD_TYPE)
        from_dt = util.get_dt(from_iso_dt, util.ISO8601_DATE)
        to_dt = util.get_dt(to_iso_dt, util.ISO8601_DATE)

        do_dt = util.get_dt(to_iso_dt, util.ISO8601_DATE) # the date being tested - can change

        final_result = []
        for i in range(5): # note works backwards through all 5 possible week days as some lists are not published exactly on a Friday
    
            fields = self.query_fields
            fields[self.date_field] = do_dt.strftime(self.request_date_format)
            if self.DEBUG: print fields
            response = util.open_url(self.br, self.search_url, fields)
    
            while response:
                html = response.read()
                url = response.geturl()
                if self.DEBUG: print html
                result = scrapemark.scrape(self.scrape_ids, html, url)
                if result and result.get('records'):
                    self.clean_ids(result['records'])
                    final_result.extend(result['records'])
                else:
                    break
                try:
                    new_html = self.junk_regex.sub('', html) # remove internal junk characters
                    result = scrapemark.scrape(self.scrape_next_link, new_html, url)
                    next_link = util.no_space(result['next_link'])
                    response = self.br.open(next_link)
                except:
                    break

            do_dt = do_dt - timedelta(days=1)

        #if not final_result:
        #    return [], None, None 
        #else:
        return final_result, from_dt, to_dt # note weekly result can be legitimately empty
        
    def get_detail_from_uid (self, uid):
        url = self.applic_url + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    scraper = IsleOfManScraper()
    scraper.run()

    #scraper.DEBUG = True
    # misc tests
    #print scraper.get_detail_from_uid ('11/00581/B')
    #result, dt1, dt2 = scraper.get_id_period(util.get_dt('30/08/2011'))
    #print len(result), result, dt1, dt2
    
# this is a scraper of Isle of Man planning applications

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import urllib
import copy

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

class IsleOfManScraper(base.PeriodScraper):

    MAX_ID_BATCH = 200 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 150 # max application details to scrape in one go
    PERIOD_TYPE = 'Friday'
    MIN_DAYS = 28 # min number of days to get when gathering current ids

    search_form = '0'
    date_field = 'PressListDate'
    query_fields =  { 'Question': '2', 'search': 'Search' }
    ref_field = 'ctl00$mainContent$appnum'
    request_date_format = '%Y-%m-%dT00:00:00.000'
    detail_submit = 'ctl00$mainContent$butAppnum'
    search_url = 'https://www.gov.im/planningapplication/services/planning/search.iom'
    applic_url = 'https://www.gov.im/planningapplication/services/planning/planningapplicationdetails.iom?ApplicationReferenceNumber='
    scrape_next_link = '<div class="pagesearchbuttons"> | <a href="{{ next_link }}"> Next </a> </div>'
    junk_regex = re.compile(r'&#xD;|&#xA;') 
    scrape_ids = """
    <table class="results"> <tr />
    {* <tr>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td> </tr>
    <tr /> *}
    </table>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div class="subsection"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <h2> Planning Application: {{ reference }} </h2>
    <th> Address </th> <td> {{ address }} </td>
    <th> Proposal </th> <td> {{ description }} </td>
    <th> Application Date </th> <td> {{ date_received }} </td>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<th> Parish </th> <td> {{ parish }} </td>',
    '<th> Status </th> <td> {{ status }} </td>',
    '<th> Date the decision was issued </th> <td> {{ decision_issued_date }} </td>',
    '<th> Status of the appeal </th> <td> {{ appeal_status }} </td>',
    '<th> Date an appeal was lodged </th> <td> {{ appeal_date }} </td>',
    '<th> Date the appeal was determined </th> <td> {{ appeal_decision_date }} </td>',
    ]

    def get_id_period (self, date):

        from_iso_dt, to_iso_dt = util.inc_dt(date.strftime(util.ISO8601_DATE), util.ISO8601_DATE, self.PERIOD_TYPE)
        from_dt = util.get_dt(from_iso_dt, util.ISO8601_DATE)
        to_dt = util.get_dt(to_iso_dt, util.ISO8601_DATE)

        do_dt = util.get_dt(to_iso_dt, util.ISO8601_DATE) # the date being tested - can change

        final_result = []
        for i in range(5): # note works backwards through all 5 possible week days as some lists are not published exactly on a Friday
    
            fields = self.query_fields
            fields[self.date_field] = do_dt.strftime(self.request_date_format)
            if self.DEBUG: print fields
            response = util.open_url(self.br, self.search_url, fields)
    
            while response:
                html = response.read()
                url = response.geturl()
                if self.DEBUG: print html
                result = scrapemark.scrape(self.scrape_ids, html, url)
                if result and result.get('records'):
                    self.clean_ids(result['records'])
                    final_result.extend(result['records'])
                else:
                    break
                try:
                    new_html = self.junk_regex.sub('', html) # remove internal junk characters
                    result = scrapemark.scrape(self.scrape_next_link, new_html, url)
                    next_link = util.no_space(result['next_link'])
                    response = self.br.open(next_link)
                except:
                    break

            do_dt = do_dt - timedelta(days=1)

        #if not final_result:
        #    return [], None, None 
        #else:
        return final_result, from_dt, to_dt # note weekly result can be legitimately empty
        
    def get_detail_from_uid (self, uid):
        url = self.applic_url + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    scraper = IsleOfManScraper()
    scraper.run()

    #scraper.DEBUG = True
    # misc tests
    #print scraper.get_detail_from_uid ('11/00581/B')
    #result, dt1, dt2 = scraper.get_id_period(util.get_dt('30/08/2011'))
    #print len(result), result, dt1, dt2
    
