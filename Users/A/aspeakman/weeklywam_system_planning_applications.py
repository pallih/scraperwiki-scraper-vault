# this is a base scraper for Weekly WAM system planning applications for use by Openly Local

# there are 6 authorities using this system

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import random
import urllib
import sys

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

systems = [
    'ColchesterScraper',
    'DartmoorScraper', # last 9 weeks only National Park
    'NorthSomersetScraper', 
    'NottinghamScraper',
    'TowerHamletsScraper',
    'WestLothianScraper',
     ]

class WeeklyWAMScraper(base.PeriodScraper):

    MAX_ID_BATCH = 300 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go
    PERIOD_TYPE = 'Sunday'

    date_field = 'endDate'
    request_date_format = '%s'
    query_fields = {  "areaCode": "%", "sortOrder": "3", "applicationType": "%", "Button": "Search", 'action': 'showWeeklyList'  }
    scrape_ids = """
    <table id="searchresults"> <tr />
    {* <tr> <td />
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    <td /> <td> {{ [records].status }} </td>
    </tr> *}
    </table>
    """
    link_next = '[Next >>]'
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <body> {{ block|html }} </body>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <table id="casefilesummary">
    <tr> <th id="development" /> <td> {{ description }} </td> </tr>
    <tr> <th id="location" /> <td> {{ address }} </td> </tr>
    <tr> <th id="appno" /> <td> {{ reference }} </td>
         <th id="regdate" /> <td> {{ date_validated }} </td>
    </tr>
    </table>"""
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr> <th id="applicant" /> <td> {{ applicant_name }} <br> {{ applicant_address }} </td> </tr>',
    '<tr> <th id="agent" /> <td> {{ agent_name }} <br> {{ agent_address }} </td> </tr>',
    '<tr> <th id="dateconsultend" /> <td> {{ consultation_end_date }} </td> </tr>',
    '<tr> <th id="dateconsultstart" /> <td> {{ consultation_start_date }} </td> </tr>',
    '<tr> <th id="caseofficer" /> <td> {{ case_officer }} </td> </tr>',
    '<tr> <th id="decdate" /> <td> {{ decision_date }} </td> </tr>',
    '<tr> <th id="apptype" /> <td> {{ application_type }} </td> </tr>',
    '<p id="comment"> <a href="{{ comment_url|abs }}" /> </p>',
    '<tr> <th id="parish" /> <td> {{ ward_name }} </td> </tr>',
    '<tr> <th id="dectype" /> <td> {{ decision }} </td> </tr>',
    ]

    def get_id_period (self, date):

        fields = self.query_fields
        from_iso_dt, to_iso_dt = util.inc_dt(date.strftime(util.ISO8601_DATE), util.ISO8601_DATE, self.PERIOD_TYPE)
        from_dt = util.get_dt(from_iso_dt, util.ISO8601_DATE)
        to_dt = util.get_dt(to_iso_dt, util.ISO8601_DATE)

        timestamp = str(int(to_dt.strftime(self.request_date_format))*1000)
        #print timestamp
        fields [self.date_field] = str(int(to_dt.strftime(self.request_date_format))*1000)

        if self.DEBUG: print fields

        final_result = []
        
        response = util.open_url(self.br, self.search_url, fields, 'POST')
        if not response:
            return [], None, None
        while response:
            html = response.read()
            url = response.geturl()
            if self.DEBUG: print html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            else:
                break # note weekly result allowed to be legitimately empty (for example in the current week)
            try:
                response = self.br.follow_link(text=self.link_next)
            except:
                response = None

        return final_result, from_dt, to_dt 

    def get_detail_from_uid (self, uid):
        url = self.applic_url + '&appNumber=' + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

class ColchesterScraper(WeeklyWAMScraper):

    TABLE_NAME = 'Colchester'
    search_url = 'http://www.planning.colchester.gov.uk/WAM/weeklyApplications.do'
    applic_url = 'http://www.planning.colchester.gov.uk/WAM/showCaseFile.do?action=show&appType=Planning'
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

class DartmoorScraper(WeeklyWAMScraper): # only gets last 9 weeks

    TABLE_NAME = 'Dartmoor'
    search_url = 'http://www2.dartmoor-npa.gov.uk/WAM/weeklyApplications.do'
    applic_url = 'http://www2.dartmoor-npa.gov.uk/WAM/showCaseFile.do?action=show&appType=Planning'
    scrape_ids = """
    <body>
    {* <p id="viewApplication"> <a href="{{ [records].url|abs }}"> </a> </p>
    <table class="searchresult">
    <tr> Application Number: {{ [records].uid }} </tr>
    <tr> District: {{ [records].district }} </tr>
    <tr> Parish: {{ [records].parish }} </tr>
    <tr> Grid Reference: {{ [records].os_grid_ref }} </tr> 
    <tr> Application Type: {{ [records].application_type }} </tr> 
    </table> *}
    </body>
    """
    scrape_min_data = """
    <table id="casefilesummary">
    <tr> <th id="apptype" /> <td> {{ reference }} </td> </tr>
    <tr> <th id="development" /> <td> {{ description }} </td> </tr>
    <tr> <th id="location" /> <td> {{ address }} </td> </tr>
    </table>"""
    scrape_optional_data = [
    '<tr> <th id="applname" /> <td> {{ applicant_name }} </td> </tr>',
    """<tr> <th id="datereceived" /> </tr> <tr> <td> {{ date_received }} </td> <td> {{ date_validated }} </td> 
    <td> {{ consultation_start_date }} </td> <td> {{ consultation_end_date }} </td> </tr>""",
    '<tr> <th id="caseofficer" /> <td> <a> {{ case_officer }} </a> </td> </tr>',
    '<tr> <th id="targetdecision" /> </tr> <tr> <td> {{ target_decision_date }} </td> <td> {{ decision_date }} </td> <td> {{ decision }} </td> </tr>',
    '<p id="comment"> <a href="{{ comment_url|abs }}" /> </p>',
    ]

    def get_id_period (self, date):

        fields = self.query_fields
        from_iso_dt, to_iso_dt = util.inc_dt(date.strftime(util.ISO8601_DATE), util.ISO8601_DATE, self.PERIOD_TYPE)
        from_dt = util.get_dt(from_iso_dt, util.ISO8601_DATE)
        to_dt = util.get_dt(to_iso_dt, util.ISO8601_DATE)

        timestamp = str(int(to_dt.strftime(self.request_date_format))*1000)
        #print timestamp
        fields [self.date_field] = str(int(to_dt.strftime(self.request_date_format))*1000)

        if self.DEBUG: print fields

        final_result = []
        
        response = util.open_url(self.br, self.search_url, fields, 'POST')
        if not response:
            return [], None, None
        while response:
            html = response.read()
            url = response.geturl()
            if self.DEBUG: print html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            else:
                return [], None, None # note weekly result not allowed to be empty in this case
            try:
                response = self.br.follow_link(text=self.link_next)
            except:
                response = None

        return final_result, from_dt, to_dt 

class NorthSomersetScraper(WeeklyWAMScraper): 

    TABLE_NAME = 'NorthSomerset'
    search_url = 'http://wam.n-somerset.gov.uk/MULTIWAM/weeklyApplications.do'
    applic_url = 'http://wam.n-somerset.gov.uk/MULTIWAM/showCaseFile.do?action=show&appType=Planning'
    query_fields = {  "areaCode": "%", "sortOrder": "3", "applicationType": "%", "Button": "Search", 'action': 'showWeeklyList', 'category': 'planning'  }

    scrape_data_block = """
    <table id="casefilesummary"> {{ block|html }} </table>
    """
    scrape_min_data = """
    <tr> <td> Development </td> <td> {{ description }} </td> </tr>
    <tr> <td> Location </td> <td> {{ address }} </td> </tr>
    <tr> <td> Application No </td> <td> {{ reference }} </td> </tr>
    """
    scrape_optional_data = [
    '<tr> <td> Application Type </td> <td> {{ application_type }} </td> </tr>',
    '<tr> <td> Date Received </td> <td> {{ date_received }} </td> </tr>',
    '<tr> <td> Valid Date </td> <td> {{ date_validated }} </td> </tr>',
    '<tr> <td> Parish </td> <td> {{ parish }} </td> </tr>',
    '<tr> <td> Decision Date </td> <td> {{ decision_date }} </td> </tr> Case Officer',
    '<tr> <td> Case Officer </td> <td> {{ case_officer }} </td> </tr>',
    '<tr> <td> Decision </td> <td> {{ decision }} </td> Appeal Reference </tr>',
    '<tr> <td> Applicant </td> <td> {{ applicant_name }} <br> {{ applicant_address|html }} </td> </tr>',
    '<tr> <td> Agent </td> <td> {{ agent_name }} <br> {{ agent_address|html }} </td> </tr>',
    '<tr> <td> Application Status </td> <td> {{ status }} </td> </tr>',
    """<tr> <td> Target Date </td> <td> {{ target_decision_date }} </td>
    <td> Target Date for Public Consultations </td> <td> {{ consultation_end_date }} </td> </tr>""",
    '<tr> <td> Appeal Decision Date </td> <td> {{ appeal_decision_date }} </td> </tr>',
    ]

class NottinghamScraper(WeeklyWAMScraper):

    TABLE_NAME = 'Nottingham'
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
    '<tr> <td> Applicant: </td> <td> {{ applicant_name }} <br> {{ applicant_address|html }} </td> </tr>',
    '<tr> <td> Agent: </td> <td> {{ agent_name }} <br> {{ agent_address|html }} </td> </tr>',
    '<tr> <td> Decision Date: </td> <td> {{ decision_date }} </td> </tr>',
    '<tr> <td> Application Type: </td> <td> {{ application_type }} </td> </tr>',
    '<tr> <td> Ward: </td> <td> {{ ward_name }} </td> </tr>',
    '<tr> <td> Decision Type: </td> <td> {{ decision }} </td> </tr>',
    ]

class TowerHamletsScraper(WeeklyWAMScraper):

    TABLE_NAME = 'TowerHamlets'
    search_url = 'http://planreg.towerhamlets.gov.uk/WAM/weeklyApplications.do'
    applic_url = 'http://planreg.towerhamlets.gov.uk/WAM/showCaseFile.do?action=show&appType=Planning'
    scrape_data_block = """
    <div id="mainTextPage"> {{ block|html }} </div>
    """

class WestLothianScraper(WeeklyWAMScraper): 

    TABLE_NAME = 'WestLothian'
    search_url = 'http://planning.westlothian.gov.uk/WAM133/weeklyApplications.do'
    applic_url = 'http://planning.westlothian.gov.uk/WAM133/showCaseFile.do?action=show&appType=Planning'
    scrape_data_block = """
    <div id="white-bg"> {{ block|html }} </div>
    """

if __name__ == 'scraper':

    #scraper = TowerHamletsScraper()
    #scraper.reset()
    #scraper.DEBUG = True
    #scraper.run()
    #sys.exit()

    random.shuffle(systems)
    for auth in systems[:4]: # do max 4 per run
        print "Authority:", auth
        try:
            scraper = eval(auth + "()")
            scraper.run()
        except Exception as err:
            print "Error - skipping this authority -", str(err)
    print "Finished"

    # misc test calls
    #scraper = ColchesterScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('120697') # Colchester OK
    #scraper = DartmoorScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('0313/12') # Dartmoor OK
    #scraper = NorthSomersetScraper()
    #scraper.DEBUG = True 
    #print scraper.get_detail_from_uid ('04/P/0751/F') # North Somerset recird scrape OK, id scrape not working
    #scraper = NottinghamScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('12/01242/PFUL3') # Nottingham OK
    #scraper = TowerHamletsScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('PA/10/00185') # TowerHamlets OK
    #scraper = WestLothianScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('0123/FUL/11') # WestLothian OK

    #result, dt1, dt2 = scraper.get_id_period(util.get_dt('13/05/2013'))
    #print len(result), result, dt1, dt2

    #util.rename_column(scraper.TABLE_NAME, 'decision_type', 'decision')

    #util.list_url_prefixes(scraper.TABLE_NAME, 'url')
    #util.replace_vals(scraper.TABLE_NAME, 'url', 'http://www.nuneatonandbedworth.gov.uk/sys_upl/templates/', 'http://apps.nuneatonandbedworth.gov.uk/', 'prefix', 'yes')
    
