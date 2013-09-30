# this is a scraper of 5 National Park planning authorities with customised systems

# there are another 10 National Parks which use standard planning systems (implemented elsewhere)

# planning applications from all 15 National Parks are collected in the cross_boundary_planning_aggregator

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import random
import urllib
import urlparse
import sys
import copy

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

systems = {
    'PembrokeshireCoast': 'PembrokeshireCoastScraper', 
    'PeakDistrict': 'PeakDistrictScraper', 
    'Exmoor': 'ExmoorScraper',
    'NorthumberlandPark': 'NorthumberlandParkScraper',
    'YorkshireDales': 'YorkshireDalesScraper',
     }

class NorthumberlandParkScraper(base.DateScraper): 

    MAX_ID_BATCH = 150 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 100 # max application details to scrape in one go
    BATCH_DAYS = 28 # batch size for each scrape - number of days to gather to produce at least one result each time
    MIN_DAYS = 28 # min number of days to get when gathering current ids
    TABLE_NAME = 'NorthumberlandPark'

    search_url = 'http://nnpa.planning-register.co.uk/PlaPlanningAppAdvSearch.aspx?mode=reset'
    applic_url = 'http://nnpa.planning-register.co.uk/plaPlanningAppDisplay.aspx?AppNo='
    date_from_field = 'ctl00_ContentPlaceHolder1_txtAppValFrom_dateInput_ClientState'
    date_to_field = 'ctl00_ContentPlaceHolder1_txtAppValTo_dateInput_ClientState'
    search_fields = { '__EVENTTARGET': '', '__EVENTARGUMENT': '', }
    search_form = '1'
    request_date_format = '{"enabled":true,"emptyMessage":"","validationText":"%Y-%m-%d-00-00-00","valueAsString":"%Y-%m-%d-00-00-00","minDateStr":"01/01/1900","maxDateStr":"12/31/2099"}'
    scrape_next_submit = '<input class="rgPageNext" name="{{ next_submit }}">'
    scrape_max_recs = '<div class="rgWrap rgInfoPart"> <strong> {{ max_recs }} </strong> items </div>'
    scrape_ids = """
    <h2>Search Results</h2> <table> <tbody>
    {* <tr>
    <td> <a href="{{ [records].url|abs }}">
    {{ [records].uid }} </a> </td>
    </tr> *}
    </tbody> </table>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = '<div id="contentbody"> {{ block|html }} </div>'
    # the minimum acceptable valid dataset on the details page
    scrape_min_data = """
    <input id="ContentPlaceHolder1_txtAppNum" value="{{ reference }}">
    <textarea id="ContentPlaceHolder1_txtLoc"> {{ address }} </textarea>
    <textarea id="ContentPlaceHolder1_txtProposal"> {{ description }} </textarea>
    <input id="ContentPlaceHolder1_txtRecDate" value="{{ date_received }}">
    <input id="ContentPlaceHolder1_txtValidDate" value="{{ date_validated }}">
    """
    # other optional parameters common to all scrapers can appear on the details page
    scrape_optional_data = [
    '<input id="ContentPlaceHolder1_txtDistrict" value="{{ district }}">',
    '<input id="ContentPlaceHolder1_txtWard" value="{{ ward_name }}">',
    '<input id="ContentPlaceHolder1_Label4" value="{{ parish }}">',
    '<input id="ContentPlaceHolder1_txtEasting" value="{{ easting }}">',
    '<input id="ContentPlaceHolder1_txtNorthing" value="{{ northing }}">',
    '<input id="ContentPlaceHolder1_txtAppStatus" value="{{ status }}">',
    '<input id="ContentPlaceHolder1_txtAppName" value="{{ applicant_name }}">',
    '<input id="ContentPlaceHolder1_txtAgName" value="{{ agent_name }}">',
    '<textarea id="ContentPlaceHolder1_txtAppAddress"> {{ applicant_address }} </textarea>',
    '<textarea id="ContentPlaceHolder1_txtAgAddress"> {{ agent_address }} </textarea>',
    '<input id="ContentPlaceHolder1_txtDecDate" value="{{ decision_date }}">',
    '<input id="ContentPlaceHolder1_txtDec" value="{{ decision }}">',
    '<input id="ContentPlaceHolder1_txtAplDate" value="{{ appeal_date }}">',
    '<input id="ContentPlaceHolder1_txtAplDec" value="{{ appeal_result }}">',
    '<input id="ContentPlaceHolder1_txtPlanOff" value="{{ case_officer }}">',
    ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)

        fields = copy.copy(self.search_fields) 
        fields[self.date_from_field] = date_from.strftime(self.request_date_format)
        fields[self.date_to_field] = date_to.strftime(self.request_date_format)
        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br)

        # note max_recs does not appear if there is only one page
        try:
            html = response.read()
            result = scrapemark.scrape(self.scrape_max_recs, html)
            num_recs = int(result['max_recs'])
        except:
            num_recs = 0
        
        final_result = []
        while response and (len(final_result) < num_recs or num_recs == 0):
            url = response.geturl()
            if self.DEBUG: print html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            else:
                break
            if len(final_result) >= num_recs or num_recs == 0: break
            try:
                result = scrapemark.scrape(self.scrape_next_submit, html)
                fields = copy.copy(self.search_fields) 
                util.setup_form(self.br, self.search_form, fields)
                if self.DEBUG: print self.br.form
                response = util.submit_form(self.br, result['next_submit'])
                html = response.read()
            except:
                break

        return final_result

    def get_detail_from_uid (self, uid):
        url = self.applic_url + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

class YorkshireDalesScraper(base.DateScraper):

    START_SEQUENCE = '2000-02-01' # gathers id data by working backwards from the current date towards this one
    MAX_ID_BATCH = 150 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 100 # max application details to scrape in one go
    MIN_DAYS = 28 # min number of days to get when gathering current ids
    TABLE_NAME = 'YorkshireDales'

    search_url = 'http://www.yorkshiredales.org.uk/planning/planningapplications/planning-applications'
    applic_url = 'http://www.yorkshiredales.org.uk/planning/planningapplications/planning-applications/detailed-results'
    date_from_field = { 'day': 'q121429:q7', 'month': 'q121429:q8', 'year': 'q121429:q9', }
    date_to_field = { 'day': 'q121429:q10', 'month': 'q121429:q11', 'year': 'q121429:q12', }
    search_form = '2'
    search_fields = { 'q121429:q6[]': '0', 'q121429:q14': 'ValidDate', }
    request_date_format = '%-d/%B/%Y'
    ref_field = 'appNo'
    next_page_link = 'Next'
    scrape_ids = """
    <div id="sectionContent"> <table> <tr />
    {* <tr>
    <td> <a href="{{ [records].url|abs }}">
    {{ [records].uid }} </a> </td>
    </tr> *}
    </table> </div>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = '<div id="sectionContent"> {{ block|html }} </div>'
    # the minimum acceptable valid dataset on the details page
    scrape_min_data = """
    <tr> <td> Application Number </td> <td> {{ reference }} </td> </tr>
    <tr> <td> Address </td> <td> {{ address }} </td> </tr>
    <tr> <td> Proposal </td> <td> {{ description }} </td> </tr>
    <tr> <th> Date Received </th> </tr> <tr> <td> {{ date_received }} </td> <td> {{ date_validated }} </td> </tr>
    """
    # other optional parameters common to all scrapers can appear on the details page
    scrape_optional_data = [
    '<tr> <td> Application Type </td> <td>  {{ application_type }} </td> </tr>',
    '<tr> <td> District </td> <td>  {{ district }} </td> </tr>',
    '<tr> <td> Parish </td> <td>  {{ parish }} </td> </tr>',
    '<tr> <td> Case Officer </td> <td>  {{ case_officer }} </td> </tr>',
    '<tr> <td> Grid Ref </td> <td>  {{ easting }} , {{ northing }} </td> </tr>', 
    '<tr> <td> Determined By </td> <td>  {{ decided_by }} </td> </tr>',
    '<tr> <td> Target Date For Decision </td> <td>  {{ target_decision_date }} </td> </tr>',
    '<tr> <th> Consultees Start </th> </tr> <tr> <td /> <td /> <td> {{ consultation_start_date }} </td> <td> {{ consultation_end_date }} </td> </tr>',
    '<tr> <th> Decision Date </th> </tr> <tr> <td /> <td /> <td /> <td /> <td> {{ decision_date }} </td> <td> {{ decision }} </td> </tr>',
    ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)

        # fix buggy option list
        html = response.get_data()
        html = html.replace('<option value="7">8</option>', '<option value="7">7</option> <option value="8">8</option>')
        if self.DEBUG: print html
        response.set_data(html)
        self.br.set_response(response)
        
        fields = self.search_fields
        date_from = date_from.strftime(self.request_date_format)
        date_parts = date_from.split('/')
        fields[self.date_from_field['day']] = [ date_parts[0] ]
        fields[self.date_from_field['month']] = [ date_parts[1] ]
        fields[self.date_from_field['year']] = [ date_parts[2] ]
        date_to = date_to.strftime(self.request_date_format)
        date_parts = date_to.split('/')
        fields[self.date_to_field['day']] = [ date_parts[0] ]
        fields[self.date_to_field['month']] = [ date_parts[1] ]
        fields[self.date_to_field['year']] = [ date_parts[2] ]
        
        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br)
        
        final_result = []
        while response:
            html = response.read()
            url = response.geturl()
            if self.DEBUG: print html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            else:
                break
            try:
                response = self.br.follow_link(text=self.next_page_link)
            except:
                break

        return final_result

    def get_detail_from_uid (self, uid):
        url = self.applic_url + '?' + self.ref_field + '=' + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

    # scrape detailed information on one record via its access URL
    def get_detail_from_url (self, url):
        try:
            response = self.br.open(url)
            html = response.read()
            html = html.replace('>1/1/1970<', '><') # kludge bad date fix
            url = response.geturl()
            if self.DEBUG:
                print "Html obtained from url:", html
        except:
            if self.DEBUG: raise
            else: return None
        return self.get_detail(html, url)

