# this is a scraper of Flintshire planning applications for use by Openly Local

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

class FlintshireScraper(base.DateScraper):

    MAX_ID_BATCH = 350 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 250 # max application details to scrape in one go

    search_url = 'http://www.flintshire.gov.uk/wps/portal/english/planningapplications?new=true'
    date_from_field = 'FCC_PlanningApplicationsPortletFormDate1'
    date_to_field = 'FCC_PlanningApplicationsPortletFormDate2'
    ref_field = 'FCC_PlanningApplicationsPortletFormRef'
    request_date_format = '%d/%m/%Y'
    search_form = '1'
    next_link = 'Next'
    scrape_ids = """
    {* <table class="planningSearchResults">
    <tr> Number {{ [records].uid }} Status </tr>
    <tr> <a href="{{ [records].url|abs }}"> </a> </tr>
    </table> *}
    """
    scrape_data_block = """
    <table class="planningDocument"> {{ block|html }} </table>
    """
    scrape_min_data = """
    <tr> <td> Reference Number </td> <td> {{ reference }} </td> </tr>
    <tr> <td> Description </td> <td> {{ description }} </td> </tr>
    <tr> <td> Location </td> <td> {{ address }} </td> </tr>
    <tr> <td> Date Valid </td> <td> {{ date_validated }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr> <td> Status </td> <td> <p> {{ status }} <a /> </p> </td> </tr>',
    '<tr> <td> Comment By </td> <td> <p> {{ comment_date }} <a /> </p> </td> </tr>',
    '<tr> <td> Type of Application </td> <td> {{ application_type }} </td> </tr>',
    '<tr> <td> Easting: {{ easting }} / Northing: {{ northing }} </td> </tr>',
    '<tr> <td> Community </td> <td> {{ parish }} </td> </tr>',
    '<tr> <td> Ward </td> <td> {{ ward_name }} </td> </tr>',
    '<tr> <td> Applicant Name </td> <td> {{ applicant_name }} </td> </tr>',
    '<tr> <td> Agent Name </td> <td> {{ agent_name }} </td> </tr>',
    '<tr> <td> Applicant Address </td> <td> {{ applicant_address}} </td> </tr>',
    '<tr> <td> Agent Address </td> <td> {{ agent_address }} </td> </tr>',
    '<tr> <td> Case Officer </td> <td> {{ case_officer }} </td> </tr>',
    '<tr> <td> Decision Target Date </td> <td> {{ target_decision_date }} </td> </tr>',
    '<tr> <td> Committee Date </td> <td> <p> {{ meeting_date }} <a /> </p> </td> </tr>',
    '<tr> <td> Decision Level </td> <td> <p> {{ decided_by }} <a /> </p> </td> </tr>',
    '<tr> <td> Decision Date </td> <td> {{ decision_date }} </td> </tr>',
    '<tr> <td> Decision Type </td> <td> {{ decision }} </td> </tr>',
    '<tr> <td> Appeal Received Date </td> <td> {{ appeal_date }} </td> </tr>',
    """<tr> <td> Appeal Decision </td> <td> {{ appeal_result }} </td> </tr>
    <tr> <td> Appeal Decision Date </td> <td> {{ appeal_decision_date }} </td> </tr>""",
    ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)

        fields = {}
        fields [self.date_from_field] = date_from.strftime(self.request_date_format)
        fields [self.date_to_field] = date_to.strftime(self.request_date_format)
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
                response = self.br.follow_link(text=self.next_link)
            except:
                response = None

        return final_result

    def get_detail_from_uid (self, uid):
        
        response = self.br.open(self.search_url)
        fields = { self.ref_field: uid }
        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br)

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

    scraper = FlintshireScraper()
    scraper.run()

    # misc test calls
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('048879') # Flintshire OK
    #result = scraper.get_id_batch(util.get_dt('08/08/2012'), util.get_dt('18/08/2012'))
    #print len(result), result

    


