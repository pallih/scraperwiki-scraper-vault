# this is a scraper of East Sussex planning applications for use by Openly Local

# currently designed to work backwards collecting applications from the current date to 1/1/2000

# note dates are stored in text ISO8601 format

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

class EastSussexScraper(base.DateScraper):

    MAX_ID_BATCH = 300 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 250 # max application details to scrape in one go
    BATCH_DAYS = 60 # batch size for each scrape (number of days to gather)

    date_from_field = { 'day': 'ctl00$content$fromDay', 'month': 'ctl00$content$fromMonth', 'year': 'ctl00$content$fromYear', }
    date_to_field = { 'day': 'ctl00$content$toDay', 'month': 'ctl00$content$toMonth', 'year': 'ctl00$content$toYear', }
    search_form = '1'
    form_fields = { 'ctl00$content$search': 'byDate', }
    submit_control = None
    link_next = 'Next >'
    request_date_format = '%-d/%-m/%Y'
    search_url = 'http://www.eastsussex.gov.uk/environment/planning/applications/register/Search.aspx'
    applic_url = 'http://www.eastsussex.gov.uk/environment/planning/applications/register/Detail.aspx?typ=dmw_planning'
    scrape_ids = """
    <section>
        {* <dl class="itemDetail"> 
            <dt> Reference: </dt> <dd > 
            <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </dd> 
            <dt> Date: </dt> <dd> {{ [records].date_received }} </dd>
          </dl>
        *}
    </section>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <article> {{ block|html }} </article>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <span id="ctl00_content_lblRefNo"> {{ reference }} </span>
    <span id="ctl00_content_lblAddress"> {{ address }} </span>
    <span id="ctl00_content_lblProposal"> {{ description }} </span>
    <span id="ctl00_content_lblRecievedDate"> {{ date_validated }} </span>
    """ # note spelling mistake and that the 'recieved' date is actually the date_validated (after date received)
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<h2 id="ctl00_content_typeTitle"> {{ application_type }} </h2>',
    '<span id="ctl00_content_lblParish"> {{ parish }} </span>',
    '<span id="ctl00_content_lblDistrict"> {{ district }} </span>',
    '<span id="ctl00_content_lblElectoralDivision"> {{ ward_name }} </span>',
    '<span id="ctl00_content_lblConsultationStart"> {{ consultation_start_date }} </span>', 
    '<span id="ctl00_content_lblConsultationEnd"> {{ consultation_end_date }} </span>',
    '<span id="ctl00_content_lblApplicant"> {{ applicant_name }} </span>',
    '<span id="ctl00_content_lblAgent"> {{ agent_name }} </span>',
    '<span id="ctl00_content_lblStatus"> {{ status }} </span>',
    '<span id="ctl00_content_lblContactOfficer"> {{ case_officer }} </span>',
    '<span id="ctl00_content_lblDecisionDate"> {{ decision_date }} </span>',
    '<span id="ctl00_content_lblDecision"> {{ decision }} </span>',
    '<a id="ctl00_content_hlComment" href="{{ comment_url|abs }}"> </a>',
    ]

    def get_id_batch (self, date_from, date_to):

        response = util.open_url(self.br, self.search_url)

        fields = self.form_fields

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
        response = util.submit_form(self.br, self.submit_control)

        final_result = []
        while response:
            html = response.read()
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            try:
                response = util.process_link(self.br, self.link_next)
            except:
                response = None
        return final_result

    def get_detail_from_uid (self, uid):
        url = self.applic_url + '&appno=' + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    scraper = EastSussexScraper()
    scraper.run()

    # misc tests
    ##scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('LW/684/CM')
    #print scraper.get_id_batch(util.get_dt('31/01/2011'), util.get_dt('08/02/2011'))
    #print scraper.gather_ids('2012-02-01')
    #print scraper.gather_ids('2011-02-01', '2012-01-18')
    #print scraper.gather_ids('2012-06-06')