class ExmoorScraper(base.PeriodScraper):

    START_SEQUENCE = '2005-01-01' # gathers id data by working backwards from the current date towards this one
    MAX_ID_BATCH = 200 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 150 # max application details to scrape in one go
    PERIOD_TYPE = 'Friday'
    TABLE_NAME = 'Exmoor'

    next_page_link = 'Next'
    request_date_format = '%m/%d/%Y'
    search_url = 'http://www.exmoor-nationalpark.gov.uk/planning/planning-searches/application-weekly-list/application-search-results?weeklylist='
    applic_url = 'http://www.exmoor-nationalpark.gov.uk/planning/planning-searches/planning-applications/detailed-results?appNo='
    scrape_ids = """
    <table id="resultsTab"> <tr />
    {* <tr>
    <td> <a href="{{ [records].url|abs }}">
    {{ [records].uid }} </a> </td>
    </tr> *}
    </table>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="colMid"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on the details page
    scrape_min_data = """
    <tr> <td> Application No </td> <td> {{ reference }} </td> </tr>
    <tr> <td> Address </td> <td> {{ address }} </td> </tr>
    <tr> <td> Proposal </td> <td> {{ description }} </td> </tr>
    <tr> <th> Date Received </th> </tr> <tr> <td> {{ date_received }} </td> <td> {{ date_validated }} </td> </tr>
    """
    # other optional parameters common to all scrapers can appear on the details page
    scrape_optional_data = [
    '<tr> <td> Application Type </td> <td>  {{ application_type }} </td> </tr>',
    '<tr> <td> County </td> <td>  {{ district }} </td> </tr>',
    '<tr> <td> Parish </td> <td>  {{ parish }} </td> </tr>',
    '<tr> <td> Case Officer </td> <td>  {{ case_officer }} </td> </tr>',
    '<tr> <td> Grid Ref </td> <td> {{ easting }} , {{ northing }} </td> </tr>', 
    '<tr> <td> Status </td> <td>  {{ status }} </td> </tr>',
    '<tr> <td> Neighbours/public Consultees Start </td> <td>  {{ neighbour_consultation_start_date }} </td> </tr>',
    '<tr> <td> Neighbours/public Consultees End </td> <td>  {{ neighbour_consultation_end_date }} </td> </tr>',
    '<tr> <td> Site Notice Start </td> <td>  {{ site_notice_start_date }} </td> </tr>',
    '<tr> <td> Site Notice End </td> <td>  {{ site_notice_end_date }} </td> </tr>',
    '<tr> <th> Consultees Start </th> </tr> <tr> <td /> <td /> <td> {{ consultation_start_date }} </td> <td> {{ consultation_end_date }} </td> </tr>',
    """<tr> <th> Target Date </th> </tr> <tr> <td /> <td /> <td /> <td /> 
    <td> {{ target_decision_date }} </td> <td> {{ decision_date }} </td> <td> {{ decision }} </td> </tr>""",
    ]

    def get_id_period (self, date):

        from_iso_dt, to_iso_dt = util.inc_dt(date.strftime(util.ISO8601_DATE), util.ISO8601_DATE, self.PERIOD_TYPE)
        from_dt = util.get_dt(from_iso_dt, util.ISO8601_DATE)
        to_dt = util.get_dt(to_iso_dt, util.ISO8601_DATE)

        url = self.search_url + urllib.quote_plus (to_dt.strftime(self.request_date_format))
        if self.DEBUG: print url
        response = self.br.open(url)

        final_result = []
        while response:
            html = response.read()
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            else:
                break
            try:
                response = self.br.follow_link(text=self.next_page_link)
            except:
                break
        
        return final_result, from_dt, to_dt # weekly scraper - so empty result can be valid

    def get_detail_from_uid (self, uid):
        url = self.applic_url + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

class PeakDistrictScraper(base.PeriodScraper):

    MAX_ID_BATCH = 250 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go
    PERIOD_TYPE = 'Month'
    TABLE_NAME = 'PeakDistrict'

    request_date_format = '%m%y'
    search_url = 'http://pam.peakdistrict.gov.uk/'
    next_page_link = '>>'
    scrape_ids = """
    <h3>Search results</h3>
    <table> <tr> Page: </tr> <tr> Reference </tr>
    {* <tr>
    <td> <a href="{{ [records].url|abs }}">
    {{ [records].uid }} </a> </td>
    </tr> *}
    <tr> Page: </tr> </table>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="pamcontent"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <h2> Application Number {{ reference }} </h2>
    <h3> Proposal  {{ description }} </h3>
    <span> Development Address </span> {{ address }} <br>
    <span> Date Validated </span> {{ date_validated }} <br>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<span> Application Status </span> {{ status }} <br>',
    '<span> Parish </span> {{ parish }} <br>',
    '<span> Decision </span> {{ decision }} <br>',
    '<p> <span> Planning Officer </span> {{ case_officer }} </p>',
    '<span> Applicant Name </span> {{ applicant_name }} <br>',
    '<p> <span> Applicant Address </span> {{ applicant_address }} </p>',
    '<span> Agent Name </span> {{ agent_name }} <br>',
    '<p> <span> Agent Address </span> {{ agent_address }} </p>',
    '<span> Target Date for Decision </span> {{ target_decision_date }} <br>',
    '<p> <span> Decision Issued </span> {{ decision_date }} </p>',
    '<span> End of Public Consultation Period </span> {{ consultation_end_date }} <br>',
    ]

    def get_id_period (self, date):

        from_iso_dt, to_iso_dt = util.inc_dt(date.strftime(util.ISO8601_DATE), util.ISO8601_DATE, self.PERIOD_TYPE)
        from_dt = util.get_dt(from_iso_dt, util.ISO8601_DATE)
        to_dt = util.get_dt(to_iso_dt, util.ISO8601_DATE)

        monyear = date.strftime(self.request_date_format) # 4 digit MMYY string
        response = self.br.open(self.search_url + '?q=' + monyear)

        final_result = []
        while response:
            html = response.read()
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                new_result = []
                for rec in result['records']:
                    if '/' + monyear + '/' in rec['uid']: # filter out records where the search term does not appear in the correct part of the uid
                        new_result.append(rec)
                self.clean_ids(new_result)
                final_result.extend(new_result)
            else:
                break
            try:
                response = self.br.follow_link(text=self.next_page_link)
            except:
                break
        
        if final_result:
            return final_result, from_dt, to_dt
        else:
            return [], None, None # monthly scraper - so empty result is always invalid

    def get_detail_from_uid (self, uid):
        url = self.search_url + '?r='+ urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

