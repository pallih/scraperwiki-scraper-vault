# this is a scraper of Elmbridge planning applications for use by Openly Local

# note no url for each application - uid only

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import urllib
import urlparse

base = scraperwiki.utils.swimport("openlylocal_base_scraper")
scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")

class ElmbridgeScraper(base.DateScraper):

    ID_ORDER = 'uid desc'
    date_from_field = 'X.searchCriteria_StartDate'
    date_to_field = 'X.searchCriteria_EndDate'
    search_form = 'ActionForm'
    search_fields = { 'ACTION': 'NEXT', }
    start_url = 'http://www2.elmbridge.gov.uk/Planet/ispforms.asp?serviceKey=SysDoc-PlanetApplicationEnquiry'
    next_fields = { 'ACTION': 'NEXT', 'X.searchCriteria_ApplicationReference': '', 'X.searchDirection': 'NEXT', }
    scrape_max = '<table id="inputTable"> <td> {{ max_recs }} applications have been found. </td> </table>'
    ref_field = 'X.searchCriteria_ApplicationReference'
    scrape_ids = """
    <table id="inputTable"> <table>
    {* <tr>  <td> <a> {{ [records].uid }} </a> </td>  </tr>
    *}
    </table> </table>
    """

    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <h2> Planning Application Enquiry </h2> <table /> <table> {{ block|html }} </table>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <td> Application Reference: {{ reference }} </td>
    <tr class="tableDetails"> <td> Site Address </td> <td> {{ address }} </td> <td> {{ description }} </td> </tr>
    <tr class="tableDetails"> <td> Date Received </td> <td> {{ date_received }} </td> </tr>
    <tr class="tableDetails"> <td> Date Validated </td> <td> {{ date_validated }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr class="tableDetails"> <td> Application Type </td> <td> {{ application_type }} </td> </tr>',
    '<tr class="tableDetails"> <td> Ward </td> <td> {{ ward_name }} </td> </tr>',
    '<tr class="tableDetails"> <td> Coordinate </td> <td> {{ easting }} , {{ northing }} </td> </tr>',
    '<tr class="tableDetails"> <td> Current Status </td> <td> {{ status }} </td> </tr>',
    '<tr class="tableDetails"> <td> Decision Details </td> <td> {{ decision }} </td> </tr>',
    '<tr class="tableDetails"> <td> Decision Date </td> <td> {{ decision_date }} </td> </tr>',
    '<tr class="tableDetails"> <td> Decision By </td> <td> {{ decided_by }} </td> </tr>',
    '<tr class="tableDetails"> <td> Response Date </td> <td> {{ target_decision_date }} </td> </tr>',
    '<tr class="tableDetails"> <td> Handling Officer </td> <td> {{ case_officer }} </td> </tr>',
    '<tr class="tableDetails"> <td> Committee Date </td> <td> {{ meeting_date }} </td> </tr>',
    '<tr class="tableDetails"> <td> Response Date </td> <td> {{ target_decision_date }} </td> </tr>',
    '<tr class="tableDetails"> <td> Start of Consultation </td> <td> {{ consultation_start_date }} </td> </tr>',
    '<tr class="tableDetails"> <td> End of Consultation </td> <td> {{ consultation_end_date }} </td> </tr>',
    '<tr class="tableDetails"> <td> Appeal Lodged Date </td> <td> {{ appeal_date }} </td> </tr>',
    '<tr class="tableDetails"> <td> Appeal Decision Date </td> <td> {{ appeal_decision_date }} </td> </tr>',
    '<tr class="tableDetails"> <td> Associated Planning Applications </td> <td> <a> {{ associated_application_uid }} </a> </td> </tr>',
    """<tr class="tableDetails"> <td> Name </td> <td> {{ applicant_name }} </td> 
    <td> Name </td> <td> {{ agent_name }} </td> </tr>
    <tr class="tableDetails"> <td> Address </td> <td> {{ applicant_address }} </td> 
    <td> Address </td> <td> {{ agent_address }} </td> </tr>
    <tr class="tableDetails"> <td> Telephone </td> <td> {{ agent_tel }} </td> </tr>""",
    ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.start_url)

        self.search_fields[self.date_from_field] = date_from.strftime(self.request_date_format)
        self.search_fields[self.date_to_field] = date_to.strftime(self.request_date_format)
        util.setup_form(self.br, self.search_form, self.search_fields )
        response = util.submit_form(self.br)

        html = response.read()
        if self.DEBUG: print "result page:", html
        try:
            result = scrapemark.scrape(self.scrape_max, html)
            max_recs = int(result['max_recs'])
        except:
            max_recs = 0
        if self.DEBUG: print "max recs:", max_recs

        final_result = []
        while response and len(final_result) < max_recs:
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            else:
                break
            if len(final_result) >= max_recs: break
            try:
                util.setup_form(self.br, self.search_form, self.next_fields  )
                response = util.submit_form(self.br)
                html = response.read()
            except:
                response = None
        return final_result

    def get_detail_from_uid (self, uid):

        try:
            response = self.br.open(self.start_url)

            fields = { self.ref_field: uid }
            util.setup_form(self.br, self.search_form, fields )
            response = util.submit_form(self.br)

            html = response.read()
            url = response.geturl()
            if self.DEBUG: print "detail page:", html
        except:
            if self.DEBUG: raise
            else: return None
        return self.get_detail(html, url)

if __name__ == 'scraper':

    scraper = ElmbridgeScraper()
    #scraper.clear_all()
    scraper.run()

    #scraper.DEBUG = True

    # misc test calls
    #print scraper.get_detail_from_uid ('2012/3631')
    #result = scraper.get_id_batch(util.get_dt('08/10/2012'), util.get_dt('18/10/2012'))
    #print len(result), result
    #print scraper.get_id_batch(util.get_dt('23/03/2012'), util.get_dt('25/03/2012'))


