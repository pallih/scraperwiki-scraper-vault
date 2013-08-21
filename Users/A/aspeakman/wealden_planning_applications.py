# this is a scraper of Wealden planning applications for use by Openly Local

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import random
import urllib

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

class WealdenScraper(base.DateScraper):

    MAX_ID_BATCH = 250 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go

    search_url = 'http://www.planning.wealden.gov.uk/disclaimer.aspx?returnURL=%2fadvsearch.aspx'
    ck = {
        'name': 'AspxAutoDetectCookieSupport',
        'value': '1',
        'domain': 'www.planning.wealden.gov.uk',
        }
    date_from_field = 'ctl00$ContentPlaceHolder1$txtDateReceivedFrom$dateInput'
    date_to_field = 'ctl00$ContentPlaceHolder1$txtDateReceivedTo$dateInput'
    ref_field = 'ctl00$ContentPlaceHolder1$txtAppNumber'
    ref_submit = 'ctl00$ContentPlaceHolder1$btnSearch2'
    search_submit = 'ctl00$ContentPlaceHolder1$btnSearch3'
    search_fields =  { '__EVENTTARGET': '', '__EVENTARGUMENT': '' }
    next_submit = 'ctl00$ContentPlaceHolder1$lvResults$RadDataPager1$ctl02$NextButton'
    request_date_format = '%Y-%m-%d-00-00-00'
    search_form = 'aspnetForm'
    scrape_max_pages = '<div class="rdpWrap"> of {{ max_pages }} </div>'

    scrape_ids = """
    <div id="news_results_list">
    {* <div>
    <h2> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </h2>
    </div> *}
    </div>
    """
    scrape_data_block = """
    <div id="contenttext"> {{ block|html }} </div>
    """
    scrape_min_data = """
    <span class="applabel"> Application No </span> <p> {{ reference }} </p>
    <span class="applabel"> Proposal </span> <p> {{ description }} </p>
    <span class="applabel"> Received Date </span> <p> {{ date_received }} </p>
    <span class="applabel"> Valid Date </span> <p> {{ date_validated }} </p>
    <span class="applabel"> Address </span> <p> {{ address }} </p>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<span class="applabel"> Type </span> <p> {{ application_type }} </p>',
    '<span class="applabel"> Case Officer </span> <p> {{ case_officer }} </p>',
    '<span class="applabel"> Status </span> <p> {{ status }} </p>',
    '<span class="applabel"> Committee/Delegated </span> <p> {{ decided_by }} </p>',
    '<span class="applabel"> Committee/Delegated Date </span> <p> {{ meeting_date }} </p>',
    '<span class="applabel"> Decision Date </span> <p> {{ decision_date }} </p>',
    '<span class="applabel"> Advert Expiry </span> <p> {{ latest_advertisement_expiry_date }} </p>',
    '<span class="applabel"> Neighbour Expiry </span> <p> {{ neighbour_consultation_end_date }} </p>',
    """<span class="applabel"> Site Notice Expiry </span> <p> {{ site_notice_end_date }} </p>
    <span class="applabel"> Decision </span> <p> {{ decision }} </p>""",
    '<span class="applabel"> Issue Date </span> <p> {{ decision_issued_date }} </p>',
    '<span class="applabel"> Ward </span> <p> {{ ward_name }} </p>',
    '<span class="applabel"> Parish </span> <p> {{ parish }} </p>',
    '<span class="applabel"> UPRN </span> <p> {{ uprn }} </p>',
    '<span class="applabel"> Easting </span> <p> {{ easting }} </p>',
    '<span class="applabel"> Northing </span> <p> {{ northing }} </p>',
    ]

    def __init__(self):
        self.br, self.handler, self.cj = util.get_browser(self.HEADERS)
        util.set_cookie(self.cj, self.ck['name'], self.ck['value'], self.ck.get('domain'), self.ck.get('path', '/'))   

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)

        util.setup_form(self.br, self.search_form)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br)

        fields = self.search_fields
        fields [self.date_from_field] = date_from.strftime(self.request_date_format)
        fields [self.date_to_field] = date_to.strftime(self.request_date_format)

        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br, self.search_submit)
        html = response.read()

        try:
            result = scrapemark.scrape(self.scrape_max_pages, html)
            max_pages = int(result['max_pages'])
        except:
            max_pages = 0
        if self.DEBUG: print max_pages

        current_page = 0
        final_result = []
        while response and current_page < max_pages:
            url = response.geturl()
            if self.DEBUG: print html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            else:
                break
            current_page += 1
            if current_page >= max_pages: break
            try:
                util.setup_form(self.br, self.search_form)
                if self.DEBUG: print self.br.form
                response = util.submit_form(self.br, self.next_submit)
                html = response.read()
            except:
                response = None
            
        return final_result

    def get_detail_from_uid (self, uid):
        
        response = self.br.open(self.search_url)

        util.setup_form(self.br, self.search_form)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br)

        fields = { self.ref_field: uid }
        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br, self.ref_submit)

        try:
            html = response.read()
            if self.DEBUG: print html
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            self.clean_ids(result['records'])
            url = result['records'][0]['url']
        except:
            return None

        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    scraper = WealdenScraper()
    scraper.run()

    # misc test calls
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('WD/2011/1512/LDP')
    #result = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('09/08/2011'))
    #print len(result), result

    




