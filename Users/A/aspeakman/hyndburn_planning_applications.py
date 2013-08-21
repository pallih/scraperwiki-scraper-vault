# this is a scraper of Hyndburn planning applications for use by Openly Local

# also see Braintree and Monmouthshire

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

class HyndburnScraper(base.DateScraper):

    MAX_ID_BATCH = 350 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 250 # max application details to scrape in one go

    date_from_field = 'startDate'
    date_to_field = 'endDate'
    request_date_format = '%d/%m/%Y'
    query_fields = { 'action2': 'Search'  }
    search_url = 'http://planning.hyndburnbc.gov.uk/WAM/findCaseFile.do'
    applic_url = 'http://planning.hyndburnbc.gov.uk/WAM/showCaseFile.do?action=show&appType=Planning'
    scrape_ids = """
    <table id="searchresults"> <tr />
    {* <tr> <td />
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    <td /> <td> {{ [records].status }} </td>
    </tr> *}
    </table>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="wam"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <table id="casefilesummary">
    <tr> <th> Application No: </th> <td> {{ reference }} </td> </tr>
    <tr> <th> Registration Date: </th> <td> {{ date_validated }} </td> </tr>
    <tr> <th> Location: </th> <td> {{ address }} </td> </tr>
    <tr> <th> Development: </th> <td> {{ description }} </td> </tr>
    </table>"""
    # other optional parameters that can appear on an application page
    scrape_optional_data = [ ]


    def get_id_batch (self, date_from, date_to):

        fields = self.query_fields
        date_to = date_to + timedelta(days=1) # end date is exclusive
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

    scraper = HyndburnScraper()
    scraper.run()

    #scraper.DEBUG = True

    # misc tests
    #print scraper.get_detail_from_uid ('11/12/0124')
    #result = scraper.get_id_batch(util.get_dt('03/04/2012'), util.get_dt('03/04/2012'))
    #print len(result), result
    #print scraper.gather_ids('2010-02-01')
    #print scraper.gather_ids(None, None)
    #scraper.gather_current_ids()

