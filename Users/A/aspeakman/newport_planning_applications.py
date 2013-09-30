# this is a scraper of Newport planning applications for use by Openly Local

# works from the sequence of application numbers (in YY/NNNN format)

# there is a date query page (see http://www.newport.gov.uk/fastWeb/search.asp) which sort of works using the Fastweb scraper
# however we are not using it because paging of results does not seem to work and the date format is unclear (sometimes month first, sometimes day first)

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import urllib
import sys

base = scraperwiki.utils.swimport("openlylocal_base_scraper")
scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")

class NewportScraper(base.ListScraper):

    START_SEQUENCE = 20000000 # gathering back to this record number (in YYYYNNNN format derived from the application number in this format = YY/NNNN)
    MAX_ID_BATCH = 250 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go
    #ID_ORDER = 'uid desc'
    ID_ORDER = "CASE uid WHEN substr(uid, 1, 2) < '50' THEN '20' || uid ELSE '19' || uid END desc"

    applic_url = 'http://www.newport.gov.uk/fastWeb/detail.asp?AltRef='
    scrape_ids = """
    <body> <h1 /> <table>
    {* <tr>
    <th> Application Number </th> <td> {{ [records].uid }} </td> </tr> *}
    </table> </body>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = "<body> <h1 /> {{ block|html }} </body>"
    # the minimum acceptable valid dataset on the details page
    scrape_min_data = """
    <tr> <th> Application Number </th> <td> {{ reference }} </td> </tr>
    <tr> <th> Site Address </th> <td> {{ address }} </td> </tr>
    <tr> <th> Description </th> <td> {{ description }} </td> </tr>
    """
    # other optional parameters that can appear on the details page
    scrape_optional_data = [
    "<tr> <th> Date Received </th> <td> {{ date_received }} </td> </tr>",
    "<tr> <th> Date Valid </th> <td> {{ date_validated }} </td> </tr>",
    "<tr> <th> Application Status </th> <td> {{ status }} </td> </tr>",
    "<tr> <th> Case Officer </th> <td> {{ case_officer }} </td> </tr>",
    "<tr> <th> Decision Level/Committee </th> <td> {{ decided_by }} </td> </tr>",
    "<tr> <th> Decision Level </th> <td> {{ decided_by }} </td> </tr>",
    "<tr> <th> Application Status </th> <td> {{ status }} </td> </tr>",
    "<tr> <th> Applicant Name </th> <td> {{ applicant_name }} <br> {{ applicant_address }} </td> </tr>",
    "<tr> <th> Agent Name </th> <td> {{ agent_name }}  <br> {{ agent_address }} </td> </tr>",
    "<tr> <th> Decision Type </th> <td> {{ decision }} </td> </tr>",
    "<tr> <th> Date Valid </th> </tr> <tr> <th> Decision </th> <td> {{ decision }} </td> </tr> <tr> <th> Decision Date </th> </tr>",
    "<tr> <th> Decision </th> <td> {{ decision }} </td> </tr> <tr> <th> Decision Status </th> <td> {{ status }} </tr>",
    "<tr> <th> Decision Date </th> <td> {{ decision_date }} </td> </tr>",
    "<tr> <th> Sent Date </th> <td> {{ decision_issued_date }} </td> </tr>",
    "<tr> <th> Target Date For Decision </th> <td> {{ target_decision_date }} </td> </tr>",
    "<tr> <th> Target Date of Application </th> <td> {{ target_decision_date }} </td> </tr>",
    "<tr> <th> Agent Phone </th> <td> {{ agent_tel }} </td> </tr>",
    "<tr> <th> Ward </th> <td> {{ ward_name }} </td> </tr>",
    "<tr> <th> Parish </th> <td> {{ parish }} </td> </tr>",
    "<tr> <th> Advert Date </th> <td> {{ last_advertised_date }} </td> </tr>",
    "<tr> <th> Appeal </th> <td> {{ appeal_result }} </td> </tr>",
    #"<tr> <th> Constraints </th> <td> {{ constraints|html }} </td> </tr>",
    #"<tr> <th> Recommendation Date </th> <td> {{ target_decision_date }} </td> </tr>",
    "<tr> <th> Area Team </th> <td> {{ district }} </td> </tr>",
    "<tr> <th> Consultation Period Begins </th> <td> {{ consultation_start_date }} </td> </tr>",
    "<tr> <th> Consultation Period Ends </th> <td> {{ consultation_end_date }} </td> </tr>",
    "<tr> <th> Consultation/Reconsultation End Date </th> <td> {{ consultation_end_date }} </td> </tr>",
    "<tr> <th> Committee Date </th> <td> {{ meeting_date }} </td> </tr>",
    '<a href="{{ comment_url|abs }}"> Comment </a>',
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
            if int(current_page) < 1500: # only testing for max 1500 applications per year (potentially there are 9999)
                current_appno = str(current_rec)[2:4] + '/' + current_page
                if self.DEBUG: print 'On page:', current_appno

                url = self.applic_url + urllib.quote_plus(current_appno)
                try:
                    response = self.br.open(url)
                except:
                    response = None
                
                if response:
                    html = response.read()
                    url = response.geturl()
                    if self.DEBUG: print 'Html:', html
                    result = scrapemark.scrape(self.scrape_ids, html, url)
                    if result and result.get('records'):
                        if not top_page: top_page = current_appno
                        bot_page = current_appno
                        if self.DEBUG: print result
                        for rec in result['records']:
                            rec['url'] = self.applic_url + urllib.quote_plus(rec['uid'])
                        self.clean_ids(result['records'])
                        final_result.extend(result['records'])
                        if self.DEBUG: print 'Output N: ', len(final_result)
            current_rec -= 1
                
        if final_result:
            if self.DEBUG: print bot_page, top_page
            num_from = int(bot_page[0:2]) + 1900
            if num_from <= 1930: num_from += 100
            num_to = int(top_page[0:2]) + 1900
            if num_to <= 1930: num_to += 100
            num_from = (num_from * 10000) + int(bot_page[3:7])
            num_to = (num_to * 10000) + int(top_page[3:7])
        return final_result, num_from, num_to

    def get_detail_from_uid (self, uid):
        url = self.applic_url + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)
                        
if __name__ == 'scraper':

    #scraperwiki.sqlite.attach('fastweb_system_planning_applications', 'fastweb')
    #scraperwiki.sqlite.execute("create table swdata as select * from fastweb.Newport")
    #scraperwiki.sqlite.commit()
    #sys.exit()

    #scraper = NewportScraper()
    #scraper.run()

    #scraper.DEBUG = True
    # misc tests
    #print scraper.get_detail_from_uid ('12/1187')
    #result = scraper.get_id_records(20050000, 20120010)
    #result = scraper.get_id_records(20120709)
    #print result
    #print scraper.gather_ids(None, None)
    #scraper.gather_current_ids()

    #util.rename_column('swdata', 'ward', 'ward_name')
    #scraperwiki.sqlite.save_var('latest', 20120800)

# this is a scraper of Newport planning applications for use by Openly Local

# works from the sequence of application numbers (in YY/NNNN format)

# there is a date query page (see http://www.newport.gov.uk/fastWeb/search.asp) which sort of works using the Fastweb scraper
# however we are not using it because paging of results does not seem to work and the date format is unclear (sometimes month first, sometimes day first)

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import urllib
import sys

base = scraperwiki.utils.swimport("openlylocal_base_scraper")
scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")

class NewportScraper(base.ListScraper):

    START_SEQUENCE = 20000000 # gathering back to this record number (in YYYYNNNN format derived from the application number in this format = YY/NNNN)
    MAX_ID_BATCH = 250 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go
    #ID_ORDER = 'uid desc'
    ID_ORDER = "CASE uid WHEN substr(uid, 1, 2) < '50' THEN '20' || uid ELSE '19' || uid END desc"

    applic_url = 'http://www.newport.gov.uk/fastWeb/detail.asp?AltRef='
    scrape_ids = """
    <body> <h1 /> <table>
    {* <tr>
    <th> Application Number </th> <td> {{ [records].uid }} </td> </tr> *}
    </table> </body>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = "<body> <h1 /> {{ block|html }} </body>"
    # the minimum acceptable valid dataset on the details page
    scrape_min_data = """
    <tr> <th> Application Number </th> <td> {{ reference }} </td> </tr>
    <tr> <th> Site Address </th> <td> {{ address }} </td> </tr>
    <tr> <th> Description </th> <td> {{ description }} </td> </tr>
    """
    # other optional parameters that can appear on the details page
    scrape_optional_data = [
    "<tr> <th> Date Received </th> <td> {{ date_received }} </td> </tr>",
    "<tr> <th> Date Valid </th> <td> {{ date_validated }} </td> </tr>",
    "<tr> <th> Application Status </th> <td> {{ status }} </td> </tr>",
    "<tr> <th> Case Officer </th> <td> {{ case_officer }} </td> </tr>",
    "<tr> <th> Decision Level/Committee </th> <td> {{ decided_by }} </td> </tr>",
    "<tr> <th> Decision Level </th> <td> {{ decided_by }} </td> </tr>",
    "<tr> <th> Application Status </th> <td> {{ status }} </td> </tr>",
    "<tr> <th> Applicant Name </th> <td> {{ applicant_name }} <br> {{ applicant_address }} </td> </tr>",
    "<tr> <th> Agent Name </th> <td> {{ agent_name }}  <br> {{ agent_address }} </td> </tr>",
    "<tr> <th> Decision Type </th> <td> {{ decision }} </td> </tr>",
    "<tr> <th> Date Valid </th> </tr> <tr> <th> Decision </th> <td> {{ decision }} </td> </tr> <tr> <th> Decision Date </th> </tr>",
    "<tr> <th> Decision </th> <td> {{ decision }} </td> </tr> <tr> <th> Decision Status </th> <td> {{ status }} </tr>",
    "<tr> <th> Decision Date </th> <td> {{ decision_date }} </td> </tr>",
    "<tr> <th> Sent Date </th> <td> {{ decision_issued_date }} </td> </tr>",
    "<tr> <th> Target Date For Decision </th> <td> {{ target_decision_date }} </td> </tr>",
    "<tr> <th> Target Date of Application </th> <td> {{ target_decision_date }} </td> </tr>",
    "<tr> <th> Agent Phone </th> <td> {{ agent_tel }} </td> </tr>",
    "<tr> <th> Ward </th> <td> {{ ward_name }} </td> </tr>",
    "<tr> <th> Parish </th> <td> {{ parish }} </td> </tr>",
    "<tr> <th> Advert Date </th> <td> {{ last_advertised_date }} </td> </tr>",
    "<tr> <th> Appeal </th> <td> {{ appeal_result }} </td> </tr>",
    #"<tr> <th> Constraints </th> <td> {{ constraints|html }} </td> </tr>",
    #"<tr> <th> Recommendation Date </th> <td> {{ target_decision_date }} </td> </tr>",
    "<tr> <th> Area Team </th> <td> {{ district }} </td> </tr>",
    "<tr> <th> Consultation Period Begins </th> <td> {{ consultation_start_date }} </td> </tr>",
    "<tr> <th> Consultation Period Ends </th> <td> {{ consultation_end_date }} </td> </tr>",
    "<tr> <th> Consultation/Reconsultation End Date </th> <td> {{ consultation_end_date }} </td> </tr>",
    "<tr> <th> Committee Date </th> <td> {{ meeting_date }} </td> </tr>",
    '<a href="{{ comment_url|abs }}"> Comment </a>',
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
            if int(current_page) < 1500: # only testing for max 1500 applications per year (potentially there are 9999)
                current_appno = str(current_rec)[2:4] + '/' + current_page
                if self.DEBUG: print 'On page:', current_appno

                url = self.applic_url + urllib.quote_plus(current_appno)
                try:
                    response = self.br.open(url)
                except:
                    response = None
                
                if response:
                    html = response.read()
                    url = response.geturl()
                    if self.DEBUG: print 'Html:', html
                    result = scrapemark.scrape(self.scrape_ids, html, url)
                    if result and result.get('records'):
                        if not top_page: top_page = current_appno
                        bot_page = current_appno
                        if self.DEBUG: print result
                        for rec in result['records']:
                            rec['url'] = self.applic_url + urllib.quote_plus(rec['uid'])
                        self.clean_ids(result['records'])
                        final_result.extend(result['records'])
                        if self.DEBUG: print 'Output N: ', len(final_result)
            current_rec -= 1
                
        if final_result:
            if self.DEBUG: print bot_page, top_page
            num_from = int(bot_page[0:2]) + 1900
            if num_from <= 1930: num_from += 100
            num_to = int(top_page[0:2]) + 1900
            if num_to <= 1930: num_to += 100
            num_from = (num_from * 10000) + int(bot_page[3:7])
            num_to = (num_to * 10000) + int(top_page[3:7])
        return final_result, num_from, num_to

    def get_detail_from_uid (self, uid):
        url = self.applic_url + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)
                        
if __name__ == 'scraper':

    #scraperwiki.sqlite.attach('fastweb_system_planning_applications', 'fastweb')
    #scraperwiki.sqlite.execute("create table swdata as select * from fastweb.Newport")
    #scraperwiki.sqlite.commit()
    #sys.exit()

    #scraper = NewportScraper()
    #scraper.run()

    #scraper.DEBUG = True
    # misc tests
    #print scraper.get_detail_from_uid ('12/1187')
    #result = scraper.get_id_records(20050000, 20120010)
    #result = scraper.get_id_records(20120709)
    #print result
    #print scraper.gather_ids(None, None)
    #scraper.gather_current_ids()

    #util.rename_column('swdata', 'ward', 'ward_name')
    #scraperwiki.sqlite.save_var('latest', 20120800)

