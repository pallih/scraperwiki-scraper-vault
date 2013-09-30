# this is a scraper of Merthyr Tydfil planning applications for use by Openly Local

# works from the sequence of application numbers (in P/YY/NNNN format) - no date or list query

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

class MerthyrTydfilScraper(base.ListScraper):

    START_SEQUENCE = 20000000 # gathering back to this record number (in YYYYNNNNN format derived from the application number in this format = P/YY/NNNN)
    MAX_ID_BATCH = 150 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 100 # max application details to scrape in one go
    ID_ORDER = 'uid desc'

    applic_url = 'http://www.merthyr.gov.uk/english/environmentandplanning/planning/pages/planningapplicationanddecisionregister.aspx?Address=&FromDate=1%2F1%2F2000&Decision='
    search_url = 'http://www.merthyr.gov.uk/english/environmentandplanning/planning/pages/planningapplicationanddecisionregister.aspx'
    search_fields = { 'FromDate': '1/1/2000', 'Address': '', 'Decision': '', }
    scrape_ids = """
    <div class="generic-list"> 
        {* <div class="row"> <div class="row"> Address : {{ [records].uid }} </div> </div> *}
    </div>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div class="generic-list"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <div class="row">
        <span class="title"> {{ address }} </span>
        <div class="row"> Address : {{ reference }} </div>
        <div class="row"> Application Date : {{ date_received }} </div>
        <div class="row"> Proposal : {{ description }} </div>
    </div>"""
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<div class="row"> <div class="row"> Decision : {{ decision }} </div> </div>',
    '<div class="row"> <div class="row"> Decision Date : {{ decision_date }} </div> </div>',
    '<div class="row"> <div class="row"> Conditions : {{ conditions }} </div> </div>',
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
            rec_from -= self.MIN_RECS

        if self.DEBUG: print 'Looking for records: ', rec_from, rec_to
        
        current_rec = rec_to
        top_page = None
        bot_page = None
        fields = self.search_fields

        while current_rec >= rec_from and len(final_result) < self.MAX_ID_BATCH:
            current_page = str(current_rec)[4:8]
            if int(current_page) < 500: # only testing for max 500 applications per year (potentially there are 9999)
                current_appno = 'P/' + str(current_rec)[2:4] + '/' + current_page
                if self.DEBUG: print 'On page:', current_appno
                fields['AppNo'] = current_appno
                response = util.open_url(self.br, self.search_url, fields, 'GET')
                if response:
                    html = response.read()
                    url = response.geturl()
                    result = scrapemark.scrape(self.scrape_ids, html, url)
                    if result and result.get('records'):
                        if not top_page: top_page = current_appno
                        bot_page = current_appno
                        if self.DEBUG: print result
                        for r in result['records']:
                            r['url'] = self.applic_url + '&AppNo=' + urllib.quote_plus(r['uid'])
                        self.clean_ids(result['records'])
                        final_result.extend(result['records'])
                        if self.DEBUG: print 'Output N: ', len(final_result)
            current_rec -= 1
                
        if final_result:
            if self.DEBUG: print bot_page, top_page
            num_from = int(bot_page[2:4]) + 1900
            if num_from <= 1930: num_from += 100
            num_to = int(top_page[2:4]) + 1900
            if num_to <= 1930: num_to += 100
            num_from = (num_from * 10000) + int(bot_page[5:9])
            num_to = (num_to * 10000) + int(top_page[5:9])
        return final_result, num_from, num_to

    def get_detail_from_uid (self, uid):
        url = self.applic_url + '&AppNo=' + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    scraper = MerthyrTydfilScraper()
    scraper.run()

    #scraper.DEBUG = True
    # misc tests
    #print scraper.get_detail_from_uid ('P/12/0110')
    #result = scraper.get_id_records(20050000, 20120050)
    #result = scraper.get_id_records(20120099)
    #print result
    #print scraper.gather_ids(None, None)
    #scraper.gather_current_ids()

    #util.rename_column('swdata', 'ward', 'ward_name')
    #scraperwiki.sqlite.save_var('latest', 20120100)
