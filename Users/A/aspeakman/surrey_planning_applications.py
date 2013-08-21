# this is a scraper of Surrey planning applications for use by Openly Local

# works from the sequence of application ids - no date or list query

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

class SurreyScraper(base.ListScraper):

    START_SEQUENCE = 1 # gathering back to this record number
    MAX_ID_BATCH = 200 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 150 # max application details to scrape in one go
    START_POINT = 1900
    #ID_ORDER = 'uid desc'
    ID_ORDER = "CASE uid WHEN substr(uid, 1, 2) < '50' THEN '20' || uid ELSE '19' || uid END desc"

    #applic_url = 'http://www1.surreycc.gov.uk/mwplan/template3.cfm'
    applic_url = 'http://www1.surreycc.gov.uk/mwplan/record.aspx'
    #search_url = 'http://www1.surreycc.gov.uk/mwplan/search.cfm'
    search_url = 'http://www1.surreycc.gov.uk/mwplan/search.aspx'
    scrape_id = """
    <div id="scc-content">
        <div class="recordDetail"> Permanent application </div> {{ uid }} <div class="recordDetail" />
    </div>
    """
    scrape_link = """
    <h5 /> <div class="recordDetail">
    <a href="{{ link|abs }}" /> </div>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="scc-content"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <div class="recordDetail"> Temporary application </div> {{ reference }} 
    <div class="recordDetail"> Permanent application </div> {{ uid }} <div class="recordDetail" />
    <div class="recordDetail"> Date received </div> {{ date_received }} 
    <div class="recordDetail"> Date valid </div> {{ date_validated }} <div class="recordDetail" />
    <div class="recordDetail"> Site location </div> {{ address }} <div class="recordDetail"> Status </div>
    <b> Description </b> <br> {{ description }} <br>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<div class="recordDetail"> Record date </div> {{ last_updated_date }} <div class="recordDetail" />',
    '<div class="recordDetail"> Application type </div>{{ application_type }} <div class="recordDetail" />',
    '<div class="recordDetail"> Applicant </div> {{ applicant_name }} <div class="recordDetail"> Site location </div>',
    '<div class="recordDetail"> Status </div> {{ status }} <div class="recordDetail" />',
    '<div class="recordDetail"> Application to be determined </div> {{ decided_by }} <br>',
    '<div class="recordDetail"> Committee date </div> {{ meeting_date }} <div class="recordDetail" />',
    '<div class="recordDetail"> Decision date </div> {{ decision_date }} <div class="recordDetail" />',
    '<div class="recordDetail"> Parish </div> {{ parish }} <div class="recordDetail" />',
    '<div class="recordDetail"> Electoral division </div> {{ ward_name }} <div class="recordDetail" />',
    '<div class="recordDetail"> Borough/district </div> {{ district }} <div class="recordDetail" />',
    '<div class="recordDetail"> Consultation Start date </div> {{ consultation_start_date }} <div class="recordDetail" />',
    '<div class="recordDetail"> Consultation Expiry date </div> {{ consultation_end_date }} <div class="recordDetail" />',
    '<a href="{{ comment_url }}"> Comment on this application online </a>'
    ]

    # NB if both are None, it's the first ever scrape
    # NB if rec_to is None, rec_from is the highest existing record and it's a current scrape
    # NB also if rec_to is None, the default should be to try to get at least self.MIN_RECS records
    def get_id_records (self, rec_from, rec_to = None):
        final_result = []
        num_from = None
        num_to = None

        if not rec_from and not rec_to:
            rec_from = self.START_SEQUENCE
            rec_to = 2200
        elif not rec_to:
            rec_to = rec_from + self.MIN_RECS # set target after highest current record to get any recent records
            rec_from -= self.MIN_RECS

        if self.DEBUG: print 'Looking for records: ', rec_from, rec_to
        
        current_rec = rec_to
        top_page = None
        bot_page = None
        fields = {}
        while current_rec >= rec_from and len(final_result) < self.MAX_ID_BATCH:
            if self.DEBUG: print 'On page:', current_rec
            fields['id'] = str(current_rec)
            response = util.open_url(self.br, self.applic_url, fields, 'GET')
            if response:
                html = response.read()
                url = response.geturl()
                if self.DEBUG: print 'Html:', html
                result = scrapemark.scrape(self.scrape_id, html, url)
                if result and result.get('uid'):
                    if not top_page: top_page = current_rec
                    bot_page = current_rec
                    result['url'] = self.applic_url + '?id=' + str(current_rec)
                    if self.DEBUG: print result
                    self.clean_ids([result])
                    final_result.extend([result])
                    if self.DEBUG: print 'Output N: ', len(final_result)
            current_rec -= 1
                
        if final_result:
            num_from = bot_page
            num_to = top_page
        return final_result, num_from, num_to

    # NB if move_forward is true, we scrape forwards from rec_start, otherwise we scrape backwards
    def get_id_records2 (self, rec_start, move_forward):
        final_result = []
        num_from = None
        num_to = None
        bad_count = 0
        current_rec = rec_start
        fields = {}
        first_good_rec = None
        last_good_rec = None
        while len(final_result) < self.MAX_ID_BATCH and bad_count < 10:
            if self.DEBUG: print 'Record:', current_rec
            fields['id'] = str(current_rec)
            response = util.open_url(self.br, self.applic_url, fields, 'GET')
            if response:
                html = response.read()
                url = response.geturl()
                if self.DEBUG: print 'Html:', html
                result = scrapemark.scrape(self.scrape_id, html, url)
                if result and result.get('uid'):
                    if not first_good_rec: first_good_rec = current_rec
                    last_good_rec = current_rec
                    result['url'] = self.applic_url + '?id=' + str(current_rec)
                    if self.DEBUG: print result
                    final_result.append(result)
                    bad_count = 0
                else:
                    bad_count += 1
            else:
                bad_count += 1
            if move_forward:
                current_rec += 1
            else:
                current_rec -= 1     
        if final_result:
            self.clean_ids(final_result)
            if move_forward:
                num_from = first_good_rec
                num_to = last_good_rec
            else:
                num_to = first_good_rec
                num_from = last_good_rec
        return final_result, num_from, num_to

    def get_detail_from_uid (self, uid):
        # search by application number
        response = util.open_url(self.br, self.search_url)
        if self.DEBUG: print response.read()

        fields = { 'ctl00$ContentPlaceHolder1$recordType': 'both', 'ctl00$ContentPlaceHolder1$txtApplicationSearch': uid  }
        util.setup_form(self.br,'aspnetForm', fields)

        response = util.submit_form(self.br)
        html = response.read()
        url = response.geturl()
        if self.DEBUG: print html

        # follow first view form if there is one
        result = scrapemark.scrape(self.scrape_link, html, url)
        if result and result.get('link'):
            if self.DEBUG: print result['link']
            return self.get_detail_from_url(result['link'])
        else:
            return None

if __name__ == 'scraper':

    scraper = SurreyScraper()
    #scraper.reset()
    scraper.run()

    #scraper.DEBUG = True
    # misc tests
    #print scraper.get_detail_from_uid ('SP12/00528')
    #result = scraper.get_id_records(1200, 1250)
    #result = scraper.get_id_records(1)
    #print result
    #print scraper.gather_ids(None, None)
    #scraper.gather_current_ids()

    #util.rename_column('swdata', 'ward', 'ward_name')
    #scraperwiki.sqlite.save_var('latest', 1750)
