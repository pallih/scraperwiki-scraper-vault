# this is a scraper of Stevenage planning applications for use by Openly Local

# NB only goes back to 1/12/2005

# also see Ceredigion

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

class StevenageScraper(base.PeriodScraper):

    START_SEQUENCE = '2005-12-01' # gathers id data by working backwards from the current date towards this one
    MAX_ID_BATCH = 250 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 150 # max application details to scrape in one go
    PERIOD_TYPE = 'Sunday'
    HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
    'Accept-Charset': 'UTF-8,*',
    'Accept': 'text/html',
    'Accept-Language': 'en-gb,en',
    }
        
    search_form = 'RW'
    weekly_fields = {  'CTRL:110:_:A': 'WEEKLYLIST' }
    ref_fields = {  'CTRL:110:_:A': 'REFERENCE' }
    start_submit = 'CTRL:111:_:B'
    search_fields = { 'CTRL:122:_:A': 'RECEIVED' }
    search_date_submit = 'CTRL:123:_:B'
    search_ref_submit = 'CTRL:118:_:B'
    page_size = 10
    next_control = 'CTRL:124:_:E.h'
    next_fields = { 'CTRL:111:_:B': None, 'CTRL:123:_:B': None, 'CTRL:124:_:E.h': '>'}
    request_date_format = '%d/%m/%Y'
    start_url = 'https://eforms.stevenage.gov.uk/ufs/ufsmain?formid=REGISTER_OF_PLANNING_APPLICATIONS'
    scrape_max = """
    <span class="eb-124-tableNavRowInfo"> of {{ max_recs }} records</span>
    """
    scrape_ids = """
    <table class="eb-124-tableContent"> <tr />
        {* <tr>
        <td> <input value="{{ [records].uid }}"> </td>
        </tr> *}
    </table>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <table class="eb-1-VerticalBoxLayoutSurround"> {{ block|html }} </table>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <div id="CTID:6:_:A"> {{ reference }} </div>
    <div id="CTID:7:_:A"> {{ address|html }} </div>
    <div id="CTID:9:_:A"> {{ description }} </div>
    <div id="CTID:31:_:A"> {{ date_received }} </div>
    <div id="CTID:35:_:A> {{ date_validated }} </div>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<div id="CTID:10:_:A"> {{ application_type }} </div>',
    '<div id="CTID:64:_:A"> {{ decision }} </div>',
    '<div id="CTID:65:_:A"> {{ decided_by }} </div>',
    '<div id="CTID:8:_:A"> {{ ward_name }} </div>',
    '<div id="CTID:11:_:A"> {{ case_officer }} </div>',
    '<div id="CTID:38:_:A"> {{ meeting_date }} </div>',
    '<div id="CTID:66:_:A"> {{ decision_date }} </div>',
    '<div id="CTID:67:_:A"> {{ decision_issued_date }} </div>',
    '<div id="CTID:68:_:A"> {{ decision_published_date }} </div>',
    '<div id="CTID:13:_:A"> {{ status }} </div>',
    '<div id="CTID:33:_:A"> {{ target_decision_date }} </div>',
    '<div id="CTID:44:_:A"> {{ consultation_start_date }} </div>',
    '<div id="CTID:49:_:A"> {{ consultation_end_date }} </div>',
    '<div id="CTID:39:_:A"> {{ neighbour_consultation_start_date }} </div>',
    '<div id="CTID:41:_:A"> {{ neighbour_consultation_end_date }} </div>',
    '<div id="CTID:51:_:A"> {{ last_advertised_date }} </div>',
    '<div id="CTID:53:_:A"> {{ latest_advertisement_expiry_date }} </div>',
    '<div id="CTID:60:_:A"> {{ permission_expires_date }} </div>',
    '<div id="CTID:72:_:A"> {{ associated_application_uid }} </div>',
    '<div id="CTID:73:_:A"> {{ appeal_status }} </div>',
    '<div id="CTID:74:_:A"> {{ appeal_date }} </div>',
    '<div id="CTID:75:_:A"> {{ appeal_result }} </div>',
    '<div id="CTID:76:_:A"> {{ appeal_decision_date }} </div>',
    '<div id="CTID:55:_:A"> {{ site_notice_start_date }} </div>',
    '<div id="CTID:57:_:A"> {{ site_notice_end_date }} </div>',
    ]
        
    def get_id_period (self, date):
        
        from_dmy_dt, to_dmy_dt = util.inc_dt(date.strftime(util.DATE_FORMAT), util.DATE_FORMAT, self.PERIOD_TYPE)
        from_dt = util.get_dt(from_dmy_dt, util.DATE_FORMAT)
        to_dt = util.get_dt(to_dmy_dt, util.DATE_FORMAT)
        
        this_week = from_dmy_dt + '-' + to_dmy_dt

        # open with jscheck page
        response = self.br.open(self.start_url)
        html = response.get_data()
        response.set_data(html.replace('<!--', '')) # remove mismatched html comment mark
        self.br.set_response(response)
        form_ok = util.setup_form(self.br)
        response = util.submit_form(self.br)
        if self.DEBUG: print "start page:", response.read()

        # got start page
        form_ok = util.setup_form(self.br, self.search_form, self.weekly_fields)
        if self.DEBUG: print "form:", self.br.form
        response = util.submit_form(self.br, self.start_submit)
        if self.DEBUG: print "search page:", response.read()

        # do date search
        fields = self.search_fields
        fields ['CTRL:121:_:A'] = this_week
        response = None
        try:
            form_ok = util.setup_form(self.br, self.search_form, fields)
            if self.DEBUG: print "form:", self.br.form
            response = util.submit_form(self.br, self.search_date_submit)
        except:
            pass # sometimes the most recent week is not yet available as a selectable option

        if not response:
            return [], None, None

        html = response.read()
        url = response.geturl()
        if self.DEBUG: print "first page:", html
        result = scrapemark.scrape(self.scrape_max, html)
        try:
            max_recs = int(result['max_recs'])
        except:
            max_recs = self.page_size
        
        final_result = []
        while len(final_result) < max_recs:
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
                if len(final_result) >= max_recs: break
                util.setup_form(self.br, self.search_form)
                self.br.form.new_control('submit', self.next_control, {'value':'>'} )
                self.br.form.fixup()
                if self.DEBUG: print "form:", self.br.form
                response = util.submit_form(self.br, self.next_control)
                html = response.read()
                url = response.geturl()
                if self.DEBUG: print "next page:", html
            else:
                break

        return final_result, from_dt, to_dt # note weekly result might some times be legitimately empty
        
    def get_detail_from_uid (self, uid):

        try:
            # open with jscheck page
            response = self.br.open(self.start_url)
            html = response.get_data()
            response.set_data(html.replace('<!--', '')) # remove mismatched html comment mark
            self.br.set_response(response)
            form_ok = util.setup_form(self.br)
            response = util.submit_form(self.br)
            if self.DEBUG: print "start page:", response.read()

            # got start page
            form_ok = util.setup_form(self.br, self.search_form, self.ref_fields)
            if self.DEBUG: print "form:", self.br.form
            response = util.submit_form(self.br, self.start_submit)
            if self.DEBUG: print "search page:", response.read()

            # do ref search
            fields = {}
            fields ['CTRL:117:_:A'] = uid
            form_ok = util.setup_form(self.br, self.search_form, fields)
            if self.DEBUG: print "form:", self.br.form
            response = util.submit_form(self.br, self.search_ref_submit)
    
            html = response.read()
            url = response.geturl()
            if self.DEBUG: print "reference page:", html
        except:
            if self.DEBUG: raise
            else: return None
        return self.get_detail(html, url)

if __name__ == 'scraper':

    scraper = StevenageScraper()
    scraper.run()

    #scraper.DEBUG = True

    #scraper.br.set_debug_http(True)
    # misc tests
    #print scraper.get_detail_from_uid ('11/00694/FP')
    #result, dfrom, dto = scraper.get_id_period(util.get_dt('17/03/2012'))
    #print result, len(result), dfrom, dto
    
