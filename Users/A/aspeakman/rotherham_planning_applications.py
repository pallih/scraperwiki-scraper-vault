# this is a scraper of Rotherham planning applications for use by Openly Local

# works from the sequence of application numbers (in RBYYYY/NNNN format) - no date or list query

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

class RotherhamScraper(base.ListScraper):

    START_SEQUENCE = 20000000 # gathering back to this record number (in YYYYNNNN format derived from the application number in this format = RBYYYY/NNNN)
    START_POINT = (date.today().year * 10000) + 1
    MAX_ID_BATCH = 150 # max application ids to fetch in one go 
    MAX_UPDATE_BATCH = 100 # max application details to scrape in one go
    ID_ORDER = 'uid desc'

    applic_url = 'http://roam.rotherham.gov.uk/planaccess2/dialogbox_infopointviewer.asp?theme=planning%20applications&layername=planning%20applications&fieldname=application_ref&fieldvalue='
    scrape_ids = """
    <table> <table>
    {* <tr> <td> Application_ref </td> <td> {{ [records].uid }} </td> </tr>
    <tr> <td> Property </td> <td> {{ [records].property }} </td> </tr>
    <tr> <td> Street </td> <td> {{ [records].street }} </td> </tr>
    <tr> <td> District </td> <td> {{ [records].district }} </td> </tr>
    *}
    </table> </table>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <table> <table> {{ block|html }} </table> </table>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <tr> <td> Application_ref </td> <td> {{ reference }} </td> </tr>
    <tr> <td> Date_Valid </td> <td> {{ date_validated }} </td>  </tr>
    <tr> <td> Proposal </td> <td> {{ description }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [ 
    '<tr> <td> District </td> <td> {{ district }} </td> </tr>',
    '<tr> <td> Case_Officer </td> <td> {{ case_officer }} </td> </tr>',
    '<tr> <td> Applicant </td> <td> {{ applicant_name }} </td> </tr>',
    '<tr> <td> Comment_on_this_Application </td> <td> <a href="{{ comment_url|abs }}" /> </td> </tr>',
    '<tr> <td> Consultation_Period_START </td> <td> {{ consultation_start_date }} </td> </tr>',
    '<tr> <td> Consultation_Period_END </td> <td> {{ consultation_end_date }} </td> </tr>',
    '<tr> <td> Provisional_Decision_Date </td> <td> {{ target_decision_date }} </td> </tr>',
    '<tr> <td> Decision </td> <td> {{ decision }} </td> </tr>',
    '<tr> <td> Decision_Date </td> <td> {{ decision_date }} </td> </tr>',
    '<tr> <td> Appeal_Decision_Date </td> <td> {{ appeal_decision_date }} </td> </tr>',
    '<tr> <td> Appeal_Decision </td> <td> {{ appeal_result }} </td> </tr>',
    '<tr> <td> Appeal </td> <td> {{ appeal_date }} </td> </tr>',
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
        while current_rec >= rec_from and len(final_result) < self.MAX_ID_BATCH:
            current_page = str(current_rec)[4:8]
            if int(current_page) < 2100: # only testing for max 2100 applications per year (potentially there are 9999)
                current_appno = 'RB' + str(current_rec)[0:4] + '/' + current_page
                if self.DEBUG: print 'On page:', current_appno

                url = self.applic_url + urllib.quote_plus(current_appno)
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
                        for rec in result['records']:
                            rec['url'] = self.applic_url + urllib.quote_plus(rec['uid'])
                            rec['address'] = rec['property'] + ' ' + rec['street'] + ' ' + rec['district'] + ' Rotherham'
                            del rec['property']
                            del rec['street']
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
            current_appno = 'RB' + current_year + '/' + current_page
            if self.DEBUG: print 'Record:', current_appno
            url = self.applic_url + urllib.quote_plus(current_appno)
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
                    for rec in result['records']:
                        rec['url'] = self.applic_url + urllib.quote_plus(rec['uid'])
                        rec['address'] = rec['property'] + ' ' + rec['street'] + ' ' + rec['district'] + ' Rotherham'
                        del rec['property']
                        del rec['street']
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
                    current_rec = ((int(current_year)-1)*10000)+2100 # expecting max 2100 applications per year (potentially 9999)
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
        url = self.applic_url + urllib.quote_plus(uid) 
        return self.get_detail_from_url(url)
                        
if __name__ == 'scraper':

    scraper = RotherhamScraper()
    scraper.run()

    #scraper.DEBUG = True
    # misc tests
    #print scraper.get_detail_from_uid ('RB2011/0959')
    #result = scraper.get_id_records(20050000, 20120050)
    #result = scraper.get_id_records(20120709)
    #print result
    #print scraper.gather_ids(None, None)
    #scraper.gather_current_ids()

    #util.rename_column('swdata', 'ward', 'ward_name')
    #scraperwiki.sqlite.save_var('latest', 20120800)
# this is a scraper of Rotherham planning applications for use by Openly Local

# works from the sequence of application numbers (in RBYYYY/NNNN format) - no date or list query

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

class RotherhamScraper(base.ListScraper):

    START_SEQUENCE = 20000000 # gathering back to this record number (in YYYYNNNN format derived from the application number in this format = RBYYYY/NNNN)
    START_POINT = (date.today().year * 10000) + 1
    MAX_ID_BATCH = 150 # max application ids to fetch in one go 
    MAX_UPDATE_BATCH = 100 # max application details to scrape in one go
    ID_ORDER = 'uid desc'

    applic_url = 'http://roam.rotherham.gov.uk/planaccess2/dialogbox_infopointviewer.asp?theme=planning%20applications&layername=planning%20applications&fieldname=application_ref&fieldvalue='
    scrape_ids = """
    <table> <table>
    {* <tr> <td> Application_ref </td> <td> {{ [records].uid }} </td> </tr>
    <tr> <td> Property </td> <td> {{ [records].property }} </td> </tr>
    <tr> <td> Street </td> <td> {{ [records].street }} </td> </tr>
    <tr> <td> District </td> <td> {{ [records].district }} </td> </tr>
    *}
    </table> </table>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <table> <table> {{ block|html }} </table> </table>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <tr> <td> Application_ref </td> <td> {{ reference }} </td> </tr>
    <tr> <td> Date_Valid </td> <td> {{ date_validated }} </td>  </tr>
    <tr> <td> Proposal </td> <td> {{ description }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [ 
    '<tr> <td> District </td> <td> {{ district }} </td> </tr>',
    '<tr> <td> Case_Officer </td> <td> {{ case_officer }} </td> </tr>',
    '<tr> <td> Applicant </td> <td> {{ applicant_name }} </td> </tr>',
    '<tr> <td> Comment_on_this_Application </td> <td> <a href="{{ comment_url|abs }}" /> </td> </tr>',
    '<tr> <td> Consultation_Period_START </td> <td> {{ consultation_start_date }} </td> </tr>',
    '<tr> <td> Consultation_Period_END </td> <td> {{ consultation_end_date }} </td> </tr>',
    '<tr> <td> Provisional_Decision_Date </td> <td> {{ target_decision_date }} </td> </tr>',
    '<tr> <td> Decision </td> <td> {{ decision }} </td> </tr>',
    '<tr> <td> Decision_Date </td> <td> {{ decision_date }} </td> </tr>',
    '<tr> <td> Appeal_Decision_Date </td> <td> {{ appeal_decision_date }} </td> </tr>',
    '<tr> <td> Appeal_Decision </td> <td> {{ appeal_result }} </td> </tr>',
    '<tr> <td> Appeal </td> <td> {{ appeal_date }} </td> </tr>',
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
        while current_rec >= rec_from and len(final_result) < self.MAX_ID_BATCH:
            current_page = str(current_rec)[4:8]
            if int(current_page) < 2100: # only testing for max 2100 applications per year (potentially there are 9999)
                current_appno = 'RB' + str(current_rec)[0:4] + '/' + current_page
                if self.DEBUG: print 'On page:', current_appno

                url = self.applic_url + urllib.quote_plus(current_appno)
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
                        for rec in result['records']:
                            rec['url'] = self.applic_url + urllib.quote_plus(rec['uid'])
                            rec['address'] = rec['property'] + ' ' + rec['street'] + ' ' + rec['district'] + ' Rotherham'
                            del rec['property']
                            del rec['street']
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
            current_appno = 'RB' + current_year + '/' + current_page
            if self.DEBUG: print 'Record:', current_appno
            url = self.applic_url + urllib.quote_plus(current_appno)
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
                    for rec in result['records']:
                        rec['url'] = self.applic_url + urllib.quote_plus(rec['uid'])
                        rec['address'] = rec['property'] + ' ' + rec['street'] + ' ' + rec['district'] + ' Rotherham'
                        del rec['property']
                        del rec['street']
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
                    current_rec = ((int(current_year)-1)*10000)+2100 # expecting max 2100 applications per year (potentially 9999)
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
        url = self.applic_url + urllib.quote_plus(uid) 
        return self.get_detail_from_url(url)
                        
if __name__ == 'scraper':

    scraper = RotherhamScraper()
    scraper.run()

    #scraper.DEBUG = True
    # misc tests
    #print scraper.get_detail_from_uid ('RB2011/0959')
    #result = scraper.get_id_records(20050000, 20120050)
    #result = scraper.get_id_records(20120709)
    #print result
    #print scraper.gather_ids(None, None)
    #scraper.gather_current_ids()

    #util.rename_column('swdata', 'ward', 'ward_name')
    #scraperwiki.sqlite.save_var('latest', 20120800)
