# this is a base scraper for PlanningExplorer system planning applications for use by Openly Local

# there are 25 authorities using this system, all 25 are defined but only 13 are scraped here

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import random
import urllib
import urlparse
import sys

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

systems = {
    'Barnsley': 'BarnsleyScraper',
    'Birmingham': 'BirminghamScraper',
    'Blackburn': 'BlackburnScraper',
    'Broadland': 'BroadlandScraper',
    'Camden': 'CamdenScraper',
    'Charnwood': 'CharnwoodScraper',
    'Conwy': 'ConwyScraper',
    'EastStaffordshire': 'EastStaffordshireScraper',
    'EppingForest': 'EppingForestScraper',
    'ForestHeath': 'ForestHeathScraper',
    'Hackney': 'HackneyScraper',
    'Islington': 'IslingtonScraper',
    'Lincoln': 'LincolnScraper',
    'Liverpool': 'LiverpoolScraper',
    # for following systems - see 2nd Planning Explorer scraper
    #'Mendip': 'MendipScraper',
    #'Merton': 'MertonScraper',
    #'NorthYorkMoors': 'NorthYorkMoorsScraper', # National Park
    #'Runnymede': 'RunnymedeScraper',
    #'SouthLanarkshire': 'SouthLanarkshireScraper',
    #'SouthNorfolk': 'SouthNorfolkScraper',    # now Idox
    #'SouthTyneside': 'SouthTynesideScraper',
    #'Swansea': 'SwanseaScraper',
    #'Tamworth': 'TamworthScraper',
    #'Trafford': 'TraffordScraper',
    #'WalthamForest': 'WalthamForestScraper',
    #'Wandsworth': 'WandsworthScraper',
    #'Wiltshire': 'WiltshireScraper',
     }

class PlanningExplorerScraper(base.DateScraper):

    MAX_ID_BATCH = 300 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go

    HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
    }
    CRLFTAB_REGEX = re.compile(r'%0D|%0A|%09')
    BADCHAR_REGEX = re.compile(r'\xc2')

    date_from_field = 'dateStart'
    date_to_field = 'dateEnd'
    search_fields = { 'rbGroup': ['rbRange'] }
    search_form = 'M3Form'
    search_submit = '#csbtnSearch'
    ref_field = 'txtApplicationNumber'
    applic_fields = { 'rbGroup': ['rbNotApplicable'] }
    scrape_dates_link = '<a href="{{ dates_link }}"> Application Dates </a>'
    scrape_ids = """
    <table class="display_table"> <tr />
    {* <tr>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    </tr> *}
    </table>
    """
    scrape_next_link = '<a href="{{ next_link }}"> <img title="Go to next page"> </a>'

    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = '<body> Details Page {{ block|html }} </body>'
    scrape_dates_block = '<body> Dates Page {{ block|html }} </body>'
    # the minimum acceptable valid dataset on the details page
    scrape_min_data = """
    <li> <span> Application Registered </span> {{ date_validated }} </li>
    <li> <span> Application Number </span> {{ reference }} </li>
    <li> <span> Site Address </span> {{ address }} </li>
    <li> <span> Proposal </span> {{ description }} </li>
    """
    scrape_min_dates = """
    <li> <span> Received </span> {{ date_received }} </li>
    """
    # other optional parameters that can appear on the details page
    scrape_optional_data = [
    "<li> <span> Application Type </span> {{ application_type }} </li>",
    "<li> <span> Current Status </span> {{ status }} </li>",
    "<li> <span> Applicant </span> {{ applicant_name }} </li>",
    "<li> Applicant </li> <li> <span> Applicant Address </span> {{ applicant_address }} </li>",
    "<li> <span> Agent </span> {{ agent_name }} </li>",
    "<li> Agent </li> <li> <span> Agent Address </span> {{ agent_address }} </li>",
    "<li> <span> Ward </span> {{ ward_name }} </li>",
    "<li> <span> Electoral Division </span> {{ ward_name }} </li>",
    "<li> <span> Parishes </span> {{ parish }} </li>",
    "<li> <span> Parish </span> {{ parish }} </li>",
    "<li> <span> Community Council </span> {{ parish }} </li>",
    "<li> <span> Comments Until </span> {{ comment_date }} </li>",
    "<li> <span> Comments Welcome Until </span> {{ comment_date }} </li>",
    "<li> <span> Date of Committee </span> {{ meeting_date }} </li>",
    "<li> <span> Committee Date </span> {{ meeting_date }} </li>",
    "<li> <span> Decision </span> {{ decision }} </li>", 
    "<li> <span> Appeal Lodged </span> {{ appeal_date }} </li>",
    "<li> <span> Appeal Logged </span> {{ appeal_date }} </li> <li>",
    "<li> <span> Appeal Decision </span> {{ appeal_result }} </li>",
    "<li> <span> Appeal Decision </span> {{ appeal_result }} </li> <li> <span> Appeal Decision Date </span> {{ appeal_decision_date }} </li>",
    "<li> <span> Appeal Date </span> {{ appeal_date }} </li> <li> <span> Appeal Decision Date </span> {{ appeal_decision_date }} </li>",
    "<li> <span> Officer </span> {{ case_officer }} </li>",
    "<li> <span> District </span> {{ district }} </li>",
    "<li> <span> Constituency </span> {{ district }} </li>",
    "<li> <span> Determination Level </span> {{ decided_by }} </li>",
    "<li> Easting {{ easting }} Northing {{ northing }} </li>",
    "<li> <span> Consultation Period Ends </span> {{ consultation_end_date }} </li>",
    "<li> <span> Expiry Date for Consultations </span> {{ consultation_end_date }} </li>",
    "<li> <span> Committee Date </span> {{ meeting_date }} </li> <li> <span> Decision Date </span> {{ decision_date }} </li>",
    ]
    scrape_optional_dates = [
    "<li> <span> Validated </span> {{ date_validated }} </li>",
    "<li> <span> Valid From </span> {{ date_validated }} </li>",
    "<li> <span> Registered </span> {{ date_validated }} </li>",
    "<li> <span> Consultation Expiry </span> {{ consultation_end_date }} </li>",
    "<li> <span> Consultation Period Ends </span> {{ consultation_end_date }} </li>",
    "<li> <span> Date of First Consultation </span> {{ consultation_start_date }} </li>",
    "<li> <span> Statutory Expiry </span> {{ application_expires_date }} </li>",
    "<li> <span> Decision Expiry </span> {{ permission_expires_date }} </li>",
    "<li> <span> Target Date </span> {{ target_decision_date }} </li>",
    "<li> <span> Target Decision Date </span> {{ target_decision_date }} </li>",
    ]

    def get_id_batch (self, date_from, date_to):

        if self.DEBUG: self.br.set_debug_http(True)

        response = self.br.open(self.search_url)

        fields = self.search_fields
        fields[self.date_from_field] = date_from.strftime(self.request_date_format)
        fields[self.date_to_field] = date_to.strftime(self.request_date_format)
        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br, self.search_submit)
        final_result = []
        while response:
            html = response.read()
            url = response.geturl()
            if self.DEBUG: print html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            else:
                break
            try:
                result = scrapemark.scrape(self.scrape_next_link, html, url)
                next_url = self.CRLFTAB_REGEX.sub('', result['next_link'])
                response = self.br.open(next_url)
            except:
                response = None
        return final_result

    # post process a set of uid/url records: strips spaces etc in uid/url
    def clean_ids (self, records):
        for record in records:
            if record.get('uid'):
                record['uid'] = util.GAPS_REGEX.sub('', record['uid']) # strip any spaces
            if record.get('url'):
                new_v = util.GAPS_REGEX.sub('', record['url']) # strip any spaces
                record['url'] = self.CRLFTAB_REGEX.sub('', new_v) # strip CR/LF/tab related junk out

    # post process - clean out bad characters
    def clean_record (self, record):
        for k, v in record.items():
            if v: record[k] = self.BADCHAR_REGEX.sub('', v)
        return base.DateScraper.clean_record(self, record)

    def get_detail_from_uid (self, uid):
        response = self.br.open(self.search_url)
        fields = self.applic_fields
        fields[self.ref_field] = uid
        util.setup_form(self.br, self.search_form, fields)
        response = util.submit_form(self.br, self.search_submit)
        try:
            html = response.read()
            if self.DEBUG: print html
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            self.clean_ids(result['records'])
            url = result['records'][0]['url']
        except:
            return None
        return self.get_detail_from_url(url)

    # scrape detailed information on one record via its access URL
    def get_detail_from_url (self, url):
        if self.DEBUG: print "Url:", url
        try:
            response = self.br.open(url)
            html = response.read()
            url = response.geturl()
            if self.DEBUG:
                print "Html obtained from details url:", html
        except:
            if self.DEBUG: raise
            else: return None
        result = self.get_detail(html, url)
        if result:
            try:
                date_result = scrapemark.scrape(self.scrape_dates_link, html, url)
                if self.DEBUG: print date_result
                dates_url = self.CRLFTAB_REGEX.sub('', date_result['dates_link'])
                response = self.br.open(dates_url)
                html = response.read()
                url = response.geturl()
                if self.DEBUG:
                    print "Html obtained from dates url:", html
                result2 = self.get_detail(html, url, self.scrape_dates_block, self.scrape_min_dates, self.scrape_optional_dates)
                if result2:
                    result.update(result2)
            except:
                pass  
        return result

