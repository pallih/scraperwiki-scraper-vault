# this is a base scraper for Idox system planning applications for use by Openly Local

# CSC

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
import gc

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

systems = {
    'Cornwall': 'CornwallScraper',
     }

class IdoxScraper(base.DateScraper):

    MAX_ID_BATCH = 300 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go

    date_from_field = 'date(applicationReceivedStart)'
    date_to_field = 'date(applicationReceivedEnd)'
    search_form = 'searchCriteriaForm'
    request_date_format = '%d/%m/%Y'
    ref_field = 'searchCriteria.reference'
    scrape_ids = """
    <ul id="searchresults">
    {* <li>
    <a href="{{ [records].url|abs }}" />
    <p> No: {{ [records].uid }} <span />
    </li> *}
    </ul>
    """
    scrape_next_link = '<p class="pager top"> <a href="{{ next_link }}" class="next"> </a> </p>'
    scrape_dates_link = '<a id="subtab_dates" href="{{ dates_link|abs }}" />'
    scrape_info_link = '<a id="subtab_details" href="{{ info_link|abs }}" />'

    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = '<body> {{ block|html }} </body>'
    scrape_dates_block = '<body> {{ block|html }} </body>'
    scrape_info_block = '<body> {{ block|html }} </body>'
    # the minimum acceptable valid dataset on each page
    scrape_min_data = """
    <th> Reference </th> <td> {{ reference }} </td>
    <th> Address </th> <td> {{ address }} </td>
    <th> Proposal </th> <td> {{ description }} </td>
    """
    scrape_min_dates = """
    <th> Validated </th> <td> {{ date_validated }} </td>
    """
    scrape_min_info = """
    <th> Application Type </th> <td> {{ application_type }} </td>
    """
    # other optional parameters on a page
    scrape_optional_data = [
    '<th> Received </th> <td> {{ date_received }} </td>',
    '<th> Planning Portal Reference </th> <td> {{ planning_portal_id }} </td>',
    '<th> Alternative Reference </th> <td> {{ reference }} </td>',
    '<th> Status </th> <td> {{ status }} </td>',
    '<th> Status </th> <td> {{ status }} </td> <th> Appeal Status </th> <td> {{ appeal_result }} </td>',
    '<th> Appeal Received </th> <td> {{ appeal_date }} </td>',
    '<a id="tab_makeComment" href="{{ comment_url|abs }}"/>',
    '<a id="tab_neighbourComments" href="{{ comment_url|abs }}"/>',
    ]
    scrape_optional_info = [
    '<th> Parish </th> <td> {{ parish }} </td>',
    '<th> Community Council </th> <td> {{ parish }} </td>',
    '<th> Ward </th> <td> {{ ward_name }} </td>',
    '<th> Case Officer </th> <td> {{ case_officer }} </td>',
    '<th> Applicant Name </th> <td> {{ applicant_name }} </td>',
    '<th> Applicant Address </th> <td> {{ applicant_address }} </td>',
    '<th> Agent Name </th> <td> {{ agent_name }} </td>',
    '<th> Agent Company </th> <td> {{ agent_name }} </td>',
    '<th> Agent Address </th> <td> {{ agent_address }} </td>',
    '<th> Agent Phone Number </th> <td> {{ agent_tel }} </td>',
    '<th> Decision </th> <td> {{ decision }} </td> <th> Decision Level </th> <td> {{ decided_by }} </td>',
    ]
    scrape_optional_dates = [
    '<th> Received </th> <td> {{ date_received }} </td>',
    '<th> Expiry Date </th> <td> {{ application_expires_date }} </td> Committee Date',
    '<th> Committee Date </th> <td> {{ meeting_date }} </td>',
    '<th> Determination Deadline </th> <td> {{ target_decision_date }} </td>',
    '<th> Target Determination Date </th> <td> {{ target_decision_date }} </td>',
    '<th> Neighbour Consultation Date </th> <td> {{ neighbour_consultation_start_date }} </td>',
    '<th> Neighbour Consultation Expiry </th> <td> {{ neighbour_consultation_end_date }} </td>',
    '<th> Standard Consultation Date </th> <td> {{ consultation_start_date }} </td>',
    '<th> Standard Consultation Expiry </th> <td> {{ consultation_end_date }} </td>',
    '<th> Site Notice Posted Date </th> <td> {{ site_notice_start_date }} </td>',
    '<th> Site Notice Expiry Date </th> <td> {{ site_notice_end_date }} </td>',
    '<th> Advertised In Press </th> <td> {{ last_advertised_date }} </td>',
    '<th> Advertisement Expiry Date  </th> <td> {{ latest_advertisement_expiry_date }} </td>',
    '<th> Decision Issued Date </th> <td> {{ decision_issued_date }} </td>',
    '<th> Decision Printed Date </th> <td> {{ decision_published_date }} </td>',
    '<th> Decision Made Date </th> <td> {{ decision_date }} </td>',
    '<th> Permission Expiry Date  </th> <td> {{ permission_expires_date }} </td>',
    ]

    def get_id_batch (self, date_from, date_to):

        if self.DEBUG: self.br.set_debug_http(True)

        response = self.br.open(self.search_url)

        fields = {}
        fields[self.date_from_field] = date_from.strftime(self.request_date_format)
        fields[self.date_to_field] = date_to.strftime(self.request_date_format)
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
                result = scrapemark.scrape(self.scrape_next_link, html, url)
                response = self.br.open(result['next_link'])
            except:
                response = None
        return final_result

    def get_detail_from_uid (self, uid):
        response = self.br.open(self.search_url)
        fields = {}
        fields[self.ref_field] = uid
        util.setup_form(self.br, self.search_form, fields)
        response = util.submit_form(self.br)
        return self.get_these_details(response)

    # scrape detailed information on one record via its access URL
    def get_detail_from_url (self, url):
        try:
            response = self.br.open(url)
        except:
            if self.DEBUG: raise
            else: return None
        return self.get_these_details(response)

    def get_these_details(self, response):
        html = response.read()
        if self.DEBUG:
                print "Html obtained from details url:", html
        this_url = response.geturl()
        if self.DEBUG: print "Url:", this_url
        
        result = self.get_detail(html, this_url)
        if result:
            try:
                temp_result = scrapemark.scrape(self.scrape_dates_link, html, this_url)
                dates_url = temp_result['dates_link']
                if self.DEBUG: print dates_url
                response = self.br.open(dates_url)
                html = response.read()
                url = response.geturl()
                if self.DEBUG:
                    print "Html obtained from dates url:", html
                result2 = self.get_detail(html, url, self.scrape_dates_block, self.scrape_min_dates, self.scrape_optional_dates)
                if result2:
                    result.update(result2)
            except:
                pass  
            try:
                temp_result = scrapemark.scrape(self.scrape_info_link, html, this_url)
                info_url = temp_result['info_link']
                if self.DEBUG: print info_url
                response = self.br.open(info_url)
                html = response.read()
                url = response.geturl()
                if self.DEBUG:
                    print "Html obtained from info url:", html
                result3 = self.get_detail(html, url, self.scrape_info_block, self.scrape_min_info, self.scrape_optional_info)
                if result3:
                    result.update(result3)
            except:
                pass
            if result.get('reference') and not result.get('planning_portal_id') and result['reference'].startswith('PP-'):
                result['planning_portal_id'] = result['reference']
                del result['reference']
        return result

