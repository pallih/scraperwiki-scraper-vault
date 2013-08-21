# this is a scraper of Ashfield planning applications for use by Openly Local

# dates query is VERY slow or produces 500 error or just hangs - so fall back to using a list scraper

# works from the sequence of application numbers (in V/YYYY/NNNN format)

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

#class AshfieldScraper(base.DateScraper):
class AshfieldScraper(base.ListScraper):

    START_SEQUENCE = 20000000 # gathering back to this record number (in YYYYNNNN format derived from the application number in this format = V/YYYY/NNNN)
    MAX_ID_BATCH = 200 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 150 # max application details to scrape in one go
    START_POINT = (date.today().year * 10000) + 1
    ID_ORDER = 'uid desc'
    HEADERS = {
        'Accept-Charset': 'UTF-8,*',
        'Accept': 'text/html',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
        }

    search_url = 'http://www.ashfield-dc.gov.uk/cfusion/planning/plan_arc_results2_v_date.cfm'
    applic_url = 'http://www.ashfield-dc.gov.uk/cfusion/planning/plan_history.cfm?reference='
    ref_url = 'http://www.ashfield-dc.gov.uk/cfusion/planning/plan_history_results.cfm'
    date_from_field = {
        'day': 'fromday',
        'month': 'frommonth',
        'year': 'fromyear',
        }
    date_to_field = {
        'day': 'to_day',
        'month': 'to_month',
        'year': 'to_year',
        }
    search_fields = { 'search_date': 'Search',  }
    ref_search = { 'search_ref': 'Search',  }
    ref_field = 'reference'
    request_date_format = '%d/%m/%Y'
    next_link = 'Next&nbsp;>>'
    scrape_ids = """
    <table class="planning_search">
    {* <tr> <td> <a href="{{ [records].url|abs }}">
    {{ [records].uid }} </a> </td> </tr> *}
    </table>
    """
    scrape_data_block = """
    <div id="mainBody"> {{ block|html }} </div>
    """
    scrape_min_data = """
    <span class="headerbg"> <strong> Ref No. </strong> <strong> {{ reference }} </strong> </span>
    <span class="planning_heading"> Location </span> <div> {{ address }} <br /> </div>
    <span class="planning_heading"> Proposal </span> <div> {{ description }} </div>
    <span class="planning_heading"> Application Received </span> <div> {{ date_received }} </div>
    <span class="planning_heading"> Planning Application Valid </span> <div> {{ date_validated }} </div>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<span class="planning_heading"> Applicant </span> <div> {{ applicant_name }} </div>',
    '<span class="planning_heading"> Agent </span> <div> {{ agent_name }} </div>',
    '<span class="planning_heading"> Case Officer </span> <div> {{ case_officer }} </div>',
    '<span class="planning_heading"> Council Ward </span> <div> {{ ward_name }} </div>',
    '<span class="planning_heading"> Consultation Sent </span> <div> {{ consultation_start_date }} </div>',
    '<span class="planning_heading"> Consultation End </span> <div> {{ consultation_end_date }} </div>',
    '<span class="planning_heading"> Decision Made By </span> <div> {{ decided_by }} </div>',
    '<span class="planning_heading"> Decision Likely By </span> <div> {{ target_decision_date }} </div>',
    '<span class="planning_heading"> Decision Type </span> <div> {{ decision }} </div>',
    '<span class="planning_heading"> Decision Date </span> <div> {{ decision_date }} </div>',
    '<a href="{{ comment_url|abs }}"> Add a comment on this Planning Application </a>',
    #'<a href="http://www.ashfield-dc.gov.uk/bigmole/?requesturl=/ashfield/rmx&centerx={{ easting }}&centery={{ northing }}&zoomwidth=150&searchinregion=true&theme=planning&geoset=Planning_history"> View Location in Interactive Map via MOLE </a>',
    '<span class="planning_heading"> Appeal Start Date </span> <div> {{ appeal_date }} </div>',
    """<span class="planning_heading"> Appeal Decision </span> <div> {{ appeal_result }} </div>
    <span class="planning_heading"> Appeal Decision Date </span> <div> {{ appeal_decision_date }} </div>""",
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
            rec_to = (date.today().year * 10000) + 9999 # last possible record of the current year        
        elif not rec_to:
            rec_to = rec_from + self.MIN_RECS # set target after highest current record to get any recent records
            min_rec_to = (date.today().year * 10000) + self.MIN_RECS # first possible record of the current year
            if rec_to < min_rec_to: rec_to = min_rec_to
            rec_from -= self.MIN_RECS

        if self.DEBUG: print 'Looking for records: ', rec_from, rec_to
        
        current_rec = rec_to
        top_page = None
        bot_page = None
        while current_rec >= rec_from and len(final_result) < self.MAX_ID_BATCH:
            current_page = str(current_rec)[4:8]
            if int(current_page) < 800: # only testing for max 800 applications per year (potentially there are 9999)
                current_appno = 'V/' + str(current_rec)[0:4] + '/' + current_page
                if self.DEBUG: print 'On page:', current_appno

                fields = self.ref_search
                fields[self.ref_field] = current_appno
                response = util.open_url(self.br, self.ref_url, fields)

                if response:
                    html = response.read()
                    url = response.geturl()
                    if self.DEBUG: print 'Html:', html
                    result = scrapemark.scrape(self.scrape_ids, html, url)
                    if result and result.get('records'):
                        if not top_page: top_page = current_appno
                        bot_page = current_appno
                        if self.DEBUG: print result
                        self.clean_ids(result['records'])
                        final_result.extend(result['records'])
                        if self.DEBUG: print 'Output N: ', len(final_result)
                
            current_rec -= 1
                
        if final_result:
            if self.DEBUG: print bot_page, top_page
            num_from = int(bot_page[2:6])
            num_to = int(top_page[2:6])
            num_from = (num_from * 10000) + int(bot_page[7:11])
            num_to = (num_to * 10000) + int(top_page[7:11])
        return final_result, num_from, num_to

    # NB if move_forward is true, we scrape forwards from rec_start, otherwise we scrape backwards
    def get_id_records2 (self, rec_start, move_forward):
        final_result = []
        num_from = None
        num_to = None
        bad_count = 0
        find_bad = True
        current_rec = rec_start
        first_good_rec = None
        last_good_rec = None
        while len(final_result) < self.MAX_ID_BATCH and bad_count < 20:
            current_year = str(current_rec)[0:4]
            current_page = str(current_rec)[4:8]
            current_appno = 'V/' + current_year + '/' + current_page
            if self.DEBUG: print 'Record:', current_appno
            fields = self.ref_search
            fields[self.ref_field] = current_appno
            response = util.open_url(self.br, self.ref_url, fields)
            if response:
                html = response.read()
                url = response.geturl()
                if self.DEBUG: print 'Html:', html
                result = scrapemark.scrape(self.scrape_ids, html, url)
                if result and result.get('records'):
                    if not first_good_rec: first_good_rec = current_rec
                    last_good_rec = current_rec
                    if self.DEBUG: print result
                    final_result.extend(result['records'])
                    bad_count = 0
                    find_bad = True
                elif find_bad:
                    bad_count += 1
            elif find_bad:
                bad_count += 1
            if move_forward:
                if bad_count == 10: # try the next year if moving forward and we reach 10 errors
                    current_rec = (int(current_year)+1)*10000
                else:
                    current_rec += 1
            else:
                if current_page == '0000': # if moving backward, swap to next year when reach zero
                    current_rec = ((int(current_year)-1)*10000)+800 # expecting max 800 applications per year (potentially 9999)
                    find_bad = False
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

    # for use by date scraper - not in use but would probably work if website sorts out date queries
    def get_id_batch (self, date_from, date_to):

        fields = self.search_fields
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

        response = util.open_url(self.br, self.search_url, fields)
        
        final_result = []
        while response:
            html = response.read()
            url = response.geturl()
            if self.DEBUG: print html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            try:
                response = self.br.follow_link(text=self.next_link)
            except:
                break
            
        return final_result

    def get_detail_from_uid (self, uid):
        url = self.applic_url + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    scraper = AshfieldScraper()
    scraper.run()

    # misc test calls
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('V/2011/0659')
    #result = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('19/08/2011'))
    #print len(result), result
    #result = scraper.get_id_records(20050001, 20120050)
    #result = scraper.get_id_records(20120709)
    #print result

    



