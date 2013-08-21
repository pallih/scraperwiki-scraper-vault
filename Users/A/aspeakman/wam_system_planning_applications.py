# this is a base scraper for WAM system planning applications for use by Openly Local

# there are now only 2 authorities using this system

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import random
import urllib
import copy

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

systems = {
    #'Braintree': 'BraintreeScraper', now moved over to Idox
    'Hyndburn': 'HyndburnScraper',
    'Monmouthshire': 'MonmouthshireScraper',
     }

class WAMScraper(base.DateScraper):

    MAX_ID_BATCH = 350 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 250 # max application details to scrape in one go

    date_from_field = 'startDate'
    date_to_field = 'endDate'
    request_date_format = '%d/%m/%Y'
    search_form = '2'
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
    <body> {{ block|html }} </body>
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

        response = self.br.open(self.search_url)

        fields = {}
        date_to = date_to + timedelta(days=1) # end date is exclusive
        fields [self.date_from_field] = date_from.strftime(self.request_date_format)
        fields [self.date_to_field] = date_to.strftime(self.request_date_format)
        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br)

        final_result = []
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

class BraintreeScraper(WAMScraper): 

    search_url = 'http://planningapp.braintree.gov.uk/WAM1/searchsubmit/performOption.do?action=search'
    applic_url = 'http://planningapp.braintree.gov.uk/WAM1/showCaseFile.do?action=show&appType=Planning'
    search_form = '1'
    scrape_ids = """
    <table id="passearchresults"> <tr />
    {* <tr> <td />
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    <td /> <td> {{ [records].status }} </td>
    </tr> *}
    </table>
    """
    scrape_data_block = """
    <div id="wamcontent"> {{ block|html }} </div>
    """
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

        response = self.br.open(self.search_url)

        fields = {}
        fields [self.date_from_field] = date_from.strftime(self.request_date_format)
        fields [self.date_to_field] = date_to.strftime(self.request_date_format)
        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br)

        final_result = []
        if response:
            html = response.read()
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])

        return final_result
    
class HyndburnScraper(WAMScraper): # low numbers

    BATCH_DAYS = 60 # batch size for each scrape - number of days to gather to produce at least one result each time
    MIN_DAYS = 32 # min number of days to get when gathering current ids

    search_url = 'http://planning.hyndburnbc.gov.uk/WAM/searchsubmit/performOption.do?action=search&appType=Planning'
    applic_url = 'http://planning.hyndburnbc.gov.uk/WAM/showCaseFile.do?action=show&appType=Planning'
    scrape_data_block = """
    <div id="wam"> {{ block|html }} </div>
    """

class MonmouthshireScraper(WAMScraper):

    BATCH_DAYS = 60 # batch size for each scrape - number of days to gather to produce at least one result each time
    MIN_DAYS = 32 # min number of days to get when gathering current ids

    search_url = 'http://idox.monmouthshire.gov.uk/WAM/searchsubmit/performOption.do?action=search&appType=Planning'
    applic_url = 'http://idox.monmouthshire.gov.uk/WAM/showCaseFile.do?action=show&appType=Planning'
    query_fields = { 'action2': 'Search', 'appType': 'Planning'  }
    scrape_data_block = """
    <div id="content"> {{ block|html }} </div>
    """

if __name__ == 'scraper':

    alist = systems.keys()
    random.shuffle(alist)
    for auth in alist[:4]: # do max 4 per run
        strexec = systems[auth] + "('" + auth + "')"
        print "Authority:", auth, strexec
        try:
            scraper = eval(strexec)
            scraper.run()
        except Exception as err:
            print "Error - skipping this authority -", str(err)
    print "Finished"

    # misc test calls
    #scraper = BraintreeScraper()
    #scraper.DEBUG = True 
    #print scraper.get_detail_from_uid ('11/01084/FUL') # Braintree not OK now Idox
    #scraper = HyndburnScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/12/0134') # Hyndburn OK
    #scraper = MonmouthshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('DC/2012/00340') # Monmouthshire OK

    #result = scraper.get_id_batch(util.get_dt('03/04/2012'), util.get_dt('23/04/2012'))
    #print len(result), result

    #util.rename_column(scraper.TABLE_NAME, 'decision_type', 'decision')

    #util.list_url_prefixes(scraper.TABLE_NAME, 'url')
    #util.replace_vals(scraper.TABLE_NAME, 'url', 'http://www.nuneatonandbedworth.gov.uk/sys_upl/templates/', 'http://apps.nuneatonandbedworth.gov.uk/', 'prefix', 'yes')
    
