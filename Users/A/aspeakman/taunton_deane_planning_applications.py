# this is a scraper of Taunton Deane planning applications for use by Openly Local

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

class TauntonDeaneScraper(base.DateScraper):

    MAX_ID_BATCH = 120 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 100 # max application details to scrape in one go

    search_url = 'http://www1.tauntondeane.gov.uk/tdbcsites/plan/plapplookup.asp'
    applic_url = 'http://www1.tauntondeane.gov.uk/tdbcsites/plan/PlAppDets.asp?casefullref='
    date_from_field = 'regdate1'
    date_to_field = 'regdate2'
    request_date_format = '%d/%m/%Y'
    search_form = '0'
    search_fields = { 'ViewAll': 'All' }
    address_regex = re.compile(r'\s+AT\s+(.+?)\s*(\([^\)]+\)\s*|AS\s+AMENDED.*?)?$', re.I) # matches AT address at the end of the proposal (ignoring case)
    nonalpha_regex = re.compile(r'\W') # excludes anything non-alphanumeric
    scrape_ids = """
    <div class="z-content">
    {* <table>
    <tr> <td> <a href="{{ [records].url|abs }}">
    Application number : {{ [records].uid }} </a> </td> </tr>
    </table> *}
    <hr /> </div>
    """
    scrape_data_block = """
    <table> {{ block|html }} </table>
    """
    scrape_min_data = """
    <tr> <th> Application Number </th> <td> {{ reference }} </td> </tr>
    <tr> <th> Received </th> <td> {{ date_received }} </td> </tr>
    <tr> <th> Registered </th> <td> {{ date_validated }} </td> </tr>
    <tr> <th> Proposal </th> <td> {{ description }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr> <th> Application Status </th> <td> {{ status }} </td> </tr>',
    '<tr> <th> Application Type </th> <td> {{ application_type }} </td> </tr>',
    '<tr> <th> Parish </th> <td> {{ parish }} </td> </tr>',
    '<tr> <th> Status </th> <td> {{ status }} </td> </tr>',
    '<tr> <th> Officer </th> <td> {{ case_officer }} </td> </tr>',
    '<tr> <th> Target Decision Date </th> <td> {{ target_decision_date }} </td> </tr>',
    '<tr> <td> Consultation Period </th> <td> {{ consultation_start_date }} - {{ consultation_end_date }} </td> </tr>',
    '<tr> <th> Applicant </th> <td> {{ applicant_name }} </td> </tr>',
    """<tr> <th> Correspondent </th> <td> {{ agent_name|html }} </td> </tr>
    <tr> <th> Correspondent Address </th> <td> {{ agent_address|html }} </td> </tr>""",
    ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)

        fields = self.search_fields
        fields [self.date_from_field] = date_from.strftime(self.request_date_format)
        fields [self.date_to_field] = date_to.strftime(self.request_date_format)

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
        url = self.applic_url + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

    # scrape detailed information on one record given its HTML and URL
    def get_detail (self, html, url, scrape_data_block = None, scrape_min_data = None, scrape_optional_data = []):
        result = base.DateScraper.get_detail(self, html, url, scrape_data_block, scrape_min_data, scrape_optional_data)
        if not result: return None
        if result.get('description'):
            address_match = self.address_regex.search(result['description'])
            if address_match and address_match.group(1):
                address = address_match.group(1)
                result['address'] = address
                try:
                    address_lower = self.nonalpha_regex.sub('', address.lower())
                    agent_address_lower = self.nonalpha_regex.sub('', result['agent_address'].lower())
                    if agent_address_lower.find(address_lower) >= 0: # if the address matches the agent address, use that, as it is likely to contain a postcode
                        result['address'] = result['agent_address']
                except:
                    pass
            else:
                result['address'] = result['description']
        return result

if __name__ == 'scraper':

    scraper = TauntonDeaneScraper()
    scraper.run()

    # misc test calls
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('17/11/0006')
    #result = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('18/08/2011'))
    #print len(result), result

    



