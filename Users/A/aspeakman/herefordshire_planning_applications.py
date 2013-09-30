# this is a scraper of Herefordshire planning applications for use by Openly Local

# now works from the sequence of reference numbers (in YYNNNN format) - no date or list query

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

class HerefordshireScraper(base.ListScraper):

    START_SEQUENCE = 20000001 # gathering back to this record number (in YYYYNNNN format derived from the application number in this format = YYNNNNN)
    START_POINT = (date.today().year * 10000) + 1
    MIN_RECS = 70
    #START_SEQUENCE = 35000 # gathering back to this record number 
    PAGE_SIZE = 50 # NB the site returns 1 more than this on each page, but starts correctly on the next page
    MAX_ID_BATCH = 100 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 150 # max application details to scrape in one go
    ID_ORDER = 'url desc'

    search_form = 'form2'
    search_submit = 'SearchForm1$SearchButton1'
    form_fields = { 'SearchForm1$pageSize': str(PAGE_SIZE) }
    page_fields = {
                   'SearchForm1$SearchButton4': None, 'SearchForm1$SearchButton3': None,
                'SearchForm1$SearchButton2': None, 'SearchForm1$SearchButton1': None,
                'HCEVENTTARGET': 'SearchForm1$blPageList', 'HCEVENTARGUMENT': '6',
                }
    search_url = 'http://www.herefordshire.gov.uk/housing/planning/searchplanningapplications.aspx'
    applic_url = 'http://www.herefordshire.gov.uk/housing/planning/58286.aspx'
    scrape_ids = """
    <table id="SearchForm1_ResultsGrid"> <tr />
        {* <tr>
         <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
         </tr> *}
    </table>
    """
    scrape_max_recs = """
    <div class="recordCount"> of {{ max_recs }} </div>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <form id="form2"> {{ block|html }} </form>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <h2> Planning application number: {{ reference }} </h2>
    <tr> Location {{ address }} </tr>
    <tr> Proposal {{ description }} </tr>
    <tr> Date received {{ date_received }} </tr>
    <tr> Date validated {{ date_validated }} </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr> Consultation start date {{ consultation_start_date }} </tr>',
    '<tr> Consultation end date {{ consultation_end_date }} </tr>',
    '<tr> Case Officer {{ case_officer }} </tr>',
    '<tr> Decision date {{ decision_date }} </tr>',
    '<tr> Appeal date {{ appeal_date }} </tr>',
    '<tr> Ward {{ ward_name }} </tr>',
    '<tr> Parish {{ parish }} </tr>',
    '<p> <span class="greenLabel"> Current status: </span> {{ status }} </p>',
    '<tr> Agent or Applicant name and address {{ agent_name }} , {{ agent_address }} . (Agent) {{ applicant_name }} , {{ applicant_address }} . (Applicant) </tr>',
    '<tr> Application type {{ application_type }} </tr>',
    '<tr> Target determination date {{ target_decision_date }} </tr>',
    '<tr> Appeal date {{ appeal_date }} </tr>',
    '<tr> Appeal decision date {{ appeal_decision_date }} </tr>',
    '<tr> Committee date {{ meeting_date }} </tr>',
    '<tr> Publicity date {{ last_advertised_date }} </tr>',
    '<tr> Comments by {{ comment_date }} </tr>',
    '<tr> Easting/Northing {{ easting }} - {{ northing }} </tr>',
    ]

    # Note pages are numbered in the reverse order, so records will be found on different page numbers as the number of records expands
    # NB records are returned in reverse sequence order
    # NB if both are None, it's the first ever scrape
    # NB if rec_to is None, rec_from is the highest existing record and it's a current scrape
    # NB also if rec_to is None, the default should be to try to get at least self.MIN_RECS records
    def get_id_records (self, rec_from, rec_to = None): 
        final_result = []
        num_from = None
        num_to = None

        response = util.open_url(self.br, self.search_url)
        util.setup_form(self.br, self.search_form, self.form_fields)
        response = util.submit_form(self.br, self.search_submit)

        html = response.read()
        #print html
        result = scrapemark.scrape(self.scrape_max_recs, html)
        num_recs = int(result['max_recs'])
        if self.DEBUG: print 'Number of records', num_recs
        self.br.select_form(name=self.search_form)
        if self.DEBUG: print 'page size, total', self.br['SearchForm1$pageSize'], self.br['SearchForm1$recordTotal']

        fields = self.page_fields

        if not rec_from and not rec_to:
            rec_from = self.START_SEQUENCE
            rec_to = num_recs
        elif not rec_to:
            rec_to = num_recs
            rec_from -= self.MIN_RECS

        if rec_to > num_recs:
            rec_to = num_recs
        if (rec_to - rec_from + 1) > self.MAX_ID_BATCH:
            rec_from = rec_to - self.MAX_ID_BATCH + 1

        page_from = ((num_recs - rec_to) / self.PAGE_SIZE) + 1
        if rec_to <= rec_from:
            page_to = page_from
        else:
            page_to = ((num_recs - rec_from) / self.PAGE_SIZE) + 1
        if self.DEBUG: print 'Looking for pages: ', page_from, page_to
        
        current_page = page_from
        if current_page > 1:
            # kludge - have to page through to get to starting page number
            fields['HCEVENTARGUMENT'] = '5' # first Next >> control
            for i in range(1, current_page):
                util.setup_form(self.br, self.search_form, fields)
                response = util.submit_form(self.br)
                fields['HCEVENTARGUMENT'] = '6' # subsequent Next >> controls
            if not response:
                page_to = current_page - 1
            else:
                html = response.read()

        while current_page <= page_to:
            if self.DEBUG: print 'On page', current_page
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                if self.DEBUG: print result
                self.clean_ids(result['records'])
                final_result.extend(result['records'][:self.PAGE_SIZE])
                if self.DEBUG: print 'Output N: ', len(final_result)
            else:
                page_to = current_page - 1
                break
            current_page += 1
            if current_page <= page_to:
                if current_page <= 2:
                    fields['HCEVENTARGUMENT'] = '5' # first Next >> control
                else:
                    fields['HCEVENTARGUMENT'] = '6' # subsequent Next >> controls
                util.setup_form(self.br, self.search_form, fields)
                response = util.submit_form(self.br)
                if not response:
                    page_to = current_page - 1
                    break
                html = response.read()

        if final_result:
            num_from = num_recs - (page_to * self.PAGE_SIZE) + 1
            if num_from <= 0: num_from = 1
            num_to = num_recs - ((page_from-1) * self.PAGE_SIZE)
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
        fields = {}
        while len(final_result) < self.MAX_ID_BATCH and bad_count < 20:
            current_year = str(current_rec)[0:4]
            current_page = str(current_rec)[4:8]
            current_appno = current_year[2:4] + '' + current_page # note lower 2 year digits only here
            if self.DEBUG: print 'Record:', current_appno
            try:
                fields['ID'] = current_appno
                response = util.open_url(self.br, self.applic_url, fields, 'GET')
                if response:
                    html = response.read()
                    url = response.geturl()
                    result = scrapemark.scrape(self.scrape_min_data, html, url)
                    if result and result.get('reference'):
                        if not first_good_rec: first_good_rec = current_rec
                        last_good_rec = current_rec
                        if self.DEBUG: print result
                        uid = result['reference']
                        final_result.append({ 'url': self.applic_url + '?ID=' + urllib.quote_plus(current_appno), 'uid': uid })
                        #print 'Gap ', bad_count
                        bad_count = 0
                        find_bad = True
                    elif find_bad:
                        bad_count += 1
                elif find_bad:
                    bad_count += 1
            except:
                if find_bad: bad_count += 1
            if move_forward:
                if bad_count == 10: # try the next year if moving forward and we reach 10 errors
                    current_rec = (int(current_year)+1)*10000
                else:
                    current_rec += 1
            else:
                if current_page == '0000': # if moving backward, swap to next year when reach zero
                    current_rec = ((int(current_year)-1)*10000)+4500 # expecting max 4500 applications per year (potentially 9999)
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

    def get_max_recs (self): # not used
        try:
            response = util.open_url(self.br, self.search_url)
            util.setup_form(self.br, self.search_form, self.form_fields)
            response = util.submit_form(self.br, self.search_submit)
            html = response.read()
            result = scrapemark.scrape(self.scrape_max_recs, html)
            max_recs = int(result['max_recs'])
        except:
            max_recs = scraperwiki.sqlite.get_var(self.DATA_END_MARKER)
        return max_recs

    def get_detail_from_uid (self, uid):
        url = self.applic_url + '?ID=' + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    scraper = HerefordshireScraper()
    #print scraper.get_id_records2(20130002, False)
    #scraper.reset(20053647, 20130890)
    #scraper.gather_current_ids2()
    #scraper.reset(34977, 48005)
    #print scraper.get_max_sequence()
    scraper.run()

    #scraper.DEBUG = True
    # misc tests
    #print scraper.get_detail_from_uid ('120881')
    #result = scraper.get_id_records(120900,120902)
    #print result
    #print scraper.gather_ids(None, None)
    #scraper.gather_current_ids()

    #util.rename_column('swdata', 'ward', 'ward_name')


# this is a scraper of Herefordshire planning applications for use by Openly Local

# now works from the sequence of reference numbers (in YYNNNN format) - no date or list query

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

class HerefordshireScraper(base.ListScraper):

    START_SEQUENCE = 20000001 # gathering back to this record number (in YYYYNNNN format derived from the application number in this format = YYNNNNN)
    START_POINT = (date.today().year * 10000) + 1
    MIN_RECS = 70
    #START_SEQUENCE = 35000 # gathering back to this record number 
    PAGE_SIZE = 50 # NB the site returns 1 more than this on each page, but starts correctly on the next page
    MAX_ID_BATCH = 100 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 150 # max application details to scrape in one go
    ID_ORDER = 'url desc'

    search_form = 'form2'
    search_submit = 'SearchForm1$SearchButton1'
    form_fields = { 'SearchForm1$pageSize': str(PAGE_SIZE) }
    page_fields = {
                   'SearchForm1$SearchButton4': None, 'SearchForm1$SearchButton3': None,
                'SearchForm1$SearchButton2': None, 'SearchForm1$SearchButton1': None,
                'HCEVENTTARGET': 'SearchForm1$blPageList', 'HCEVENTARGUMENT': '6',
                }
    search_url = 'http://www.herefordshire.gov.uk/housing/planning/searchplanningapplications.aspx'
    applic_url = 'http://www.herefordshire.gov.uk/housing/planning/58286.aspx'
    scrape_ids = """
    <table id="SearchForm1_ResultsGrid"> <tr />
        {* <tr>
         <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
         </tr> *}
    </table>
    """
    scrape_max_recs = """
    <div class="recordCount"> of {{ max_recs }} </div>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <form id="form2"> {{ block|html }} </form>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <h2> Planning application number: {{ reference }} </h2>
    <tr> Location {{ address }} </tr>
    <tr> Proposal {{ description }} </tr>
    <tr> Date received {{ date_received }} </tr>
    <tr> Date validated {{ date_validated }} </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr> Consultation start date {{ consultation_start_date }} </tr>',
    '<tr> Consultation end date {{ consultation_end_date }} </tr>',
    '<tr> Case Officer {{ case_officer }} </tr>',
    '<tr> Decision date {{ decision_date }} </tr>',
    '<tr> Appeal date {{ appeal_date }} </tr>',
    '<tr> Ward {{ ward_name }} </tr>',
    '<tr> Parish {{ parish }} </tr>',
    '<p> <span class="greenLabel"> Current status: </span> {{ status }} </p>',
    '<tr> Agent or Applicant name and address {{ agent_name }} , {{ agent_address }} . (Agent) {{ applicant_name }} , {{ applicant_address }} . (Applicant) </tr>',
    '<tr> Application type {{ application_type }} </tr>',
    '<tr> Target determination date {{ target_decision_date }} </tr>',
    '<tr> Appeal date {{ appeal_date }} </tr>',
    '<tr> Appeal decision date {{ appeal_decision_date }} </tr>',
    '<tr> Committee date {{ meeting_date }} </tr>',
    '<tr> Publicity date {{ last_advertised_date }} </tr>',
    '<tr> Comments by {{ comment_date }} </tr>',
    '<tr> Easting/Northing {{ easting }} - {{ northing }} </tr>',
    ]

    # Note pages are numbered in the reverse order, so records will be found on different page numbers as the number of records expands
    # NB records are returned in reverse sequence order
    # NB if both are None, it's the first ever scrape
    # NB if rec_to is None, rec_from is the highest existing record and it's a current scrape
    # NB also if rec_to is None, the default should be to try to get at least self.MIN_RECS records
    def get_id_records (self, rec_from, rec_to = None): 
        final_result = []
        num_from = None
        num_to = None

        response = util.open_url(self.br, self.search_url)
        util.setup_form(self.br, self.search_form, self.form_fields)
        response = util.submit_form(self.br, self.search_submit)

        html = response.read()
        #print html
        result = scrapemark.scrape(self.scrape_max_recs, html)
        num_recs = int(result['max_recs'])
        if self.DEBUG: print 'Number of records', num_recs
        self.br.select_form(name=self.search_form)
        if self.DEBUG: print 'page size, total', self.br['SearchForm1$pageSize'], self.br['SearchForm1$recordTotal']

        fields = self.page_fields

        if not rec_from and not rec_to:
            rec_from = self.START_SEQUENCE
            rec_to = num_recs
        elif not rec_to:
            rec_to = num_recs
            rec_from -= self.MIN_RECS

        if rec_to > num_recs:
            rec_to = num_recs
        if (rec_to - rec_from + 1) > self.MAX_ID_BATCH:
            rec_from = rec_to - self.MAX_ID_BATCH + 1

        page_from = ((num_recs - rec_to) / self.PAGE_SIZE) + 1
        if rec_to <= rec_from:
            page_to = page_from
        else:
            page_to = ((num_recs - rec_from) / self.PAGE_SIZE) + 1
        if self.DEBUG: print 'Looking for pages: ', page_from, page_to
        
        current_page = page_from
        if current_page > 1:
            # kludge - have to page through to get to starting page number
            fields['HCEVENTARGUMENT'] = '5' # first Next >> control
            for i in range(1, current_page):
                util.setup_form(self.br, self.search_form, fields)
                response = util.submit_form(self.br)
                fields['HCEVENTARGUMENT'] = '6' # subsequent Next >> controls
            if not response:
                page_to = current_page - 1
            else:
                html = response.read()

        while current_page <= page_to:
            if self.DEBUG: print 'On page', current_page
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                if self.DEBUG: print result
                self.clean_ids(result['records'])
                final_result.extend(result['records'][:self.PAGE_SIZE])
                if self.DEBUG: print 'Output N: ', len(final_result)
            else:
                page_to = current_page - 1
                break
            current_page += 1
            if current_page <= page_to:
                if current_page <= 2:
                    fields['HCEVENTARGUMENT'] = '5' # first Next >> control
                else:
                    fields['HCEVENTARGUMENT'] = '6' # subsequent Next >> controls
                util.setup_form(self.br, self.search_form, fields)
                response = util.submit_form(self.br)
                if not response:
                    page_to = current_page - 1
                    break
                html = response.read()

        if final_result:
            num_from = num_recs - (page_to * self.PAGE_SIZE) + 1
            if num_from <= 0: num_from = 1
            num_to = num_recs - ((page_from-1) * self.PAGE_SIZE)
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
        fields = {}
        while len(final_result) < self.MAX_ID_BATCH and bad_count < 20:
            current_year = str(current_rec)[0:4]
            current_page = str(current_rec)[4:8]
            current_appno = current_year[2:4] + '' + current_page # note lower 2 year digits only here
            if self.DEBUG: print 'Record:', current_appno
            try:
                fields['ID'] = current_appno
                response = util.open_url(self.br, self.applic_url, fields, 'GET')
                if response:
                    html = response.read()
                    url = response.geturl()
                    result = scrapemark.scrape(self.scrape_min_data, html, url)
                    if result and result.get('reference'):
                        if not first_good_rec: first_good_rec = current_rec
                        last_good_rec = current_rec
                        if self.DEBUG: print result
                        uid = result['reference']
                        final_result.append({ 'url': self.applic_url + '?ID=' + urllib.quote_plus(current_appno), 'uid': uid })
                        #print 'Gap ', bad_count
                        bad_count = 0
                        find_bad = True
                    elif find_bad:
                        bad_count += 1
                elif find_bad:
                    bad_count += 1
            except:
                if find_bad: bad_count += 1
            if move_forward:
                if bad_count == 10: # try the next year if moving forward and we reach 10 errors
                    current_rec = (int(current_year)+1)*10000
                else:
                    current_rec += 1
            else:
                if current_page == '0000': # if moving backward, swap to next year when reach zero
                    current_rec = ((int(current_year)-1)*10000)+4500 # expecting max 4500 applications per year (potentially 9999)
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

    def get_max_recs (self): # not used
        try:
            response = util.open_url(self.br, self.search_url)
            util.setup_form(self.br, self.search_form, self.form_fields)
            response = util.submit_form(self.br, self.search_submit)
            html = response.read()
            result = scrapemark.scrape(self.scrape_max_recs, html)
            max_recs = int(result['max_recs'])
        except:
            max_recs = scraperwiki.sqlite.get_var(self.DATA_END_MARKER)
        return max_recs

    def get_detail_from_uid (self, uid):
        url = self.applic_url + '?ID=' + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    scraper = HerefordshireScraper()
    #print scraper.get_id_records2(20130002, False)
    #scraper.reset(20053647, 20130890)
    #scraper.gather_current_ids2()
    #scraper.reset(34977, 48005)
    #print scraper.get_max_sequence()
    scraper.run()

    #scraper.DEBUG = True
    # misc tests
    #print scraper.get_detail_from_uid ('120881')
    #result = scraper.get_id_records(120900,120902)
    #print result
    #print scraper.gather_ids(None, None)
    #scraper.gather_current_ids()

    #util.rename_column('swdata', 'ward', 'ward_name')


