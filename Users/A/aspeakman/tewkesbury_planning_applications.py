# this is a scraper of Tewkesbury planning applications for use by Openly Local

# works from the sequence of application numbers (in YY/NNNNN/ABC) - no date or list query

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

class TewkesburyScraper(base.ListScraper):

    START_SEQUENCE = 200000000 # gathering back to this record number (in YYYYNNNNN format derived from the application number in this format = YY/NNNNN/ABC)
    MAX_ID_BATCH = 300 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go
    START_POINT = (date.today().year * 100000) + 1
    MIN_RECS = 100
    #ID_ORDER = 'uid desc'
    ID_ORDER = "CASE uid WHEN substr(uid, 1, 2) < '50' THEN '20' || uid ELSE '19' || uid END desc"

    applic_url = 'http://planning2.tewkesbury.gov.uk/WAM/showCaseFile.do?action=show&appType=Planning'
    search_url = 'http://planning2.tewkesbury.gov.uk/WAM/findCaseFile.do'
    search_fields = { 'action': 'Search' }
    scrape_ids = """
    <table id="searchresults"> <tr />
        {* <tr>
         <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
         </tr> *}
    </table>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="info"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <table id="casefilesummary">
    <tr> <th id="application" /> <td> {{ reference }} </td> </tr>
    <tr> <th id="proposal" /> <td> {{ description }} </td> </tr>
    <tr> <th id="location" /> <td> {{ address }} </td> </tr>
    </table>
    <table id="relevantdates">
    <tr> <th> Application Received: </th> <td> {{ date_received }} </td> </tr>
    <tr> <th> Application Valid: </th> <td> {{ date_validated }} </td> </tr>
    </table>"""
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr> <th id="applicant" /> <td> {{ applicant_name }} <br> {{ applicant_address }} </td> </tr>',
    '<tr> <th id="agent" /> <td> {{ agent_name }} <br> {{ agent_address }} </td> </tr>',
    '<tr> <th> Please submit your comments by: </th> <td> {{ comment_date }} </td> </tr>',
    '<tr> <th id="caseofficer" /> <td> {{ case_officer }} </td> </tr>',
    '<tr> <th> Decision Date : </th> <td> {{ decision_date }} </td> </tr>',
    '<tr> <th> Committee Date: </th> <td> {{ meeting_date }} </td> </tr>',
    '<tr> <th> Appeal Lodged Date: </th> <td> {{ appeal_date }} </td> </tr>',
    '<tr> <th> Appeal Decision Date: </th> <td> {{ appeal_decision_date }} </td> </tr>',
    '<tr> <th id="applicationstatus" /> <td> {{ status }} </td> </tr>',
    '<tr> <th id="parish" /> <td> {{ parish }} </td> </tr>',
    '<tr> <th id="ward" /> <td> {{ ward_name }} </td> </tr>',
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
            rec_to = (date.today().year * 100000) + 99999 # last possible record of the current year
        elif not rec_to:
            rec_to = rec_from + self.MIN_RECS # set target after highest current record to get any recent records
            min_rec_to = (date.today().year * 100000) + self.MIN_RECS # first possible record of the current year 
            if rec_to < min_rec_to: rec_to = min_rec_to
            rec_from -= self.MIN_RECS

        if self.DEBUG: print 'Looking for records: ', rec_from, rec_to
        
        current_rec = rec_to
        top_page = None
        bot_page = None
        fields = self.search_fields

        while current_rec >= rec_from and len(final_result) < self.MAX_ID_BATCH:
            current_page = str(current_rec)[4:7]
            if int(current_page) < 20: # only testing for max 20 pages of 100 records per year (potentially there are 999)
                current_appno = str(current_rec)[2:4] + '/' + current_page
                if self.DEBUG: print 'On page:', current_appno
                fields['appNumber'] = current_appno
                #response = util.open_url(self.br, self.search_url, fields, 'GET') # dont use this = unicode BOM characters in web page cause lxml exception
                url = util.add_to_query(self.search_url, fields) 
                response = urllib.urlopen(url)
                if response:
                    html = response.read()
                    url = response.geturl()
                    result = scrapemark.scrape(self.scrape_ids, html, url)
                    if result and result.get('records'):
                        if not top_page: top_page = current_appno
                        bot_page = current_appno
                        if self.DEBUG: print result
                        self.clean_ids(result['records'])
                        final_result.extend(result['records'])
                        if self.DEBUG: print 'Output N: ', len(final_result)
                else:
                    break
            current_rec -= 100
                
        if final_result:
            if self.DEBUG: print bot_page, top_page
            num_from = int(bot_page[:2]) + 1900
            if num_from <= 1930: num_from += 100
            num_to = int(top_page[:2]) + 1900
            if num_to <= 1930: num_to += 100
            num_from = (num_from * 100000) + (int(bot_page[3:6]) * 100)
            num_to = (num_to * 100000) + (int(top_page[3:6]) * 100) + 99
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
        fields = self.search_fields
        while len(final_result) < self.MAX_ID_BATCH and find_bad and bad_count < 20:
            current_year = str(current_rec)[0:4]
            current_page = str(current_rec)[4:9]
            current_appno = current_year[2:4] + '/' + current_page # note lower 2 year digits only here
            if self.DEBUG: print 'Record:', current_appno
            fields['appNumber'] = current_appno
            #response = util.open_url(self.br, self.search_url, fields, 'GET') # dont use this = unicode BOM characters in web page cause lxml exception
            url = util.add_to_query(self.search_url, fields)
            response = urllib.urlopen(url)
            if response:
                html = response.read()
                url = response.geturl()
                result = scrapemark.scrape(self.scrape_min_data, html, url)
                if result and result.get('reference'):
                    if not first_good_rec: first_good_rec = current_rec
                    last_good_rec = current_rec
                    if self.DEBUG: print result
                    uid = result['reference']
                    final_result.append({ 'url': self.applic_url + '&appNumber=' + urllib.quote_plus(uid), 'uid': uid })
                    bad_count = 0
                    find_bad = True
                elif find_bad:
                    bad_count += 1
            elif find_bad:
                bad_count += 1
            if move_forward:
                if bad_count == 10: # try the next year if moving forward and we reach 10 errors
                    current_rec = (int(current_year)+1)*100000
                else:
                    current_rec += 1
            else:
                if current_page == '00000': # if moving backward, swap to next year when reach zero
                    current_rec = ((int(current_year)-1)*100000)+2000 # expecting max 2000 applications per year (potentially 9999)
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

    def get_detail_from_uid (self, uid):
        url = self.applic_url + '&appNumber=' + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    scraper = TewkesburyScraper()
    scraper.run()

    #scraper.DEBUG = True
    # misc tests
    #print scraper.get_detail_from_uid ('04/00099/FUL')
    #result = scraper.get_id_records(200500000, 201200199)
    #result = scraper.get_id_records(201200599)
    #print result
    #print scraper.gather_ids(None, None)
    #scraper.gather_current_ids()

    #util.rename_column('swdata', 'ward', 'ward_name')
    #scraperwiki.sqlite.save_var('latest', 201200600)