# note uses the record sequence, with records notionally numbered from 1 (oldest) to max_sequence (most recent)
class PembrokeshireCoastScraper(base.ListScraper):

    START_SEQUENCE = 6500 # gathering back to this record number (around year 2000)
    MAX_ID_BATCH = 250 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 150 # max application details to scrape in one go
    PAGE_SIZE = 20
    START_POINT = 15200
    TABLE_NAME = 'PembrokeshireCoast'

    search_url = 'http://www.pembrokeshirecoast.org.uk/default.asp?PID=243'
    applic_url = 'http://www.pembrokeshirecoast.org.uk/default.asp?PID=243&APASID='
    scrape_ids = """
    <table> <tr />
    {* <tr /> <tr>
    <td> <a href="{{ [records].url|abs }}">
    {{ [records].uid }} </a> </td>
    </tr> *}
    </table>
    """
    scrape_max_recs = "<tr> 1 to 20 of {{ max_recs }} <a /> </tr>"
    scrape_data_block = """
    <div id="page_content"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <tr> <td> Application </td> <td /> <td> {{ reference }} - received on {{ date_received }} </td> </tr>
    <tr> <td> Proposal </td> <td /> <td> {{ description }} </td> </tr>
    <tr> <td> Location </td> <td /> <td> {{ address|html }} </td> </tr>
    <tr> <td> Registered Date </td> <td /> <td> {{ date_validated }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr> <td> Applicant </td> <td /> <td> {{ applicant_name|html }} </td> </tr>',
    '<tr> <td> Agent </td> <td /> <td> {{ agent_name|html }} </td> </tr>',
    '<tr> <td> Case Officer </td> <td /> <td> {{ case_officer }} </td> </tr>',
    '<tr> <td> Current Stage </td> <td /> <td> {{ status }} </td> </tr>',
    '<tr> <td> 8 Week Date </td> <td /> <td> {{ application_expires_date }} </td> </tr>',
    '<tr> <td> Level Of Decision </td> <td /> <td> {{ decided_by }} </td> </tr> <tr> <td> Decision </td> <td /> <td> {{ decision }} </td> </tr>',
    ]

    # Note records are listed using an 'offset' parameter where our notional record number = max_recs - offset
    # NB if both are None, it's the first ever scrape
    # NB if rec_to is None, rec_from is the highest existing record and it's a current scrape
    # NB also if rec_to is None, the default should be to try to get at least self.MIN_RECS records
    def get_id_records (self, rec_from, rec_to = None):
        final_result = []
        num_from = None
        num_to = None

        response = util.open_url(self.br, self.search_url)
        html = response.read()
        try:
            result = scrapemark.scrape(self.scrape_max_recs, html)
            num_recs = int(result['max_recs'])
        except:
            num_recs = 0
        
        if not rec_from and not rec_to:
            rec_from = self.START_SEQUENCE
            rec_to = num_recs
        elif not rec_to:
            rec_to = num_recs # set target to highest recent record
            rec_from -= self.MIN_RECS

        if rec_to > num_recs:
            rec_to = num_recs

        if self.DEBUG: print 'Looking for records: ', rec_from, rec_to
        
        current_rec = rec_to
        top_rec = None
        bot_rec = None
        while current_rec >= rec_from and len(final_result) < self.MAX_ID_BATCH:
            offset = num_recs - current_rec
            if self.DEBUG: print "Offset:", offset
            url = self.search_url + '&offset=' + str(offset)
            response = util.open_url(self.br, url)
            if response:
                html = response.read()
                url = response.geturl()
                result = scrapemark.scrape(self.scrape_ids, html, url)
                if result and result.get('records'):
                    if not top_rec: top_rec = current_rec
                    bot_rec = current_rec - len(result['records']) + 1
                    if self.DEBUG: print result
                    self.clean_ids(result['records'])
                    final_result.extend(result['records'])
                    if self.DEBUG: print 'Output N: ', len(final_result)
                    current_rec = bot_rec - 1
                else:
                    break
            else:
                break
                
        if final_result:
            if self.DEBUG: print bot_rec, top_rec
            num_from = bot_rec
            num_to = top_rec
        return final_result, num_from, num_to

    # NB if move_forward is true, we scrape forwards from rec_start, otherwise we scrape backwards
    def get_id_records2 (self, rec_start, move_forward):
        final_result = []
        num_from = None
        num_to = None
        bad_count = 0
        current_rec = rec_start
        num_recs = self.get_max_sequence()
        fields = {}
        first_good_rec = None
        last_good_rec = None
        offset = int((num_recs - current_rec) / 20) * 20 # whole page of 20 records only
        while len(final_result) < self.MAX_ID_BATCH and offset >= 0:
            url = self.search_url + '&offset=' + str(offset)
            response = util.open_url(self.br, url)
            if self.DEBUG: print 'Offset:', offset
            if response:
                html = response.read()
                url = response.geturl()
                if self.DEBUG: print 'Html:', html
                result = scrapemark.scrape(self.scrape_ids, html, url)
                if result and result.get('records'):
                    if not first_good_rec: 
                        if move_forward: first_good_rec = num_recs - (offset + 19)
                        else: first_good_rec = num_recs - offset 
                    if move_forward: last_good_rec = num_recs - offset
                    else: last_good_rec = num_recs - (offset + 19)
                    if self.DEBUG: print first_good_rec, last_good_rec
                    if self.DEBUG: print result
                    final_result.extend(result['records'])
                else:
                    break
            else:
                break
            if move_forward:
                offset -= 20
            else:
                offset += 20
        if final_result:
            self.clean_ids(final_result)
            if move_forward:
                num_from = first_good_rec
                num_to = last_good_rec
            else:
                num_to = first_good_rec
                num_from = last_good_rec
        return final_result, num_from, num_to
    
    def get_max_sequence (self):
        max_recs = scraperwiki.sqlite.get_var(self.DATA_END_MARKER)
        response = util.open_url(self.br, self.search_url)
        html = response.read()
        try:
            result = scrapemark.scrape(self.scrape_max_recs, html)
            num_recs = int(result['max_recs'])
        except:
            num_recs = 0
        if num_recs > 0:
            max_recs = num_recs
        return max_recs

    def get_detail_from_uid (self, uid):
        url = self.applic_url + urllib.quote_plus(uid)
        result = self.get_detail_from_url(url)
        if result or uid.startswith('NP/'):
            return result
        else:
            url = self.applic_url + urllib.quote_plus('NP/' + uid)
            return self.get_detail_from_url(url)

if __name__ == 'scraper':

    #scraper = PembrokeshireCoastScraper()
    #scraper.DEBUG = True
    #scraper.MAX_ID_BATCH = 30
    #print scraper.get_id_records2(scraper.get_max_sequence()-20, True)
    #scraper.run()
    #sys.exit()

    sys_list = []
    for k, v in systems.items(): # get latest date scraped for each system
        sys_list.append( (k, v, scraperwiki.sqlite.get_var('latest-' + k)) )
    sort_sys = sorted(sys_list, key=lambda system: system[2]) # sort so least recent are first
    for auth in sort_sys[:4]: # do max 4 per run
        strexec = auth[1] + "('" + auth[0] + "')"
        print "Scraping from:", strexec
        try:
            scraper = eval(strexec)
            scraper.run()
        except Exception as err:
            print "Error - skipping this authority -", str(err)
    print "Finished"

    # misc test calls
    #scraper = NorthumberlandParkScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11NP0040EL') # NorthumberlandPark OK
    #scraper = YorkshireDalesScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('C/33/192J') # YorkshireDales OK
    #scraper = SedgefieldScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('7/2011/0334/DM') # Sedgefield
    
    #res = scraper.get_id_batch(util.get_dt('01/09/2012'), util.get_dt('29/09/2012'))
    #print res, len(res)

    #scraper = ExmoorScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('6/27/11/132') # Exmoor OK
    #scraper = PeakDistrictScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('NP/DDD/0912/0879') # PeakDistrict OK

    #res, dt1, dt2 = scraper.get_id_period(util.get_dt('12/09/2012')) 
    #print res, len(res), dt1, dt2

    #scraper = PembrokeshireCoastScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('12/0469') # PembrokeshireCoast

    #result, nfrom, nto = scraper.get_id_records(14984, 15004)
    #result, nfrom, nto = scraper.get_id_records(15000)
    #print result, len(result), nfrom, nto


# this is a scraper of 5 National Park planning authorities with customised systems

# there are another 10 National Parks which use standard planning systems (implemented elsewhere)

# planning applications from all 15 National Parks are collected in the cross_boundary_planning_aggregator

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import random
import urllib
import urlparse
import sys
import copy

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

systems = {
    'PembrokeshireCoast': 'PembrokeshireCoastScraper', 
    'PeakDistrict': 'PeakDistrictScraper', 
    'Exmoor': 'ExmoorScraper',
    'NorthumberlandPark': 'NorthumberlandParkScraper',
    'YorkshireDales': 'YorkshireDalesScraper',
     }

class NorthumberlandParkScraper(base.DateScraper): 

    MAX_ID_BATCH = 150 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 100 # max application details to scrape in one go
    BATCH_DAYS = 28 # batch size for each scrape - number of days to gather to produce at least one result each time
    MIN_DAYS = 28 # min number of days to get when gathering current ids
    TABLE_NAME = 'NorthumberlandPark'

    search_url = 'http://nnpa.planning-register.co.uk/PlaPlanningAppAdvSearch.aspx?mode=reset'
    applic_url = 'http://nnpa.planning-register.co.uk/plaPlanningAppDisplay.aspx?AppNo='
    date_from_field = 'ctl00_ContentPlaceHolder1_txtAppValFrom_dateInput_ClientState'
    date_to_field = 'ctl00_ContentPlaceHolder1_txtAppValTo_dateInput_ClientState'
    search_fields = { '__EVENTTARGET': '', '__EVENTARGUMENT': '', }
    search_form = '1'
    request_date_format = '{"enabled":true,"emptyMessage":"","validationText":"%Y-%m-%d-00-00-00","valueAsString":"%Y-%m-%d-00-00-00","minDateStr":"01/01/1900","maxDateStr":"12/31/2099"}'
    scrape_next_submit = '<input class="rgPageNext" name="{{ next_submit }}">'
    scrape_max_recs = '<div class="rgWrap rgInfoPart"> <strong> {{ max_recs }} </strong> items </div>'
    scrape_ids = """
    <h2>Search Results</h2> <table> <tbody>
    {* <tr>
    <td> <a href="{{ [records].url|abs }}">
    {{ [records].uid }} </a> </td>
    </tr> *}
    </tbody> </table>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = '<div id="contentbody"> {{ block|html }} </div>'
    # the minimum acceptable valid dataset on the details page
    scrape_min_data = """
    <input id="ContentPlaceHolder1_txtAppNum" value="{{ reference }}">
    <textarea id="ContentPlaceHolder1_txtLoc"> {{ address }} </textarea>
    <textarea id="ContentPlaceHolder1_txtProposal"> {{ description }} </textarea>
    <input id="ContentPlaceHolder1_txtRecDate" value="{{ date_received }}">
    <input id="ContentPlaceHolder1_txtValidDate" value="{{ date_validated }}">
    """
    # other optional parameters common to all scrapers can appear on the details page
    scrape_optional_data = [
    '<input id="ContentPlaceHolder1_txtDistrict" value="{{ district }}">',
    '<input id="ContentPlaceHolder1_txtWard" value="{{ ward_name }}">',
    '<input id="ContentPlaceHolder1_Label4" value="{{ parish }}">',
    '<input id="ContentPlaceHolder1_txtEasting" value="{{ easting }}">',
    '<input id="ContentPlaceHolder1_txtNorthing" value="{{ northing }}">',
    '<input id="ContentPlaceHolder1_txtAppStatus" value="{{ status }}">',
    '<input id="ContentPlaceHolder1_txtAppName" value="{{ applicant_name }}">',
    '<input id="ContentPlaceHolder1_txtAgName" value="{{ agent_name }}">',
    '<textarea id="ContentPlaceHolder1_txtAppAddress"> {{ applicant_address }} </textarea>',
    '<textarea id="ContentPlaceHolder1_txtAgAddress"> {{ agent_address }} </textarea>',
    '<input id="ContentPlaceHolder1_txtDecDate" value="{{ decision_date }}">',
    '<input id="ContentPlaceHolder1_txtDec" value="{{ decision }}">',
    '<input id="ContentPlaceHolder1_txtAplDate" value="{{ appeal_date }}">',
    '<input id="ContentPlaceHolder1_txtAplDec" value="{{ appeal_result }}">',
    '<input id="ContentPlaceHolder1_txtPlanOff" value="{{ case_officer }}">',
    ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)

        fields = copy.copy(self.search_fields) 
        fields[self.date_from_field] = date_from.strftime(self.request_date_format)
        fields[self.date_to_field] = date_to.strftime(self.request_date_format)
        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br)

        # note max_recs does not appear if there is only one page
        try:
            html = response.read()
            result = scrapemark.scrape(self.scrape_max_recs, html)
            num_recs = int(result['max_recs'])
        except:
            num_recs = 0
        
        final_result = []
        while response and (len(final_result) < num_recs or num_recs == 0):
            url = response.geturl()
            if self.DEBUG: print html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            else:
                break
            if len(final_result) >= num_recs or num_recs == 0: break
            try:
                result = scrapemark.scrape(self.scrape_next_submit, html)
                fields = copy.copy(self.search_fields) 
                util.setup_form(self.br, self.search_form, fields)
                if self.DEBUG: print self.br.form
                response = util.submit_form(self.br, result['next_submit'])
                html = response.read()
            except:
                break

        return final_result

    def get_detail_from_uid (self, uid):
        url = self.applic_url + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

