# this is a scraper of Walsall planning applications for use by Openly Local

# works from the sequence of application numbers (in YY/NNNN/EXT format) - no date or list query

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

class WalsallScraper(base.ListScraper):

    START_SEQUENCE = 20020001 # gathering back to this record number (in YYYYNNNN format derived from the application number in this format = YY/NNNN/EXT)
    MAX_ID_BATCH = 350 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go
    START_POINT = (date.today().year * 10000) + 1
    #ID_ORDER = 'uid desc'
    ID_ORDER = "CASE uid WHEN substr(uid, 1, 2) < '50' THEN '20' || uid ELSE '19' || uid END desc"

    applic_url = 'http://www2.walsall.gov.uk/dcaccess/headway/AppNumberSearchResults.asp'
    search_url = 'http://www2.walsall.gov.uk/dcaccess/headway/AppNumberSearchResults.asp'
    scrape_ids = """
    <table class="MISresults">
        {* <tr> <input type="HIDDEN" value="{{ [records].uid }}" name="AppNumber">
                <input type="HIDDEN" value="{{ [records].reference }}" name="AppID">
                <input type="HIDDEN" value="{{ [records].uprn }}" name="UPRN"> 
            </tr> *}
    </table>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="content"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <tr> <td> APPLICATION NUMBER </td> <td> {{ reference }} </td> </tr>
    <tr> <td> DATE RECEIVED </td> <td> {{ date_received }} </td> </tr>
    <tr> <td> DATE VALID </td> <td> {{ date_validated }} </td> </tr>
    <tr> <td> DESCRIPTION </td> <td> {{ description }} </td> </tr>
    <tr> <td> ADDRESS </td> <td> {{ address }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr> <td> APPLICATION TYPE </td> <td> {{ application_type }} </td> </tr>',
    '<tr> <td> DECISION DATE </td> <td> {{ decision_date }} </td> </tr>',
    '<tr> <td> OFFICER </td> <td> {{ case_officer }} </td> </tr>',
    '<tr> <td> WARD </td> <td> {{ ward_name }} </td> </tr>',
    '<tr> <td> DECISION DETAIL </td> <td> {{ decision }} </td> </tr>',
    '<a href="{{ comment_url }}">Click here to comment on this application</a>'
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
        fields = {}
        while current_rec >= rec_from and len(final_result) < self.MAX_ID_BATCH:
            current_page = str(current_rec)[4:8]
            if int(current_page) < 2000: # only testing for max 2000 applications per year (potentially there are 9999)
                current_appno = str(current_rec)[2:4] + '/' + current_page + '/'
                if self.DEBUG: print 'On page:', current_appno
                fields['AppNo'] = current_appno
                response = util.open_url(self.br, self.search_url, fields, 'POST')
                if response:
                    html = response.read()
                    url = response.geturl()
                    if self.DEBUG: print 'Html:', html
                    result = scrapemark.scrape(self.scrape_ids, html, url)
                    if result and result.get('records'):
                        if not top_page: top_page = current_appno
                        bot_page = current_appno
                        if self.DEBUG: print result
                        unique_refs = [ ]
                        unique_records = [ ]
                        for r in result['records']:
                            if r['reference'] not in unique_refs: # remove duplicates
                                r['url'] = self.applic_url + '?AppNo=' + urllib.quote_plus(r['uid'])
                                unique_refs.append(r['reference'])
                                unique_records.append(r)
                        self.clean_ids(unique_records)
                        final_result.extend(unique_records)
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

    # NB if move_forward is true, we scrape forwards from rec_start, otherwise we scrape backwards
    def get_id_records2 (self, rec_start, move_forward):
        final_result = []
        num_from = None
        num_to = None
        bad_count = 0
        find_bad = True
        current_rec = rec_start
        fields = {}
        first_good_rec = None
        last_good_rec = None
        while len(final_result) < self.MAX_ID_BATCH and bad_count < 20:
            current_year = str(current_rec)[0:4]
            current_page = str(current_rec)[4:8]
            current_appno = current_year[2:4] + '/' + current_page + '/' # note lower 2 year digits only here
            if self.DEBUG: print 'Record:', current_appno
            fields['AppNo'] = current_appno
            response = util.open_url(self.br, self.search_url, fields, 'POST')
            if response:
                html = response.read()
                url = response.geturl()
                if self.DEBUG: print 'Html:', html
                result = scrapemark.scrape(self.scrape_ids, html, url)
                if result and result.get('records'):
                    if not first_good_rec: first_good_rec = current_rec
                    last_good_rec = current_rec
                    if self.DEBUG: print result
                    unique_refs = [ ]
                    unique_records = [ ]
                    for r in result['records']:
                        if r['reference'] not in unique_refs: # remove duplicates
                            r['url'] = self.applic_url + '?AppNo=' + urllib.quote_plus(r['uid'])
                            unique_refs.append(r['reference'])
                            unique_records.append(r)
                    final_result.extend(unique_records)
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
                    current_rec = ((int(current_year)-1)*10000)+2000 # expecting max 2000 applications per year (potentially 9999)
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
        try:
            # search by application number
            fields = { 'AppNo': uid  }
            response = util.open_url(self.br, self.applic_url, fields)

            # follow first view form if there is one
            form_ok = util.setup_form(self.br)
            response = util.submit_form(self.br)

            html = response.read()
            url = response.geturl()
            if self.DEBUG: print "detail page:", html
        except:
            if self.DEBUG: raise
            else: return None
        return self.get_detail(html, url)

if __name__ == 'scraper':

    scraper = WalsallScraper()
    scraper.run()

    #scraper.DEBUG = True
    # misc tests
    #print scraper.get_detail_from_uid ('12/0001/')
    #result = scraper.get_id_records(20050000, 20120050)
    #result = scraper.get_id_records(20120709)
    #print result
    #print scraper.gather_ids(None, None)
    #scraper.gather_current_ids()

    #util.rename_column('swdata', 'ward', 'ward_name')
    #scraperwiki.sqlite.save_var('latest', 20120800)
