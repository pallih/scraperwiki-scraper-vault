# this is a scraper of Braintree planning applications for use by Openly Local

# also see Hyndburn and Monmouthshire

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import urllib

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

class BraintreeScraper(base.DateScraper):

    MAX_ID_BATCH = 350 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 250 # max application details to scrape in one go

    date_from_field = 'startDate'
    date_to_field = 'endDate'
    request_date_format = '%d/%m/%Y'
    query_fields = { 'action2': 'Search'  }
    search_url = 'http://planningapp.braintree.gov.uk/WAM1/findCaseFile.do'
    applic_url = 'http://planningapp.braintree.gov.uk/WAM1/showCaseFile.do?action=show&appType=Planning'
    scrape_ids = """
    <table id="passearchresults"> <tr />
    {* <tr> <td />
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    <td /> <td> {{ [records].status }} </td>
    </tr> *}
    </table>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="wamcontent"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <table id="casefilesummary">
    <tr> <th id="development" /> <td> {{ description }} </td> </tr>
    <tr> <th id="location" /> <td> {{ address }} </td> </tr>
    <tr> <th id="appno" /> <td> {{ reference }} </td>
         <th id="regdate" /> <td> {{ date_received }} </td>
    </tr>
    <tr> <th id="decdate"> Validation/Registration date: </th> <td> {{ date_validated }} </td> </tr>
    </table>"""
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr> <th id="applicant" /> <td> {{ applicant_name }} <br> {{ applicant_address }} </td> </tr>',
    '<tr> <th id="agent" /> <td> {{ agent_name }} <br> {{ agent_address }} </td> </tr>',
    '<tr> <th id="decdate"> End date of Public Consultation </th> <td> {{ consultation_end_date }} </td> </tr>',
    '<tr> <th id="dectype"> Start date of Public Consultation: </th> <td> {{ consultation_start_date }} </td> </tr>',
    '<tr> <th id="caseofficer" /> <td> {{ case_officer }} </td> </tr>',
    '<tr> <th id="apptype"> Application Type: </th> <td> {{ application_type }} </td> </tr>',
    '<p id="comment"> <a href="{{ comment_url|abs }}" /> </p>',
    '<tr> <th id="parish" /> <td> {{ parish }} </td> </tr>',
    '<tr> <th id="dectype"> Decision Type: </th> <td> {{ decision }} </td> </tr>',
    '<tr> <th id="decdate"> Decision date: </th> <td> {{ decision_date }} </td> </tr>',
    ]

    def get_id_batch (self, date_from, date_to):

        dt_to = date_to.strftime(util.ISO8601_DATE) # dates 2/3/2008 to 16/3/2008 cause 500 error
        if dt_to == '2008-03-16':
            date_to = date(2008,3,8)

        fields = self.query_fields
        fields [self.date_from_field] = date_from.strftime(self.request_date_format) 
        fields [self.date_to_field] = date_to.strftime(self.request_date_format)

        final_result = []
        
        response = util.open_url(self.br, self.search_url, fields, 'POST')
        if response:
            html = response.read()
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])

        return final_result

    def get_detail_from_uid (self, uid):
        url = self.applic_url + '&appNumber=' + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    scraper = BraintreeScraper()
    scraper.run()

    #scraper.DEBUG = True

    # misc tests
    #print scraper.get_detail_from_uid ('12/00467/FUL')
    #result = scraper.get_id_batch(util.get_dt('03/04/2012'), util.get_dt('05/04/2012'))
    #print len(result), result
    #print scraper.gather_ids('2010-02-01')
    #print scraper.gather_ids(None, None)
    #scraper.gather_current_ids()

    #util.rename_column(scraper.TABLE_NAME, 'decision_type', 'decision')