class BarnsleyScraper(PlanningExplorerScraper):

    TABLE_NAME = 'Barnsley'
    BATCH_DAYS = 18 # batch size for each scrape - number of days to gather to produce at least one result each time
    search_url = 'http://applications.barnsley.gov.uk/PlanningExplorer/GeneralSearch.aspx'
    search_form = '0'

class BirminghamScraper(PlanningExplorerScraper): # does not like returning large numbers

    TABLE_NAME = 'Birmingham'
    BATCH_DAYS = 6 # batch size for each scrape - number of days to gather to produce at least one result each time
    MIN_DAYS = 10 # min number of days to get when gathering current ids
    MAX_ID_BATCH = 250 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 150 # max application details to scrape in one go
    search_url = 'http://eplanning.birmingham.gov.uk/Northgate/PlanningExplorer/GeneralSearch.aspx'

class BlackburnScraper(PlanningExplorerScraper):

    TABLE_NAME = 'Blackburn'
    search_url = 'http://planning.blackburn.gov.uk/Northgate/PlanningExplorer/GeneralSearch.aspx'

class BroadlandScraper(PlanningExplorerScraper):

    TABLE_NAME = 'Broadland'
    search_url = 'http://www.broadland.gov.uk/Northgate/PlanningExplorer/GeneralSearch.aspx'
    search_form = '0'
    scrape_data_block = 'Details Page {{ block|html }} </body>'
    scrape_min_data = """
    <li> <span> Application Valid </span> {{ date_validated }} </li>
    <li> <span> Application Number </span> {{ reference }} </li>
    <li> <span> Site Address </span> {{ address }} </li>
    <li> <span> Proposal </span> {{ description }} </li>
    """

class CharnwoodScraper(PlanningExplorerScraper):

    search_url = 'http://portal.charnwood.gov.uk/Northgate/PlanningExplorerAA/GeneralSearch.aspx'

class CamdenScraper(PlanningExplorerScraper):

    search_url = 'http://planningrecords.camden.gov.uk/Northgate/PlanningExplorer17/GeneralSearch.aspx'

class ConwyScraper(PlanningExplorerScraper):

    search_url = 'http://www.conwy.gov.uk/Northgate/planningexplorerenglish/generalsearch.aspx'
    scrape_min_data = """
    <li> <span> Date Registered </span> {{ date_validated }} </li>
    <li> <span> Application Number </span> {{ reference }} </li>
    <li> <span> Site Address </span> {{ address }} </li>
    <li> <span> Proposal </span> {{ description }} </li>
    """

class EastStaffordshireScraper(PlanningExplorerScraper):

    search_url = 'http://www2.eaststaffsbc.gov.uk/Northgate/PlanningExplorer/GeneralSearch.aspx'

class EppingForestScraper(PlanningExplorerScraper):

    search_url = 'http://plan1.eppingforestdc.gov.uk/Northgate/PlanningExplorer/GeneralSearch.aspx'
    scrape_dates_link = '<h1 /> <a href="{{ dates_link }}"> Application Dates </a>'
    scrape_next_link = '<h1 /> <a href="{{ next_link }}"> <img title="Go to next page"> </a>'

class ForestHeathScraper(PlanningExplorerScraper):

    search_url = 'http://www.eplan.forest-heath.gov.uk/Northgate/PlanningExplorer/GeneralSearch.aspx'

