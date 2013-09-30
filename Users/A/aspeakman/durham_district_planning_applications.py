# this is a scraper of 4 Durham district authorities with customised systems

# there are another 4 district offices which use standard planning systems (implemented elsewhere)

# planning applications from all 8 Durham districts are collected in the durham_county_planning_aggregator

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
import socket

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

systems = {
    'BarnardCastle': 'BarnardCastleScraper', # Teesdale
    'Consett': 'ConsettScraper', # Derwentside
    'DurhamCounty': 'DurhamCountyScraper', # restricted to county matters  - minerals, waste, education etc
    'Sedgefield': 'SedgefieldScraper',
     }

class BarnardCastleScraper(base.DateScraper):

    MAX_ID_BATCH = 300 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go
    TABLE_NAME = 'BarnardCastle'

    search_url = 'http://teesdale.planning-register.co.uk'
    date_from_field = 'txtAppRecFrom'
    date_to_field = 'txtAppRecTo'
    search_form = 'frmAppSel'
    action = 'PlanAppList.asp?PerPage=500'
    request_date_format = '%d/%m/%Y'
    ref_field = 'txtAppNum'
    scrape_ids = """
    <table> <tr />
    {* <tr> <td> <a href="{{ [records].url|abs }}">
    {{ [records].uid }} </a> </td>
    </tr> <tr /> *}
    </table>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = '<body> {{ block|html }} </body>'
    # the minimum acceptable valid dataset on the details page
    scrape_min_data = """
    <input name="txtAppNum" value="{{ reference }}">
    <textarea name="Location"> {{ address }} </textarea>
    <textarea name="Proposal"> {{ description }} </textarea>
    """
    # other optional parameters common to all scrapers can appear on the details page
    scrape_optional_data = [
    '<input name="txtAppStatus" value="{{ status }}">',
    '<input name="Ward" value="{{ ward_name }}">',
    '<input name="Parish" value="{{ parish }}">',
    '<input name="Easting" value="{{ easting }}">',
    '<input name="Northing" value="{{ northing }}">',
    '<input name="CommDate" value="{{ date_validated }}"> <input name="CommDate" value="{{ decision_date }}">',
    '<input name="delegComm" value="{{ application_type }}">',
    '<input name="txtCaseOff" value="{{ case_officer }}">',
    '<input name="AppName" value="{{ applicant_name }}">',
    '<input name="AgentName" value="{{ agent_name }}">',
    '<input name="AgentTel" value="{{ agent_tel }}">',
    '<textarea name="AppAddr"> {{ applicant_address }} </textarea>',
    '<textarea name="AgentAddr"> {{ agent_address }} </textarea>',
    '<input name="c_c_l_e_d" value="{{ consultation_start_date }}"> <input name="c_c_l_e_d" value="{{ consultation_end_date }}">',
    '<input name="n_c_l_e_d" value="{{ neighbour_consultation_start_date }}"> <input name="n_c_l_e_d" value="{{ neighbour_consultation_end_date }}">',
    '<input name="s_n_e_d" value="{{ site_notice_start_date }}"> <input name="s_n_e_d" value="{{ site_notice_end_date }}">',
    '<input name="r_l_e_d" value="{{ last_advertised_date }}"> <input name="r_l_e_d" value="{{ latest_advertisement_expiry_date }}">',
    ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)

        fields = {}
        fields[self.date_from_field] = date_from.strftime(self.request_date_format)
        fields[self.date_to_field] = date_to.strftime(self.request_date_format)
        util.setup_form(self.br, self.search_form, fields, self.action)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br)
        
        final_result = []
        if response:
            html = response.read()
            url = response.geturl()
            if self.DEBUG: print html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])

        return final_result

    def get_detail_from_uid (self, uid):
        response = self.br.open(self.search_url)

        fields = {}
        fields[self.ref_field] = uid
        util.setup_form(self.br, self.search_form, fields)
        response = util.submit_form(self.br)
        try:
            html = response.read()
            if self.DEBUG: print html
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            url = result['records'][0]['url']
            if self.DEBUG: print url
        except:
            return None
        return self.get_detail_from_url(url)

class ConsettScraper(base.DateScraper):

    MAX_ID_BATCH = 300 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go
    TABLE_NAME = 'Consett'

    search_url = 'http://ddc.durham.gov.uk/planning/planningsearch/index.cfm'
    date_from_field = { 'day': 'validdayfrom', 'month': 'validmonthfrom', 'year': 'validyearfrom', }
    date_to_field = { 'day': 'validdayto', 'month': 'validmonthto', 'year': 'validyearto', }
    search_form = 'searchApplications'
    request_date_format = '%-d/%b/%Y'
    ref_field = 'ref_no'
    scrape_max_pages = "<p> returned by your search in {{ max_pages }} page(s). </p>"
    next_page_link = '?step=2&page='
    scrape_ids = """
    <table> <tr />
    {* <tr> <td> <a href="{{ [records].url|abs }}">
    {{ [records].uid }} </a> </td>
    </tr> *}
    </table>
    """
    scrape_id_plus = """
    <table> <tr />
    <tr> <td> <a> {{ reference }} </a> </td>
    <td> {{ date_received }} </td> <td> {{ address }} </td> <td> {{ description }} </td>
    </tr>
    </table>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = '<div id="midcontent"> {{ block|html }} </div>'
    # the minimum acceptable valid dataset on the details page
    scrape_min_data = """
    <th> Reference </th> <td> {{ reference }} </td>
    <th> Location </th> <td> {{ address|html }} </td>
    <th> Development </th> <td> {{ description }} </td>
    <th> Received Date </th> <td> {{ date_received }} </td>
    <th> Valid Date </th> <td> {{ date_validated }} </td>
    """
    # other optional parameters common to all scrapers can appear on the details page
    scrape_optional_data = [
    '<th> Application Type </th> <td> {{ application_type }} </td>',
    '<th> Council Decision </th> <td> {{ decision }} </td>',
    '<th> Decision Date </th> <td> {{ decision_date }} </td>',
    '<th> Officer </th> <td> {{ case_officer }} </td>',
    '<th> Decision Level </th> <td> {{ decided_by }} </td>',
    '<th> Applicant Name </th> <td> {{ applicant_name }} </td>',
    '<th> Agent Name </th> <td> {{ agent_name }} </td>',
    '<th> Agent Address </th> <td> {{ agent_address|html }} </td>',
    '<th> Ward </th> <td> {{ ward_name }} </td>',
    ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)

        date_to = date_to + timedelta(days=1) # end date is exclusive
        
        fields = {}
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

        html = response.read()
        url = response.geturl()
        if self.DEBUG: print html
            
        result = scrapemark.scrape(self.scrape_max_pages, html)
        try:
            max_pages = int(result['max_pages'])
        except:
            max_pages = 1
        page_count = 1
        
        final_result = []
        while page_count <= max_pages:
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            else:
                break
            page_count += 1
            if page_count > max_pages: break
            try:
                response = self.br.open(self.next_page_link + str(page_count))
                html = response.read()
                url = response.geturl()
            except:
                break

        return final_result

    def get_detail_from_uid (self, uid):
        url = self.search_url + '?step=4&ref=' + urllib.quote_plus(uid)
        result = self.get_detail_from_url(url)
        if not result:
            return self.get_detail_from_uid2(uid)
        else:
            return result

    # sometimes the main record has no details, so we go via the search form instead to get basic data = address, date, description
    def get_detail_from_uid2 (self, uid): 
        try:
            response = self.br.open(self.search_url)
            fields = {}
            fields[self.ref_field] = uid
            util.setup_form(self.br, self.search_form, fields)
            response = util.submit_form(self.br)
            html = response.read()
            if self.DEBUG: print html
            url = response.geturl()
        except:
            if self.DEBUG: raise
            else: return None
        return self.get_detail(html, url, self.scrape_data_block, self.scrape_id_plus)