class YorkshireDalesScraper(base.DateScraper):

    START_SEQUENCE = '2000-02-01' # gathers id data by working backwards from the current date towards this one
    MAX_ID_BATCH = 150 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 100 # max application details to scrape in one go
    MIN_DAYS = 28 # min number of days to get when gathering current ids
    TABLE_NAME = 'YorkshireDales'

    search_url = 'http://www.yorkshiredales.org.uk/planning/planningapplications/planning-applications'
    applic_url = 'http://www.yorkshiredales.org.uk/planning/planningapplications/planning-applications/detailed-results'
    date_from_field = { 'day': 'q121429:q7', 'month': 'q121429:q8', 'year': 'q121429:q9', }
    date_to_field = { 'day': 'q121429:q10', 'month': 'q121429:q11', 'year': 'q121429:q12', }
    search_form = '2'
    search_fields = { 'q121429:q6[]': '0', 'q121429:q14': 'ValidDate', }
    request_date_format = '%-d/%B/%Y'
    ref_field = 'appNo'
    next_page_link = 'Next'
    scrape_ids = """
    <div id="sectionContent"> <table> <tr />
    {* <tr>
    <td> <a href="{{ [records].url|abs }}">
    {{ [records].uid }} </a> </td>
    </tr> *}
    </table> </div>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = '<div id="sectionContent"> {{ block|html }} </div>'
    # the minimum acceptable valid dataset on the details page
    scrape_min_data = """
    <tr> <td> Application Number </td> <td> {{ reference }} </td> </tr>
    <tr> <td> Address </td> <td> {{ address }} </td> </tr>
    <tr> <td> Proposal </td> <td> {{ description }} </td> </tr>
    <tr> <th> Date Received </th> </tr> <tr> <td> {{ date_received }} </td> <td> {{ date_validated }} </td> </tr>
    """
    # other optional parameters common to all scrapers can appear on the details page
    scrape_optional_data = [
    '<tr> <td> Application Type </td> <td>  {{ application_type }} </td> </tr>',
    '<tr> <td> District </td> <td>  {{ district }} </td> </tr>',
    '<tr> <td> Parish </td> <td>  {{ parish }} </td> </tr>',
    '<tr> <td> Case Officer </td> <td>  {{ case_officer }} </td> </tr>',
    '<tr> <td> Grid Ref </td> <td>  {{ easting }} , {{ northing }} </td> </tr>', 
    '<tr> <td> Determined By </td> <td>  {{ decided_by }} </td> </tr>',
    '<tr> <td> Target Date For Decision </td> <td>  {{ target_decision_date }} </td> </tr>',
    '<tr> <th> Consultees Start </th> </tr> <tr> <td /> <td /> <td> {{ consultation_start_date }} </td> <td> {{ consultation_end_date }} </td> </tr>',
    '<tr> <th> Decision Date </th> </tr> <tr> <td /> <td /> <td /> <td /> <td> {{ decision_date }} </td> <td> {{ decision }} </td> </tr>',
    ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)

        # fix buggy option list
        html = response.get_data()
        html = html.replace('<option value="7">8</option>', '<option value="7">7</option> <option value="8">8</option>')
        if self.DEBUG: print html
        response.set_data(html)
        self.br.set_response(response)
        
        fields = self.search_fields
        date_from = date_from.strftime(self.request_date_format)
        date_parts = date_from.split('/')
        fields[self.date_from_field['day']] = [ date_parts[0] ]
        fields[self.date_from_field['month']] = [ date_parts[1] ]
        fields[self.date_from_field['year']] = [ date_parts[2] ]
        date_to = date_to.strftime(self.request_date_format)
        date_parts = date_to.split('/')
        fields[self.date_to_field['day']] = [ date_parts[0] ]
        fields[self.date_to_field['month']] = [ date_parts[1] ]
        fields[self.date_to_field['year']] = [ date_parts[2] ]
        
        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br)
        
        final_result = []
        while response:
            html = response.read()
            url = response.geturl()
            if self.DEBUG: print html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            else:
                break
            try:
                response = self.br.follow_link(text=self.next_page_link)
            except:
                break

        return final_result

    def get_detail_from_uid (self, uid):
        url = self.applic_url + '?' + self.ref_field + '=' + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

    # scrape detailed information on one record via its access URL
    def get_detail_from_url (self, url):
        try:
            response = self.br.open(url)
            html = response.read()
            html = html.replace('>1/1/1970<', '><') # kludge bad date fix
            url = response.geturl()
            if self.DEBUG:
                print "Html obtained from url:", html
        except:
            if self.DEBUG: raise
            else: return None
        return self.get_detail(html, url)

class ExmoorScraper(base.PeriodScraper):

    START_SEQUENCE = '2005-01-01' # gathers id data by working backwards from the current date towards this one
    MAX_ID_BATCH = 200 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 150 # max application details to scrape in one go
    PERIOD_TYPE = 'Friday'
    TABLE_NAME = 'Exmoor'

    next_page_link = 'Next'
    request_date_format = '%m/%d/%Y'
    search_url = 'http://www.exmoor-nationalpark.gov.uk/planning/planning-searches/application-weekly-list/application-search-results?weeklylist='
    applic_url = 'http://www.exmoor-nationalpark.gov.uk/planning/planning-searches/planning-applications/detailed-results?appNo='
    scrape_ids = """
    <table id="resultsTab"> <tr />
    {* <tr>
    <td> <a href="{{ [records].url|abs }}">
    {{ [records].uid }} </a> </td>
    </tr> *}
    </table>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="colMid"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on the details page
    scrape_min_data = """
    <tr> <td> Application No </td> <td> {{ reference }} </td> </tr>
    <tr> <td> Address </td> <td> {{ address }} </td> </tr>
    <tr> <td> Proposal </td> <td> {{ description }} </td> </tr>
    <tr> <th> Date Received </th> </tr> <tr> <td> {{ date_received }} </td> <td> {{ date_validated }} </td> </tr>
    """
    # other optional parameters common to all scrapers can appear on the details page
    scrape_optional_data = [
    '<tr> <td> Application Type </td> <td>  {{ application_type }} </td> </tr>',
    '<tr> <td> County </td> <td>  {{ district }} </td> </tr>',
    '<tr> <td> Parish </td> <td>  {{ parish }} </td> </tr>',
    '<tr> <td> Case Officer </td> <td>  {{ case_officer }} </td> </tr>',
    '<tr> <td> Grid Ref </td> <td> {{ easting }} , {{ northing }} </td> </tr>', 
    '<tr> <td> Status </td> <td>  {{ status }} </td> </tr>',
    '<tr> <td> Neighbours/public Consultees Start </td> <td>  {{ neighbour_consultation_start_date }} </td> </tr>',
    '<tr> <td> Neighbours/public Consultees End </td> <td>  {{ neighbour_consultation_end_date }} </td> </tr>',
    '<tr> <td> Site Notice Start </td> <td>  {{ site_notice_start_date }} </td> </tr>',
    '<tr> <td> Site Notice End </td> <td>  {{ site_notice_end_date }} </td> </tr>',
    '<tr> <th> Consultees Start </th> </tr> <tr> <td /> <td /> <td> {{ consultation_start_date }} </td> <td> {{ consultation_end_date }} </td> </tr>',
    """<tr> <th> Target Date </th> </tr> <tr> <td /> <td /> <td /> <td /> 
    <td> {{ target_decision_date }} </td> <td> {{ decision_date }} </td> <td> {{ decision }} </td> </tr>""",
    ]

    def get_id_period (self, date):

        from_iso_dt, to_iso_dt = util.inc_dt(date.strftime(util.ISO8601_DATE), util.ISO8601_DATE, self.PERIOD_TYPE)
        from_dt = util.get_dt(from_iso_dt, util.ISO8601_DATE)
        to_dt = util.get_dt(to_iso_dt, util.ISO8601_DATE)

        url = self.search_url + urllib.quote_plus (to_dt.strftime(self.request_date_format))
        if self.DEBUG: print url
        response = self.br.open(url)

        final_result = []
        while response:
            html = response.read()
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            else:
                break
            try:
                response = self.br.follow_link(text=self.next_page_link)
            except:
                break
        
        return final_result, from_dt, to_dt # weekly scraper - so empty result can be valid

    def get_detail_from_uid (self, uid):
        url = self.applic_url + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