class AylesburyValeScraper(IdoxScraper): # does not like delivering large nos - limit requests to 7 days

    BATCH_DAYS = 7 # batch size for each scrape - number of days to gather to produce at least one result each time
    MIN_DAYS = 10 # min number of days to get when gathering current ids
    search_url = 'http://publicaccess.aylesburyvaledc.gov.uk/online-applications/search.do?action=advanced'
    date_from_field = 'date(applicationValidatedStart)'
    date_to_field = 'date(applicationValidatedEnd)'

class CornwallScraper(IdoxScraper):

    search_url = 'http://planning.cornwall.gov.uk/online-applications/pagedSearchResults.do?action=advanced&searchCriteria.simpleSearchString=Angarrack'

if __name__ == 'scraper':

    #scraper = GlasgowScraper('Glasgow')
    #scraper.run()
    #scraperwiki.sqlite.execute("alter table 'Cairngroms' rename to 'Cairngorms'")
    #scraperwiki.sqlite.commit()
    #sys.exit()

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
            scraper = None
            gc.collect()
        except Exception as err:
            print "Error - skipping this authority -", str(err)
    print "Finished"

    # misc test calls
    #scraper = AylesburyValeScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/01736/APP') # AylesburyVale OK
    #scraper = BromleyScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('12/02973/FULL6') # Bromley OK
    #scraper = EastRenfrewshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('2011/0523/TP') # EastRenfrewshire OK
    #scraper = EdinburghScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/02705/FUL') # Edinburgh OK
    #scraper = HinckleyScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('12/00774/HOU') # Hinckley OK
    #scraper = LichfieldScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/00878/FUL') # Lichfield OK
    #scraper = MerthyrTydfilScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('P/12/0223') # MerthyrTydfil OK  
    #scraper = SouthamptonScraper()
    #scraper.DEBUG = True
    #scraper.br.set_debug_http(True)
    #print scraper.get_detail_from_uid ('11/01790/FULLS') # Southampton NOT WORKING
    #scraper = TestValleyScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/01790/FULLS') # TestValley OK

    #res = scraper.get_id_batch(util.get_dt('27/08/2012'), util.get_dt('28/08/2012'))
    #print res, len(res)