class HackneyScraper(PlanningExplorerScraper):

    search_url = 'http://apps.hackney.gov.uk/servapps/Northgate/PlanningExplorer/generalsearch.aspx'

class IslingtonScraper(PlanningExplorerScraper):

    search_url = 'http://planning.islington.gov.uk/northgate/planningexplorer/generalsearch.aspx'

class LincolnScraper(PlanningExplorerScraper):

    search_url = 'http://online.lincoln.gov.uk/northgate/planningexplorer/generalsearch.aspx'

class LiverpoolScraper(PlanningExplorerScraper): # solves problem with expired results by reloading pages multiple times

    search_url = 'http://northgate.liverpool.gov.uk/PlanningExplorer17/GeneralSearch.aspx?'

    scrape_expired = '<span id="lblPagePosition"> The Results have expired. {{ expired }} </span>'

    def get_id_batch (self, date_from, date_to):

        if self.DEBUG: self.br.set_debug_http(True)

        response = self.br.open(self.search_url)
        fields = self.search_fields
        fields[self.date_from_field] = date_from.strftime(self.request_date_format)
        fields[self.date_to_field] = date_to.strftime(self.request_date_format)
        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br, self.search_submit)
        html = response.read()
        expired = scrapemark.scrape(self.scrape_expired, html)
        while expired:
            response = self.br.reload()
            html = response.read()
            expired = scrapemark.scrape(self.scrape_expired, html)
        final_result = []
        while response:
            url = response.geturl()
            if self.DEBUG: print html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            else:
                break
            try:
                result = scrapemark.scrape(self.scrape_next_link, html, url)
                next_url = self.CRLFTAB_REGEX.sub('', result['next_link'])
                response = self.br.open(next_url)
                html = response.read()
                expired = scrapemark.scrape(self.scrape_expired, html)
                while expired:
                    response = self.br.reload()
                    html = response.read()
                    expired = scrapemark.scrape(self.scrape_expired, html)
            except:
                response = None
        return final_result

    def get_detail_from_uid (self, uid):
        response = self.br.open(self.search_url)
        fields = self.applic_fields
        fields[self.ref_field] = uid
        util.setup_form(self.br, self.search_form, fields)
        response = util.submit_form(self.br, self.search_submit)
        try:
            html = response.read()
            expired = scrapemark.scrape(self.scrape_expired, html)
            while expired:
                response = self.br.reload()
                html = response.read()
                expired = scrapemark.scrape(self.scrape_expired, html)
            url = response.geturl()
            if self.DEBUG: print html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            self.clean_ids(result['records'])
            url = result['records'][0]['url']
        except:
            return None
        return self.get_detail_from_url(url)

    # scrape detailed information on one record via its access URL
    def get_detail_from_url (self, url):
        if self.DEBUG: print "Url:", url
        try:
            response = self.br.open(url)
            html = response.read()
            expired = scrapemark.scrape(self.scrape_expired, html)
            while expired:
                response = self.br.reload()
                html = response.read()
                expired = scrapemark.scrape(self.scrape_expired, html)
            url = response.geturl()
            if self.DEBUG:
                print "Html obtained from details url:", html
        except:
            if self.DEBUG: raise
            else: return None
        result = self.get_detail(html, url)
        if result:
            try:
                date_result = scrapemark.scrape(self.scrape_dates_link, html, url)
                if self.DEBUG: print date_result
                dates_url = self.CRLFTAB_REGEX.sub('', date_result['dates_link'])
                response = self.br.open(dates_url)
                html = response.read()
                expired = scrapemark.scrape(self.scrape_expired, html)
                while expired:
                    response = self.br.reload()
                    html = response.read()
                    expired = scrapemark.scrape(self.scrape_expired, html)
                url = response.geturl()
                if self.DEBUG:
                    print "Html obtained from dates url:", html
                result2 = self.get_detail(html, url, self.scrape_dates_block, self.scrape_min_dates, self.scrape_optional_dates)
                if result2:
                    result.update(result2)
            except:
                pass  
        return result

class MendipScraper(PlanningExplorerScraper):

    search_url = 'http://planning.mendip.gov.uk/northgate/planningexplorer/generalsearch.aspx'
    scrape_data_block = '<body> Search Details {{ block|html }} </body>'

class MertonScraper(PlanningExplorerScraper):

    search_url = 'http://planning.merton.gov.uk/Northgate/PlanningExplorerAA/GeneralSearch.aspx'

class NorthYorkMoorsScraper(PlanningExplorerScraper): # National Park

    search_url = 'http://planning.northyorkmoors.org.uk/Northgate/PlanningExplorer/GeneralSearch.aspx'

class RunnymedeScraper(PlanningExplorerScraper):

    search_url = 'http://planning.runnymede.gov.uk/Northgate/PlanningExplorer/GeneralSearch.aspx'
    scrape_data_block = '<body> Application Details {{ block|html }} </body>'
    scrape_min_data = """
    <li> <span> Application Number </span> {{ reference }} </li>
    <li> <span> Site Address </span> {{ address }} </li>
    <li> <span> Proposal </span> {{ description }} </li>
    <li> <span> Valid Date </span> {{ date_validated }} </li>
    """


class SouthLanarkshireScraper(PlanningExplorerScraper):

    search_url = 'http://pbsportal.southlanarkshire.gov.uk/Northgate/PlanningExplorerV17/GeneralSearch.aspx'

class SouthNorfolkScraper(PlanningExplorerScraper):

    search_url = 'http://planning.south-norfolk.gov.uk/Northgate/PlanningExplorer/GeneralSearch.aspx'

class SouthTynesideScraper(PlanningExplorerScraper):

    search_url = 'http://poppy.southtyneside.gov.uk/Northgate/PlanningExplorer/GeneralSearch.aspx'

class SwanseaScraper(PlanningExplorerScraper):

    search_url = 'http://www2.swansea.gov.uk/Northgate/PlanningExplorer/GeneralSearch.aspx'

class TamworthScraper(PlanningExplorerScraper):

    search_url = 'http://planning.tamworth.gov.uk/northgate/planningexplorer/generalsearch.aspx'

class TraffordScraper(PlanningExplorerScraper):

    search_url = 'http://planning.trafford.gov.uk/Northgate/PlanningExplorerAA/GeneralSearch.aspx'