class PeakDistrictScraper(base.PeriodScraper):

    MAX_ID_BATCH = 250 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go
    PERIOD_TYPE = 'Month'
    TABLE_NAME = 'PeakDistrict'

    request_date_format = '%m%y'
    search_url = 'http://pam.peakdistrict.gov.uk/'
    next_page_link = '>>'
    scrape_ids = """
    <h3>Search results</h3>
    <table> <tr> Page: </tr> <tr> Reference </tr>
    {* <tr>
    <td> <a href="{{ [records].url|abs }}">
    {{ [records].uid }} </a> </td>
    </tr> *}
    <tr> Page: </tr> </table>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="pamcontent"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <h2> Application Number {{ reference }} </h2>
    <h3> Proposal  {{ description }} </h3>
    <span> Development Address </span> {{ address }} <br>
    <span> Date Validated </span> {{ date_validated }} <br>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<span> Application Status </span> {{ status }} <br>',
    '<span> Parish </span> {{ parish }} <br>',
    '<span> Decision </span> {{ decision }} <br>',
    '<p> <span> Planning Officer </span> {{ case_officer }} </p>',
    '<span> Applicant Name </span> {{ applicant_name }} <br>',
    '<p> <span> Applicant Address </span> {{ applicant_address }} </p>',
    '<span> Agent Name </span> {{ agent_name }} <br>',
    '<p> <span> Agent Address </span> {{ agent_address }} </p>',
    '<span> Target Date for Decision </span> {{ target_decision_date }} <br>',
    '<p> <span> Decision Issued </span> {{ decision_date }} </p>',
    '<span> End of Public Consultation Period </span> {{ consultation_end_date }} <br>',
    ]

    def get_id_period (self, date):

        from_iso_dt, to_iso_dt = util.inc_dt(date.strftime(util.ISO8601_DATE), util.ISO8601_DATE, self.PERIOD_TYPE)
        from_dt = util.get_dt(from_iso_dt, util.ISO8601_DATE)
        to_dt = util.get_dt(to_iso_dt, util.ISO8601_DATE)

        monyear = date.strftime(self.request_date_format) # 4 digit MMYY string
        response = self.br.open(self.search_url + '?q=' + monyear)

        final_result = []
        while response:
            html = response.read()
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                new_result = []
                for rec in result['records']:
                    if '/' + monyear + '/' in rec['uid']: # filter out records where the search term does not appear in the correct part of the uid
                        new_result.append(rec)
                self.clean_ids(new_result)
                final_result.extend(new_result)
            else:
                break
            try:
                response = self.br.follow_link(text=self.next_page_link)
            except:
                break
        
        if final_result:
            return final_result, from_dt, to_dt
        else:
            return [], None, None # monthly scraper - so empty result is always invalid

    def get_detail_from_uid (self, uid):
        url = self.search_url + '?r='+ urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

# note uses the record sequence, with records notionally numbered from 1 (oldest) to max_sequence (most recent)
class PembrokeshireCoastScraper(base.ListScraper):

    START_SEQUENCE = 6500 # gathering back to this record number (around year 2000)
    MAX_ID_BATCH = 250 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 150 # max application details to scrape in one go
    PAGE_SIZE = 20
    START_POINT = 15200
    TABLE_NAME = 'PembrokeshireCoast'

    search_url = 'http://www.pembrokeshirecoast.org.uk/default.asp?PID=243'
    applic_url = 'http://www.pembrokeshirecoast.org.uk/default.asp?PID=243&APASID='
    scrape_ids = """
    <table> <tr />
    {* <tr /> <tr>
    <td> <a href="{{ [records].url|abs }}">
    {{ [records].uid }} </a> </td>
    </tr> *}
    </table>
    """
    scrape_max_recs = "<tr> 1 to 20 of {{ max_recs }} <a /> </tr>"
    scrape_data_block = """
    <div id="page_content"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <tr> <td> Application </td> <td /> <td> {{ reference }} - received on {{ date_received }} </td> </tr>
    <tr> <td> Proposal </td> <td /> <td> {{ description }} </td> </tr>
    <tr> <td> Location </td> <td /> <td> {{ address|html }} </td> </tr>
    <tr> <td> Registered Date </td> <td /> <td> {{ date_validated }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr> <td> Applicant </td> <td /> <td> {{ applicant_name|html }} </td> </tr>',
    '<tr> <td> Agent </td> <td /> <td> {{ agent_name|html }} </td> </tr>',
    '<tr> <td> Case Officer </td> <td /> <td> {{ case_officer }} </td> </tr>',
    '<tr> <td> Current Stage </td> <td /> <td> {{ status }} </td> </tr>',
    '<tr> <td> 8 Week Date </td> <td /> <td> {{ application_expires_date }} </td> </tr>',
    '<tr> <td> Level Of Decision </td> <td /> <td> {{ decided_by }} </td> </tr> <tr> <td> Decision </td> <td /> <td> {{ decision }} </td> </tr>',
    ]

    # Note records are listed using an 'offset' parameter where our notional record number = max_recs - offset
    # NB if both are None, it's the first ever scrape
    # NB if rec_to is None, rec_from is the highest existing record and it's a current scrape
    # NB also if rec_to is None, the default should be to try to get at least self.MIN_RECS records
    def get_id_records (self, rec_from, rec_to = None):
        final_result = []
        num_from = None
        num_to = None

        response = util.open_url(self.br, self.search_url)
        html = response.read()
        try:
            result = scrapemark.scrape(self.scrape_max_recs, html)
            num_recs = int(result['max_recs'])
        except:
            num_recs = 0
        
        if not rec_from and not rec_to:
            rec_from = self.START_SEQUENCE
            rec_to = num_recs
        elif not rec_to:
            rec_to = num_recs # set target to highest recent record
            rec_from -= self.MIN_RECS

        if rec_to > num_recs:
            rec_to = num_recs

        if self.DEBUG: print 'Looking for records: ', rec_from, rec_to
        
        current_rec = rec_to
        top_rec = None
        bot_rec = None
        while current_rec >= rec_from and len(final_result) < self.MAX_ID_BATCH:
            offset = num_recs - current_rec
            if self.DEBUG: print "Offset:", offset
            url = self.search_url + '&offset=' + str(offset)
            response = util.open_url(self.br, url)
            if response:
                html = response.read()
                url = response.geturl()
                result = scrapemark.scrape(self.scrape_ids, html, url)
                if result and result.get('records'):
                    if not top_rec: top_rec = current_rec
                    bot_rec = current_rec - len(result['records']) + 1
                    if self.DEBUG: print result
                    self.clean_ids(result['records'])
                    final_result.extend(result['records'])
                    if self.DEBUG: print 'Output N: ', len(final_result)
                    current_rec = bot_rec - 1
                else:
                    break
            else:
                break
                
        if final_result:
            if self.DEBUG: print bot_rec, top_rec
            num_from = bot_rec
            num_to = top_rec
        return final_result, num_from, num_to

    # NB if move_forward is true, we scrape forwards from rec_start, otherwise we scrape backwards
    def get_id_records2 (self, rec_start, move_forward):
        final_result = []
        num_from = None
        num_to = None
        bad_count = 0
        current_rec = rec_start
        num_recs = self.get_max_sequence()
        fields = {}
        first_good_rec = None
        last_good_rec = None
        offset = int((num_recs - current_rec) / 20) * 20 # whole page of 20 records only
        while len(final_result) < self.MAX_ID_BATCH and offset >= 0:
            url = self.search_url + '&offset=' + str(offset)
            response = util.open_url(self.br, url)
            if self.DEBUG: print 'Offset:', offset
            if response:
                html = response.read()
                url = response.geturl()
                if self.DEBUG: print 'Html:', html
                result = scrapemark.scrape(self.scrape_ids, html, url)
                if result and result.get('records'):
                    if not first_good_rec: 
                        if move_forward: first_good_rec = num_recs - (offset + 19)
                        else: first_good_rec = num_recs - offset 
                    if move_forward: last_good_rec = num_recs - offset
                    else: last_good_rec = num_recs - (offset + 19)
                    if self.DEBUG: print first_good_rec, last_good_rec
                    if self.DEBUG: print result
                    final_result.extend(result['records'])
                else:
                    break
            else:
                break
            if move_forward:
                offset -= 20
            else:
                offset += 20
        if final_result:
            self.clean_ids(final_result)
            if move_forward:
                num_from = first_good_rec
                num_to = last_good_rec
            else:
                num_to = first_good_rec
                num_from = last_good_rec
        return final_result, num_from, num_to
    
    def get_max_sequence (self):
        max_recs = scraperwiki.sqlite.get_var(self.DATA_END_MARKER)
        response = util.open_url(self.br, self.search_url)
        html = response.read()
        try:
            result = scrapemark.scrape(self.scrape_max_recs, html)
            num_recs = int(result['max_recs'])
        except:
            num_recs = 0
        if num_recs > 0:
            max_recs = num_recs
        return max_recs

    def get_detail_from_uid (self, uid):
        url = self.applic_url + urllib.quote_plus(uid)
        result = self.get_detail_from_url(url)
        if result or uid.startswith('NP/'):
            return result
        else:
            url = self.applic_url + urllib.quote_plus('NP/' + uid)
            return self.get_detail_from_url(url)

