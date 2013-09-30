# this is a scraper of Hastings planning applications for use by Openly Local

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

class HastingsScraper(base.PeriodScraper):

    MAX_ID_BATCH = 200 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 150 # max application details to scrape in one go
    PERIOD_TYPE = 'Saturday'

    search_form = '1'
    date_fields = { 'day': 'ctl00$mainContent$day', 'month': 'ctl00$mainContent$mon', 'year': 'ctl00$mainContent$year', }
    query_fields =  { '__EVENTTARGET': '', '__EVENTARGUMENT': '', }
    ref_field = 'ctl00$mainContent$appnum'
    request_date_format = '%-d/%-m/%Y'
    search_submit = 'ctl00$mainContent$butAppDecDate'
    detail_submit = 'ctl00$mainContent$butAppnum'
    search_url = 'http://www.hastings.gov.uk/environment_planning/planning/view_planning_apps/'
    scrape_ids = """
    {* <div class="csstable">
    <div> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </div>
    </div> *}
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="mainContent_results"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <span> Case Number </span> <p> {{ reference }} </p>
    <span> Registration </span> <p> {{ date_validated }} </p>
    <span> Location </span> <p> {{ address }} </p>
    <span> Proposal </span> <p> {{ description }} </p>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<span> Case Officer </span> <p> {{ case_officer }} </p>',
    '<span> Status </span> <p> {{ status }} </p>',
    '<span> Ward </span> <p> {{ ward_name }} </p>',
    '<span> Application Type </span> <p> {{ application_type }} </p>',
    '<span> Applicant </span> <p> {{ applicant_name }} <br> {{ applicant_address|html }} </p>',
    '<span> Agent </span> <p> {{ agent_name }} <br> {{ agent_address|html }} </p>',
    '<span> Decision Level </span> <p> {{ decided_by }} </p>',
    '<span> Decision Level </span> <p> {{ decided_by }} </p>',
    "<span> Council's Decision </span> <p> {{ decision }} </p>",
    '<span> Decision Date </span> <p> {{ decision_date }} </p>',
    '<span> Appeal Received </span> <p> {{ appeal_date }} </p>',
    ]

    def get_id_period (self, date):

        from_iso_dt, to_iso_dt = util.inc_dt(date.strftime(util.ISO8601_DATE), util.ISO8601_DATE, self.PERIOD_TYPE)
        from_dt = util.get_dt(from_iso_dt, util.ISO8601_DATE)
        to_dt = util.get_dt(to_iso_dt, util.ISO8601_DATE)

        response = self.br.open(self.search_url)

        fields = {}
        fields.update(self.query_fields) 
        use_date = to_dt.strftime(self.request_date_format)
        date_parts = use_date.split('/')
        fields[self.date_fields['day']] = [ date_parts[0] ]
        fields[self.date_fields['month']] = [ date_parts[1] ]
        fields[self.date_fields['year']] = [ date_parts[2] ]

        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br, self.search_submit)

        final_result = []
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
        
        response = self.br.open(self.search_url)
        fields = {}
        fields.update(self.query_fields)
        fields [self.ref_field] = uid
        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br, self.detail_submit)

        try:
            html = response.read()
            if self.DEBUG: print html
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            self.clean_ids(result['records'])
            url = result['records'][0]['url']
        except:
            return None

        return self.get_detail_from_url(url)


if __name__ == 'scraper':

    scraper = HastingsScraper()
    scraper.run()

    #scraper.DEBUG = True
    # misc tests
    #print scraper.get_detail_from_uid ('HS/LB/11/00146')
    #result, dt1, dt2 = scraper.get_id_period(util.get_dt('01/03/2011'))
    #print len(result), result, dt1, dt2
    
# this is a scraper of Hastings planning applications for use by Openly Local

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

class HastingsScraper(base.PeriodScraper):

    MAX_ID_BATCH = 200 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 150 # max application details to scrape in one go
    PERIOD_TYPE = 'Saturday'

    search_form = '1'
    date_fields = { 'day': 'ctl00$mainContent$day', 'month': 'ctl00$mainContent$mon', 'year': 'ctl00$mainContent$year', }
    query_fields =  { '__EVENTTARGET': '', '__EVENTARGUMENT': '', }
    ref_field = 'ctl00$mainContent$appnum'
    request_date_format = '%-d/%-m/%Y'
    search_submit = 'ctl00$mainContent$butAppDecDate'
    detail_submit = 'ctl00$mainContent$butAppnum'
    search_url = 'http://www.hastings.gov.uk/environment_planning/planning/view_planning_apps/'
    scrape_ids = """
    {* <div class="csstable">
    <div> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </div>
    </div> *}
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="mainContent_results"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <span> Case Number </span> <p> {{ reference }} </p>
    <span> Registration </span> <p> {{ date_validated }} </p>
    <span> Location </span> <p> {{ address }} </p>
    <span> Proposal </span> <p> {{ description }} </p>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<span> Case Officer </span> <p> {{ case_officer }} </p>',
    '<span> Status </span> <p> {{ status }} </p>',
    '<span> Ward </span> <p> {{ ward_name }} </p>',
    '<span> Application Type </span> <p> {{ application_type }} </p>',
    '<span> Applicant </span> <p> {{ applicant_name }} <br> {{ applicant_address|html }} </p>',
    '<span> Agent </span> <p> {{ agent_name }} <br> {{ agent_address|html }} </p>',
    '<span> Decision Level </span> <p> {{ decided_by }} </p>',
    '<span> Decision Level </span> <p> {{ decided_by }} </p>',
    "<span> Council's Decision </span> <p> {{ decision }} </p>",
    '<span> Decision Date </span> <p> {{ decision_date }} </p>',
    '<span> Appeal Received </span> <p> {{ appeal_date }} </p>',
    ]

    def get_id_period (self, date):

        from_iso_dt, to_iso_dt = util.inc_dt(date.strftime(util.ISO8601_DATE), util.ISO8601_DATE, self.PERIOD_TYPE)
        from_dt = util.get_dt(from_iso_dt, util.ISO8601_DATE)
        to_dt = util.get_dt(to_iso_dt, util.ISO8601_DATE)

        response = self.br.open(self.search_url)

        fields = {}
        fields.update(self.query_fields) 
        use_date = to_dt.strftime(self.request_date_format)
        date_parts = use_date.split('/')
        fields[self.date_fields['day']] = [ date_parts[0] ]
        fields[self.date_fields['month']] = [ date_parts[1] ]
        fields[self.date_fields['year']] = [ date_parts[2] ]

        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br, self.search_submit)

        final_result = []
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
        
        response = self.br.open(self.search_url)
        fields = {}
        fields.update(self.query_fields)
        fields [self.ref_field] = uid
        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br, self.detail_submit)

        try:
            html = response.read()
            if self.DEBUG: print html
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            self.clean_ids(result['records'])
            url = result['records'][0]['url']
        except:
            return None

        return self.get_detail_from_url(url)


if __name__ == 'scraper':

    scraper = HastingsScraper()
    scraper.run()

    #scraper.DEBUG = True
    # misc tests
    #print scraper.get_detail_from_uid ('HS/LB/11/00146')
    #result, dt1, dt2 = scraper.get_id_period(util.get_dt('01/03/2011'))
    #print len(result), result, dt1, dt2
    