class DurhamCountyScraper(base.PeriodScraper): 

    START_SEQUENCE = '2003-01-01' # gathers id data by working backwards from the current date towards this one
    MAX_ID_BATCH = 250 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go
    PERIOD_TYPE = 'Month'
    HEADERS = {
    'Accept-Charset': 'UTF-8,*',
    'Accept': 'text/html',
    'Accept-Encoding': 'gzip, deflate',
    'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
    }
    TABLE_NAME = 'DurhamCounty'

    search_form = 'input'
    date_field_from = { 'month': 'Month', 'year': 'Year' }
    ref_field = 'AppRef'
    request_date_format = '%d/%b/%Y'
    search_url = 'http://gis.durham.gov.uk/website/dcs/SearchMain.asp'
    scrape_ids = """
    <table> <tr />
    {* <tr>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    </tr> *}
    </table>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="content"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <tr> <td> Application Ref </td> <td> {{ reference }} </td> </tr>
    <tr> <td> Development </td> <td> {{ description }} </td> </tr>
    <tr> <td> Location </td> <td> {{ address }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr> <td> Type of Application </td> <td> {{ application_type }} </td> </tr>',
    '<tr> <td> Current Status </td> <td> {{ status }} </td> </tr>',
    '<tr> <td> Decision Level </td> <td> {{ decided_by }} </td> </tr>',
    '<tr> <td> Decision </td> <td> {{ decision }} </td> <td> Date of Decision </td> <td> {{ decision_date }} </td> </tr>',
    '<tr> <td> Appeal Lodged </td> <td> {{ appeal_date }} </td> </tr>',
    '<tr> <td> Case Officer </td> <td> {{ case_officer }} </td> </tr>',
    '<tr> <td> Parish </td> <td> {{ parish }} </td> </tr>',
    '<tr> <td> Date Received </td> <td> {{ date_received }} </td> </tr>',
    '<tr> <td> Date of Validation </td> <td> {{ date_validated }} </td> </tr>',
    '<tr> <td> Expiry Date </td> <td> {{ application_expires_date }} </td> </tr>',
    '<tr> <td> Committee Date </td> <td> {{ meeting_date }} </td> </tr>',
    '<tr> <td> Site Notice Posted </td> <td> {{ site_notice_start_date }} </td> </tr>',
    '<tr> <td> Site Notice Expiry </td> <td> {{ site_notice_end_date }} </td> </tr>',
    '<tr> <td> Press Notice Posted </td> <td> {{ last_advertised_date }} </td> </tr>',
    '<tr> <td> Press Notice Expiry </td> <td> {{ latest_advertisement_expiry_date }} </td> </tr>',
    '<tr> <td> Applicant Name </td> <td> {{ applicant_name }} </td> </tr>',
    '<tr> <td> Agent Name </td> <td> {{ agent_name }} </td> </tr>',
    '<tr> <td> Agent Phone </td> <td> {{ agent_tel }} </td> </tr>',
    '<td> Applicant Address </td> {{ applicant_address|html }} Top of Page',
    '<td> Agent Address </td> {{ agent_address|html }} Agent Phone',
    ]

    def get_id_period (self, date):

        from_iso_dt, to_iso_dt = util.inc_dt(date.strftime(util.ISO8601_DATE), util.ISO8601_DATE, self.PERIOD_TYPE)
        from_dt = util.get_dt(from_iso_dt, util.ISO8601_DATE)
        to_dt = util.get_dt(to_iso_dt, util.ISO8601_DATE)

        response = self.br.open(self.search_url)
        
        fields = {}
        date = date.strftime(self.request_date_format)
        date_parts = date.split('/')
        #fields [self.date_from_field['day']] = date_parts[0]
        fields [self.date_field_from['month']] = date_parts[1]
        fields [self.date_field_from['year']] = date_parts[2]
        
        util.setup_form(self.br, self.search_form, fields )
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br)

        final_result = []
        if response:
            html = response.read()
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
        
        if final_result:
            return final_result, from_dt, to_dt
        else:
            return [], None, None # monthly scraper - so empty result is always invalid

    def get_detail_from_uid (self, uid):
        response = self.br.open(self.search_url)

        fields = {}
        fields[self.ref_field] = uid
        util.setup_form(self.br, self.search_form, fields)
        response = util.submit_form(self.br)
        try:
            html = response.read()
            if self.DEBUG: print html
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            url = result['records'][0]['url']
            if self.DEBUG: print url
        except:
            return None
        return self.get_detail_from_url(url)

    # scrape detailed information on one record via its access URL
    # note urllib does not like the "HTML" returned here (because it is badly formed - consisting of multiple concatenated <html> <head> <body> sections)
    # it only return the first html section
    # so we have to do a raw http connect to get all the rubbish data - then parse that
    def get_detail_from_url (self, url):
        try:
            o = urlparse.urlparse(url)
            CRLF = "\r\n"
            request = [
                "GET " + o.path + '?' + o.query + " HTTP/1.1",
                "Host: " + o.hostname,
                "Connection: Close",
                "",
                "",
            ]
            s = socket.socket()
            if o.port:
                s.connect((o.hostname, int(o.port)))
            else:
                s.connect((o.hostname, 80))
            s.send(CRLF.join(request))
            html = ''
            buffer = s.recv(4096)
            while buffer:
                html += buffer
                buffer = s.recv(4096)
            if self.DEBUG:
                print "Html obtained from url:", html
        except:
            if self.DEBUG: raise
            else: return None
        result = self.get_detail(html, url)
        return result

class SedgefieldScraper(base.DateScraper):

    MAX_ID_BATCH = 300 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go
    TABLE_NAME = 'Sedgefield'

    search_url = 'http://www2.sedgefield.gov.uk/planning_search/index.php'
    date_from_field = 'Appfrom'
    date_to_field = 'Appto'
    search_form = 'form'
    request_date_format = '%-d/%-m/%Y'
    ref_field = 'ApplicationNo'
    scrape_ids = """
    <h3 /> <table> <tr />
    {* <tr>
    <td> {{ [records].uid }} </td>
    <td> <a href="{{ [records].url|abs }}"> </a> </td>
    </tr>
    *}
    </table>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = '<body> {{ block|html }} </body>'
    # the minimum acceptable valid dataset on the details page
    scrape_min_data = """
    <th> Application No </th> <td> {{ reference }} </td> <td />
    <td> {{ address }} </td> <td> {{ description }} </td>
    <th> Date Received </th> 
    <td> {{ date_received }} </td> <td> {{ date_validated }} </td>
    """
    # other optional parameters common to all scrapers can appear on the details page
    scrape_optional_data = [
    '<td> UPRN </td> <td> {{ uprn }} </td>',
    '<th> Applicant </th>  <td /> <td> {{ applicant_name }} </td>',
    '<th> Agent </th>  <td /> <td /> <td /> <td /> <td> {{ agent_name }} </td>',
    '<th> Consultation End Date </th> <td /> <td /> <td> {{ consultation_end_date }} </td>',
    '<th> Committee Date </th> <td /> <td /> <td /> <td> {{ meeting_date }} </td>',
    '<th> Decision Date </th> <td> {{ decision_date }} </td>',
    '<th> Target Date </th> <td /> <td> {{ target_decision_date }} </td>',
    '<th> Expiry Date </th> <td /> <td /> <td> {{ application_expires_date }} </td>',
    '<th> Status </th> <td> {{ decision }} </td> <td> {{ status }} </td>',
    '<h3> Case Officer - {{ case_officer }} </h3>',
    ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)

        fields = {}
        fields[self.date_from_field] = date_from.strftime(self.request_date_format)
        fields[self.date_to_field] = date_to.strftime(self.request_date_format)
        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br)
        
        final_result = []
        if response:
            html = response.read()
            url = response.geturl()
            if self.DEBUG: print html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])

        return final_result

    def get_detail_from_uid (self, uid):
        response = self.br.open(self.search_url)

        fields = {}
        fields[self.ref_field] = uid
        util.setup_form(self.br, self.search_form, fields)
        response = util.submit_form(self.br)
        try:
            html = response.read()
            if self.DEBUG: print html
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            url = result['records'][0]['url']
            if self.DEBUG: print url
        except:
            return None
        return self.get_detail_from_url(url)


