# this is a scraper of Ashford planning applications for use by Openly Local

# date query results filled out using JQuery/AJAX - not accessible?

# so works from the sequence of systemkey record numbers 

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import urllib
import sys

base = scraperwiki.utils.swimport("openlylocal_base_scraper")
scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")

class AshfordScraper(base.ListScraper):

    START_SEQUENCE = 50000 # gathering back to this record number
    START_POINT = 95000 # default starting point, if there is no other information ie database is empty
    MAX_ID_BATCH = 200 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 150 # max application details to scrape in one go
    ID_ORDER = "uid desc"
    MIN_RECS = 70

    ck = { 'name': 'ABCPLANNINGTERMS', 'value': '22 Feb 2017 08:21:18 AM', 'domain': 'planning.ashford.gov.uk', 'path': '/' }

    """date_from_field = 'ctl00$CPH_Details$Details_TabContainer$Date_Tab$searchby_date1$StartDate$myCalendar'
    date_to_field = 'ctl00$CPH_Details$Details_TabContainer$Date_Tab$searchby_date1$EndDate$myCalendar'
    from_prev = 'ctl00$CPH_Details$Details_TabContainer$Date_Tab$searchby_date1$StartDate$LB_Prev'
    to_prev = 'ctl00$CPH_Details$Details_TabContainer$Date_Tab$searchby_date1$EndDate$LB_Prev'
    uid_year = 'ctl00$CPH_Details$Details_TabContainer$CaseNo_Tab$searchby_caseNo1$CaseYear'
    search_form = '0'
    fields = { '__EVENTTARGET': '', '__EVENTARGUMENT': '' }
    search_fields = { '__EVENTTARGET': '', '__EVENTARGUMENT': '', 'ctl00$CPH_Details$Details_TabContainer$Date_Tab$searchby_date1$DateSearchBy': 'Registration Date' }
    next_link = 'Next >'
    submit_control = 'ctl00$CPH_Details$Details_TabContainer$Date_Tab$searchby_date1$Search_Button'
    start_url = 'http://planning.ashford.gov.uk/planning/Default.aspx?new=true'"""

    applic_url = 'http://planning.ashford.gov.uk/Planning/details.aspx?pageindex=0'
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="contents"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    # note overwrites uid to correct value
    scrape_min_data = """
    <th> Application Ref </th> <td> {{ uid }} </td>
    <th> Site Address </th> <td> {{ address }} </td>
    <th> Description </th> <td> {{ description }} </td>
    <th> Date Received </th> <td> {{ date_received }} </td>
    <th> Date Registered </th> <td> {{ date_validated }} </td>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<th> Application Ref </th> <td> {{ reference }} </td>',
    '<th> Application Type </th> <td> {{ application_type }} </td>',
    '<th> Status </th> <td> {{ status }} </td>',
    '<th> Council Decision </th> <td> {{ decision }} </td>',
    '<th> Ward </th> <td> {{ ward_name }} </td>',
    '<th> Parish </th> <td> {{ parish }} </td>',
    '<th> Officer Name </th> <td> {{ case_officer }} </td>',
    '<th> Applicant </th> <td> {{ applicant_address }} </td>',
    '<th> Agent </th> <td> {{ agent_address }} </td>',
    '<th> Grid Reference </th> <td> {{ easting }} / {{ northing }} </td>',
    """<th> Target Decision Date </th> <td> {{ target_decision_date }} </td>
    <th> Decision Date </th> <td> {{ decision_date }} </td>""",
    '<th> Committee Date </th> <td> {{ meeting_date }} </td>',
    '<th> Comments By </th> <td> {{ comment_date }} </td>',
    '<th> Start of Consultation </th> <td> {{ consultation_start_date }} </td>',
    '<th> End of Consultation </th> <td> {{ consultation_end_date }} </td>',
    '<th> Decision Level </th> <td> {{ decided_by }} </td>',
    ]

    def __init__(self, table_name = None):
        base.ListScraper.__init__(self, table_name)
        if self.ck:
            util.set_cookie(self.cj, self.ck['name'], self.ck['value'], self.ck.get('domain'), self.ck.get('path', '/'))   

    """def get_id_batch (self, date_from, date_to):

        response = util.open_url(self.br, self.start_url)
        if self.DEBUG: print "start page:", response.read()

        origin = date(2000,1,1)
        fields = self.fields

        # sequentially page back to appropriate month
        current_year = date.today().year
        current_month = date.today().month
        target_month = date_from.month
        target_year = date_from.year
        while current_year > target_year or current_month > target_month:
            current_month -= 1
            if current_month <= 0:
                current_month = 12
                current_year -= 1
            delta = date(current_year, current_month, 1) - origin
            if self.DEBUG: print "month from num:", delta.days
            fields['__EVENTTARGET'] = ''
            fields['__EVENTARGUMENT'] = ''
            form_ok = util.setup_form(self.br, self.search_form, self.fields)
            if self.DEBUG: print "form:", self.br.form
            response = util.submit_form(self.br, self.from_prev)
            if self.DEBUG: print "from month page:", response.read()

        # set from day
        delta = date_from - origin
        if self.DEBUG: print "day from num:", delta.days
        fields['__EVENTTARGET'] = self.date_from_field
        fields['__EVENTARGUMENT'] = str(delta.days)
        form_ok = util.setup_form(self.br, self.search_form, fields)
        for control in self.br.form.controls:
            if control.type == "submit":
                control.disabled = True
        if self.DEBUG: print "form:", self.br.form
        response = util.submit_form(self.br)
        if self.DEBUG: print "from page:", response.read()

        # sequentially page back to appropriate month
        current_year = date.today().year
        current_month = date.today().month
        target_month = date_to.month
        target_year = date_to.year
        while current_year > target_year or current_month > target_month:
            current_month -= 1
            if current_month <= 0:
                current_month = 12
                current_year -= 1
            delta = date(current_year, current_month, 1) - origin
            if self.DEBUG: print "month to num:", delta.days
            fields['__EVENTTARGET'] = ''
            fields['__EVENTARGUMENT'] = ''
            form_ok = util.setup_form(self.br, self.search_form, self.fields)
            if self.DEBUG: print "form:", self.br.form
            response = util.submit_form(self.br, self.to_prev)
            if self.DEBUG: print "to month page:", response.read()

        # set to day
        delta = date_to - origin
        if self.DEBUG: print "day to num:", delta.days
        fields['__EVENTTARGET'] = self.date_to_field
        fields['__EVENTARGUMENT'] = str(delta.days)
        form_ok = util.setup_form(self.br, self.search_form, fields)
        for control in self.br.form.controls:
            if control.type == "submit":
                control.disabled = True
        if self.DEBUG: print "form:", self.br.form
        response = util.submit_form(self.br)
        if self.DEBUG: print "to page:", response.read()

        form_ok = util.setup_form(self.br, self.search_form, self.search_fields)
        if self.DEBUG: print "form:", self.br.form
        response = util.submit_form(self.br, self.submit_control)

        html = response.read()
        url = response.geturl()
        if self.DEBUG: print "result page:", url, html

        final_result = []
        while response:
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
                try:
                    response = self.br.follow_link(text=self.next_link)
                except:
                    break
                html = response.read()
                url = response.geturl()
                if self.DEBUG: print "next page:", html
            else:
                break

        return final_result"""

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
            this_url = self.applic_url + '&systemkey=' + str(current_rec)
            response = util.open_url(self.br, this_url)
            if response:
                html = response.read()
                url = response.geturl()
                if self.DEBUG: print 'Html:', html
                result = scrapemark.scrape(self.scrape_min_data, html, url)
                if result and result.get('uid'):
                    if not first_good_rec: first_good_rec = current_rec
                    last_good_rec = current_rec
                    if self.DEBUG: print result
                    final_result.append( { 'url': this_url, 'uid': str(current_rec) } ) # temporarily sets uid to the systemkey
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

    # note only works if the 'uid' is set temporarily to the systemkey
    def get_detail_from_uid (self, uid):
        url = self.applic_url + '&systemkey=' + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    scraper = AshfordScraper()
    scraper.run()

    # misc tests
    #scraper.DEBUG = True
    #scraper.br.set_debug_http(True)
    #print scraper.get_detail_from_uid ('12/00779/ADV')
    #print scraper.get_detail_from_uid('95425')
    #res = scraper.get_id_batch(util.get_dt('06/06/2012'), util.get_dt('14/06/2012'))

    #result = scraper.get_id_records2(15000, True)
    #print result

    #print len(res), res
    #print scraper.gather_ids('2012-02-01')
    #print scraper.gather_ids('2011-02-01', '2012-01-18')


# this is a scraper of Ashford planning applications for use by Openly Local

# date query results filled out using JQuery/AJAX - not accessible?

# so works from the sequence of systemkey record numbers 

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import urllib
import sys

base = scraperwiki.utils.swimport("openlylocal_base_scraper")
scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")

class AshfordScraper(base.ListScraper):

    START_SEQUENCE = 50000 # gathering back to this record number
    START_POINT = 95000 # default starting point, if there is no other information ie database is empty
    MAX_ID_BATCH = 200 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 150 # max application details to scrape in one go
    ID_ORDER = "uid desc"
    MIN_RECS = 70

    ck = { 'name': 'ABCPLANNINGTERMS', 'value': '22 Feb 2017 08:21:18 AM', 'domain': 'planning.ashford.gov.uk', 'path': '/' }

    """date_from_field = 'ctl00$CPH_Details$Details_TabContainer$Date_Tab$searchby_date1$StartDate$myCalendar'
    date_to_field = 'ctl00$CPH_Details$Details_TabContainer$Date_Tab$searchby_date1$EndDate$myCalendar'
    from_prev = 'ctl00$CPH_Details$Details_TabContainer$Date_Tab$searchby_date1$StartDate$LB_Prev'
    to_prev = 'ctl00$CPH_Details$Details_TabContainer$Date_Tab$searchby_date1$EndDate$LB_Prev'
    uid_year = 'ctl00$CPH_Details$Details_TabContainer$CaseNo_Tab$searchby_caseNo1$CaseYear'
    search_form = '0'
    fields = { '__EVENTTARGET': '', '__EVENTARGUMENT': '' }
    search_fields = { '__EVENTTARGET': '', '__EVENTARGUMENT': '', 'ctl00$CPH_Details$Details_TabContainer$Date_Tab$searchby_date1$DateSearchBy': 'Registration Date' }
    next_link = 'Next >'
    submit_control = 'ctl00$CPH_Details$Details_TabContainer$Date_Tab$searchby_date1$Search_Button'
    start_url = 'http://planning.ashford.gov.uk/planning/Default.aspx?new=true'"""

    applic_url = 'http://planning.ashford.gov.uk/Planning/details.aspx?pageindex=0'
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="contents"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    # note overwrites uid to correct value
    scrape_min_data = """
    <th> Application Ref </th> <td> {{ uid }} </td>
    <th> Site Address </th> <td> {{ address }} </td>
    <th> Description </th> <td> {{ description }} </td>
    <th> Date Received </th> <td> {{ date_received }} </td>
    <th> Date Registered </th> <td> {{ date_validated }} </td>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<th> Application Ref </th> <td> {{ reference }} </td>',
    '<th> Application Type </th> <td> {{ application_type }} </td>',
    '<th> Status </th> <td> {{ status }} </td>',
    '<th> Council Decision </th> <td> {{ decision }} </td>',
    '<th> Ward </th> <td> {{ ward_name }} </td>',
    '<th> Parish </th> <td> {{ parish }} </td>',
    '<th> Officer Name </th> <td> {{ case_officer }} </td>',
    '<th> Applicant </th> <td> {{ applicant_address }} </td>',
    '<th> Agent </th> <td> {{ agent_address }} </td>',
    '<th> Grid Reference </th> <td> {{ easting }} / {{ northing }} </td>',
    """<th> Target Decision Date </th> <td> {{ target_decision_date }} </td>
    <th> Decision Date </th> <td> {{ decision_date }} </td>""",
    '<th> Committee Date </th> <td> {{ meeting_date }} </td>',
    '<th> Comments By </th> <td> {{ comment_date }} </td>',
    '<th> Start of Consultation </th> <td> {{ consultation_start_date }} </td>',
    '<th> End of Consultation </th> <td> {{ consultation_end_date }} </td>',
    '<th> Decision Level </th> <td> {{ decided_by }} </td>',
    ]

    def __init__(self, table_name = None):
        base.ListScraper.__init__(self, table_name)
        if self.ck:
            util.set_cookie(self.cj, self.ck['name'], self.ck['value'], self.ck.get('domain'), self.ck.get('path', '/'))   

    """def get_id_batch (self, date_from, date_to):

        response = util.open_url(self.br, self.start_url)
        if self.DEBUG: print "start page:", response.read()

        origin = date(2000,1,1)
        fields = self.fields

        # sequentially page back to appropriate month
        current_year = date.today().year
        current_month = date.today().month
        target_month = date_from.month
        target_year = date_from.year
        while current_year > target_year or current_month > target_month:
            current_month -= 1
            if current_month <= 0:
                current_month = 12
                current_year -= 1
            delta = date(current_year, current_month, 1) - origin
            if self.DEBUG: print "month from num:", delta.days
            fields['__EVENTTARGET'] = ''
            fields['__EVENTARGUMENT'] = ''
            form_ok = util.setup_form(self.br, self.search_form, self.fields)
            if self.DEBUG: print "form:", self.br.form
            response = util.submit_form(self.br, self.from_prev)
            if self.DEBUG: print "from month page:", response.read()

        # set from day
        delta = date_from - origin
        if self.DEBUG: print "day from num:", delta.days
        fields['__EVENTTARGET'] = self.date_from_field
        fields['__EVENTARGUMENT'] = str(delta.days)
        form_ok = util.setup_form(self.br, self.search_form, fields)
        for control in self.br.form.controls:
            if control.type == "submit":
                control.disabled = True
        if self.DEBUG: print "form:", self.br.form
        response = util.submit_form(self.br)
        if self.DEBUG: print "from page:", response.read()

        # sequentially page back to appropriate month
        current_year = date.today().year
        current_month = date.today().month
        target_month = date_to.month
        target_year = date_to.year
        while current_year > target_year or current_month > target_month:
            current_month -= 1
            if current_month <= 0:
                current_month = 12
                current_year -= 1
            delta = date(current_year, current_month, 1) - origin
            if self.DEBUG: print "month to num:", delta.days
            fields['__EVENTTARGET'] = ''
            fields['__EVENTARGUMENT'] = ''
            form_ok = util.setup_form(self.br, self.search_form, self.fields)
            if self.DEBUG: print "form:", self.br.form
            response = util.submit_form(self.br, self.to_prev)
            if self.DEBUG: print "to month page:", response.read()

        # set to day
        delta = date_to - origin
        if self.DEBUG: print "day to num:", delta.days
        fields['__EVENTTARGET'] = self.date_to_field
        fields['__EVENTARGUMENT'] = str(delta.days)
        form_ok = util.setup_form(self.br, self.search_form, fields)
        for control in self.br.form.controls:
            if control.type == "submit":
                control.disabled = True
        if self.DEBUG: print "form:", self.br.form
        response = util.submit_form(self.br)
        if self.DEBUG: print "to page:", response.read()

        form_ok = util.setup_form(self.br, self.search_form, self.search_fields)
        if self.DEBUG: print "form:", self.br.form
        response = util.submit_form(self.br, self.submit_control)

        html = response.read()
        url = response.geturl()
        if self.DEBUG: print "result page:", url, html

        final_result = []
        while response:
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
                try:
                    response = self.br.follow_link(text=self.next_link)
                except:
                    break
                html = response.read()
                url = response.geturl()
                if self.DEBUG: print "next page:", html
            else:
                break

        return final_result"""

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
            this_url = self.applic_url + '&systemkey=' + str(current_rec)
            response = util.open_url(self.br, this_url)
            if response:
                html = response.read()
                url = response.geturl()
                if self.DEBUG: print 'Html:', html
                result = scrapemark.scrape(self.scrape_min_data, html, url)
                if result and result.get('uid'):
                    if not first_good_rec: first_good_rec = current_rec
                    last_good_rec = current_rec
                    if self.DEBUG: print result
                    final_result.append( { 'url': this_url, 'uid': str(current_rec) } ) # temporarily sets uid to the systemkey
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

    # note only works if the 'uid' is set temporarily to the systemkey
    def get_detail_from_uid (self, uid):
        url = self.applic_url + '&systemkey=' + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    scraper = AshfordScraper()
    scraper.run()

    # misc tests
    #scraper.DEBUG = True
    #scraper.br.set_debug_http(True)
    #print scraper.get_detail_from_uid ('12/00779/ADV')
    #print scraper.get_detail_from_uid('95425')
    #res = scraper.get_id_batch(util.get_dt('06/06/2012'), util.get_dt('14/06/2012'))

    #result = scraper.get_id_records2(15000, True)
    #print result

    #print len(res), res
    #print scraper.gather_ids('2012-02-01')
    #print scraper.gather_ids('2011-02-01', '2012-01-18')


