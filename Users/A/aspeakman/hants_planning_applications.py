# this is a scraper of Hampshire planning applications for use by Openly Local

# works from the sequence of application ids - no date or list query

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import urllib

BASE_URL = "http://www3.hants.gov.uk/mineralsandwaste/applications-search.htm"

base = scraperwiki.utils.swimport("openlylocal_base_scraper")
scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")

class HantsScraper(base.ListScraper):

    START_SEQUENCE = 4000 # gathering back to this record number
    MAX_ID_BATCH = 200 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 150 # max application details to scrape in one go
    START_POINT = 15000
    ID_ORDER = 'url desc'

    applic_url = 'http://www3.hants.gov.uk/mineralsandwaste/application-details.htm'
    search_url = 'http://www3.hants.gov.uk/mineralsandwaste/application-search-results.htm'
    scrape_id = """
    <div id="pageinfo">
        <tr> <th> Application no </th> <td> {{ uid }} </td> </tr>
    </div>
    """
    scrape_link = """
    <div id="pageinfo"> <a href="{{ link|abs }}" /> </div>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="pageinfo"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <th> Application no </th> <td> {{ uid }} </td>
    <th> Site Reference </th> <td> {{ reference }} </td>
    <th> Location </th> <td> {{ address }} </td>
    <th> Proposal </th> <td> {{ description }} </td>
    <th> Received </th> <td> {{ date_received }} </td>
    <th> Validated </th> <td> {{ date_validated }} </td>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<th> Start of Public Consultation </th> <td> {{ consultation_start_date }} </td>',
    '<th> Decision </th> <td> {{ decision }} </td> <th> Decision date </th> <td> {{ decision_date }} </td>',
    "<th> Name </th> <td> {{ agent_name }} </td>", # nb for now ignore unicode apostrophe in agent's name
    '<th> Appeal status </th> <td> {{ appeal_status }} </td>',
    ]

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
        while len(final_result) < self.MAX_ID_BATCH and bad_count < 30:
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
        fields = { 'search': 'yes', 'appno': uid  }
        response = util.open_url(self.br, self.search_url, fields, 'GET')
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

    scraper = HantsScraper()
    #scraper.clear_all()
    scraper.run()
    
    #scraper.DEBUG = True
    #print scraper.gather_ids2(None)
    # misc tests
    #print scraper.get_detail_from_uid ('K6390/12')
    #print scraper.get_detail_from_uid ('HDC23999')
    #result = scraper.get_id_records2(1200, True)
    #result = scraper.get_id_records(1)
    #print result
    #print scraper.gather_ids(None, None)
    #scraper.gather_current_ids()


# this is a scraper of Hampshire planning applications for use by Openly Local

# works from the sequence of application ids - no date or list query

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import urllib

BASE_URL = "http://www3.hants.gov.uk/mineralsandwaste/applications-search.htm"

base = scraperwiki.utils.swimport("openlylocal_base_scraper")
scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")

class HantsScraper(base.ListScraper):

    START_SEQUENCE = 4000 # gathering back to this record number
    MAX_ID_BATCH = 200 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 150 # max application details to scrape in one go
    START_POINT = 15000
    ID_ORDER = 'url desc'

    applic_url = 'http://www3.hants.gov.uk/mineralsandwaste/application-details.htm'
    search_url = 'http://www3.hants.gov.uk/mineralsandwaste/application-search-results.htm'
    scrape_id = """
    <div id="pageinfo">
        <tr> <th> Application no </th> <td> {{ uid }} </td> </tr>
    </div>
    """
    scrape_link = """
    <div id="pageinfo"> <a href="{{ link|abs }}" /> </div>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="pageinfo"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <th> Application no </th> <td> {{ uid }} </td>
    <th> Site Reference </th> <td> {{ reference }} </td>
    <th> Location </th> <td> {{ address }} </td>
    <th> Proposal </th> <td> {{ description }} </td>
    <th> Received </th> <td> {{ date_received }} </td>
    <th> Validated </th> <td> {{ date_validated }} </td>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<th> Start of Public Consultation </th> <td> {{ consultation_start_date }} </td>',
    '<th> Decision </th> <td> {{ decision }} </td> <th> Decision date </th> <td> {{ decision_date }} </td>',
    "<th> Name </th> <td> {{ agent_name }} </td>", # nb for now ignore unicode apostrophe in agent's name
    '<th> Appeal status </th> <td> {{ appeal_status }} </td>',
    ]

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
        while len(final_result) < self.MAX_ID_BATCH and bad_count < 30:
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
        fields = { 'search': 'yes', 'appno': uid  }
        response = util.open_url(self.br, self.search_url, fields, 'GET')
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

    scraper = HantsScraper()
    #scraper.clear_all()
    scraper.run()
    
    #scraper.DEBUG = True
    #print scraper.gather_ids2(None)
    # misc tests
    #print scraper.get_detail_from_uid ('K6390/12')
    #print scraper.get_detail_from_uid ('HDC23999')
    #result = scraper.get_id_records2(1200, True)
    #result = scraper.get_id_records(1)
    #print result
    #print scraper.gather_ids(None, None)
    #scraper.gather_current_ids()