if __name__ == 'scraper':

    sys_list = []
    for k, v in systems.items(): # get latest date scraped for each system
        sys_list.append( (k, v, scraperwiki.sqlite.get_var('latest-' + k)) )
    sort_sys = sorted(sys_list, key=lambda system: system[2]) # sort so least recent are first
    for auth in sort_sys[:5]: # do max 5 per run
        strexec = auth[1] + "('" + auth[0] + "')"
        print "Scraping from:", strexec
        try:
            scraper = eval(strexec)
            scraper.run()
        except Exception as err:
            print "Error - skipping this authority -", str(err)
    print "Finished"

    # misc test calls
    #scraper = BarnardCastleScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('6/2012/0011/AF') # BarnardCastle OK
    #scraper = ConsettScraper()
    #scraper.DEBUG = True
    #scraper.populate_missing_applications()
    #print scraper.get_detail_from_uid ('1/2000/0049') # Consett OK
    #print scraper.get_detail_from_uid ('1/2011/0404') # Consett no details returned
    #scraper = SedgefieldScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('7/2011/0334/DM') # Sedgefield OK
    
    #res = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('18/08/2011'))
    #print res, len(res)

    #scraper = DurhamCountyScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('928/5/164(15)') # DurhamCounty
    #res, dt1, dt2 = scraper.get_id_period(util.get_dt('01/01/2011'))
    #print res, len(res), dt1, dt2


    