class WalthamForestScraper(PlanningExplorerScraper):

    BATCH_DAYS = 28 # batch size for each scrape - number of days to gather to produce at least one result each time
    MIN_DAYS = 28 # min number of days to get when gathering current ids
    search_url = 'http://planning.walthamforest.gov.uk/PlanningExplorer/GeneralSearch.aspx'

class WandsworthScraper(PlanningExplorerScraper):

    search_url = 'http://ww3.wandsworth.gov.uk/Northgate/PlanningExplorer/GeneralSearch.aspx'
    scrape_data_block = '<body> Page for Planning Application {{ block|html }} </body>'

class WiltshireScraper(PlanningExplorerScraper): # now covers Salisbury and Devizes (and Chippenham and Trowbridge?)

    TABLE_NAME = 'Wiltshire'
    search_url = 'http://planning.wiltshire.gov.uk/Northgate/PlanningExplorer/GeneralSearch.aspx'
    scrape_ids = """
    <table summary="Results of the Search"> <tr />
    {* <tr>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    </tr> *}
    </table>"""
    scrape_next_link = '<a href="{{ next_link }}" title="Go to the next page"> </a>'
    scrape_data_block = '<div id="article"> {{ block|html }} </div>'
    scrape_min_data = """
    <h2> Planning application {{ reference }} </h2>
    <dt> Registered </dt> <dd> {{ date_validated }} </dd>
    <dt> Site Address </dt> <dd> {{ address }} </dd>
    <dt> Proposed Development </dt> <dd> {{ description }} </dd>
    """
    scrape_optional_data = [
    "<dt> Application Type </dt> <dd> {{ application_type }} </dd>",
    "<dt> Decision </dt> <dd> {{ decision_date }} ( {{ decision }} ) </dd>",
    "<dt> Current Status </dt> <dd> {{ status }} </dd>",
    "<dt> Applicant </dt> <dd> {{ applicant_name }} </dd>",
    "<dt> Applicant </dt> <dt> Applicant Address </dt> <dd> {{ applicant_address }} </dd>",
    "<dt> Agent </dt> <dd> {{ agent_name }} </li>",
    "<dt> Agent </dt> <dt> Agent Address </dt> <dd> {{ agent_address }} </dd>",
    "<dt> Wards </dt> <dd> {{ ward_name }} </dd>",
    "<dt> Parishes </dt> <dd> {{ parish }} </dd>",
    "<dt> Case Officer </dt> <dd> {{ case_officer }} </dd>",
    "<dt> Target Date For Decision </dt> <dd> {{ target_decision_date }} </dd>",
    "<dt> Consultation Expiry </dt> <dd> {{ consultation_end_date }} </dd>",
    "<dt> Committee Date </dt> <dd> {{ meeting_date }} </dd>",
    '<li class="commentlink"> <a href="{{ comment_url|abs }}" /> </li>'
    ]

    # scrape detailed information on one record via its access URL
    def get_detail_from_url (self, url):
        return base.DateScraper.get_detail_from_url (self, url)

if __name__ == 'scraper':

    #scraper = EastStaffordshireScraper('EastStaffordshire')
    #scraper.replace_all_with('explorealike_planning_applications', 'EastStaffordshire')
    #scraper.run()
    #scraper.gather_current_ids()
    #sys.exit()

    sys_list = []
    for k, v in systems.items(): # get latest date scraped for each system
        sys_list.append( (k, v, scraperwiki.sqlite.get_var('latest-' + k)) )
    sort_sys = sorted(sys_list, key=lambda system: system[2]) # sort so least recent are first
    for auth in sort_sys[:6]: # do max 6 per run
        strexec = auth[1] + "('" + auth[0] + "')"
        print "Scraping from:", strexec
        try:
            scraper = eval(strexec)
            scraper.run()
        except Exception as err:
            print "Error - skipping this authority -", str(err)
    print "Finished"

    #scraper.run()
    #scraper.DEBUG = True

    # misc test calls
    #scraper = BarnsleyScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('2011/1001') # Barnsley OK
    #scraper = BirminghamScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('2012/06298/PA') # Birmingham OK
    #scraper = BlackburnScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('10/11/0878') # Blackburn OK
    #scraper = BroadlandScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('20111169') # Broadland OK
    #scraper = CamdenScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('2011/4317/P') # Camden OK
    #scraper = CharnwoodScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('P/11/1816/2') # Charnwood OK
    #scraper = ConwyScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('0/38507') # Conwy OK
    #scraper = EastStaffordshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('P/2012/00774') # EastStaffordshire OK
    #scraper = EppingForestScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('EPF/1680/11') # EppingForest OK
    #scraper = ForestHeathScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('F/2011/0509/LBC') # ForestHeath OK
    #scraper = HackneyScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('2011/2184') # Hackney OK
    #scraper = IslingtonScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('P121406') # Islington OK
    #scraper = LincolnScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('2011/1030/F') # Lincoln OK
    #scraper = LiverpoolScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11F/1844') # Liverpool OK
    #scraper = MendipScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('2011/2111') # Mendip OK
    #scraper = MertonScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/P2351') # Merton OK
    #scraper = NorthYorkMoorsScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('NYM/2012/0543/FL') # NorthYorkMoors OK
    #scraper = RunnymedeScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('RU.11/1249') # Runnymede
    #scraper = SouthLanarkshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('CL/11/0401') # SouthLanarkshire OK
    #scraper = SouthNorfolkScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('2011/1357') # SouthNorfolk - now Idox
    #scraper = SouthTynesideScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('ST/1355/11/FUL') # SouthTyneside OK
    #scraper = SwanseaScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('2011/1134') # Swansea OK
    #scraper = TamworthScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('0424/2011') # Tamworth OK
    #scraper = TraffordScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('77342/HHA/2011') # Trafford OK
    #scraper = WalthamForestScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('2011/1234') # WalthamForest OK
    #scraper = WandsworthScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('2011/2375') # Wandsworth OK
    #scraper = WiltshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('S/2012/1252') # Wiltshire OK
    #print scraper.get_detail_from_uid ('13/00688/FUL')

    #res = scraper.get_id_batch(util.get_dt('20/06/2012'), util.get_dt('25/06/2012'))
    #print res, len(res)
    #print scraper.get_id_batch(util.get_dt('23/03/2012'), util.get_dt('25/03/2012'))


    