if __name__ == 'scraper':

    #scraper = PembrokeshireCoastScraper()
    #scraper.DEBUG = True
    #scraper.MAX_ID_BATCH = 30
    #print scraper.get_id_records2(scraper.get_max_sequence()-20, True)
    #scraper.run()
    #sys.exit()

    sys_list = []
    for k, v in systems.items(): # get latest date scraped for each system
        sys_list.append( (k, v, scraperwiki.sqlite.get_var('latest-' + k)) )
    sort_sys = sorted(sys_list, key=lambda system: system[2]) # sort so least recent are first
    for auth in sort_sys[:4]: # do max 4 per run
        strexec = auth[1] + "('" + auth[0] + "')"
        print "Scraping from:", strexec
        try:
            scraper = eval(strexec)
            scraper.run()
        except Exception as err:
            print "Error - skipping this authority -", str(err)
    print "Finished"

    # misc test calls
    #scraper = NorthumberlandParkScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11NP0040EL') # NorthumberlandPark OK
    #scraper = YorkshireDalesScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('C/33/192J') # YorkshireDales OK
    #scraper = SedgefieldScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('7/2011/0334/DM') # Sedgefield
    
    #res = scraper.get_id_batch(util.get_dt('01/09/2012'), util.get_dt('29/09/2012'))
    #print res, len(res)

    #scraper = ExmoorScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('6/27/11/132') # Exmoor OK
    #scraper = PeakDistrictScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('NP/DDD/0912/0879') # PeakDistrict OK

    #res, dt1, dt2 = scraper.get_id_period(util.get_dt('12/09/2012')) 
    #print res, len(res), dt1, dt2

    #scraper = PembrokeshireCoastScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('12/0469') # PembrokeshireCoast

    #result, nfrom, nto = scraper.get_id_records(14984, 15004)
    #result, nfrom, nto = scraper.get_id_records(15000)
    #print result, len(result), nfrom, nto