# this is a scraper of 4 Durham district authorities with customised systems

# there are another 4 district offices which use standard planning systems (implemented elsewhere)

# planning applications from all 8 Durham districts are collected in the durham_county_planning_aggregator

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
import socket

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

systems = {
    'BarnardCastle': 'BarnardCastleScraper', # Teesdale
    'Consett': 'ConsettScraper', # Derwentside
    'DurhamCounty': 'DurhamCountyScraper', # restricted to county matters  - minerals, waste, education etc
    'Sedgefield': 'SedgefieldScraper',
     }

class BarnardCastleScraper(base.DateScraper):

    MAX_ID_BATCH = 300 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go
    TABLE_NAME = 'BarnardCastle'

    search_url = 'http://teesdale.planning-register.co.uk'
    date_from_field = 'txtAppRecFrom'
    date_to_field = 'txtAppRecTo'
    search_form = 'frmAppSel'
    action = 'PlanAppList.asp?PerPage=500'
    request_date_format = '%d/%m/%Y'
    ref_field = 'txtAppNum'
    scrape_ids = """
    <table> <tr />
    {* <tr> <td> <a href="{{ [records].url|abs }}">
    {{ [records].uid }} </a> </td>
    </tr> <tr /> *}
    </table>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = '<body> {{ block|html }} </body>'
    # the minimum acceptable valid dataset on the details page
    scrape_min_data = """
    <input name="txtAppNum" value="{{ reference }}">
    <textarea name="Location"> {{ address }} </textarea>
    <textarea name="Proposal"> {{ description }} </textarea>
    """
    # other optional parameters common to all scrapers can appear on the details page
    scrape_optional_data = [
    '<input name="txtAppStatus" value="{{ status }}">',
    '<input name="Ward" value="{{ ward_name }}">',
    '<input name="Parish" value="{{ parish }}">',
    '<input name="Easting" value="{{ easting }}">',
    '<input name="Northing" value="{{ northing }}">',
    '<input name="CommDate" value="{{ date_validated }}"> <input name="CommDate" value="{{ decision_date }}">',
    '<input name="delegComm" value="{{ application_type }}">',
    '<input name="txtCaseOff" value="{{ case_officer }}">',
    '<input name="AppName" value="{{ applicant_name }}">',
    '<input name="AgentName" value="{{ agent_name }}">',
    '<input name="AgentTel" value="{{ agent_tel }}">',
    '<textarea name="AppAddr"> {{ applicant_address }} </textarea>',
    '<textarea name="AgentAddr"> {{ agent_address }} </textarea>',
    '<input name="c_c_l_e_d" value="{{ consultation_start_date }}"> <input name="c_c_l_e_d" value="{{ consultation_end_date }}">',
    '<input name="n_c_l_e_d" value="{{ neighbour_consultation_start_date }}"> <input name="n_c_l_e_d" value="{{ neighbour_consultation_end_date }}">',
    '<input name="s_n_e_d" value="{{ site_notice_start_date }}"> <input name="s_n_e_d" value="{{ site_notice_end_date }}">',
    '<input name="r_l_e_d" value="{{ last_advertised_date }}"> <input name="r_l_e_d" value="{{ latest_advertisement_expiry_date }}">',
    ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)

        fields = {}
        fields[self.date_from_field] = date_from.strftime(self.request_date_format)
        fields[self.date_to_field] = date_to.strftime(self.request_date_format)
        util.setup_form(self.br, self.search_form, fields, self.action)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br)
        
        final_result = []
        if response:
            html = response.read()
            url = response.geturl()
            if self.DEBUG: print html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])

        return final_result

    def get_detail_from_uid (self, uid):
        response = self.br.open(self.search_url)

        fields = {}
        fields[self.ref_field] = uid
        util.setup_form(self.br, self.search_form, fields)
        response = util.submit_form(self.br)
        try:
            html = response.read()
            if self.DEBUG: print html
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            url = result['records'][0]['url']
            if self.DEBUG: print url
        except:
            return None
        return self.get_detail_from_url(url)

class ConsettScraper(base.DateScraper):

    MAX_ID_BATCH = 300 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go
    TABLE_NAME = 'Consett'

    search_url = 'http://ddc.durham.gov.uk/planning/planningsearch/index.cfm'
    date_from_field = { 'day': 'validdayfrom', 'month': 'validmonthfrom', 'year': 'validyearfrom', }
    date_to_field = { 'day': 'validdayto', 'month': 'validmonthto', 'year': 'validyearto', }
    search_form = 'searchApplications'
    request_date_format = '%-d/%b/%Y'
    ref_field = 'ref_no'
    scrape_max_pages = "<p> returned by your search in {{ max_pages }} page(s). </p>"
    next_page_link = '?step=2&page='
    scrape_ids = """
    <table> <tr />
    {* <tr> <td> <a href="{{ [records].url|abs }}">
    {{ [records].uid }} </a> </td>
    </tr> *}
    </table>
    """
    scrape_id_plus = """
    <table> <tr />
    <tr> <td> <a> {{ reference }} </a> </td>
    <td> {{ date_received }} </td> <td> {{ address }} </td> <td> {{ description }} </td>
    </tr>
    </table>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = '<div id="midcontent"> {{ block|html }} </div>'
    # the minimum acceptable valid dataset on the details page
    scrape_min_data = """
    <th> Reference </th> <td> {{ reference }} </td>
    <th> Location </th> <td> {{ address|html }} </td>
    <th> Development </th> <td> {{ description }} </td>
    <th> Received Date </th> <td> {{ date_received }} </td>
    <th> Valid Date </th> <td> {{ date_validated }} </td>
    """
    # other optional parameters common to all scrapers can appear on the details page
    scrape_optional_data = [
    '<th> Application Type </th> <td> {{ application_type }} </td>',
    '<th> Council Decision </th> <td> {{ decision }} </td>',
    '<th> Decision Date </th> <td> {{ decision_date }} </td>',
    '<th> Officer </th> <td> {{ case_officer }} </td>',
    '<th> Decision Level </th> <td> {{ decided_by }} </td>',
    '<th> Applicant Name </th> <td> {{ applicant_name }} </td>',
    '<th> Agent Name </th> <td> {{ agent_name }} </td>',
    '<th> Agent Address </th> <td> {{ agent_address|html }} </td>',
    '<th> Ward </th> <td> {{ ward_name }} </td>',
    ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)

        date_to = date_to + timedelta(days=1) # end date is exclusive
        
        fields = {}
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

        html = response.read()
        url = response.geturl()
        if self.DEBUG: print html
            
        result = scrapemark.scrape(self.scrape_max_pages, html)
        try:
            max_pages = int(result['max_pages'])
        except:
            max_pages = 1
        page_count = 1
        
        final_result = []
        while page_count <= max_pages:
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            else:
                break
            page_count += 1
            if page_count > max_pages: break
            try:
                response = self.br.open(self.next_page_link + str(page_count))
                html = response.read()
                url = response.geturl()
            except:
                break

        return final_result

    def get_detail_from_uid (self, uid):
        url = self.search_url + '?step=4&ref=' + urllib.quote_plus(uid)
        result = self.get_detail_from_url(url)
        if not result:
            return self.get_detail_from_uid2(uid)
        else:
            return result

    # sometimes the main record has no details, so we go via the search form instead to get basic data = address, date, description
    def get_detail_from_uid2 (self, uid): 
        try:
            response = self.br.open(self.search_url)
            fields = {}
            fields[self.ref_field] = uid
            util.setup_form(self.br, self.search_form, fields)
            response = util.submit_form(self.br)
            html = response.read()
            if self.DEBUG: print html
            url = response.geturl()
        except:
            if self.DEBUG: raise
            else: return None
        return self.get_detail(html, url, self.scrape_data_block, self.scrape_id_plus)