# this is a base scraper for PlanningExplorer system planning applications for use by Openly Local

# there are 25 authorities using this system, all 25 are defined but only 13 are scraped here

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import random
import urllib
import urlparse
import sys

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

systems = {
    'Barnsley': 'BarnsleyScraper',
    'Birmingham': 'BirminghamScraper',
    'Blackburn': 'BlackburnScraper',
    'Broadland': 'BroadlandScraper',
    'Camden': 'CamdenScraper',
    'Charnwood': 'CharnwoodScraper',
    'Conwy': 'ConwyScraper',
    'EastStaffordshire': 'EastStaffordshireScraper',
    'EppingForest': 'EppingForestScraper',
    'ForestHeath': 'ForestHeathScraper',
    'Hackney': 'HackneyScraper',
    'Islington': 'IslingtonScraper',
    'Lincoln': 'LincolnScraper',
    'Liverpool': 'LiverpoolScraper',
    # for following systems - see 2nd Planning Explorer scraper
    #'Mendip': 'MendipScraper',
    #'Merton': 'MertonScraper',
    #'NorthYorkMoors': 'NorthYorkMoorsScraper', # National Park
    #'Runnymede': 'RunnymedeScraper',
    #'SouthLanarkshire': 'SouthLanarkshireScraper',
    #'SouthNorfolk': 'SouthNorfolkScraper',    # now Idox
    #'SouthTyneside': 'SouthTynesideScraper',
    #'Swansea': 'SwanseaScraper',
    #'Tamworth': 'TamworthScraper',
    #'Trafford': 'TraffordScraper',
    #'WalthamForest': 'WalthamForestScraper',
    #'Wandsworth': 'WandsworthScraper',
    #'Wiltshire': 'WiltshireScraper',
     }

class PlanningExplorerScraper(base.DateScraper):

    MAX_ID_BATCH = 300 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go

    HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
    }
    CRLFTAB_REGEX = re.compile(r'%0D|%0A|%09')
    BADCHAR_REGEX = re.compile(r'\xc2')

    date_from_field = 'dateStart'
    date_to_field = 'dateEnd'
    search_fields = { 'rbGroup': ['rbRange'] }
    search_form = 'M3Form'
    search_submit = '#csbtnSearch'
    ref_field = 'txtApplicationNumber'
    applic_fields = { 'rbGroup': ['rbNotApplicable'] }
    scrape_dates_link = '<a href="{{ dates_link }}"> Application Dates </a>'
    scrape_ids = """
    <table class="display_table"> <tr />
    {* <tr>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    </tr> *}
    </table>
    """
    scrape_next_link = '<a href="{{ next_link }}"> <img title="Go to next page"> </a>'

    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = '<body> Details Page {{ block|html }} </body>'
    scrape_dates_block = '<body> Dates Page {{ block|html }} </body>'
    # the minimum acceptable valid dataset on the details page
    scrape_min_data = """
    <li> <span> Application Registered </span> {{ date_validated }} </li>
    <li> <span> Application Number </span> {{ reference }} </li>
    <li> <span> Site Address </span> {{ address }} </li>
    <li> <span> Proposal </span> {{ description }} </li>
    """
    scrape_min_dates = """
    <li> <span> Received </span> {{ date_received }} </li>
    """
    # other optional parameters that can appear on the details page
    scrape_optional_data = [
    "<li> <span> Application Type </span> {{ application_type }} </li>",
    "<li> <span> Current Status </span> {{ status }} </li>",
    "<li> <span> Applicant </span> {{ applicant_name }} </li>",
    "<li> Applicant </li> <li> <span> Applicant Address </span> {{ applicant_address }} </li>",
    "<li> <span> Agent </span> {{ agent_name }} </li>",
    "<li> Agent </li> <li> <span> Agent Address </span> {{ agent_address }} </li>",
    "<li> <span> Ward </span> {{ ward_name }} </li>",
    "<li> <span> Electoral Division </span> {{ ward_name }} </li>",
    "<li> <span> Parishes </span> {{ parish }} </li>",
    "<li> <span> Parish </span> {{ parish }} </li>",
    "<li> <span> Community Council </span> {{ parish }} </li>",
    "<li> <span> Comments Until </span> {{ comment_date }} </li>",
    "<li> <span> Comments Welcome Until </span> {{ comment_date }} </li>",
    "<li> <span> Date of Committee </span> {{ meeting_date }} </li>",
    "<li> <span> Committee Date </span> {{ meeting_date }} </li>",
    "<li> <span> Decision </span> {{ decision }} </li>", 
    "<li> <span> Appeal Lodged </span> {{ appeal_date }} </li>",
    "<li> <span> Appeal Logged </span> {{ appeal_date }} </li> <li>",
    "<li> <span> Appeal Decision </span> {{ appeal_result }} </li>",
    "<li> <span> Appeal Decision </span> {{ appeal_result }} </li> <li> <span> Appeal Decision Date </span> {{ appeal_decision_date }} </li>",
    "<li> <span> Appeal Date </span> {{ appeal_date }} </li> <li> <span> Appeal Decision Date </span> {{ appeal_decision_date }} </li>",
    "<li> <span> Officer </span> {{ case_officer }} </li>",
    "<li> <span> District </span> {{ district }} </li>",
    "<li> <span> Constituency </span> {{ district }} </li>",
    "<li> <span> Determination Level </span> {{ decided_by }} </li>",
    "<li> Easting {{ easting }} Northing {{ northing }} </li>",
    "<li> <span> Consultation Period Ends </span> {{ consultation_end_date }} </li>",
    "<li> <span> Expiry Date for Consultations </span> {{ consultation_end_date }} </li>",
    "<li> <span> Committee Date </span> {{ meeting_date }} </li> <li> <span> Decision Date </span> {{ decision_date }} </li>",
    ]
    scrape_optional_dates = [
    "<li> <span> Validated </span> {{ date_validated }} </li>",
    "<li> <span> Valid From </span> {{ date_validated }} </li>",
    "<li> <span> Registered </span> {{ date_validated }} </li>",
    "<li> <span> Consultation Expiry </span> {{ consultation_end_date }} </li>",
    "<li> <span> Consultation Period Ends </span> {{ consultation_end_date }} </li>",
    "<li> <span> Date of First Consultation </span> {{ consultation_start_date }} </li>",
    "<li> <span> Statutory Expiry </span> {{ application_expires_date }} </li>",
    "<li> <span> Decision Expiry </span> {{ permission_expires_date }} </li>",
    "<li> <span> Target Date </span> {{ target_decision_date }} </li>",
    "<li> <span> Target Decision Date </span> {{ target_decision_date }} </li>",
    ]

    def get_id_batch (self, date_from, date_to):

        if self.DEBUG: self.br.set_debug_http(True)

        response = self.br.open(self.search_url)

        fields = self.search_fields
        fields[self.date_from_field] = date_from.strftime(self.request_date_format)
        fields[self.date_to_field] = date_to.strftime(self.request_date_format)
        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br, self.search_submit)
        final_result = []
        while response:
            html = response.read()
            url = response.geturl()
            if self.DEBUG: print html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            else:
                break
            try:
                result = scrapemark.scrape(self.scrape_next_link, html, url)
                next_url = self.CRLFTAB_REGEX.sub('', result['next_link'])
                response = self.br.open(next_url)
            except:
                response = None
        return final_result

    # post process a set of uid/url records: strips spaces etc in uid/url
    def clean_ids (self, records):
        for record in records:
            if record.get('uid'):
                record['uid'] = util.GAPS_REGEX.sub('', record['uid']) # strip any spaces
            if record.get('url'):
                new_v = util.GAPS_REGEX.sub('', record['url']) # strip any spaces
                record['url'] = self.CRLFTAB_REGEX.sub('', new_v) # strip CR/LF/tab related junk out

    # post process - clean out bad characters
    def clean_record (self, record):
        for k, v in record.items():
            if v: record[k] = self.BADCHAR_REGEX.sub('', v)
        return base.DateScraper.clean_record(self, record)

    def get_detail_from_uid (self, uid):
        response = self.br.open(self.search_url)
        fields = self.applic_fields
        fields[self.ref_field] = uid
        util.setup_form(self.br, self.search_form, fields)
        response = util.submit_form(self.br, self.search_submit)
        try:
            html = response.read()
            if self.DEBUG: print html
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            self.clean_ids(result['records'])
            url = result['records'][0]['url']
        except:
            return None
        return self.get_detail_from_url(url)

    # scrape detailed information on one record via its access URL
    def get_detail_from_url (self, url):
        if self.DEBUG: print "Url:", url
        try:
            response = self.br.open(url)
            html = response.read()
            url = response.geturl()
            if self.DEBUG:
                print "Html obtained from details url:", html
        except:
            if self.DEBUG: raise
            else: return None
        result = self.get_detail(html, url)
        if result:
            try:
                date_result = scrapemark.scrape(self.scrape_dates_link, html, url)
                if self.DEBUG: print date_result
                dates_url = self.CRLFTAB_REGEX.sub('', date_result['dates_link'])
                response = self.br.open(dates_url)
                html = response.read()
                url = response.geturl()
                if self.DEBUG:
                    print "Html obtained from dates url:", html
                result2 = self.get_detail(html, url, self.scrape_dates_block, self.scrape_min_dates, self.scrape_optional_dates)
                if result2:
                    result.update(result2)
            except:
                pass  
        return result