# this is a scraper of East Sussex planning applications for use by Openly Local

# currently designed to work backwards collecting applications from the current date to 1/1/2000

# note dates are stored in text ISO8601 format

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

class EastSussexScraper(base.DateScraper):

    MAX_ID_BATCH = 300 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 250 # max application details to scrape in one go
    BATCH_DAYS = 60 # batch size for each scrape (number of days to gather)

    date_from_field = { 'day': 'ctl00$content$fromDay', 'month': 'ctl00$content$fromMonth', 'year': 'ctl00$content$fromYear', }
    date_to_field = { 'day': 'ctl00$content$toDay', 'month': 'ctl00$content$toMonth', 'year': 'ctl00$content$toYear', }
    search_form = '1'
    form_fields = { 'ctl00$content$search': 'byDate', }
    submit_control = None
    link_next = 'Next >'
    request_date_format = '%-d/%-m/%Y'
    search_url = 'http://www.eastsussex.gov.uk/environment/planning/applications/register/Search.aspx'
    applic_url = 'http://www.eastsussex.gov.uk/environment/planning/applications/register/Detail.aspx?typ=dmw_planning'
    scrape_ids = """
    <section>
        {* <dl class="itemDetail"> 
            <dt> Reference: </dt> <dd > 
            <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </dd> 
            <dt> Date: </dt> <dd> {{ [records].date_received }} </dd>
          </dl>
        *}
    </section>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <article> {{ block|html }} </article>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <span id="ctl00_content_lblRefNo"> {{ reference }} </span>
    <span id="ctl00_content_lblAddress"> {{ address }} </span>
    <span id="ctl00_content_lblProposal"> {{ description }} </span>
    <span id="ctl00_content_lblRecievedDate"> {{ date_validated }} </span>
    """ # note spelling mistake and that the 'recieved' date is actually the date_validated (after date received)
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<h2 id="ctl00_content_typeTitle"> {{ application_type }} </h2>',
    '<span id="ctl00_content_lblParish"> {{ parish }} </span>',
    '<span id="ctl00_content_lblDistrict"> {{ district }} </span>',
    '<span id="ctl00_content_lblElectoralDivision"> {{ ward_name }} </span>',
    '<span id="ctl00_content_lblConsultationStart"> {{ consultation_start_date }} </span>', 
    '<span id="ctl00_content_lblConsultationEnd"> {{ consultation_end_date }} </span>',
    '<span id="ctl00_content_lblApplicant"> {{ applicant_name }} </span>',
    '<span id="ctl00_content_lblAgent"> {{ agent_name }} </span>',
    '<span id="ctl00_content_lblStatus"> {{ status }} </span>',
    '<span id="ctl00_content_lblContactOfficer"> {{ case_officer }} </span>',
    '<span id="ctl00_content_lblDecisionDate"> {{ decision_date }} </span>',
    '<span id="ctl00_content_lblDecision"> {{ decision }} </span>',
    '<a id="ctl00_content_hlComment" href="{{ comment_url|abs }}"> </a>',
    ]

    def get_id_batch (self, date_from, date_to):

        response = util.open_url(self.br, self.search_url)

        fields = self.form_fields

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
        response = util.submit_form(self.br, self.submit_control)

        final_result = []
        while response:
            html = response.read()
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            try:
                response = util.process_link(self.br, self.link_next)
            except:
                response = None
        return final_result

    def get_detail_from_uid (self, uid):
        url = self.applic_url + '&appno=' + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    scraper = EastSussexScraper()
    scraper.run()

    # misc tests
    ##scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('LW/684/CM')
    #print scraper.get_id_batch(util.get_dt('31/01/2011'), util.get_dt('08/02/2011'))
    #print scraper.gather_ids('2012-02-01')
    #print scraper.gather_ids('2011-02-01', '2012-01-18')
    #print scraper.gather_ids('2012-06-06')

