# this is a scraper of Derbyshire planning applications for use by Openly Local

# works from one short list of 70 or so current applications, most recent first

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

class DerbyshireScraper(base.ListScraper):

    START_SEQUENCE = 1 # gathering back to this record number
    MIN_RECS = 30

    search_url = 'http://www.derbyshire.gov.uk/environment/planning/planning_applications/current_applications/default.asp'
    applic_url = 'http://www.derbyshire.gov.uk/environment/planning/planning_applications/current_applications/application_details/app-details.asp'
    scrape_ids = """
    <table id="AutoNumber1"> <tr />
    {* <tr> <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    </tr> *}
    </table>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="appleft"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <h1> Planning Application - Case file for {{ reference }} </h1>
    <tr> <td> Location </td> <td> {{ address }} </td> </tr>
    <tr> <td> Development </td> <td> {{ description }} </td> </tr>
    <tr> <td> Date received </td> <td> {{ date_received }} </td> </tr>
    <tr> <td> Date valid </td> <td> {{ date_validated }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr> <td> Application Type </td> <td> {{ application_type }} </td> </tr>',
    '<tr> <td> Status </td> <td> {{ status }} </td> </tr>',
    '<tr> <td> Officer </td> <td> {{ case_officer }} </td> </tr>',

    '<tr> <td> Applicant Name </td> <td> {{ applicant_name }} </td> </tr>',
    '<tr> <td> Applicant Address </td> <td> {{ applicant_address|html }} </td> </tr>',
    '<tr> <td> Agent Name </td> <td> {{ agent_name }} </td> </tr>',
    '<tr> <td> Agent Address </td> <td> {{ agent_address|html }} </td> </tr>',
    '<tr> <td> Agent Telephone </td> <td> {{ agent_tel }} </td> </tr>',

    '<tr> <td> Public Consultation Dates </td> <td> From {{ consultation_start_date }} to {{ consultation_end_date }} </td> </tr>',
    '<tr> <td> Committee Date </td> <td> {{ meeting_date }} </td> </tr>',
    '<tr> <td> Ward </td> <td> {{ ward_name }} </td> </tr>',
    '<tr> <td> Parish </td> <td> {{ parish }} </td> </tr>',

    '<a href="{{ comment_url|abs }}"> Comment on this application </a>'
    ]

    # NB if both are None, it's the first ever scrape
    # NB if rec_to is None, rec_from is the highest existing record and it's a current scrape
    # NB also if rec_to is None, the default should be to try to get at least self.MIN_RECS records
    def get_id_records (self, rec_from, rec_to = None):
        final_result = []
        num_from = None
        num_to = None

        response = util.open_url(self.br, self.search_url)
        html = response.read()
        url = response.geturl()
        result = scrapemark.scrape(self.scrape_ids, html, url)

        if result and result.get('records'):
            self.clean_ids(result['records'])
            final_result.extend(result['records'])

        if not final_result:
            return final_result, num_from, num_to

        num_to = len(final_result)      
        if not rec_from and not rec_to:
            num_from = self.START_SEQUENCE
            num_to = len (final_result)
        elif not rec_to:
            num_from = rec_from - self.MIN_RECS
            num_to = len (final_result)
        else:    
            num_from = rec_from
            num_to = rec_to
        if num_from <= 1:
            num_from = 1
        return final_result[num_from-1:num_to], num_from, num_to

    # NB if move_forward is true, we scrape forwards from rec_start, otherwise we scrape backwards
    def get_id_records2 (self, rec_start, move_forward):
        final_result = []
        num_from = None
        num_to = None
        response = util.open_url(self.br, self.search_url)
        html = response.read()
        url = response.geturl()
        result = scrapemark.scrape(self.scrape_ids, html, url)
        if result and result.get('records'):
            self.clean_ids(result['records'])
            final_result.extend(result['records'])
        if not final_result:
            return final_result, num_from, num_to
        final_result.reverse() # most recent first
        if not rec_start:
            num_from = self.START_SEQUENCE
            num_to = len (final_result)
        elif move_forward:
            num_from = rec_start
            num_to = len (final_result)
        else:    
            num_from = self.START_SEQUENCE
            num_to = rec_start
        if num_from <= 1:
            num_from = 1
        return final_result[num_from-1:num_to], num_from, num_to

    def get_detail_from_uid (self, uid):
        url = self.applic_url + '?AppType=2&AppCode=' + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)
            
if __name__ == 'scraper':
    
    #scraperwiki.sqlite.execute("create table swdata (`url` text, `uid` text) ")
    #scraperwiki.sqlite.commit()
    #scraperwiki.sqlite.execute("drop table if exists swdata")
    #scraperwiki.sqlite.commit()

    scraper = DerbyshireScraper()
    #scraper.reset()

    #scraper.DEBUG = True
    scraper.run()
    
    # misc tests
    #print scraper.get_detail_from_uid ('CW4/1209/176')
    #result = scraper.get_id_records(20050000, 20120050)
    #result = scraper.get_id_records2(45, True)
    #print result
    
    


# this is a scraper of Derbyshire planning applications for use by Openly Local

# works from one short list of 70 or so current applications, most recent first

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

class DerbyshireScraper(base.ListScraper):

    START_SEQUENCE = 1 # gathering back to this record number
    MIN_RECS = 30

    search_url = 'http://www.derbyshire.gov.uk/environment/planning/planning_applications/current_applications/default.asp'
    applic_url = 'http://www.derbyshire.gov.uk/environment/planning/planning_applications/current_applications/application_details/app-details.asp'
    scrape_ids = """
    <table id="AutoNumber1"> <tr />
    {* <tr> <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    </tr> *}
    </table>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="appleft"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <h1> Planning Application - Case file for {{ reference }} </h1>
    <tr> <td> Location </td> <td> {{ address }} </td> </tr>
    <tr> <td> Development </td> <td> {{ description }} </td> </tr>
    <tr> <td> Date received </td> <td> {{ date_received }} </td> </tr>
    <tr> <td> Date valid </td> <td> {{ date_validated }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr> <td> Application Type </td> <td> {{ application_type }} </td> </tr>',
    '<tr> <td> Status </td> <td> {{ status }} </td> </tr>',
    '<tr> <td> Officer </td> <td> {{ case_officer }} </td> </tr>',

    '<tr> <td> Applicant Name </td> <td> {{ applicant_name }} </td> </tr>',
    '<tr> <td> Applicant Address </td> <td> {{ applicant_address|html }} </td> </tr>',
    '<tr> <td> Agent Name </td> <td> {{ agent_name }} </td> </tr>',
    '<tr> <td> Agent Address </td> <td> {{ agent_address|html }} </td> </tr>',
    '<tr> <td> Agent Telephone </td> <td> {{ agent_tel }} </td> </tr>',

    '<tr> <td> Public Consultation Dates </td> <td> From {{ consultation_start_date }} to {{ consultation_end_date }} </td> </tr>',
    '<tr> <td> Committee Date </td> <td> {{ meeting_date }} </td> </tr>',
    '<tr> <td> Ward </td> <td> {{ ward_name }} </td> </tr>',
    '<tr> <td> Parish </td> <td> {{ parish }} </td> </tr>',

    '<a href="{{ comment_url|abs }}"> Comment on this application </a>'
    ]

    # NB if both are None, it's the first ever scrape
    # NB if rec_to is None, rec_from is the highest existing record and it's a current scrape
    # NB also if rec_to is None, the default should be to try to get at least self.MIN_RECS records
    def get_id_records (self, rec_from, rec_to = None):
        final_result = []
        num_from = None
        num_to = None

        response = util.open_url(self.br, self.search_url)
        html = response.read()
        url = response.geturl()
        result = scrapemark.scrape(self.scrape_ids, html, url)

        if result and result.get('records'):
            self.clean_ids(result['records'])
            final_result.extend(result['records'])

        if not final_result:
            return final_result, num_from, num_to

        num_to = len(final_result)      
        if not rec_from and not rec_to:
            num_from = self.START_SEQUENCE
            num_to = len (final_result)
        elif not rec_to:
            num_from = rec_from - self.MIN_RECS
            num_to = len (final_result)
        else:    
            num_from = rec_from
            num_to = rec_to
        if num_from <= 1:
            num_from = 1
        return final_result[num_from-1:num_to], num_from, num_to

    # NB if move_forward is true, we scrape forwards from rec_start, otherwise we scrape backwards
    def get_id_records2 (self, rec_start, move_forward):
        final_result = []
        num_from = None
        num_to = None
        response = util.open_url(self.br, self.search_url)
        html = response.read()
        url = response.geturl()
        result = scrapemark.scrape(self.scrape_ids, html, url)
        if result and result.get('records'):
            self.clean_ids(result['records'])
            final_result.extend(result['records'])
        if not final_result:
            return final_result, num_from, num_to
        final_result.reverse() # most recent first
        if not rec_start:
            num_from = self.START_SEQUENCE
            num_to = len (final_result)
        elif move_forward:
            num_from = rec_start
            num_to = len (final_result)
        else:    
            num_from = self.START_SEQUENCE
            num_to = rec_start
        if num_from <= 1:
            num_from = 1
        return final_result[num_from-1:num_to], num_from, num_to

    def get_detail_from_uid (self, uid):
        url = self.applic_url + '?AppType=2&AppCode=' + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)
            
if __name__ == 'scraper':
    
    #scraperwiki.sqlite.execute("create table swdata (`url` text, `uid` text) ")
    #scraperwiki.sqlite.commit()
    #scraperwiki.sqlite.execute("drop table if exists swdata")
    #scraperwiki.sqlite.commit()

    scraper = DerbyshireScraper()
    #scraper.reset()

    #scraper.DEBUG = True
    scraper.run()
    
    # misc tests
    #print scraper.get_detail_from_uid ('CW4/1209/176')
    #result = scraper.get_id_records(20050000, 20120050)
    #result = scraper.get_id_records2(45, True)
    #print result
    
    


