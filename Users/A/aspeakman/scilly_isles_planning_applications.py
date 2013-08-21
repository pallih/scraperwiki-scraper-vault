# this is a scraper of Scilly Isles planning applications for use by Openly Local

# two types of application number (in P.NNNN and P-YY-NNN format) - also date search applies to dates of meetings not date received

# so work from sequence of id numbers embedded in URLs

# records go back to id number 1 in 2005?

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

class ScillyIslesScraper(base.ListScraper):

    START_SEQUENCE = 1 # gathering back to this id number
    MAX_ID_BATCH = 70 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 50 # max application details to scrape in one go
    MIN_RECS = 20
    ID_ORDER = 'url desc'
    START_POINT = 900
    
    applic_url = 'http://www.scilly.gov.uk/environment/planning/applications.htm?mode=10'
    search_url = 'http://www.scilly.gov.uk/environment/planning/applications.htm'
    scrape_ids = """
    <table class="view_table"> <tr />
    {* <tr>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    </tr> *}
    </table>
    """
    scrape_id = """
    <div id="content"> <tr> <td> Application No: </td> <td> {{ uid }} </td> </tr> </div>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="content"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <tr> <td> Application No: </td> <td> {{ reference }} </td> </tr>
    <tr> <td> Location: </td> <td> {{ address }} </td> </tr>
    <tr> <td> Proposal: </td> <td> <p> {{ description }} </p> </td> </tr>
    <tr> <tr> <td> Date application received: </td> <td> {{ date_received }} </td> </tr> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr> <tr> <td> Type: </td> <td> {{ application_type }} </td> </tr> </tr>',
    """<tr> <tr> <td> Public consultation starts: </td> <td> {{ consultation_start_date }} </td> 
          <td> Public consultation ends: </td> <td> {{ consultation_end_date }} </td> </tr> </tr>""",
    '<tr> <td> Officer: </td> <td> {{ case_officer }} <br /> </td> </tr>',
    '<tr> <tr> <td> Planning meeting date: </td> <td> {{ meeting_date }} </td> </tr> </tr>',
    '<tr> <tr> <td> Decision: </td> <td> {{ decision }} </td> </tr> </tr>',
    '<tr> <td> Agent: </td> <td> {{ agent_name }} <br> {{ agent_address }} </td> </tr>',
    '<tr> <td> Applicant: </td> <td> {{ applicant_name }} <br> {{ applicant_address }} </td> </tr>',
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
            rec_to = 900 # last possible record     
        elif not rec_to:
            rec_to = rec_from + self.MIN_RECS # set target after highest current record to get any recent records
            rec_from -= self.MIN_RECS

        if self.DEBUG: print 'Looking for records: ', rec_from, rec_to
        
        current_rec = rec_to
        top_page = None
        bot_page = None
        fields = {}
        while current_rec >= rec_from and len(final_result) < self.MAX_ID_BATCH:
            current_appno = str(current_rec)
            if self.DEBUG: print 'On page:', current_appno
            try:
                fields = { 'mode': '10', 'id': current_appno }
                response = util.open_url(self.br, self.search_url, fields, 'GET')
                if response:
                    html = response.read()
                    url = response.geturl()
                    if self.DEBUG: print 'Html:', html
                    result = scrapemark.scrape(self.scrape_id, html, url)
                    if result:
                        if not top_page: top_page = current_appno
                        bot_page = current_appno
                        if self.DEBUG: print result
                        result['url'] = self.applic_url + '&id=' + current_appno
                        self.clean_ids([result])
                        final_result.extend([result])
            except:
                pass
            current_rec -= 1
                
        if final_result:
            num_from = int(bot_page)
            num_to = int(top_page)
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
            try:
                fields = { 'mode': '10', 'id': str(current_rec) }
                response = util.open_url(self.br, self.search_url, fields, 'GET')
                if response:
                    html = response.read()
                    url = response.geturl()
                    if self.DEBUG: print 'Html:', html
                    result = scrapemark.scrape(self.scrape_id, html, url)
                    if result and result.get('uid'):
                        if not first_good_rec: first_good_rec = current_rec
                        last_good_rec = current_rec
                        result['url'] = self.applic_url + '&id=' + str(current_rec)
                        if self.DEBUG: print result
                        final_result.append(result)
                        bad_count = 0
                    else:
                        bad_count += 1
                else:
                    bad_count += 1
            except:
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
        try:
            # search by application number
            fields = { 'mode': '1', 'pasearch': uid  }
            response = util.open_url(self.br, self.search_url, fields, 'GET')

            # follow first result if there is one
            html = response.read()
            url = response.geturl()
                
            result = scrapemark.scrape(self.scrape_ids, html, url)
            url = result['records'][0]['url']

            response = util.open_url(self.br, url)
            html = response.read()
            url = response.geturl()
        except:
            if self.DEBUG: raise
            else: return None
        return self.get_detail(html, url)

if __name__ == 'scraper':

    scraper = ScillyIslesScraper()
    #scraper.DEBUG = True
    scraper.run()

    # misc tests
    #print scraper.get_detail_from_uid ('P-07-043')
    #print scraper.get_detail_from_uid ('P-13-002')
    #print scraper.get_detail_from_uid ('P-13-001')
    #result = scraper.get_id_records(200, 210)
    #result = scraper.get_id_records(None, None)
    #print result
    #print scraper.gather_ids(None, None)
    #scraper.gather_current_ids()

    #util.rename_column('swdata', 'ward', 'ward_name')
    #scraperwiki.sqlite.save_var('latest', 800)
