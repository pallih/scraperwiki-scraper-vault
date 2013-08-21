# this is a scraper of Cheshire East planning applications for use by Openly Local

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

class CheshireEastScraper(base.DateScraper):

    MAX_ID_BATCH = 350 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 250 # max application details to scrape in one go

    search_url = 'http://planning.cheshireeast.gov.uk/AdvancedSearch.aspx'
    applic_url = 'http://planning.cheshireeast.gov.uk/applicationdetails.aspx?pr='
    date_from_field = 'ctl00$ContentPlaceHolder1$txtDateRegisteredFrom'
    date_to_field = 'ctl00$ContentPlaceHolder1$txtDateRegisteredTo'
    next_link = 'Next page'
    request_date_format = '%d/%m/%Y'
    search_form = '1'
    search_submit = 'ctl00$ContentPlaceHolder1$btnAdvancedSearch'
    search_fields = {
        'ctl00$ContentPlaceHolder1$optResultsTo': 'map',
        'ctl00$ContentPlaceHolder1$txtJSEnabled': '1',
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        }
    scrape_ids = """
    <div id="searchResults">
    {* <div>
    <p> <a href="{{ [records].url|abs }}"> Planning ref {{ [records].uid }} </a> </p>
    </div> *}
    </div>
    """
    scrape_data_block = """
    <div id="detailscontainer"> {{ block|html }} </div>
    """
    scrape_min_data = """
    <h3> Reference Number </h3> <span> {{ reference }} </span>
    <h3> Location </h3> <span> {{ address }} </span>
    <h3> Proposal </h3> <span> {{ description }} </span>
    <h3> Date Registered </h3> <p> {{ date_validated }} </p>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<h3> Type of Application </h3> <span> {{ application_type }} </span>',
    '<h3> Case Officer </h3> <span> {{ case_officer }} </span>',
    '<h3> Status </h3> <span> {{ status }} </span>',
    '<h3> Ward / Parish </h3> <span> {{ ward_name }} / {{ parish }} </span>', 
    '<h3> Decision / Date Decision Made </h3> <span> {{ decision }} / {{ decision_date }} </span>',
    '<h3> Committee Date </h3> <p> {{ meeting_date }} </p>',
    '<h3> Last Date For Submitting Comments </h3> <p> {{ consultation_end_date }} </p>',
    '<h3> Decision Target Date </h3> <p> {{ target_decision_date }} </p>',
    '<h3> Applicant Name </h3> <span> {{ applicant_name }} </span>',
    '<h3> Agent Name </h3> <span> {{ agent_name }} </span>',
    '<h3> Applicant Address </h3> <span> {{ applicant_address }} </span>',
    '<h3> Agent Address </h3> <span> {{ agent_address }} </span>',
    ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)

        fields = self.search_fields
        fields [self.date_from_field] = date_from.strftime(self.request_date_format)
        fields [self.date_to_field] = date_to.strftime(self.request_date_format)

        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br, self.search_submit)
        
        final_result = []
        while response:
            url = response.geturl()
            html = response.read()
            if self.DEBUG: print html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            else:
                break
            try:
                response = self.br.follow_link(text=self.next_link)
            except:
                break
            
        return final_result

    def get_detail_from_uid (self, uid):
        url = self.applic_url + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    scraper = CheshireEastScraper()
    scraper.run()

    # misc test calls
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/3076N')
    #result = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('08/08/2011'))
    #print len(result), result

    





