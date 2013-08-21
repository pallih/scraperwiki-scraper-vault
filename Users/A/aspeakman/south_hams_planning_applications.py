# this is a scraper of South Hams planning applications for use by Openly Local

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

class SouthHamsScraper(base.DateScraper):

    date_from_field = { 'day': 'startday', 'month': 'startmonth', 'year': 'startyear', }
    date_to_field = { 'day': 'endday', 'month': 'endmonth', 'year': 'endyear', }
    search_form = 'form1'
    form_fields = { 'show': '15', 'page': '1', "submit": "Search", 'selectparish': 'None', 'address': '', 'applicant': '', 'appno': '' }
    submit_control = None
    request_date_format = '%d/%m/%Y'
    search_url = 'http://www.southhams.gov.uk/index/residents_index/ksp_development_and_planning/spec-search-planning-apps-m3_simple.htm'
    list_url = 'http://www.southhams.gov.uk/spec_planning_apps_list-m3.htm'
    applic_url = 'http://www.southhams.gov.uk/spec_planning_apps_detail-m3.htm'
    scrape_ids = """
    <a name="content"></a>
    <table> <tr> <td colspan="5" /> </tr> <tr />
    {* <tr>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    <td /> <td /> <td /> <td> {{ [records].parish }} </td>
    </tr> *}
    <tr> <td colspan="5" /> </tr> </table>
    """
    page_list = '<td align="center" colspan="5"> {{ page_list }} </td>'
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <table summary="This table contains the left navigation and content"> {{ block|html }} </table>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <table width="100%" border="1"> Application Ref: <b> {{ reference }} </b> </table>
    <table width="100%" border="1"> Address: {{ address }} </table>
    <table width="100%" border="1"> <tr> Description: {{ description }} </tr> </table>
    <table width="100%" border="1"> <tr> Date Application Received: {{ date_received }} </tr>
    <tr> Date Application Valid: {{ date_validated }} </tr> </table>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<table> <tr> <td> Application Status: </td> <td> {{ status }} </td> </tr> </table>',
    '<table> <tr> Applicant details </tr> Name: {{ applicant_name }} Address: {{ applicant_address }} </table>',
    '<table> <tr> Agent details </tr> Name: {{ agent_name }} Address: {{ agent_address }} </table>',
    '<table> <tr> Officer Dealing </tr> <tr> Case Officer {{ case_officer }} </tr> </table>',
    '<table> <tr> Important Dates </tr> <tr> Target Date: {{ target_decision_date }} </tr> </table>',
    '<table> <tr> Important Dates </tr> <tr> Expiry Date for Advertisement(Comments): {{ latest_advertisement_expiry_date }} </tr> </table>',
    '<table> <tr> Important Dates </tr> <tr> Advertised on: {{ last_advertised_date }} </tr> </table>',
    '<table> <table> <tr> Decision Method {{ decided_by }} </tr> </table> </table>',
    '<table border="0"> <table> <tr> <th> Decision Status </th> </tr> <tr> <td> Final Decision </td> <td> {{ decision }} </td> <td> {{ decision_date }} </td> </tr> </table> </table>',
    '<table> <tr> Consultation and Comments </tr> <tr> <a href="{{ comment_url }}"> </a> </tr> </table>',
    ]

    def get_id_batch (self, date_from, date_to):

        #response = util.open_url(self.br, self.search_url)

        fields = self.form_fields

        date_from = date_from.strftime(self.request_date_format)
        date_parts = date_from.split('/')
        fields [self.date_from_field['day']] = date_parts[0]
        fields [self.date_from_field['month']] = date_parts[1]
        fields [self.date_from_field['year']] = date_parts[2]

        date_to = date_to.strftime(self.request_date_format)
        date_parts = date_to.split('/')
        fields [self.date_to_field['day']] = date_parts[0]
        fields [self.date_to_field['month']] = date_parts[1]
        fields [self.date_to_field['year']] = date_parts[2]

        #util.setup_form(self.br, self.search_form, fields)
        #response = util.submit_form(self.br, self.submit_control)
        response = util.open_url(self.br, self.list_url, fields, 'GET')

        final_result = []
        if response:
            html = response.read()
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])

            try: # try to get paged results
                result = scrapemark.scrape(self.page_list, html)
                page_list = result.get('page_list', '')
                pag_value_list = page_list.split()
                max_pages = pag_value_list[-1] # can be a space separated list, so take the last value
                for i in range(1, int(max_pages)):
                    fields['page'] = str(i+1)
                    response = util.open_url(self.br, self.list_url, fields, 'GET')
                    if response:
                        html = response.read()
                        url = response.geturl()
                        result = scrapemark.scrape(self.scrape_ids, html, url)
                        if result and result.get('records'):
                            self.clean_ids(result['records'])
                            final_result.extend(result['records'])
            except:
                pass # not a loop

        return final_result

    def get_detail_from_uid (self, uid):
        url = self.applic_url + '?SHORTID=' + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    #scraper = SouthHamsScraper()
    #scraper.run()

    # misc tests
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('2036/11/F')
    #print scraper.get_detail_from_uid ('0770/11/F')
    #res = scraper.get_id_batch(util.get_dt('01/01/2013'), util.get_dt('07/01/2013'))
    #print len(res), res
    #print scraper.gather_ids('2012-02-01')
    #print scraper.gather_ids('2011-02-01', '2012-01-18')

