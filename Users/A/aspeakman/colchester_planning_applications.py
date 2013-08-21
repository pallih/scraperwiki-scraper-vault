# this is a scraper of Colchester planning applications for use by Openly Local

# also see West Lothian, Tower Hamlets, Nottingham

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

class ColchesterScraper(base.PeriodScraper):

    MAX_ID_BATCH = 350 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 300 # max application details to scrape in one go
    PERIOD_TYPE = 'Sunday'

    date_field = 'endDate'
    request_date_format = '%s'
    query_fields = {  "areaCode": "%", "sortOrder": "3", "applicationType": "%", "Button": "Search", 'action': 'showWeeklyList'  }
    search_url = 'http://www.planning.colchester.gov.uk/WAM/weeklyApplications.do'
    applic_url = 'http://www.planning.colchester.gov.uk/WAM/showCaseFile.do?action=show&appType=Planning'
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
    <td id="content"> {{ block|html }} </td>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <table id="casefilesummary">
    <tr> <td id="applicationumbervalue"> {{ reference }} </td> </tr>
    <tr> <th> Development: </th> <td> {{ description }} </td> </tr>
    <tr> <th> Site Address: </th> <td> {{ address }} </td> </tr>
    <tr> 
         <th> Date Received: </th> <td> {{ date_received }} </td>
         <th> Registration Date: </th> <td> {{ date_validated }} </td>
    </tr>
    </table>"""
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr> <th> Applicant: </th> <td> {{ applicant_name }} </td> </tr>',
    '<tr> <th> Agent: </th> <td> {{ agent_name }} </td> </tr>',
    '<tr> <th> Consultation Expiry Date: </th> <td> {{ consultation_end_date }} </td> </tr>',
    '<tr> <th> CBC Decision Date: </th> <td> {{ decision_date }} </td> </tr>',
    '<tr> <th> Target Date: </th> <td> {{ target_decision_date }} </td> </tr>',
    '<tr> <th> Application Type: </th> <td> {{ application_type }} </td> </tr>',
    '<p id="comment"> <a href="{{ comment_url|abs }}" /> </p>',
    '<tr> <th> Application Status: </th> <td> {{ status }} </td> </tr>',
    '<tr> <th> UPRN: </th> <td> {{ uprn }} </td> </tr>',
    '<tr> <th> Parish: </th> <td> {{ parish }} </td> </tr>',
    '<tr> <th> Ward: </th> <td> {{ ward_name }} </td> </tr>',
    '<tr> <th> Decision Type: </th> <td> {{ decision }} </td> </tr>',
    '<tr> <th> Case Officer: </th> <td> {{ case_officer }} </td> </tr>',
    '<tr> <th> Appeal Start Date: </th> <td> {{ appeal_date }} </td> </tr>',
    '<tr> <th> Appeal Determination Date: </th> <td> {{ appeal_decision_date }} </td> </tr>',
    '<tr> <th> Appeal Decision: </th> <td> {{ appeal_result }} </td> </tr>',
    ]

    def get_id_period (self, date):

        fields = self.query_fields
        from_iso_dt, to_iso_dt = util.inc_dt(date.strftime(util.ISO8601_DATE), util.ISO8601_DATE, self.PERIOD_TYPE)
        from_dt = util.get_dt(from_iso_dt, util.ISO8601_DATE)
        to_dt = util.get_dt(to_iso_dt, util.ISO8601_DATE)

        timestamp = str(int(to_dt.strftime(self.request_date_format))*1000)
        #print timestamp
        fields [self.date_field] = str(int(to_dt.strftime(self.request_date_format))*1000)

        final_result = []
        
        response = util.open_url(self.br, self.search_url, fields, 'POST')
        if response:
            html = response.read()
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
        else:
            return [], None, None

        return final_result, from_dt, to_dt # note weekly result might some times be legitimately empty

    def get_detail_from_uid (self, uid):
        url = self.applic_url + '&appNumber=' + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    scraper = ColchesterScraper()
    scraper.run()

    #scraper.DEBUG = True

    # misc tests
    #print scraper.get_detail_from_uid ('120697')
    #result = scraper.get_id_period(util.get_dt('01/03/2011'))
    #result, dt1, dt2 = scraper.get_id_period(util.get_dt('11/05/2010'))
    #print len(result), result, dt1, dt2
    #print scraper.gather_ids('2010-02-01')
    #print scraper.gather_ids(None, None)
    #scraper.gather_current_ids()

    #util.rename_column(scraper.TABLE_NAME, 'decision_type', 'decision')

