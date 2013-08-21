# this is a scraper of Sedgemoor planning applications for use by Openly Local

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import urllib, urllib2
import mechanize

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

class SedgemoorScraper(base.PeriodScraper):

    MAX_ID_BATCH = 250 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go
    PERIOD_TYPE = 'Month'
        
    search_form = 'Form1'
    start_fields = {  'drpYearRange': '2', 'ImageButton1': None }
    search_fields_date = { '__EVENTTARGET': '', '__EVENTARGUMENT': '' }
    search_fields_applic = { '__EVENTTARGET': '', '__EVENTARGUMENT': '' }
    detail_fields = { 'TextBox1': '', '__EVENTTARGET': 'dgrList:_ctl3:_ctl0', '__EVENTARGUMENT': '', 'imbSubmit': None, 'ibSendME': None }
    next_fields = { 'TextBox1': '', '__EVENTTARGET': 'dgrList$_ctl1$_ctl1', '__EVENTARGUMENT': '', 'imbSubmit': None } 
    next_form = 'Form1'
    request_date_format = '%d/%m/%Y'
    start_url = 'http://www.sedgemoor.gov.uk/planning%20online/enl.aspx'
    search_url = 'http://www.sedgemoor.gov.uk/planning%20online/search.aspx'
    scrape_max = """
    <span id="lblPageCount"><b> of {{ max_pages }} </b></span>
    """
    scrape_ids = """
    <table id="dgrList">
        {* <tr class="DgItem">
        <tr> <td> Application No: </td> <td> {{ [records].uid }} </td> </tr>
        </tr>  *}
    </table>
    """
    scrape_applic_types = """
    <select id="ddlAppType"> <option />
        {* <option value="{{ [options] }}" /> *}
    </select>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <td class="LowerMiddle">  {{ block|html }} </table>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <span id="lblApplicationNo"> {{ reference }} </span>
    <table id="TABLE3"> <td> Application Received {{ date_received }} </td> </table>
    <table class="details">
    <tr> <td> Location: </td> <td> {{ address }} </td> </tr>
    <tr> <td> Proposal: </td> <td> {{ description }} </td> </tr>
    <tr> <td> Registered Date: </td> <td> {{ date_validated }} </td> </tr>
    </table>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<span id="LblParish"> {{ parish }} </span>',
    '<table id="TABLE3"> <td> Comments Welcome By {{ consultation_end_date }} </td> </table>',
    '<table class="details"> <tr> <td> Type: </td> <td> {{ application_type }} </td> </tr> </tr> </table>',
    '<table class="details"> <tr> <td> Applicant: </td> <td> {{ applicant_name }} </td> </tr> </tr> </table>',
    '<table class="details"> <tr> <td> Case Officer: </td> <td> {{ case_officer }} </td> </tr> </tr> </table>',
    '<table class="details"> <tr> <td> Applicant Address: </td> <td> {{ applicant_address }} </td> </tr> </table>',
    '<table class="details"> <tr> <td> Agent Name: </td> <td> {{ agent_name }} </td> </tr> </table>',
    '<table class="details"> <tr> <td> Agent Address: </td> <td> {{ agent_address }} </td> </tr> </table>',
    '<table class="details"> <tr> <td> Consultation Start Date: </td> <td> {{ consultation_start_date }} </td> </tr> </table>', 
    '<table class="details"> <tr> <td> Earliest Decision Date: </td> <td> {{ target_decision_date }} </td> </tr> </table>', 
    '<table class="details"> <tr> <td> Committee or Delegated: </td> <td> {{ decided_by }} </td> </tr> </table>', 
    '<table class="details"> <tr> <td> Committee Date: </td> <td> {{ meeting_date }} </td> </tr> </table>', 
    '<table class="details"> <tr> <td> Decision: </td> <td> {{ decision }} </td> </tr> </table>',
    '<table class="details"> <tr> <td> Decision Date: </td> <td> {{ decision_date }} </td> </tr> </table>', 
    '<table class="details"> <tr> <td> Appeal Received Date: </td> <td> {{ appeal_date }} </td> </tr> </table>',
    '<table class="details"> <tr> <td> Appeal Decision: </td> <td> {{ appeal_result }} </td> </tr> </table>',
    '<table class="details"> <tr> <td> Appeal Decision Date: </td> <td> {{ appeal_decision_date }} </td> </tr> </table>', 
    '<span id="CNR">Conditions And Reasons:</span> {{ conditions }}',
    ]

    def __init__(self):
        self.br, self.handler, self.cj = util.get_browser(self.HEADERS)
        # Follows refresh 0 but not hangs on refresh > 0
        self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    def get_id_period (self, date):
        
        from_iso_dt, to_iso_dt = util.inc_dt(date.strftime(util.ISO8601_DATE), util.ISO8601_DATE, self.PERIOD_TYPE)
        from_dt = util.get_dt(from_iso_dt, util.ISO8601_DATE)
        to_dt = util.get_dt(to_iso_dt, util.ISO8601_DATE)
        
        this_date = date.strftime(self.request_date_format)
        date_parts = this_date.split('/')
        month = date_parts[1]
        year = date_parts[2]

        app_types = []

        # get disclaimer page
        response = self.br.open(self.start_url)

        # get search page
        form_ok = util.setup_form(self.br, self.search_form)
        response = util.submit_form(self.br)
        html = response.read()
                
        # get list of possible application types
        result = scrapemark.scrape(self.scrape_applic_types, html)
        #print result
        try:
            app_types = result['options']
        except:
            app_types = []

        final_result = []

        for apptype in app_types: # repeat query for each type = will not accept one query of all types

            interim_result = []

            # do date search
            fields = self.search_fields_date
            fields ['ddlmonth1'] = month
            fields ['ddlyear1'] = year
            fields ['ddlAppType'] = apptype
            form_ok = util.setup_form(self.br, self.search_form, fields)
            response = util.submit_form(self.br)
            
            html = response.read()
            url = response.geturl()
            #if self.DEBUG: print "first page:", html
            result = scrapemark.scrape(self.scrape_max, html)
            try:
                max_pages = int(result['max_pages'])
            except:
                max_pages = 1
            page_count = 1
            
            while page_count <= max_pages:
                result = scrapemark.scrape(self.scrape_ids, html, url)
                if result and result.get('records'):
                    self.clean_ids(result['records'])
                    interim_result.extend(result['records'])
                if page_count >= max_pages: break
                form_ok = util.setup_form(self.br, self.next_form, self.next_fields)
                response = util.submit_form(self.br)
                html = response.read()
                url = response.geturl()
                if self.DEBUG: print "next page:", html
                page_count += 1

            if self.DEBUG: print "Found %d applications for %s" % (len(interim_result), apptype)

            final_result.extend(interim_result)

            # back to search page
            response = self.br.open(self.search_url)

        if final_result:
            return final_result, from_dt, to_dt
        else:
            return [], None, None # monthly scraper - so empty result is always invalid

    def get_detail_from_uid (self, uid):

        try:
            # get disclaimer page
            response = self.br.open(self.start_url)
    
            # get search page
            form_ok = util.setup_form(self.br, self.search_form)
            response = util.submit_form(self.br)
    
            # get first application page
            fields = self.search_fields_applic
            fields ['ddlCaseType'] = uid[0:2]
            fields ['ddlCaseYear'] = uid[3:5]
            fields ['txtCaseNo'] = uid[6:11]
            if self.DEBUG: print "fields:", fields
            form_ok = util.setup_form(self.br, self.search_form, fields)
            response = util.submit_form(self.br)
            if self.DEBUG: print "first page:", response.read()
    
            # get second detailed application page
            form_ok = util.setup_form(self.br, self.search_form, self.detail_fields)
            response = util.submit_form(self.br)
            html = response.read()
            url = response.geturl()
            if self.DEBUG: print "detail page:", html
        except:
            if self.DEBUG: raise
            else: return None
        return self.get_detail(html, url)

if __name__ == 'scraper':

    scraper = SedgemoorScraper()
    scraper.run()

    #scraper.DEBUG = True

    #scraper.br.set_debug_http(True)
    # misc tests
    #print scraper.get_detail_from_uid ('08/11/00250')
    #result, dfrom, dto = scraper.get_id_period(util.get_dt('01/06/2012'))
    #print result, len(result), dfrom, dto
    #print util.inc_dt('2010-02-01', util.ISO8601_DATE, 'Month')
    #print "Found " + str(len(result)) + " ids for Mar 2012"
    #print scraper.gather_ids('2010-02-01')
    #print scraper.gather_ids(None, None)
    #scraper.gather_current_ids()