class DurhamCountyScraper(base.PeriodScraper): 

    START_SEQUENCE = '2003-01-01' # gathers id data by working backwards from the current date towards this one
    MAX_ID_BATCH = 250 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go
    PERIOD_TYPE = 'Month'
    HEADERS = {
    'Accept-Charset': 'UTF-8,*',
    'Accept': 'text/html',
    'Accept-Encoding': 'gzip, deflate',
    'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
    }
    TABLE_NAME = 'DurhamCounty'

    search_form = 'input'
    date_field_from = { 'month': 'Month', 'year': 'Year' }
    ref_field = 'AppRef'
    request_date_format = '%d/%b/%Y'
    search_url = 'http://gis.durham.gov.uk/website/dcs/SearchMain.asp'
    scrape_ids = """
    <table> <tr />
    {* <tr>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    </tr> *}
    </table>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="content"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <tr> <td> Application Ref </td> <td> {{ reference }} </td> </tr>
    <tr> <td> Development </td> <td> {{ description }} </td> </tr>
    <tr> <td> Location </td> <td> {{ address }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr> <td> Type of Application </td> <td> {{ application_type }} </td> </tr>',
    '<tr> <td> Current Status </td> <td> {{ status }} </td> </tr>',
    '<tr> <td> Decision Level </td> <td> {{ decided_by }} </td> </tr>',
    '<tr> <td> Decision </td> <td> {{ decision }} </td> <td> Date of Decision </td> <td> {{ decision_date }} </td> </tr>',
    '<tr> <td> Appeal Lodged </td> <td> {{ appeal_date }} </td> </tr>',
    '<tr> <td> Case Officer </td> <td> {{ case_officer }} </td> </tr>',
    '<tr> <td> Parish </td> <td> {{ parish }} </td> </tr>',
    '<tr> <td> Date Received </td> <td> {{ date_received }} </td> </tr>',
    '<tr> <td> Date of Validation </td> <td> {{ date_validated }} </td> </tr>',
    '<tr> <td> Expiry Date </td> <td> {{ application_expires_date }} </td> </tr>',
    '<tr> <td> Committee Date </td> <td> {{ meeting_date }} </td> </tr>',
    '<tr> <td> Site Notice Posted </td> <td> {{ site_notice_start_date }} </td> </tr>',
    '<tr> <td> Site Notice Expiry </td> <td> {{ site_notice_end_date }} </td> </tr>',
    '<tr> <td> Press Notice Posted </td> <td> {{ last_advertised_date }} </td> </tr>',
    '<tr> <td> Press Notice Expiry </td> <td> {{ latest_advertisement_expiry_date }} </td> </tr>',
    '<tr> <td> Applicant Name </td> <td> {{ applicant_name }} </td> </tr>',
    '<tr> <td> Agent Name </td> <td> {{ agent_name }} </td> </tr>',
    '<tr> <td> Agent Phone </td> <td> {{ agent_tel }} </td> </tr>',
    '<td> Applicant Address </td> {{ applicant_address|html }} Top of Page',
    '<td> Agent Address </td> {{ agent_address|html }} Agent Phone',
    ]

    def get_id_period (self, date):

        from_iso_dt, to_iso_dt = util.inc_dt(date.strftime(util.ISO8601_DATE), util.ISO8601_DATE, self.PERIOD_TYPE)
        from_dt = util.get_dt(from_iso_dt, util.ISO8601_DATE)
        to_dt = util.get_dt(to_iso_dt, util.ISO8601_DATE)

        response = self.br.open(self.search_url)
        
        fields = {}
        date = date.strftime(self.request_date_format)
        date_parts = date.split('/')
        #fields [self.date_from_field['day']] = date_parts[0]
        fields [self.date_field_from['month']] = date_parts[1]
        fields [self.date_field_from['year']] = date_parts[2]
        
        util.setup_form(self.br, self.search_form, fields )
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br)

        final_result = []
        if response:
            html = response.read()
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
        
        if final_result:
            return final_result, from_dt, to_dt
        else:
            return [], None, None # monthly scraper - so empty result is always invalid

    def get_detail_from_uid (self, uid):
        response = self.br.open(self.search_url)

        fields = {}
        fields[self.ref_field] = uid
        util.setup_form(self.br, self.search_form, fields)
        response = util.submit_form(self.br)
        try:
            html = response.read()
            if self.DEBUG: print html
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            url = result['records'][0]['url']
            if self.DEBUG: print url
        except:
            return None
        return self.get_detail_from_url(url)

    # scrape detailed information on one record via its access URL
    # note urllib does not like the "HTML" returned here (because it is badly formed - consisting of multiple concatenated <html> <head> <body> sections)
    # it only return the first html section
    # so we have to do a raw http connect to get all the rubbish data - then parse that
    def get_detail_from_url (self, url):
        try:
            o = urlparse.urlparse(url)
            CRLF = "\r\n"
            request = [
                "GET " + o.path + '?' + o.query + " HTTP/1.1",
                "Host: " + o.hostname,
                "Connection: Close",
                "",
                "",
            ]
            s = socket.socket()
            if o.port:
                s.connect((o.hostname, int(o.port)))
            else:
                s.connect((o.hostname, 80))
            s.send(CRLF.join(request))
            html = ''
            buffer = s.recv(4096)
            while buffer:
                html += buffer
                buffer = s.recv(4096)
            if self.DEBUG:
                print "Html obtained from url:", html
        except:
            if self.DEBUG: raise
            else: return None
        result = self.get_detail(html, url)
        return result

class SedgefieldScraper(base.DateScraper):

    MAX_ID_BATCH = 300 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go
    TABLE_NAME = 'Sedgefield'

    search_url = 'http://www2.sedgefield.gov.uk/planning_search/index.php'
    date_from_field = 'Appfrom'
    date_to_field = 'Appto'
    search_form = 'form'
    request_date_format = '%-d/%-m/%Y'
    ref_field = 'ApplicationNo'
    scrape_ids = """
    <h3 /> <table> <tr />
    {* <tr>
    <td> {{ [records].uid }} </td>
    <td> <a href="{{ [records].url|abs }}"> </a> </td>
    </tr>
    *}
    </table>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = '<body> {{ block|html }} </body>'
    # the minimum acceptable valid dataset on the details page
    scrape_min_data = """
    <th> Application No </th> <td> {{ reference }} </td> <td />
    <td> {{ address }} </td> <td> {{ description }} </td>
    <th> Date Received </th> 
    <td> {{ date_received }} </td> <td> {{ date_validated }} </td>
    """
    # other optional parameters common to all scrapers can appear on the details page
    scrape_optional_data = [
    '<td> UPRN </td> <td> {{ uprn }} </td>',
    '<th> Applicant </th>  <td /> <td> {{ applicant_name }} </td>',
    '<th> Agent </th>  <td /> <td /> <td /> <td /> <td> {{ agent_name }} </td>',
    '<th> Consultation End Date </th> <td /> <td /> <td> {{ consultation_end_date }} </td>',
    '<th> Committee Date </th> <td /> <td /> <td /> <td> {{ meeting_date }} </td>',
    '<th> Decision Date </th> <td> {{ decision_date }} </td>',
    '<th> Target Date </th> <td /> <td> {{ target_decision_date }} </td>',
    '<th> Expiry Date </th> <td /> <td /> <td> {{ application_expires_date }} </td>',
    '<th> Status </th> <td> {{ decision }} </td> <td> {{ status }} </td>',
    '<h3> Case Officer - {{ case_officer }} </h3>',
    ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)

        fields = {}
        fields[self.date_from_field] = date_from.strftime(self.request_date_format)
        fields[self.date_to_field] = date_to.strftime(self.request_date_format)
        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br)
        
        final_result = []
        if response:
            html = response.read()
            url = response.geturl()
            if self.DEBUG: print html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])

        return final_result

    def get_detail_from_uid (self, uid):
        response = self.br.open(self.search_url)

        fields = {}
        fields[self.ref_field] = uid
        util.setup_form(self.br, self.search_form, fields)
        response = util.submit_form(self.br)
        try:
            html = response.read()
            if self.DEBUG: print html
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            url = result['records'][0]['url']
            if self.DEBUG: print url
        except:
            return None
        return self.get_detail_from_url(url)


