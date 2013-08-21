# this is a scraper of Nottingham planning applications for use by Openly Local

# also see West Lothian, Tower Hamlets, Colchester

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

class NottinghamScraper(base.PeriodScraper):

    MAX_ID_BATCH = 250 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 150 # max application details to scrape in one go
    PERIOD_TYPE = 'Sunday'

    date_field = 'endDate'
    request_date_format = '%s'
    query_fields = {  "areaCode": "%", "sortOrder": "3", "applicationType": "%", "Button": "Search", 'action': 'showWeeklyList'  }
    search_url = 'http://plan4.nottinghamcity.gov.uk/WAM/pas/searchApplications.do'
    applic_url = 'http://plan4.nottinghamcity.gov.uk/WAM/pas/showCaseFile.do?councilName=Nottingham+City+Council'
    scrape_ids = """
    <div id="page"> <table> <tr />
    {* <tr> <td />
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    <td /> <td> {{ [records].status }} </td>
    </tr> *}
    </table> </div>
    """
    link_next = '[Next >>]'
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="page"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <div id="casefile"> <table>
    <tr> <td> Application No: </td> <td> {{ reference }} </td>
         <td> Registration Date: </td> <td> {{ date_validated }} </td> </tr>
    <tr> <td> Location: </td> <td> {{ address }} </td> </tr>
    <tr> <td> Development: </td> <td> {{ description }} </td> </tr>
    </table> </div>"""
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr> <td> Applicant: </td> <td> {{ applicant_name }} <br> {{ applicant_address }} </td> </tr>',
    '<tr> <td> Agent: </td> <td> {{ agent_name }} <br> {{ agent_address }} </td> </tr>',
    '<tr> <td> Decision Date: </td> <td> {{ decision_date }} </td> </tr>',
    '<tr> <td> Application Type: </td> <td> {{ application_type }} </td> </tr>',
    '<tr> <td> Ward: </td> <td> {{ ward_name }} </td> </tr>',
    '<tr> <td> Decision Type: </td> <td> {{ decision }} </td> </tr>',
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
        if not response:
            return [], None, None
        while response:
            html = response.read()
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            try:
                response = self.br.follow_link(text=self.link_next)
            except:
                response = None

        return final_result, from_dt, to_dt # note weekly result might some times be legitimately empty

    def get_detail_from_uid (self, uid):
        url = self.applic_url + '&appNumber=' + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    scraper = NottinghamScraper()
    scraper.run()

    #scraper.DEBUG = True

    # misc tests
    #print scraper.get_detail_from_uid ('12/01242/PFUL3')
    #result, dt1, dt2 = scraper.get_id_period(util.get_dt('27/05/2012'))
    #result, dt1, dt2 = scraper.get_id_period(util.get_dt('11/05/2010'))
    #print len(result), result, dt1, dt2
    #print scraper.gather_ids('2010-02-01')
    #print scraper.gather_ids(None, None)
    #scraper.gather_current_ids()

    #util.rename_column(scraper.TABLE_NAME, 'decision_type', 'decision')

