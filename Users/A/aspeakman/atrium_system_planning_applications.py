# this is a scraper of Atrium system planning applications for use by Openly Local

# there are 9 authorities using this system
# all are counties, so low number of applications for minerals, waste, schools etc

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import random
import sys

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

systems = {
    'Somerset': 'SomersetScraper',
    'Suffolk': 'SuffolkScraper',
    'WestSussex': 'WestSussexScraper',
    'Kent': 'KentScraper',
    'Leicestershire': 'LeicestershireScraper',
    'Cumbria': 'CumbriaScraper', 
    'Dorset': 'DorsetScraper',
    'Hertfordshire': 'HertfordshireScraper', 
    'Lincolnshire': 'LincolnshireScraper'
     }

class AtriumScraper(base.DateScraper):

    MAX_ID_BATCH = 100 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 150 # max application details to scrape in one go
    BATCH_DAYS = 28 # batch size for each scrape - number of days to gather to produce at least TWO results each time (a list)
    MIN_DAYS = 28 # min number of days to get when gathering current ids

    date_from_field = { 'day': 'dayRegStart', 'month': 'monthRegStart', 'year': 'yearRegStart', }
    date_to_field = { 'day': 'dayRegEnd', 'month': 'monthRegEnd', 'year': 'yearRegEnd', }
    ref_field = 'aplRef'
    search_form = 'SearchForms'
    request_date_format = '%d/%b/%Y'

    scrape_ids = """
    <div class="sectionHeaderBackground_Dark"> Planning Applications Found: </div>
    <table>
    {* <tr> <td> Application Ref No. </td> <td> {{ [records].uid }} </td> </tr> 
    <tr> <a href="{{ [records].url|abs }}"> </a> </tr>
    *}
    </table>
    """

    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <body> <p> Main Details </p> {{ block|html }} </body>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <tr> <td> Application Number </td> <td> {{ reference }} </td> </tr>
    <tr> <td> Date Registered </td> <td> {{ date_validated }} </td> </tr>
    <tr> <td> Date Valid </td> <td> {{ date_received }} </td> </tr>
    <tr> <td> Location </td> <td> {{ address }} </td> </tr>
    <tr> <td> Proposal </td> <td> {{ description }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    # checked against Suffolk, Somerset
    scrape_optional_data = [
    "<tr> <td> Application Type </td> <td> {{ application_type }} </td> </tr>", 
    "<tr> <td> Application Status/Decision </td> <td> {{ status }} </td> </tr>", 
    "<tr> <td> Case Officer </td> <td> {{ case_officer }} </td> </tr>", 
    "<tr> <td> Ward </td> <td> {{ ward_name }} </td> </tr>", 
    "<tr> <td> Parish\Town </td> <td> {{ parish }} </td> </tr>", 
    "<tr> <td> Parish </td> <td> {{ parish }} </td> </tr>", 
    "<tr> <td> Council </td> <td> {{ district }} </td> </tr>", 
    "<tr> <td> Applicant </td> <td> {{ applicant_name }} </td> </tr>", 
    "<tr> <td> Agent </td> <td> {{ agent_name }} </td> </tr>", 

    "<tr> <td> Committee Date </td> <td> {{ meeting_date }} </td> </tr>",
    "<tr> <td> Consultation Start Date </td> <td> {{ consultation_start_date }} </td> </tr>",
    "<tr> <td> Consultation End Date </td> <td> {{ consultation_end_date }} </td> </tr>",

    "<tr> <td> Determination Target </td> <td> {{ target_decision_date }} </td> </tr>",
    "<tr> <td> Determine By </td> <td> {{ target_decision_date }} </td> </tr>",
    "<tr> <td> Decision </td> <td> {{ decision }} </td> </tr> <tr> <td> Decision Date </td> <td> {{ decision_date }} </td> </tr>", 
    "<tr> <td> Decision Method </td> <td> {{ decided_by }} </td> </tr>", 

    "<tr> <td> Appeal Date </td> <td> {{ appeal_date }} </td> </tr>", 
    "<tr> <td> Appeal Decision </td> <td> {{ appeal_result }} </td> </tr>", 
    "<tr> <td> Hearing Date </td> <td> {{ appeal_decision_date }} </td> </tr>", 
    ]

    def get_id_batch (self, date_from, date_to):
        response = self.br.open(self.search_url)
        self.br.select_form(name=self.search_form)
        date_from = date_from.strftime(self.request_date_format)
        date_parts = date_from.split('/')
        self.br[self.date_from_field['day']] = [ date_parts[0] ]
        self.br[self.date_from_field['month']] = [ date_parts[1] ]
        self.br[self.date_from_field['year']] = [ date_parts[2] ]
        date_to = date_to.strftime(self.request_date_format)
        date_parts = date_to.split('/')
        self.br[self.date_to_field['day']] = [ date_parts[0] ]
        self.br[self.date_to_field['month']] = [ date_parts[1] ]
        self.br[self.date_to_field['year']] = [ date_parts[2] ]
        response = self.br.submit()
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

    # post process a set of uid/url records: strips spaces in the uid and converts the reference
    def clean_ids (self, records):
        for record in records:
            if record.get('uid'):
                record['uid'] = util.GAPS_REGEX.sub('', record['uid']) # strip any spaces
                record['uid'] = re.sub(r'([^\(\)$]+).*', r'\1', record['uid'], 1, re.U)
                record['uid'] = record['uid'].replace('\\', '/')

    def get_detail_from_uid (self, uid):
        response = self.br.open(self.search_url)
        self.br.select_form(name=self.search_form)
        self.br[self.ref_field] = uid
        try:
            response = self.br.submit()
            html = response.read()
            url = response.geturl()
        except:
            return None
        if self.DEBUG: print html
        return self.get_detail(html, url)

class SomersetScraper(AtriumScraper):

    START_SEQUENCE = '2004-02-01' # gathers id data by working backwards from the current date towards this one
    search_url = 'http://webapp1.somerset.gov.uk/ePlanning/searchPageLoad.do'

class SuffolkScraper(AtriumScraper):

    search_url = 'http://atrium.suffolkcc.gov.uk/ePlanning//searchPageLoad.do'

class WestSussexScraper(AtriumScraper):

    BATCH_DAYS = 42 # batch size for each scrape - number of days to gather to produce at least TWO results (a list) each time
    search_url = 'http://buildings.westsussex.gov.uk/ePlanningOPS/searchPageLoad.do'

class KentScraper(AtriumScraper):

    START_SEQUENCE = '2004-02-01' # gathers id data by working backwards from the current date towards this one
    search_url = 'http://host1.atriumsoft.com/ePlanningOPSkent/searchPageLoad.do'

class LeicestershireScraper(AtriumScraper):

    START_SEQUENCE = '2004-02-01' # gathers id data by working backwards from the current date towards this one
    search_url = 'http://planning.leics.gov.uk/ePlanning/searchPageLoad.do'

class CumbriaScraper(AtriumScraper): # very slow site

    START_SEQUENCE = '2004-02-01' # gathers id data by working backwards from the current date towards this one
    MAX_ID_BATCH = 50 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 75 # max application details to scrape in one go
    search_url = 'http://onlineplanning.cumbria.gov.uk/ePlanningOPS/searchPageLoad.do'

class HertfordshireScraper(AtriumScraper): # low numbers

    START_SEQUENCE = '2004-02-01' # gathers id data by working backwards from the current date towards this one
    BATCH_DAYS = 60 # batch size for each scrape - number of days to gather to produce at least TWO results (a list) each time
    #search_url = 'https://www.hertsdirect.org/ePlanningOPS/searchPageLoad.do'
    search_url = 'https://cloud1.atriumsoft.com/HCCePlanningOPS/searchPageLoad.do'

class LincolnshireScraper(AtriumScraper):

    BATCH_DAYS = 42 # batch size for each scrape - number of days to gather to produce at least TWO results (a list) each time
    search_url = 'http://eplanning.lincolnshire.gov.uk/ePlanning/searchPageLoad.do'

class DorsetScraper(AtriumScraper):

    search_url = 'http://countyplanning.dorsetforyou.com/ePlanningOPS/searchPageLoad.do'

if __name__ == 'scraper':

    #scraper = CumbriaScraper('Cumbria')
    #scraper.run()
    #sys.exit()

    sys_list = []
    for k, v in systems.items(): # get latest date scraped for each system
        sys_list.append( (k, v, scraperwiki.sqlite.get_var('latest-' + k)) )
    sort_sys = sorted(sys_list, key=lambda system: system[2]) # sort so least recent are first
    for auth in sort_sys[:6]: # max 6 per run
        strexec = auth[1] + "('" + auth[0] + "')"
        print "Scraping from:", strexec
        try:
            scraper = eval(strexec)
            scraper.run()
        except Exception as err:
            print "Error - skipping this authority -", str(err)
    print "Finished"

    #scraper = LincolnshireScraper('Lincolnshire')
    #scraper.run()
    #scraper.DEBUG = True

    # misc test calls
    #print scraper.get_detail_from_uid ('PL/1967/10') # Somerset
    #print scraper.get_detail_from_uid ('PL/0258/11') # Suffolk
    #print scraper.get_detail_from_uid ('KCC/TM/0403/2011') # Kent
    #print scraper.get_detail_from_uid ('WSCC/056/11/SU') # West Sussex
    #print scraper.get_detail_from_uid ('2011/0752/04') # Leics
    #print scraper.get_detail_from_uid ('PL/0904/05') # Cumbria
    #print scraper.get_detail_from_uid ('PL/1237/11') # Dorset
    #print scraper.get_detail_from_uid ('PL/0382/11') # Herts
    #print scraper.get_detail_from_uid ('PL/0155/11') # Lincs
    #res = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('18/09/2011'))
    #print res, len(res)
    #print scraper.get_id_batch(util.get_dt('23/03/2012'), util.get_dt('25/03/2012'))

    #util.replace_vals('swvariables', 'name', 'West Sussex', 'WestSussex', 'suffix', 'yes')
    #scraperwiki.sqlite.execute("alter table `West Sussex` rename to `WestSussex`")
    #scraperwiki.sqlite.commit()


    


# this is a scraper of Atrium system planning applications for use by Openly Local

# there are 9 authorities using this system
# all are counties, so low number of applications for minerals, waste, schools etc

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import random
import sys

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

systems = {
    'Somerset': 'SomersetScraper',
    'Suffolk': 'SuffolkScraper',
    'WestSussex': 'WestSussexScraper',
    'Kent': 'KentScraper',
    'Leicestershire': 'LeicestershireScraper',
    'Cumbria': 'CumbriaScraper', 
    'Dorset': 'DorsetScraper',
    'Hertfordshire': 'HertfordshireScraper', 
    'Lincolnshire': 'LincolnshireScraper'
     }

class AtriumScraper(base.DateScraper):

    MAX_ID_BATCH = 100 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 150 # max application details to scrape in one go
    BATCH_DAYS = 28 # batch size for each scrape - number of days to gather to produce at least TWO results each time (a list)
    MIN_DAYS = 28 # min number of days to get when gathering current ids

    date_from_field = { 'day': 'dayRegStart', 'month': 'monthRegStart', 'year': 'yearRegStart', }
    date_to_field = { 'day': 'dayRegEnd', 'month': 'monthRegEnd', 'year': 'yearRegEnd', }
    ref_field = 'aplRef'
    search_form = 'SearchForms'
    request_date_format = '%d/%b/%Y'

    scrape_ids = """
    <div class="sectionHeaderBackground_Dark"> Planning Applications Found: </div>
    <table>
    {* <tr> <td> Application Ref No. </td> <td> {{ [records].uid }} </td> </tr> 
    <tr> <a href="{{ [records].url|abs }}"> </a> </tr>
    *}
    </table>
    """

    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <body> <p> Main Details </p> {{ block|html }} </body>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <tr> <td> Application Number </td> <td> {{ reference }} </td> </tr>
    <tr> <td> Date Registered </td> <td> {{ date_validated }} </td> </tr>
    <tr> <td> Date Valid </td> <td> {{ date_received }} </td> </tr>
    <tr> <td> Location </td> <td> {{ address }} </td> </tr>
    <tr> <td> Proposal </td> <td> {{ description }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    # checked against Suffolk, Somerset
    scrape_optional_data = [
    "<tr> <td> Application Type </td> <td> {{ application_type }} </td> </tr>", 
    "<tr> <td> Application Status/Decision </td> <td> {{ status }} </td> </tr>", 
    "<tr> <td> Case Officer </td> <td> {{ case_officer }} </td> </tr>", 
    "<tr> <td> Ward </td> <td> {{ ward_name }} </td> </tr>", 
    "<tr> <td> Parish\Town </td> <td> {{ parish }} </td> </tr>", 
    "<tr> <td> Parish </td> <td> {{ parish }} </td> </tr>", 
    "<tr> <td> Council </td> <td> {{ district }} </td> </tr>", 
    "<tr> <td> Applicant </td> <td> {{ applicant_name }} </td> </tr>", 
    "<tr> <td> Agent </td> <td> {{ agent_name }} </td> </tr>", 

    "<tr> <td> Committee Date </td> <td> {{ meeting_date }} </td> </tr>",
    "<tr> <td> Consultation Start Date </td> <td> {{ consultation_start_date }} </td> </tr>",
    "<tr> <td> Consultation End Date </td> <td> {{ consultation_end_date }} </td> </tr>",

    "<tr> <td> Determination Target </td> <td> {{ target_decision_date }} </td> </tr>",
    "<tr> <td> Determine By </td> <td> {{ target_decision_date }} </td> </tr>",
    "<tr> <td> Decision </td> <td> {{ decision }} </td> </tr> <tr> <td> Decision Date </td> <td> {{ decision_date }} </td> </tr>", 
    "<tr> <td> Decision Method </td> <td> {{ decided_by }} </td> </tr>", 

    "<tr> <td> Appeal Date </td> <td> {{ appeal_date }} </td> </tr>", 
    "<tr> <td> Appeal Decision </td> <td> {{ appeal_result }} </td> </tr>", 
    "<tr> <td> Hearing Date </td> <td> {{ appeal_decision_date }} </td> </tr>", 
    ]

    def get_id_batch (self, date_from, date_to):
        response = self.br.open(self.search_url)
        self.br.select_form(name=self.search_form)
        date_from = date_from.strftime(self.request_date_format)
        date_parts = date_from.split('/')
        self.br[self.date_from_field['day']] = [ date_parts[0] ]
        self.br[self.date_from_field['month']] = [ date_parts[1] ]
        self.br[self.date_from_field['year']] = [ date_parts[2] ]
        date_to = date_to.strftime(self.request_date_format)
        date_parts = date_to.split('/')
        self.br[self.date_to_field['day']] = [ date_parts[0] ]
        self.br[self.date_to_field['month']] = [ date_parts[1] ]
        self.br[self.date_to_field['year']] = [ date_parts[2] ]
        response = self.br.submit()
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

    # post process a set of uid/url records: strips spaces in the uid and converts the reference
    def clean_ids (self, records):
        for record in records:
            if record.get('uid'):
                record['uid'] = util.GAPS_REGEX.sub('', record['uid']) # strip any spaces
                record['uid'] = re.sub(r'([^\(\)$]+).*', r'\1', record['uid'], 1, re.U)
                record['uid'] = record['uid'].replace('\\', '/')

    def get_detail_from_uid (self, uid):
        response = self.br.open(self.search_url)
        self.br.select_form(name=self.search_form)
        self.br[self.ref_field] = uid
        try:
            response = self.br.submit()
            html = response.read()
            url = response.geturl()
        except:
            return None
        if self.DEBUG: print html
        return self.get_detail(html, url)

class SomersetScraper(AtriumScraper):

    START_SEQUENCE = '2004-02-01' # gathers id data by working backwards from the current date towards this one
    search_url = 'http://webapp1.somerset.gov.uk/ePlanning/searchPageLoad.do'

class SuffolkScraper(AtriumScraper):

    search_url = 'http://atrium.suffolkcc.gov.uk/ePlanning//searchPageLoad.do'

class WestSussexScraper(AtriumScraper):

    BATCH_DAYS = 42 # batch size for each scrape - number of days to gather to produce at least TWO results (a list) each time
    search_url = 'http://buildings.westsussex.gov.uk/ePlanningOPS/searchPageLoad.do'

class KentScraper(AtriumScraper):

    START_SEQUENCE = '2004-02-01' # gathers id data by working backwards from the current date towards this one
    search_url = 'http://host1.atriumsoft.com/ePlanningOPSkent/searchPageLoad.do'

class LeicestershireScraper(AtriumScraper):

    START_SEQUENCE = '2004-02-01' # gathers id data by working backwards from the current date towards this one
    search_url = 'http://planning.leics.gov.uk/ePlanning/searchPageLoad.do'

class CumbriaScraper(AtriumScraper): # very slow site

    START_SEQUENCE = '2004-02-01' # gathers id data by working backwards from the current date towards this one
    MAX_ID_BATCH = 50 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 75 # max application details to scrape in one go
    search_url = 'http://onlineplanning.cumbria.gov.uk/ePlanningOPS/searchPageLoad.do'

class HertfordshireScraper(AtriumScraper): # low numbers

    START_SEQUENCE = '2004-02-01' # gathers id data by working backwards from the current date towards this one
    BATCH_DAYS = 60 # batch size for each scrape - number of days to gather to produce at least TWO results (a list) each time
    #search_url = 'https://www.hertsdirect.org/ePlanningOPS/searchPageLoad.do'
    search_url = 'https://cloud1.atriumsoft.com/HCCePlanningOPS/searchPageLoad.do'

class LincolnshireScraper(AtriumScraper):

    BATCH_DAYS = 42 # batch size for each scrape - number of days to gather to produce at least TWO results (a list) each time
    search_url = 'http://eplanning.lincolnshire.gov.uk/ePlanning/searchPageLoad.do'

class DorsetScraper(AtriumScraper):

    search_url = 'http://countyplanning.dorsetforyou.com/ePlanningOPS/searchPageLoad.do'

if __name__ == 'scraper':

    #scraper = CumbriaScraper('Cumbria')
    #scraper.run()
    #sys.exit()

    sys_list = []
    for k, v in systems.items(): # get latest date scraped for each system
        sys_list.append( (k, v, scraperwiki.sqlite.get_var('latest-' + k)) )
    sort_sys = sorted(sys_list, key=lambda system: system[2]) # sort so least recent are first
    for auth in sort_sys[:6]: # max 6 per run
        strexec = auth[1] + "('" + auth[0] + "')"
        print "Scraping from:", strexec
        try:
            scraper = eval(strexec)
            scraper.run()
        except Exception as err:
            print "Error - skipping this authority -", str(err)
    print "Finished"

    #scraper = LincolnshireScraper('Lincolnshire')
    #scraper.run()
    #scraper.DEBUG = True

    # misc test calls
    #print scraper.get_detail_from_uid ('PL/1967/10') # Somerset
    #print scraper.get_detail_from_uid ('PL/0258/11') # Suffolk
    #print scraper.get_detail_from_uid ('KCC/TM/0403/2011') # Kent
    #print scraper.get_detail_from_uid ('WSCC/056/11/SU') # West Sussex
    #print scraper.get_detail_from_uid ('2011/0752/04') # Leics
    #print scraper.get_detail_from_uid ('PL/0904/05') # Cumbria
    #print scraper.get_detail_from_uid ('PL/1237/11') # Dorset
    #print scraper.get_detail_from_uid ('PL/0382/11') # Herts
    #print scraper.get_detail_from_uid ('PL/0155/11') # Lincs
    #res = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('18/09/2011'))
    #print res, len(res)
    #print scraper.get_id_batch(util.get_dt('23/03/2012'), util.get_dt('25/03/2012'))

    #util.replace_vals('swvariables', 'name', 'West Sussex', 'WestSussex', 'suffix', 'yes')
    #scraperwiki.sqlite.execute("alter table `West Sussex` rename to `WestSussex`")
    #scraperwiki.sqlite.commit()


    