if __name__ == 'scraper':

    sys_list = []
    for k, v in systems.items(): # get latest date scraped for each system
        sys_list.append( (k, v, scraperwiki.sqlite.get_var('latest-' + k)) )
    sort_sys = sorted(sys_list, key=lambda system: system[2]) # sort so least recent are first
    for auth in sort_sys[:5]: # do max 5 per run
        strexec = auth[1] + "('" + auth[0] + "')"
        print "Scraping from:", strexec
        try:
            scraper = eval(strexec)
            scraper.run()
        except Exception as err:
            print "Error - skipping this authority -", str(err)
    print "Finished"

    # misc test calls
    #scraper = BarnardCastleScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('6/2012/0011/AF') # BarnardCastle OK
    #scraper = ConsettScraper()
    #scraper.DEBUG = True
    #scraper.populate_missing_applications()
    #print scraper.get_detail_from_uid ('1/2000/0049') # Consett OK
    #print scraper.get_detail_from_uid ('1/2011/0404') # Consett no details returned
    #scraper = SedgefieldScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('7/2011/0334/DM') # Sedgefield OK
    
    #res = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('18/08/2011'))
    #print res, len(res)

    #scraper = DurhamCountyScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('928/5/164(15)') # DurhamCounty
    #res, dt1, dt2 = scraper.get_id_period(util.get_dt('01/01/2011'))
    #print res, len(res), dt1, dt2


    

