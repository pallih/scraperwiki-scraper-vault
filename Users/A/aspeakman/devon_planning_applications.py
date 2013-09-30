# this is a scraper of Devon planning applications for use by Openly Local

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

class DevonScraper(base.DateScraper):

    MAX_ID_BATCH = 150 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 100 # max application details to scrape in one go
    BATCH_DAYS = 28 # batch size for each scrape - number of days to gather to produce at least one result each time
    MIN_DAYS = 28 # min number of days to get when gathering current ids

    search_url = 'http://www.devon.gov.uk/index/environmentplanning/planning-system/planningapplications-all/planning_applications.htm'
    date_from_field = 'reg_date_start'
    date_to_field = 'reg_date_end'
    ref_field = 'reference'
    request_date_format = '%d/%m/%y'
    search_form = '2'
    # badly formatted optgroup in select statement
    html_subs = {
    r'<select name="district_ward".*?</select>': r'' }
    scrape_ids = """
    <div id="ful_head">
    {* <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    *} </div>
    """
    scrape_data_block = """
    <table class="datatable"> {{ block|html }} </table>
    """
    scrape_min_data = """
    <a name="{{ reference }}"> Application Reference </a>
    <tr> <th> Location </th> <td> {{ address }} </td> </tr>
    <tr> <th> Proposal </th> <td> {{ description }} </td> </tr>
    <tr> <th> Date Received </th> <td> {{ date_received }} </td> </tr>
    <tr> <th> Date Validated </th> <td> {{ date_validated }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr> <th> Status </th> <td> {{ status }}</td> </tr>',
    '<tr> <th> Division </th> <td> {{ ward_name }} </td> </tr>',
    '<tr> <th> District </th> <td> {{ district }} </td> </tr>',
    '<tr> <th> Applicant </th> <td> {{ applicant_name }} </td> </tr>',
    '<tr> <th> Agent </th> <td> {{ agent_name }} </td> </tr>',
    '<tr> <th> Case Officer </th> <td> {{ case_officer }} </td> </tr>',
    '<tr> <th> Target Date For Decision </th> <td> {{ target_decision_date }} </td> </tr>',
    """<tr> <th> Committee Date </th> <td> {{ meeting_date }} </td> </tr>
    <tr> <th> Decision </th> <td> {{ decision }} </td> </tr>""",
    '<tr> <th> Decision Level </th> <td> {{ decided_by }} </td> </tr>',
    '<tr> <th> Decision Date </th> <td> {{ decision_date }} </td> </tr>',
    '<tr> <th> Start of Consultation Period </th> <td> {{ consultation_start_date }} </td> </tr>',
    '<tr> <th> End of Consultation Period </th> <td> {{ consultation_end_date }} </td> </tr>',
    '<a> Application Reference </a> <a href="{{ comment_url|abs }}" />'
    ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)

        #response = self.br.response()  # this is a copy of the current browser response
        html = response.get_data()
        for k, v in self.html_subs.items(): # adjust bad html
            html = re.sub(k, v, html, 0, re.U|re.S|re.I) # unicode|dot matches new line|ignore case
        if self.DEBUG: print "dbg: html post sub:", html
        response.set_data(html)
        self.br.set_response(response)

        fields = {}
        fields [self.date_from_field] = date_from.strftime(self.request_date_format)
        fields [self.date_to_field] = date_to.strftime(self.request_date_format)
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
        
        response = self.br.open(self.search_url)

        #response = self.br.response()  # this is a copy of the current browser response
        html = response.get_data()
        for k, v in self.html_subs.items(): # adjust bad html
            html = re.sub(k, v, html, 0, re.U|re.S|re.I) # unicode|dot matches new line|ignore case
        if self.DEBUG: print "dbg: html post sub:", html
        response.set_data(html)
        self.br.set_response(response)
        
        fields = { self.ref_field: uid }
        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br)

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

    scraper = DevonScraper()
    scraper.run()

    # misc test calls
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('DCC/3291/2011') # Devon OK
    #result = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('18/10/2011'))
    #print len(result), result

    

# this is a scraper of Devon planning applications for use by Openly Local

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

class DevonScraper(base.DateScraper):

    MAX_ID_BATCH = 150 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 100 # max application details to scrape in one go
    BATCH_DAYS = 28 # batch size for each scrape - number of days to gather to produce at least one result each time
    MIN_DAYS = 28 # min number of days to get when gathering current ids

    search_url = 'http://www.devon.gov.uk/index/environmentplanning/planning-system/planningapplications-all/planning_applications.htm'
    date_from_field = 'reg_date_start'
    date_to_field = 'reg_date_end'
    ref_field = 'reference'
    request_date_format = '%d/%m/%y'
    search_form = '2'
    # badly formatted optgroup in select statement
    html_subs = {
    r'<select name="district_ward".*?</select>': r'' }
    scrape_ids = """
    <div id="ful_head">
    {* <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    *} </div>
    """
    scrape_data_block = """
    <table class="datatable"> {{ block|html }} </table>
    """
    scrape_min_data = """
    <a name="{{ reference }}"> Application Reference </a>
    <tr> <th> Location </th> <td> {{ address }} </td> </tr>
    <tr> <th> Proposal </th> <td> {{ description }} </td> </tr>
    <tr> <th> Date Received </th> <td> {{ date_received }} </td> </tr>
    <tr> <th> Date Validated </th> <td> {{ date_validated }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr> <th> Status </th> <td> {{ status }}</td> </tr>',
    '<tr> <th> Division </th> <td> {{ ward_name }} </td> </tr>',
    '<tr> <th> District </th> <td> {{ district }} </td> </tr>',
    '<tr> <th> Applicant </th> <td> {{ applicant_name }} </td> </tr>',
    '<tr> <th> Agent </th> <td> {{ agent_name }} </td> </tr>',
    '<tr> <th> Case Officer </th> <td> {{ case_officer }} </td> </tr>',
    '<tr> <th> Target Date For Decision </th> <td> {{ target_decision_date }} </td> </tr>',
    """<tr> <th> Committee Date </th> <td> {{ meeting_date }} </td> </tr>
    <tr> <th> Decision </th> <td> {{ decision }} </td> </tr>""",
    '<tr> <th> Decision Level </th> <td> {{ decided_by }} </td> </tr>',
    '<tr> <th> Decision Date </th> <td> {{ decision_date }} </td> </tr>',
    '<tr> <th> Start of Consultation Period </th> <td> {{ consultation_start_date }} </td> </tr>',
    '<tr> <th> End of Consultation Period </th> <td> {{ consultation_end_date }} </td> </tr>',
    '<a> Application Reference </a> <a href="{{ comment_url|abs }}" />'
    ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)

        #response = self.br.response()  # this is a copy of the current browser response
        html = response.get_data()
        for k, v in self.html_subs.items(): # adjust bad html
            html = re.sub(k, v, html, 0, re.U|re.S|re.I) # unicode|dot matches new line|ignore case
        if self.DEBUG: print "dbg: html post sub:", html
        response.set_data(html)
        self.br.set_response(response)

        fields = {}
        fields [self.date_from_field] = date_from.strftime(self.request_date_format)
        fields [self.date_to_field] = date_to.strftime(self.request_date_format)
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
        
        response = self.br.open(self.search_url)

        #response = self.br.response()  # this is a copy of the current browser response
        html = response.get_data()
        for k, v in self.html_subs.items(): # adjust bad html
            html = re.sub(k, v, html, 0, re.U|re.S|re.I) # unicode|dot matches new line|ignore case
        if self.DEBUG: print "dbg: html post sub:", html
        response.set_data(html)
        self.br.set_response(response)
        
        fields = { self.ref_field: uid }
        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br)

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

    scraper = DevonScraper()
    scraper.run()

    # misc test calls
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('DCC/3291/2011') # Devon OK
    #result = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('18/10/2011'))
    #print len(result), result

    

