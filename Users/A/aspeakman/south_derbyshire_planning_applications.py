# this is a scraper of South Derbyshire planning applications for use by Openly Local

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

class SouthDerbyshireScraper(base.DateScraper):

    MAX_ID_BATCH = 250 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go

    search_url = 'http://www.planning.south-derbys.gov.uk/'
    applic_url = 'http://www.planning.south-derbys.gov.uk/ApplicationDetail.aspx?Ref='
    date_from_field = {
        'day': 'ctl00$Mainpage$FromDay',
        'month': 'ctl00$Mainpage$FromMonth',
        'year': 'ctl00$Mainpage$FromYear',
        }
    date_to_field = {
        'day': 'ctl00$Mainpage$ToDay',
        'month': 'ctl00$Mainpage$ToMonth',
        'year': 'ctl00$Mainpage$ToYear',
        }
    search_fields = {
        'ctl00$Mainpage$Selectdate': 'optValid',
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        }
    next_target = 'ctl00$Mainpage$gridMain'
    request_date_format = '%d/%b/%Y'
    search_form = 'aspnetForm'
    search_submit = 'ctl00$Mainpage$cmdSetDates'
    scrape_ids = """
    <table id="ctl00_Mainpage_gridMain"> <tr />
    {* <tr> <td> {{ [records].uid }} </td>
    <td /> <td /> <td /> <td />
    </tr> *}
    </table>
    """
    scrape_max_pages = '<tr> <td colspan="8"> {{ max_pages }} </td> </tr>'
    scrape_data_block = """
    <table id="ctl00_Mainpage_detailPlanning"> {{ block|html }} </table>
    """
    scrape_min_data = """
    <tr> <td> Reference </td> <td> {{ reference }} </td> </tr>
    <tr> <td> Development </td> <td> {{ description }} </td> </tr>
    <tr> <td> Location </td> <td> {{ address }} </td> </tr>
    <tr> <td> Date Received </td> <td> {{ date_received }} </td> </tr>
    <tr> <td> Date Valid </td> <td> {{ date_validated }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr> <td> Postcode </td> <td> {{ postcode }} </td> </tr>',
    '<tr> <td> Easting </td> <td> {{ easting }} </td> </tr>',
    '<tr> <td> Northing </td> <td> {{ northing }} </td> </tr>',
    '<tr> <td> Consultation Start Date </td> <td> {{ consultation_start_date }} </td> </tr>',
    '<tr> <td> Consultation End Date </td> <td> {{ consultation_end_date }} </td> </tr>',
    '<tr> <td> Target Date </td> <td> {{ target_decision_date }} </td> </tr>',
    '<tr> <td> Delegated </td> <td> {{ decided_by }} </td> </tr>',
    '<tr> <td> Date of Committee </td> <td> {{ meeting_date }} </td> </tr>',
    """<tr> <td> Case Officer </td> <td> {{ case_officer }} </td> </tr>
    <tr> <td> Decision </td> <td> {{ decision }} </td> </tr>""",
    '<tr> <td> Date of Decision </td> <td> {{ decision_date }} </td> </tr>',
    ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)

        fields = self.search_fields
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

        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br, self.search_submit)
        html = response.read()

        # page count not used at the moment
        try:
            result = scrapemark.scrape(self.scrape_max_pages, html)
            page_list = result['max_pages'].split()
            max_pages = int(page_list[-1]) # can be a space separated list, so take the last value
        except:
            max_pages = 0
        if self.DEBUG: print max_pages
        
        current_page = 1
        final_result = []
        while response:
            url = response.geturl()
            if self.DEBUG: print html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                for rec in result['records']:
                    rec['url'] = self.applic_url + urllib.quote_plus(rec['uid'])
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            else:
                break
            current_page += 1
            fields = { '__EVENTTARGET': self.next_target,  '__EVENTARGUMENT': 'Page$' + str(current_page) }
            try:
                util.setup_form(self.br, self.search_form, fields)
                for control in self.br.form.controls:
                    if control.type == "submit":
                        control.disabled = True
                if self.DEBUG: print self.br.form
                response = util.submit_form(self.br)
                html = response.read()
            except:
                break
            
        return final_result

    def get_detail_from_uid (self, uid):
        url = self.applic_url + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    scraper = SouthDerbyshireScraper()
    scraper.run()

    # misc test calls
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('9/2012/0665')
    #result = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('09/08/2011'))
    #print len(result), result

    



