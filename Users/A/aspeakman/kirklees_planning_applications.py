# this is a scraper of Kirklees planning applications for use by Openly Local

# currently designed to work backwards collecting applications from the current date to 1/1/2000

# also see Redcar and Glamorgan

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

class KirkleesScraper(base.DateScraper):

    date_from_field = 'ctl00$plhCenterCol$txtDateFrom'
    date_to_field = 'ctl00$plhCenterCol$txtDateTo'
    appno_field = 'ctl00$plhCenterCol$txtSearch'
    search_form = 'aspnetForm'
    advanced_submit = 'ctl00$plhCenterCol$btnAdvancedSearch'
    next_fields = { '__EVENTTARGET': 'ctl00$plhCenterCol$dgSearchResults$ctl01$ctl01', '__EVENTARGUMENT': '', 'ctl00$plhCenterCol$searchAgain': None }
    request_date_format = '%d/%m/%Y'
    start_url = 'http://www2.kirklees.gov.uk/business/planning/application_search/default.aspx'
    applic_url = 'http://www2.kirklees.gov.uk/business/planning/application_search/detail.aspx'
    scrape_ids = """
    <table id="ctl00_plhCenterCol_dgSearchResults"> 
    {* <div class="searchResult"> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </div>
     *}
    </table>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="page"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <span id="ctl00_plhCenterCol_lbl_number_formatted"> {{ reference }} </span>
    <span id="ctl00_plhCenterCol_lbl_development_locality"> {{ address }} </span>
    <span id="ctl00_plhCenterCol_lbl_development_description"> {{ description }} </span>
    <span id="ctl00_plhCenterCol_lbl_received_date"> {{ date_received }} </span>
    <span id="ctl00_plhCenterCol_lbl_registration_date"> {{ date_validated }} </span>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<span id="ctl00_plhCenterCol_lbl_last_updated"> {{ date_last_updated }} </span>',
    '<span id="ctl00_plhCenterCol_lbl_applicant_name"> {{ applicant_name }} </span>',
    '<span id="ctl00_plhCenterCol_lbl_ward"> {{ ward_name }} </span>',
    '<span id="ctl00_plhCenterCol_lbl_agent_name"> {{ agent_name }} </span>',
    '<span id="ctl00_plhCenterCol_lbl_agent_address"> {{ agent_address }} </span>',
    '<span id="ctl00_plhCenterCol_lbl_case_officer"> {{ case_officer }} </span>',
    '<span id="ctl00_plhCenterCol_lbl_public_consultation_start_date">{{ consultation_start_date }} </span>',
    '<span id="ctl00_plhCenterCol_lbl_public_consultation_end_date">{{ consultation_end_date }} </span>',
    '<span id="ctl00_plhCenterCol_lbl_decision_date">{{ decision_date }} </span>',
    '<span id="ctl00_plhCenterCol_lbl_decision_text">{{ decision }} </span>',
    '<span id="ctl00_plhCenterCol_lbl_appeal_lodged_date">{{ appeal_date }} </span>',
    ]

    def get_id_batch (self, date_from, date_to):

        response = util.open_url(self.br, self.start_url)
        form_ok = util.setup_form(self.br, self.search_form)
        response = util.submit_form(self.br, self.advanced_submit)
        if self.DEBUG: print "search page:", response.read()

        fields = {}
        date_from = date_from.strftime(self.request_date_format)
        date_to = date_to.strftime(self.request_date_format)
        fields[self.date_from_field] = date_from
        fields[self.date_to_field] = date_to

        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print "form:", self.br.form
        response = util.submit_form(self.br)
        
        final_result = []
        while response:
            html = response.read()
            url = response.geturl()
            if self.DEBUG: print "result page:", html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
                try:
                    util.setup_form(self.br, self.search_form, self.next_fields)
                    if self.DEBUG: print "form:", self.br.form
                    response = util.submit_form(self.br)
                except:
                    break
            else:
                break

        return final_result

    def get_detail_from_uid (self, uid):
        url = self.applic_url + '?id=' + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    scraper = KirkleesScraper()
    scraper.run()

    # misc tests
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('2011/92400')
    #res = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('18/08/2011'))
    #print len(res), res
    #print scraper.gather_ids('2012-02-01')
    #print scraper.gather_ids('2011-02-01', '2012-01-18')

