# this is a scraper of Waverley planning applications for use by Openly Local

# works from the sequence of application numbers (in WA/YYYY/NNNN format) - no date or list query

# some similarities to AcolNet

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

class WaverleyScraper(base.ListScraper):

    START_SEQUENCE = 20010618 # gathering back to this record number (in YYYYNNNN format derived from the application number in this format = WA/YYYY/NNNN)
    START_POINT = (date.today().year * 10000) + 1
    MAX_ID_BATCH = 350 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go
    ID_ORDER = 'uid desc'

    applic_url = 'http://waverweb.waverley.gov.uk/live/wbc/pwl.nsf/(RefNoLU)/%s?OpenDocument'
    search_url = 'http://waverweb.waverley.gov.uk/live/wbc/PWL.nsf/Weekly%%20List%%20New?SearchView&Query=FIELD+ref_no+CONTAINS+%s+OR+FIELD+ref_no+CONTAINS+%s&count=20&start=1'
    scrape_ids = """
    <table> Back to search </table>
    {* <td bgcolor="ddeeff"> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    *}
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <form action=""> {{ block|html }} </form>
    """
    # the minimum acceptable valid dataset on an application page 
    
    scrape_min_data = """
    <td> Application Record : {{ reference }} </td>
    <td width="158"> Location </td> <td> {{ address }} </td>
    <td width="158"> Proposal </td> <td> {{ description }} </td>
    <td width="158"> Received Date </td> <td> {{ date_received }} </td>
    <td width="158"> Valid Date </td> <td> {{ date_validated }} </td>  
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<td width="158"> Grid Ref </td> <td> {{ easting_northing }} </td>', 
    '<td bgcolor="#F7F7F7"> Latest date for comments: {{ comment_date }} </td>',
    """<td width="158"> Decision Target</td> 
    <td width="158"> Decision </td> <td> {{ decision }} </td>
    <td width="158"> Decision Date </td> <td> {{ decision_date }} </td>""",
    '<td width="158"> Decision Target </td> <td> {{ target_decision_date }} </td>',
    '<td width="158"> Ward </td> <td> {{ ward_name }} </td>',
    '<td width="158"> Parish </td> <td> {{ parish }} </td>',
    '<td width="158"> Applicant </td> <td> {{ applicant_name }} </td>',
    '<td width="158"> Agent </td> <td> {{ agent_name }} </td>',
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
            if int(current_page) < 2500: # only testing for max 2500 applications per year (potentially there are 9999)
                current_appno = 'WA/' + str(current_rec)[0:4] + '/' + current_page
                if self.DEBUG: print 'On page:', current_appno

                url = self.search_url % (current_appno, current_appno) 
                response = self.br.open(url)
                
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
            num_from = int(bot_page[3:7])
            num_to = int(top_page[3:7])
            num_from = (num_from * 10000) + int(bot_page[8:12])
            num_to = (num_to * 10000) + int(top_page[8:12])
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
            current_appno = 'WA/' + current_year + '/' + current_page
            if self.DEBUG: print 'Record:', current_appno
            url = self.search_url % (current_appno, current_appno)
            response = self.br.open(url)
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
                    current_rec = ((int(current_year)-1)*10000)+2500 # expecting max 2500 applications per year (potentially 9999)
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
        uid = uid.replace('/', '')
        url = self.applic_url % uid
        return self.get_detail_from_url(url)

    # post process a scraped record: parses dates, converts to ISO8601 format, strips spaces, tags etc
    def clean_record (self, record):
        if record.get('easting_northing'):
            spl = record['easting_northing'].split(' ')
            record['easting'] = spl[0]
            record['northing'] = spl[1]
            del record['easting_northing']
        return base.ListScraper.clean_record(self, record)

if __name__ == 'scraper':

    scraper = WaverleyScraper()
    scraper.run()

    #scraper.DEBUG = True
    # misc tests
    #print scraper.get_detail_from_uid ('WA/2011/1959')
    #result = scraper.get_id_records(20050000, 20120050)
    #result = scraper.get_id_records(20122050)
    #print result
    #print scraper.gather_ids(None, None)
    #scraper.gather_current_ids()

    #util.rename_column('swdata', 'ward', 'ward_name')
    #scraperwiki.sqlite.save_var('latest', 20120800)

    #util.update_columns('swdata', 'northing')
    #util.update_columns('swdata', 'easting')
    #sql = 'uid, os_grid_ref from swdata'
    #res = scraperwiki.sqlite.select(sql)
    #for i in res:
    #    if i.get('os_grid_ref'):
    #        spl = i['os_grid_ref'].split(' ')
    #        sql = "update swdata set easting = '%s', northing = '%s' where uid = '%s'" % (spl[0], spl[1], i['uid'])
    #        scraperwiki.sqlite.execute(sql)
    #scraperwiki.sqlite.commit()
    #sql = "update swdata set os_grid_ref = null"
    #scraperwiki.sqlite.execute(sql)
    #scraperwiki.sqlite.commit()