class BarnsleyScraper(PlanningExplorerScraper):

    TABLE_NAME = 'Barnsley'
    BATCH_DAYS = 18 # batch size for each scrape - number of days to gather to produce at least one result each time
    search_url = 'http://applications.barnsley.gov.uk/PlanningExplorer/GeneralSearch.aspx'
    search_form = '0'

class BirminghamScraper(PlanningExplorerScraper): # does not like returning large numbers

    TABLE_NAME = 'Birmingham'
    BATCH_DAYS = 6 # batch size for each scrape - number of days to gather to produce at least one result each time
    MIN_DAYS = 10 # min number of days to get when gathering current ids
    MAX_ID_BATCH = 250 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 150 # max application details to scrape in one go
    search_url = 'http://eplanning.birmingham.gov.uk/Northgate/PlanningExplorer/GeneralSearch.aspx'

class BlackburnScraper(PlanningExplorerScraper):

    TABLE_NAME = 'Blackburn'
    search_url = 'http://planning.blackburn.gov.uk/Northgate/PlanningExplorer/GeneralSearch.aspx'

class BroadlandScraper(PlanningExplorerScraper):

    TABLE_NAME = 'Broadland'
    search_url = 'http://www.broadland.gov.uk/Northgate/PlanningExplorer/GeneralSearch.aspx'
    search_form = '0'
    scrape_data_block = 'Details Page {{ block|html }} </body>'
    scrape_min_data = """
    <li> <span> Application Valid </span> {{ date_validated }} </li>
    <li> <span> Application Number </span> {{ reference }} </li>
    <li> <span> Site Address </span> {{ address }} </li>
    <li> <span> Proposal </span> {{ description }} </li>
    """

class CharnwoodScraper(PlanningExplorerScraper):

    search_url = 'http://portal.charnwood.gov.uk/Northgate/PlanningExplorerAA/GeneralSearch.aspx'

class CamdenScraper(PlanningExplorerScraper):

    search_url = 'http://planningrecords.camden.gov.uk/Northgate/PlanningExplorer17/GeneralSearch.aspx'

class ConwyScraper(PlanningExplorerScraper):

    search_url = 'http://www.conwy.gov.uk/Northgate/planningexplorerenglish/generalsearch.aspx'
    scrape_min_data = """
    <li> <span> Date Registered </span> {{ date_validated }} </li>
    <li> <span> Application Number </span> {{ reference }} </li>
    <li> <span> Site Address </span> {{ address }} </li>
    <li> <span> Proposal </span> {{ description }} </li>
    """

class EastStaffordshireScraper(PlanningExplorerScraper):

    search_url = 'http://www2.eaststaffsbc.gov.uk/Northgate/PlanningExplorer/GeneralSearch.aspx'

class EppingForestScraper(PlanningExplorerScraper):

    search_url = 'http://plan1.eppingforestdc.gov.uk/Northgate/PlanningExplorer/GeneralSearch.aspx'
    scrape_dates_link = '<h1 /> <a href="{{ dates_link }}"> Application Dates </a>'
    scrape_next_link = '<h1 /> <a href="{{ next_link }}"> <img title="Go to next page"> </a>'

class ForestHeathScraper(PlanningExplorerScraper):

    search_url = 'http://www.eplan.forest-heath.gov.uk/Northgate/PlanningExplorer/GeneralSearch.aspx'

