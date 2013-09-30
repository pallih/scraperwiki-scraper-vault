# this is a scraper of North Lincs planning applications for use by Openly Local

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

class NorthLincsScraper(base.DateScraper):

    START_SEQUENCE = '2003-08-01' # gathers id data by working backwards from the current date towards this one
    HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
    'Accept-Charset': 'UTF-8,*',
    'Accept': 'text/html',
    'Accept-Language': 'en-gb,en',
    }

    date_from_field = 'n_cal_usercalfrom'
    date_to_field = 'n_cal_usercalto'
    search_form = 'n_form_main'
    submit_control = 'n_bt_search'
    fields = { '__EVENTTARGET': '', '__EVENTARGUMENT': '', 'n_bt_search': None, 'n_bt_clearsearch': None, 'n_bt_viewapp': None }
    search_url = 'http://www.planning.northlincs.gov.uk/newplanet/Default.aspx'
    applic_url = 'http://www.planning.northlincs.gov.uk/newplanet/planetMain.aspx'
    scrape_ids = """
    <div id="n_div_resultsholder"> <tr />
    {* <tr> <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td> </tr> *}
    </div>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <form id="form1"> {{ block|html }} </form>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <h2> Reference Number: {{ reference }} </h2>
    <table id="FormView1_reginald"> <tr /> <tr> <td> {{ date_validated }} </td> </tr> </table>
    <tr class="tableDetails"> <td> Site Address: </td> <td> {{ address }} </td> </tr>
    <tr class="tableDetails"> <td> Proposal </td> <td> {{ description }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr class="tableDetails"> <td> Ward: </td> <td> {{ ward_name }} </td> </tr>',
    '<tr class="tableDetails"> <td> Parish: </td> <td> {{ parish }} </td> </tr>',
    '<tr class="tableDetails"> <td> Grid Reference: </td> <td> E: {{ easting }} N: {{ northing }} </td> </tr>',
    '<tr class="tableDetails"> <td> Name: </td> <td> {{ applicant_name }}</td> <td> Name: </td> <td> {{ agent_name }}</td> </tr>',
    '<tr class="tableDetails"> <td> Address: </td> <td> {{ applicant_address }}</td> <td> Address: </td> <td> {{ agent_address }}</td> </tr>',
    '<tr class="tableDetails"> <td> Name: </td> <td> {{ case_officer }} </td> <td> email: </td> </tr>',   
    '<table id="FormView1_reginald"> <tr /> <tr> <td /> <td> {{ comment_date }} </td> </tr> </table>',
    '<table id="FormView1_reginald"> <tr /> <tr> <td /> <td /> <td> {{ status }} </td> </tr> </table>',
    '<table id="FormView1_reginald"> <tr /> <tr> <td /> <td /> <td /> <td> {{ application_expires_date }} </td> </tr> </table>',
    '<table id="FormView1_reginald"> <tr /> <tr> <td /> <td /> <td /> <td /> <td> {{ decided_by }} </td> </tr> </table>',
    '<table id="FormView1_reginald"> <tr /> <tr> <td /> <td /> <td /> <td /> <td /> <td> {{ decision_date }} <br> {{ decision }} </td> </tr> </table>',
    ]

    def get_id_batch (self, date_from, date_to):

        response = util.open_url(self.br, self.search_url)
        if self.DEBUG: print "search page:", response.read()

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
            fields['__EVENTTARGET'] = self.date_from_field
            fields['__EVENTARGUMENT'] = "V" + str(delta.days)
            form_ok = util.setup_form(self.br, self.search_form, fields)
            if self.DEBUG: print "form:", self.br.form
            response = util.submit_form(self.br)
            if self.DEBUG: print "from month page:", response.read()

        # set from day
        delta = date_from - origin
        if self.DEBUG: print "day from num:", delta.days
        fields['__EVENTTARGET'] = self.date_from_field
        fields['__EVENTARGUMENT'] = str(delta.days)
        form_ok = util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print "form:", self.br.form
        response = util.submit_form(self.br)
        if self.DEBUG: print "from page:", response.read()

        # page back to appropriate month
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
            fields['__EVENTTARGET'] = self.date_to_field
            fields['__EVENTARGUMENT'] = "V" + str(delta.days)
            form_ok = util.setup_form(self.br, self.search_form, fields)
            if self.DEBUG: print "form:", self.br.form
            response = util.submit_form(self.br)
            if self.DEBUG: print "from month page:", response.read()

        # set to day
        delta = date_to - origin
        if self.DEBUG: print "day to num:", delta.days
        fields['__EVENTTARGET'] = self.date_to_field
        fields['__EVENTARGUMENT'] = str(delta.days)
        form_ok = util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print "form:", self.br.form
        response = util.submit_form(self.br)
        if self.DEBUG: print "to page:", response.read()
        
        form_ok = util.setup_form(self.br, self.search_form)
        if self.DEBUG: print "form:", self.br.form
        response = util.submit_form(self.br, self.submit_control)
        
        final_result = []
        if response:
            html = response.read()
            url = response.geturl()
            if self.DEBUG: print "result page:", html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])

        return final_result

    def get_detail_from_uid (self, uid):
        url = self.applic_url + '?refno=' + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    #util.rename_column('swdata', 'application_expiry_date', 'application_expires_date')
    #sys.exit()

    scraper = NorthLincsScraper()
    scraper.run()

    # misc tests
    #scraper.DEBUG = True
    #scraper.br.set_debug_http(True)
    #print scraper.get_detail_from_uid ('PA/2012/0584')
    #res = scraper.get_id_batch(util.get_dt('30/09/2011'), util.get_dt('01/10/2011'))
    #print len(res), res
    #print scraper.gather_ids('2012-02-01')
    #print scraper.gather_ids('2011-02-01', '2012-01-18')

# this is a scraper of North Lincs planning applications for use by Openly Local

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

class NorthLincsScraper(base.DateScraper):

    START_SEQUENCE = '2003-08-01' # gathers id data by working backwards from the current date towards this one
    HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
    'Accept-Charset': 'UTF-8,*',
    'Accept': 'text/html',
    'Accept-Language': 'en-gb,en',
    }

    date_from_field = 'n_cal_usercalfrom'
    date_to_field = 'n_cal_usercalto'
    search_form = 'n_form_main'
    submit_control = 'n_bt_search'
    fields = { '__EVENTTARGET': '', '__EVENTARGUMENT': '', 'n_bt_search': None, 'n_bt_clearsearch': None, 'n_bt_viewapp': None }
    search_url = 'http://www.planning.northlincs.gov.uk/newplanet/Default.aspx'
    applic_url = 'http://www.planning.northlincs.gov.uk/newplanet/planetMain.aspx'
    scrape_ids = """
    <div id="n_div_resultsholder"> <tr />
    {* <tr> <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td> </tr> *}
    </div>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <form id="form1"> {{ block|html }} </form>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <h2> Reference Number: {{ reference }} </h2>
    <table id="FormView1_reginald"> <tr /> <tr> <td> {{ date_validated }} </td> </tr> </table>
    <tr class="tableDetails"> <td> Site Address: </td> <td> {{ address }} </td> </tr>
    <tr class="tableDetails"> <td> Proposal </td> <td> {{ description }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr class="tableDetails"> <td> Ward: </td> <td> {{ ward_name }} </td> </tr>',
    '<tr class="tableDetails"> <td> Parish: </td> <td> {{ parish }} </td> </tr>',
    '<tr class="tableDetails"> <td> Grid Reference: </td> <td> E: {{ easting }} N: {{ northing }} </td> </tr>',
    '<tr class="tableDetails"> <td> Name: </td> <td> {{ applicant_name }}</td> <td> Name: </td> <td> {{ agent_name }}</td> </tr>',
    '<tr class="tableDetails"> <td> Address: </td> <td> {{ applicant_address }}</td> <td> Address: </td> <td> {{ agent_address }}</td> </tr>',
    '<tr class="tableDetails"> <td> Name: </td> <td> {{ case_officer }} </td> <td> email: </td> </tr>',   
    '<table id="FormView1_reginald"> <tr /> <tr> <td /> <td> {{ comment_date }} </td> </tr> </table>',
    '<table id="FormView1_reginald"> <tr /> <tr> <td /> <td /> <td> {{ status }} </td> </tr> </table>',
    '<table id="FormView1_reginald"> <tr /> <tr> <td /> <td /> <td /> <td> {{ application_expires_date }} </td> </tr> </table>',
    '<table id="FormView1_reginald"> <tr /> <tr> <td /> <td /> <td /> <td /> <td> {{ decided_by }} </td> </tr> </table>',
    '<table id="FormView1_reginald"> <tr /> <tr> <td /> <td /> <td /> <td /> <td /> <td> {{ decision_date }} <br> {{ decision }} </td> </tr> </table>',
    ]

    def get_id_batch (self, date_from, date_to):

        response = util.open_url(self.br, self.search_url)
        if self.DEBUG: print "search page:", response.read()

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
            fields['__EVENTTARGET'] = self.date_from_field
            fields['__EVENTARGUMENT'] = "V" + str(delta.days)
            form_ok = util.setup_form(self.br, self.search_form, fields)
            if self.DEBUG: print "form:", self.br.form
            response = util.submit_form(self.br)
            if self.DEBUG: print "from month page:", response.read()

        # set from day
        delta = date_from - origin
        if self.DEBUG: print "day from num:", delta.days
        fields['__EVENTTARGET'] = self.date_from_field
        fields['__EVENTARGUMENT'] = str(delta.days)
        form_ok = util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print "form:", self.br.form
        response = util.submit_form(self.br)
        if self.DEBUG: print "from page:", response.read()

        # page back to appropriate month
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
            fields['__EVENTTARGET'] = self.date_to_field
            fields['__EVENTARGUMENT'] = "V" + str(delta.days)
            form_ok = util.setup_form(self.br, self.search_form, fields)
            if self.DEBUG: print "form:", self.br.form
            response = util.submit_form(self.br)
            if self.DEBUG: print "from month page:", response.read()

        # set to day
        delta = date_to - origin
        if self.DEBUG: print "day to num:", delta.days
        fields['__EVENTTARGET'] = self.date_to_field
        fields['__EVENTARGUMENT'] = str(delta.days)
        form_ok = util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print "form:", self.br.form
        response = util.submit_form(self.br)
        if self.DEBUG: print "to page:", response.read()
        
        form_ok = util.setup_form(self.br, self.search_form)
        if self.DEBUG: print "form:", self.br.form
        response = util.submit_form(self.br, self.submit_control)
        
        final_result = []
        if response:
            html = response.read()
            url = response.geturl()
            if self.DEBUG: print "result page:", html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])

        return final_result

    def get_detail_from_uid (self, uid):
        url = self.applic_url + '?refno=' + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    #util.rename_column('swdata', 'application_expiry_date', 'application_expires_date')
    #sys.exit()

    scraper = NorthLincsScraper()
    scraper.run()

    # misc tests
    #scraper.DEBUG = True
    #scraper.br.set_debug_http(True)
    #print scraper.get_detail_from_uid ('PA/2012/0584')
    #res = scraper.get_id_batch(util.get_dt('30/09/2011'), util.get_dt('01/10/2011'))
    #print len(res), res
    #print scraper.gather_ids('2012-02-01')
    #print scraper.gather_ids('2011-02-01', '2012-01-18')