# this is a scraper of Merthyr Tydfil planning applications for use by Openly Local

# works from the sequence of application numbers (in P/YY/NNNN format) - no date or list query

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

class MerthyrTydfilScraper(base.ListScraper):

    START_SEQUENCE = 20000000 # gathering back to this record number (in YYYYNNNNN format derived from the application number in this format = P/YY/NNNN)
    MAX_ID_BATCH = 150 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 100 # max application details to scrape in one go
    ID_ORDER = 'uid desc'

    applic_url = 'http://www.merthyr.gov.uk/english/environmentandplanning/planning/pages/planningapplicationanddecisionregister.aspx?Address=&FromDate=1%2F1%2F2000&Decision='
    search_url = 'http://www.merthyr.gov.uk/english/environmentandplanning/planning/pages/planningapplicationanddecisionregister.aspx'
    search_fields = { 'FromDate': '1/1/2000', 'Address': '', 'Decision': '', }
    scrape_ids = """
    <div class="generic-list"> 
        {* <div class="row"> <div class="row"> Address : {{ [records].uid }} </div> </div> *}
    </div>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div class="generic-list"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <div class="row">
        <span class="title"> {{ address }} </span>
        <div class="row"> Address : {{ reference }} </div>
        <div class="row"> Application Date : {{ date_received }} </div>
        <div class="row"> Proposal : {{ description }} </div>
    </div>"""
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<div class="row"> <div class="row"> Decision : {{ decision }} </div> </div>',
    '<div class="row"> <div class="row"> Decision Date : {{ decision_date }} </div> </div>',
    '<div class="row"> <div class="row"> Conditions : {{ conditions }} </div> </div>',
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
            rec_from -= self.MIN_RECS

        if self.DEBUG: print 'Looking for records: ', rec_from, rec_to
        
        current_rec = rec_to
        top_page = None
        bot_page = None
        fields = self.search_fields

        while current_rec >= rec_from and len(final_result) < self.MAX_ID_BATCH:
            current_page = str(current_rec)[4:8]
            if int(current_page) < 500: # only testing for max 500 applications per year (potentially there are 9999)
                current_appno = 'P/' + str(current_rec)[2:4] + '/' + current_page
                if self.DEBUG: print 'On page:', current_appno
                fields['AppNo'] = current_appno
                response = util.open_url(self.br, self.search_url, fields, 'GET')
                if response:
                    html = response.read()
                    url = response.geturl()
                    result = scrapemark.scrape(self.scrape_ids, html, url)
                    if result and result.get('records'):
                        if not top_page: top_page = current_appno
                        bot_page = current_appno
                        if self.DEBUG: print result
                        for r in result['records']:
                            r['url'] = self.applic_url + '&AppNo=' + urllib.quote_plus(r['uid'])
                        self.clean_ids(result['records'])
                        final_result.extend(result['records'])
                        if self.DEBUG: print 'Output N: ', len(final_result)
            current_rec -= 1
                
        if final_result:
            if self.DEBUG: print bot_page, top_page
            num_from = int(bot_page[2:4]) + 1900
            if num_from <= 1930: num_from += 100
            num_to = int(top_page[2:4]) + 1900
            if num_to <= 1930: num_to += 100
            num_from = (num_from * 10000) + int(bot_page[5:9])
            num_to = (num_to * 10000) + int(top_page[5:9])
        return final_result, num_from, num_to

    def get_detail_from_uid (self, uid):
        url = self.applic_url + '&AppNo=' + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    scraper = MerthyrTydfilScraper()
    scraper.run()

    #scraper.DEBUG = True
    # misc tests
    #print scraper.get_detail_from_uid ('P/12/0110')
    #result = scraper.get_id_records(20050000, 20120050)
    #result = scraper.get_id_records(20120099)
    #print result
    #print scraper.gather_ids(None, None)
    #scraper.gather_current_ids()

    #util.rename_column('swdata', 'ward', 'ward_name')
    #scraperwiki.sqlite.save_var('latest', 20120100)