class HackneyScraper(PlanningExplorerScraper):

    search_url = 'http://apps.hackney.gov.uk/servapps/Northgate/PlanningExplorer/generalsearch.aspx'

class IslingtonScraper(PlanningExplorerScraper):

    search_url = 'http://planning.islington.gov.uk/northgate/planningexplorer/generalsearch.aspx'

class LincolnScraper(PlanningExplorerScraper):

    search_url = 'http://online.lincoln.gov.uk/northgate/planningexplorer/generalsearch.aspx'

class LiverpoolScraper(PlanningExplorerScraper): # solves problem with expired results by reloading pages multiple times

    search_url = 'http://northgate.liverpool.gov.uk/PlanningExplorer17/GeneralSearch.aspx?'

    scrape_expired = '<span id="lblPagePosition"> The Results have expired. {{ expired }} </span>'

    def get_id_batch (self, date_from, date_to):

        if self.DEBUG: self.br.set_debug_http(True)

        response = self.br.open(self.search_url)
        fields = self.search_fields
        fields[self.date_from_field] = date_from.strftime(self.request_date_format)
        fields[self.date_to_field] = date_to.strftime(self.request_date_format)
        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br, self.search_submit)
        html = response.read()
        expired = scrapemark.scrape(self.scrape_expired, html)
        while expired:
            response = self.br.reload()
            html = response.read()
            expired = scrapemark.scrape(self.scrape_expired, html)
        final_result = []
        while response:
            url = response.geturl()
            if self.DEBUG: print html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            else:
                break
            try:
                result = scrapemark.scrape(self.scrape_next_link, html, url)
                next_url = self.CRLFTAB_REGEX.sub('', result['next_link'])
                response = self.br.open(next_url)
                html = response.read()
                expired = scrapemark.scrape(self.scrape_expired, html)
                while expired:
                    response = self.br.reload()
                    html = response.read()
                    expired = scrapemark.scrape(self.scrape_expired, html)
            except:
                response = None
        return final_result

    def get_detail_from_uid (self, uid):
        response = self.br.open(self.search_url)
        fields = self.applic_fields
        fields[self.ref_field] = uid
        util.setup_form(self.br, self.search_form, fields)
        response = util.submit_form(self.br, self.search_submit)
        try:
            html = response.read()
            expired = scrapemark.scrape(self.scrape_expired, html)
            while expired:
                response = self.br.reload()
                html = response.read()
                expired = scrapemark.scrape(self.scrape_expired, html)
            url = response.geturl()
            if self.DEBUG: print html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            self.clean_ids(result['records'])
            url = result['records'][0]['url']
        except:
            return None
        return self.get_detail_from_url(url)

    # scrape detailed information on one record via its access URL
    def get_detail_from_url (self, url):
        if self.DEBUG: print "Url:", url
        try:
            response = self.br.open(url)
            html = response.read()
            expired = scrapemark.scrape(self.scrape_expired, html)
            while expired:
                response = self.br.reload()
                html = response.read()
                expired = scrapemark.scrape(self.scrape_expired, html)
            url = response.geturl()
            if self.DEBUG:
                print "Html obtained from details url:", html
        except:
            if self.DEBUG: raise
            else: return None
        result = self.get_detail(html, url)
        if result:
            try:
                date_result = scrapemark.scrape(self.scrape_dates_link, html, url)
                if self.DEBUG: print date_result
                dates_url = self.CRLFTAB_REGEX.sub('', date_result['dates_link'])
                response = self.br.open(dates_url)
                html = response.read()
                expired = scrapemark.scrape(self.scrape_expired, html)
                while expired:
                    response = self.br.reload()
                    html = response.read()
                    expired = scrapemark.scrape(self.scrape_expired, html)
                url = response.geturl()
                if self.DEBUG:
                    print "Html obtained from dates url:", html
                result2 = self.get_detail(html, url, self.scrape_dates_block, self.scrape_min_dates, self.scrape_optional_dates)
                if result2:
                    result.update(result2)
            except:
                pass  
        return result

class MendipScraper(PlanningExplorerScraper):

    search_url = 'http://planning.mendip.gov.uk/northgate/planningexplorer/generalsearch.aspx'
    scrape_data_block = '<body> Search Details {{ block|html }} </body>'

class MertonScraper(PlanningExplorerScraper):

    search_url = 'http://planning.merton.gov.uk/Northgate/PlanningExplorerAA/GeneralSearch.aspx'

class NorthYorkMoorsScraper(PlanningExplorerScraper): # National Park

    search_url = 'http://planning.northyorkmoors.org.uk/Northgate/PlanningExplorer/GeneralSearch.aspx'

class RunnymedeScraper(PlanningExplorerScraper):

    search_url = 'http://planning.runnymede.gov.uk/Northgate/PlanningExplorer/GeneralSearch.aspx'
    scrape_data_block = '<body> Application Details {{ block|html }} </body>'
    scrape_min_data = """
    <li> <span> Application Number </span> {{ reference }} </li>
    <li> <span> Site Address </span> {{ address }} </li>
    <li> <span> Proposal </span> {{ description }} </li>
    <li> <span> Valid Date </span> {{ date_validated }} </li>
    """


class SouthLanarkshireScraper(PlanningExplorerScraper):

    search_url = 'http://pbsportal.southlanarkshire.gov.uk/Northgate/PlanningExplorerV17/GeneralSearch.aspx'

class SouthNorfolkScraper(PlanningExplorerScraper):

    search_url = 'http://planning.south-norfolk.gov.uk/Northgate/PlanningExplorer/GeneralSearch.aspx'

class SouthTynesideScraper(PlanningExplorerScraper):

    search_url = 'http://poppy.southtyneside.gov.uk/Northgate/PlanningExplorer/GeneralSearch.aspx'

class SwanseaScraper(PlanningExplorerScraper):

    search_url = 'http://www2.swansea.gov.uk/Northgate/PlanningExplorer/GeneralSearch.aspx'

class TamworthScraper(PlanningExplorerScraper):

    search_url = 'http://planning.tamworth.gov.uk/northgate/planningexplorer/generalsearch.aspx'

class TraffordScraper(PlanningExplorerScraper):

    search_url = 'http://planning.trafford.gov.uk/Northgate/PlanningExplorerAA/GeneralSearch.aspx'

class WalthamForestScraper(PlanningExplorerScraper):

    BATCH_DAYS = 28 # batch size for each scrape - number of days to gather to produce at least one result each time
    MIN_DAYS = 28 # min number of days to get when gathering current ids
    search_url = 'http://planning.walthamforest.gov.uk/PlanningExplorer/GeneralSearch.aspx'

class WandsworthScraper(PlanningExplorerScraper):

    search_url = 'http://ww3.wandsworth.gov.uk/Northgate/PlanningExplorer/GeneralSearch.aspx'
    scrape_data_block = '<body> Page for Planning Application {{ block|html }} </body>'

class WiltshireScraper(PlanningExplorerScraper): # now covers Salisbury and Devizes (and Chippenham and Trowbridge?)

    TABLE_NAME = 'Wiltshire'
    search_url = 'http://planning.wiltshire.gov.uk/Northgate/PlanningExplorer/GeneralSearch.aspx'
    scrape_ids = """
    <table summary="Results of the Search"> <tr />
    {* <tr>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    </tr> *}
    </table>"""
    scrape_next_link = '<a href="{{ next_link }}" title="Go to the next page"> </a>'
    scrape_data_block = '<div id="article"> {{ block|html }} </div>'
    scrape_min_data = """
    <h2> Planning application {{ reference }} </h2>
    <dt> Registered </dt> <dd> {{ date_validated }} </dd>
    <dt> Site Address </dt> <dd> {{ address }} </dd>
    <dt> Proposed Development </dt> <dd> {{ description }} </dd>
    """
    scrape_optional_data = [
    "<dt> Application Type </dt> <dd> {{ application_type }} </dd>",
    "<dt> Decision </dt> <dd> {{ decision_date }} ( {{ decision }} ) </dd>",
    "<dt> Current Status </dt> <dd> {{ status }} </dd>",
    "<dt> Applicant </dt> <dd> {{ applicant_name }} </dd>",
    "<dt> Applicant </dt> <dt> Applicant Address </dt> <dd> {{ applicant_address }} </dd>",
    "<dt> Agent </dt> <dd> {{ agent_name }} </li>",
    "<dt> Agent </dt> <dt> Agent Address </dt> <dd> {{ agent_address }} </dd>",
    "<dt> Wards </dt> <dd> {{ ward_name }} </dd>",
    "<dt> Parishes </dt> <dd> {{ parish }} </dd>",
    "<dt> Case Officer </dt> <dd> {{ case_officer }} </dd>",
    "<dt> Target Date For Decision </dt> <dd> {{ target_decision_date }} </dd>",
    "<dt> Consultation Expiry </dt> <dd> {{ consultation_end_date }} </dd>",
    "<dt> Committee Date </dt> <dd> {{ meeting_date }} </dd>",
    '<li class="commentlink"> <a href="{{ comment_url|abs }}" /> </li>'
    ]

    # scrape detailed information on one record via its access URL
    def get_detail_from_url (self, url):
        return base.DateScraper.get_detail_from_url (self, url)

if __name__ == 'scraper':

    #scraper = EastStaffordshireScraper('EastStaffordshire')
    #scraper.replace_all_with('explorealike_planning_applications', 'EastStaffordshire')
    #scraper.run()
    #scraper.gather_current_ids()
    #sys.exit()

    sys_list = []
    for k, v in systems.items(): # get latest date scraped for each system
        sys_list.append( (k, v, scraperwiki.sqlite.get_var('latest-' + k)) )
    sort_sys = sorted(sys_list, key=lambda system: system[2]) # sort so least recent are first
    for auth in sort_sys[:6]: # do max 6 per run
        strexec = auth[1] + "('" + auth[0] + "')"
        print "Scraping from:", strexec
        try:
            scraper = eval(strexec)
            scraper.run()
        except Exception as err:
            print "Error - skipping this authority -", str(err)
    print "Finished"

    #scraper.run()
    #scraper.DEBUG = True

    # misc test calls
    #scraper = BarnsleyScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('2011/1001') # Barnsley OK
    #scraper = BirminghamScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('2012/06298/PA') # Birmingham OK
    #scraper = BlackburnScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('10/11/0878') # Blackburn OK
    #scraper = BroadlandScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('20111169') # Broadland OK
    #scraper = CamdenScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('2011/4317/P') # Camden OK
    #scraper = CharnwoodScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('P/11/1816/2') # Charnwood OK
    #scraper = ConwyScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('0/38507') # Conwy OK
    #scraper = EastStaffordshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('P/2012/00774') # EastStaffordshire OK
    #scraper = EppingForestScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('EPF/1680/11') # EppingForest OK
    #scraper = ForestHeathScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('F/2011/0509/LBC') # ForestHeath OK
    #scraper = HackneyScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('2011/2184') # Hackney OK
    #scraper = IslingtonScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('P121406') # Islington OK
    #scraper = LincolnScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('2011/1030/F') # Lincoln OK
    #scraper = LiverpoolScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11F/1844') # Liverpool OK
    #scraper = MendipScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('2011/2111') # Mendip OK
    #scraper = MertonScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/P2351') # Merton OK
    #scraper = NorthYorkMoorsScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('NYM/2012/0543/FL') # NorthYorkMoors OK
    #scraper = RunnymedeScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('RU.11/1249') # Runnymede
    #scraper = SouthLanarkshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('CL/11/0401') # SouthLanarkshire OK
    #scraper = SouthNorfolkScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('2011/1357') # SouthNorfolk - now Idox
    #scraper = SouthTynesideScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('ST/1355/11/FUL') # SouthTyneside OK
    #scraper = SwanseaScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('2011/1134') # Swansea OK
    #scraper = TamworthScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('0424/2011') # Tamworth OK
    #scraper = TraffordScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('77342/HHA/2011') # Trafford OK
    #scraper = WalthamForestScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('2011/1234') # WalthamForest OK
    #scraper = WandsworthScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('2011/2375') # Wandsworth OK
    #scraper = WiltshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('S/2012/1252') # Wiltshire OK
    #print scraper.get_detail_from_uid ('13/00688/FUL')

    #res = scraper.get_id_batch(util.get_dt('20/06/2012'), util.get_dt('25/06/2012'))
    #print res, len(res)
    #print scraper.get_id_batch(util.get_dt('23/03/2012'), util.get_dt('25/03/2012'))


    

