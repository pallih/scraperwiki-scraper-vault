# this is a scraper of Civica system planning applications for use by Openly Local

# note most of these are based on Ruby originals by Tom Hughes (which are much more elegantly coded)

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import random
import urllib
import urlparse
import copy
import gc

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

systems = [ 
    'BroxbourneScraper', 
    'DarlingtonScraper', 
    'DenbighshireScraper', 
    'EastbourneScraper', 
    'ErewashScraper', 
    'HarrowScraper', 
    'MaldonScraper', 
    'NorthamptonScraper', 
    'PendleScraper', 
    'StAlbansScraper', 
    'WrexhamScraper',
    ]

class CivicaScraper(base.DateScraper):

    MAX_ID_BATCH = 350 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go

    HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:8.0) Gecko/20100101 Firefox/8.0',
    'Accept-Charset': 'UTF-8,*',
    'Accept': 'text/html',
    'Accept-Language': 'en-gb,en',
    }
    search_form = '0'
    next_form = '0'
    ref_form = None
    ref_submit = None
    search_fields = {}
    start_url = ''
    scrape_max_pages = '<table class="scroller"> {{ max_pages }} </table>'

    scrape_ids = """
    <table title="List of planning applications"> <tbody>
    {* <tr> <td> <input value="{{ [records].uid }}" /> </td> </tr> *}
    </tbody> </table>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="content"> {{ block|html }} </div>"
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = ""
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr> <td> Postcode </td> <td> {{ postcode }} </td> </tr>',
    '<tr> <td> Officer </td> <td> {{ case_officer }} </td> </tr>',
    '<tr> <td> Case Officer </td> <td> {{ case_officer }} </td> </tr>',
    '<tr> <td> Decision Type </td> <td> {{ decided_by }} </td> </tr>',
    '<tr> <td> Decision Level </td> <td> {{ decided_by }} </td> </tr>',
    '<tr> <td> Decision Date </td> <td> {{ decision_date }} </td> </tr>',
    '<tr> <td> Decision Due Date </td> <td> {{ target_decision_date }} </td> </tr>',
    '<tr> <td> Target Date </td> <td> {{ target_decision_date }} </td> </tr>',
    '<tr> <td> 8 Week Determination Date </td> <td> {{ target_decision_date }} </td> </tr>',
    '<tr> <td> Community </td> <td> {{ parish }} </td> </tr>',
    '<tr> <td> UPRN </td> <td> {{ uprn }} </td> </tr>',
    '<tr> <td> Planning Portal Reference </td> <td> {{ planning_portal_id }} </td> </tr>',
    '<tr> <td> Parish </td> <td> {{ parish }} </td> </tr>',
    '<tr> <td> Ward </td> <td> {{ ward_name }} </td> </tr>',
    '<tr> <td> Case Type </td> <td> {{ application_type }} </td> </tr>',
    '<tr> <td> Application Type </td> <td> {{ application_type }} </td> </tr>',
    '<tr> <td> Status </td> <td> {{ status }} </td> </tr>',
    '<tr> <td> Development Type </td> <td> {{ development_type }} </td> </tr>',
    '<tr> <td> Applicant Name </td> <td> {{ applicant_name }} </td> </tr>',
    '<tr> <td> Agent Name </td> <td> {{ agent_name }} </td> </tr>',
    '<tr> <td> Agent Address </td> <td> {{ agent_address }} </td> </tr>',
    '<tr> <td> Committee Date </td> <td> {{ meeting_date }} </td> </tr>',
    '<tr> <td> Consultation End Date </td> <td> {{ consultation_end_date }} </td> </tr>',
    '<tr> <td> Consultee Finish Date </td> <td> {{ consultation_end_date }} </td> </tr>',
    '<tr> <td> Appeal Lodged Date </td> <td> {{ appeal_date }} </td> </tr>',
    '<tr> <td> Appeal Start Date </td> <td> {{ appeal_date }} </td> </tr>',
    '<tr> <td> Appeal Decision Date </td> <td> {{ appeal_decision_date }} </td> </tr>',
    '<tr> <td> Date Advertised </td> <td> {{ last_advertised_date }} </td> </tr>',

    'Postcode <tr> <td> Area </td> <td> {{ district }} </td> </tr>',
    'Case Officer <tr> <td> Decision </td> <td> {{ decision }} </td> </tr>',
    'Received Date <tr> <td> Decision </td> <td> {{ decision }} </td> </tr>',
    '<tr> <td> Committee </td> <td> {{ decided_by }} </td> </tr> Committee Date',
    'Appeal Lodged <tr> <td> Appeal Decision </td> <td> {{ appeal_result }} </td> </tr>',
    """Hectares <tr> <td> Applicant </td> <td> {{ applicant_name }} </td> </tr>
    <td> Agent </td> <td> {{ agent_name }} </td> </tr>""",
    'Decision Level <tr> <td> Decision </td> <td> {{ decision }} </td> </tr> Decision Date ',
    ]

    def get_id_batch (self, date_from, date_to):

        if self.start_url:
            response = self.br.open(self.start_url)
            if self.DEBUG: print response.read()

        response = self.br.open(self.search_url)
        if self.DEBUG: print response.read()

        fields = {}
        fields.update(self.search_fields)
        fields [self.date_from_field] = date_from.strftime(self.request_date_format)
        fields [self.date_to_field] = date_to.strftime(self.request_date_format)
        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br, self.search_submit)

        html = response.read()
        if self.DEBUG: print html
        try:
            result = scrapemark.scrape(self.scrape_max_pages, html)
            page_list = result['max_pages'].split()
            max_pages = int(page_list[-1]) # can be a space separated list, so take the last value
        except:
            max_pages = 1
        if self.DEBUG: print "max pages:", max_pages

        if max_pages >= 10: # limit of 10 pages is the max, so if we hit it then split things up
            half_days = int((date_to - date_from).days / 2)
            mid_date = date_from + timedelta(days=half_days)
            result1 = self.get_id_batch(date_from, mid_date)
            result2 = self.get_id_batch(mid_date + timedelta(days=1), date_to)
            result1.extend(result2)
            return result1

        page_count = 1
        final_result = []
        while page_count <= max_pages:
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            else:
                break
            page_count += 1
            if page_count > max_pages:
                break
            try:
                fields = { self.next_field: 'next' }
                util.setup_form(self.br, self.next_form, fields)
                if self.DEBUG: print self.br.form
                response = util.submit_form(self.br)
                html = response.read()
            except:
                break
            
        return final_result

    def get_detail_from_uid (self, uid):
        
        try:
            if self.start_url:
                response = self.br.open(self.start_url)
            response = self.br.open(self.search_url)
            fields = { self.ref_field: uid }
            if self.ref_form:
                util.setup_form(self.br, self.ref_form, fields)
            else:
                util.setup_form(self.br, self.search_form, fields)
            if self.DEBUG: print self.br.form
            if self.ref_submit:
                response = util.submit_form(self.br, self.ref_submit)
            else:
                response = util.submit_form(self.br, self.search_submit)
            html = response.read()
            if self.DEBUG: print html
            url = response.geturl()
        except:
            return None

        return self.get_detail(html, url)

class BroxbourneScraper(CivicaScraper):

    TABLE_NAME = 'Broxbourne'
    start_url = 'http://planning.broxbourne.gov.uk/Planning/_javascriptDetector_?goto=/Planning/lg/GFPlanningSearch.page%3FParam=lg.Planning%26org.apache.shale.dialog.DIALOG_NAME=gfplanningsearch'
    search_url = 'http://planning.broxbourne.gov.uk/Planning/lg/plansearch.page?org.apache.shale.dialog.DIALOG_NAME=gfplanningsearch&Param=lg.Planning'

    date_from_field = '_id68:received_dateFrom'
    date_to_field = '_id68:received_dateTo'
    search_submit = '_id68:_id81'
    ref_field = '_id68:ref_no'
    next_field = '_id71:scroll_1'

    scrape_min_data = """
    <td> Reference Number </td> <td> {{ reference }} </td>
    <td> Location </td> <td> {{ address }} </td>
    <td> Proposal </td> <td> {{ description }} </td>
    <td> Received Date </td> <td> {{ date_received }} </td>
    <td> Valid Date </td> <td> {{ date_validated }} </td>
    """

class DarlingtonScraper(CivicaScraper):

    TABLE_NAME = 'Darlington'
    start_url = 'http://msp.darlington.gov.uk/Planning/_javascriptDetector_?goto=/Planning/lg/GFPlanningSearch.page'
    search_url = 'http://msp.darlington.gov.uk/Planning/lg/plansearch.page?org.apache.shale.dialog.DIALOG_NAME=gfplanningsearch&Param=lg.Planning'

    date_from_field = '_id113:SDate5From'
    date_to_field = '_id113:SDate5To'
    search_submit = '_id113:_id160'
    ref_field = '_id113:SDescription'
    next_field = '_id116:scroll_1'

    scrape_min_data = """
    <table title="Address Details"> UPRN {* <tr> <td /> <td> {{ [address] }} </td> </tr> *} Area </table>
    <table> <td> Case No </td> <td> {{ reference }} </td>
    <td> Date Received </td> <td> {{ date_received }} </td>
    <td> Date Valid </td> <td> {{ date_validated }} </td>
    <td> Proposal </td> <td> {{ description }} </td> </table>
    """

class DenbighshireScraper(CivicaScraper):

    TABLE_NAME = 'Denbighshire'
    start_url = 'http://planning.denbighshire.gov.uk/Planning/_javascriptDetector_?goto=/Planning/lg/GFPlanningSearch.page'
    search_url = 'http://planning.denbighshire.gov.uk/Planning/lg/plansearch.page?org.apache.shale.dialog.DIALOG_NAME=gfplanningsearch&Param=lg.Planning'

    search_form = '2'
    next_form = '2'
    date_from_field = '_id143:valid_dateFrom'
    date_to_field = '_id143:valid_dateTo'
    search_submit = '_id143:_id155'
    ref_field = '_id143:ref_no'
    next_field = '_id146:scroll_1'

    scrape_min_data = """
    <td> Location </td> <td> {{ address }} </td>
    <td> Reference Number </td> <td> {{ reference }} </td>
    <td> Proposal </td> <td> {{ description }} </td>
    <td> Received Date </td> <td> {{ date_received }} </td>
    <td> Valid Date </td> <td> {{ date_validated }} </td>
    """

class EastbourneScraper(CivicaScraper):

    TABLE_NAME = 'Eastbourne'
    #start_url = 'http://planning.eastbourne.gov.uk/Planning/_javascriptDetector_?goto=/lg/GFPlanningSearch.page '
    search_url = 'http://planning.eastbourne.gov.uk/lg/plansearch.page?org.apache.shale.dialog.DIALOG_NAME=gfplanningsearch&Param=APP.Planning'

    search_form = '2'
    next_form = '1'
    date_from_field = '_id292:ApplicationValidDateFrom'
    date_to_field = '_id292:ApplicationValidDateTo'
    search_submit = '_id292:_id349'
    ref_field = '_id292:KeyNo'
    next_field = '_id278:scroll_1'

    scrape_min_data = """
    <table title="Address Details"> {* <tr> <td /> <td> {{ [address] }} </td> </tr> *} Ward </table>
    <table> <td> Previous Application </td> <td> {{ reference }} </td>
    <td> Description </td> <td> {{ description }} </td> 
    <td> Received Date </td> <td> {{ date_received }} </td>
    <td> Valid Date </td> <td> {{ date_validated }} </td> </table>
    """

class ErewashScraper(CivicaScraper):

    TABLE_NAME = 'Erewash'
    BATCH_DAYS = 21
    MIN_DAYS = 21
    start_url = 'http://planportal.erewash.gov.uk/PlanningLive/_javascriptDetector_?goto=/PlanningLive/lg/GFPlanningSearch.page'
    search_url = 'http://planportal.erewash.gov.uk/PlanningLive/lg/plansearch.page?org.apache.shale.dialog.DIALOG_NAME=gfplanningsearch&Param=lg.Planning'

    date_from_field = 'ResponseDateFrom'
    date_to_field = 'ResponseDateTo'
    search_submit = '_id44:_id63'
    ref_field = '_id44:LARef'
    next_field = '_id49:scroll_1'

    scrape_data_block = """
    <div id="MainContentArea">{{ block|html }} </div>"
    """
    scrape_min_data = """
    <table> Address Details {* <tr> <td /> <td> {{ [address] }} </td> </tr> *} Ward </table>
    <table> <td> Application Reference </td> <td> {{ reference }} </td>
    <td> Application Description </td> <td> {{ description }} </td>
    <td> Valid Date </td> <td> {{ date_validated }} </td>
    </table>
    """

    def get_id_batch (self, date_from, date_to):

        if self.start_url:
            response = self.br.open(self.start_url)
            if self.DEBUG: print response.read()

        current_day = date.today().weekday() 
        ref_date = date.today() - timedelta(days=current_day) # reference date is Monday (day 0) of the current week
        fields = {}
        fields [self.date_from_field] = "fw%+d" % (date_from - ref_date).days
        fields [self.date_to_field] = "fw%+d" % (date_to - ref_date).days
        query_url = util.add_to_query(self.search_url, fields)
        if self.DEBUG: print query_url

        response = self.br.open(query_url)
        html = response.read()
        if self.DEBUG: print html

        try:
            result = scrapemark.scrape(self.scrape_max_pages, html)
            page_list = result['max_pages'].split()
            max_pages = int(page_list[-1]) # can be a space separated list, so take the last value
        except:
            max_pages = 1
        if self.DEBUG: print "max pages:", max_pages

        if max_pages >= 10: # 10 pages is the max, so if we hit it then split things up
            half_days = int((date_to - date_from).days / 2)
            mid_date = date_from + timedelta(days=half_days)
            result1 = self.get_id_batch(date_from, mid_date)
            result2 = self.get_id_batch(mid_date + timedelta(days=1), date_to)
            result1.extend(result2)
            return result1

        page_count = 1
        final_result = []
        while page_count <= max_pages:
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            else:
                break
            page_count += 1
            if page_count > max_pages:
                break
            try:
                fields = { self.next_field: 'next' }
                util.setup_form(self.br, self.next_form, fields)
                if self.DEBUG: print self.br.form
                response = util.submit_form(self.br)
                html = response.read()
            except:
                break
            
        return final_result

class HarrowScraper(CivicaScraper):

    TABLE_NAME = 'Harrow'
    search_url = 'http://www.harrow.gov.uk/planningsearch/lg/plansearch.page?org.apache.shale.dialog.DIALOG_NAME=planningsearch&Param=lg.Planning&searchType=quick'

    search_form = '4'
    ref_form = '1'
    date_from_field = '_id185:SDate2From'
    date_to_field = '_id185:SDate2To'
    search_submit = '_id185:_id273'
    ref_submit = '_id164:_id266'
    ref_field = '_id164:SDescription'
    next_field = '_id61:scroll_2'

    scrape_max_pages = '<div class="scroller"> {{ max_pages }} </div>'

    scrape_ids = """
    <table title="List of planning applications"> <tbody>
    {* <tr> <td> {{ [records].uid }} </td> </tr>
    *}
    </tbody> </table>"""

    scrape_data_block = """
    <div id="civicabody"> {{ block|html }} </div>"
    """
    scrape_min_data = """
    <table> Application Address {* <tr> <td /> <td> {{ [address] }} </td> </tr> *} Ward </table>
    <table> <td> Application Number </td> <td> {{ reference }} </td>
    <td> Date Registered </td> <td> {{ date_validated }} </td>
    <td> Proposal </td> <td> {{ description }} </td> </table>
    """

class MaldonScraper(CivicaScraper):

    TABLE_NAME = 'Maldon'
    start_url = 'http://myplan80.maldon.gov.uk/Planning/_javascriptDetector_?goto=/Planning/lg/GFPlanningWelcome.page'
    search_url = 'http://myplan80.maldon.gov.uk/Planning/lg/plansearch.page?org.apache.shale.dialog.DIALOG_NAME=gfplanningsearch&Param=lg.Planning'

    date_from_field = '_id61:SDate1From'
    date_to_field = '_id61:SDate1To'
    search_submit = '_id61:_id105'
    ref_field = '_id61:SDescription'
    next_field = '_id60:scroll_1'

    scrape_data_block = """
    <div class="bodycontent"> {{ block|html }} </div>"
    """
    scrape_min_data = """
    <table title="Address Details"> UPRN {* <tr> <td /> <td> {{ [address] }} </td> </tr> *} Area </table>
    <table> <td> Case No </td> <td> {{ reference }} </td>
    <td> Date Received </td> <td> {{ date_received }} </td>
    <td> Date Valid </td> <td> {{ date_validated }} </td>
    <td> Proposal </td> <td> {{ description }} </td> </table>
    """

class NorthamptonScraper(CivicaScraper):

    TABLE_NAME = 'Northampton'
    start_url = 'http://planning.northamptonboroughcouncil.com/Planning/_javascriptDetector_?goto=/Planning/lg/GFPlanningSearch.page%3FParam=lg.Planning%26org.apache.shale.dialog.DIALOG_NAME=gfplanningsearch'
    search_url = 'http://planning.northamptonboroughcouncil.com/Planning/lg/GFPlanningSearch.page?Param=lg.Planning&org.apache.shale.dialog.DIALOG_NAME=gfplanningsearch'

    search_form = '1'
    next_form = '1'
    date_from_field = '_id122:SDate1From'
    date_to_field = '_id122:SDate1To'
    search_submit = '_id122:_id162'
    ref_field = '_id122:SDescription'
    next_field = '_id123:scroll_1'

    scrape_min_data = """
    <table title="Address Details"> {* <tr> <td /> <td> {{ [address] }} </td> </tr> *} Parish </table>
    <table> <td> Application Number </td> <td> {{ reference }} </td>
    <td> Proposal </td> <td> {{ description }} </td>
    <td> Date Received </td> <td> {{ date_received }} </td>
    <td> Date Valid </td> <td> {{ date_validated }} </td> </table>
    """

class PendleScraper(CivicaScraper):

    TABLE_NAME = 'Pendle'
    start_url = 'http://planning.pendle.gov.uk/Planning/lg/GFPlanningSearch.page'
    search_url = 'http://planning.pendle.gov.uk/Planning/lg/plansearch.page?org.apache.shale.dialog.DIALOG_NAME=gfplanningsearch&Param=lg.Planning'

    date_from_field = '_id96:SDate1From'
    date_to_field = '_id96:SDate1To'
    search_submit = '_id96:_id139'
    ref_field = '_id96:SDescription'
    next_field = '_id99:scroll_1'

    scrape_min_data = """
    <table title="Address Details"> {* <tr> <td /> <td> {{ [address] }} </td> </tr> *} </table>
    <table> <td> Case Reference </td> <td> {{ reference }} </td>
    <td> Proposal/Details </td> <td> {{ description }} </td>
    <td> Date Registered </td> <td> {{ date_validated }} </td> </table>
    """

class StAlbansScraper(CivicaScraper):

    TABLE_NAME = 'StAlbans'
    start_url = 'http://planning.stalbans.gov.uk/Planning/_javascriptDetector_?goto=/Planning/lg/GFPlanningWelcome.page'
    search_url = 'http://planning.stalbans.gov.uk/Planning/lg/plansearch.page?org.apache.shale.dialog.DIALOG_NAME=gfplanningsearch&Param=lg.Planning'

    date_from_field = '_id206:received_dateFrom'
    date_to_field = '_id206:received_dateTo'
    search_submit = '_id206:_id284'
    ref_field = '_id206:ref_no'
    next_field = '_id209:scroll_1'

    scrape_min_data = """
    <td> Application Reference </td> <td> {{ reference }} </td>
    <td> Location </td> <td> {{ address }} </td>
    <td> Proposal </td> <td> {{ description }} </td>
    <td> Received Date </td> <td> {{ date_received }} </td> 
    <td> Registration Date </td> <td> {{ date_validated }} </td> 
    """

class WrexhamScraper(CivicaScraper):

    TABLE_NAME = 'Wrexham'
    start_url = 'http://planning.wrexham.gov.uk/Planning/_javascriptDetector_?goto=/Planning/lg/GFPlanningWelcome.page'
    search_url = 'http://planning.wrexham.gov.uk/Planning/lg/plansearch.page?org.apache.shale.dialog.DIALOG_NAME=gfplanningsearch&Param=lg.Planning'

    date_from_field = '_id423:SDate1From'
    date_to_field = '_id423:SDate1To'
    search_form = '2'
    next_form = '2'
    search_submit = '_id423:_id434'
    ref_field = '_id423:SDescription'
    next_field = '_id426:scroll_1'

    scrape_min_data = """
    <table title="Address Details"> {* <tr> <td /> <td> {{ [address] }} </td> </tr> *} Community </table>
    <table> <td> Case Number </td> <td> {{ reference }} </td>
    <td> Received Date </td> <td> {{ date_received }} </td>
    <td> Proposed development </td> <td> {{ description }} </td> </table>
    """

if __name__ == 'scraper':

    sys_list = []
    for k in systems: # get latest date scraped for each system
        try:
            scraper = eval(k + "()")
            latest_val = scraperwiki.sqlite.get_var('latest-' + scraper.TABLE_NAME)
            scraper = None
            gc.collect()
        except:
            latest_val = None
        sys_list.append( (k, latest_val) )
    sort_sys = sorted(sys_list, key=lambda system: system[1]) # sort so least recent are first
    for auth in sort_sys[:5]: # do max 5 per run
        strexec = auth[0] + "()"
        print "Scraping from:", strexec
        try:
            scraper = eval(strexec)
            scraper.run()
            scraper = None
            gc.collect()
        except Exception as err:
            print "Error - skipping this authority -", str(err)
    print "Finished"

    #scraper = BroxbourneScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('07/12/0629/LDC') # Broxbourne OK
    #scraper = DarlingtonScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('12/00531/FUL') # Darlington OK
    #scraper = DenbighshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('03/2012/1039') # Denbighshire OK
    #scraper = EastbourneScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('120699') # Eastbourne OK
    #scraper = ErewashScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('0313/0070') # Erewash OK
    #scraper = HarrowScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('P/2633/12/4721') # Harrow OK
    #scraper = MaldonScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('12/00358/FUL') # Maldon OK
    #scraper = NorthamptonScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('N/2012/0791') # Northampton OK
    #scraper = PendleScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('13/12/0352P') # Pendle OK
    #scraper = StAlbansScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('5/2012/2091') # St Albans OK
    #scraper = WrexhamScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('P/2011/0574') # Wrexham OK

    #result = scraper.get_id_batch(util.get_dt('15/04/2012'), util.get_dt('21/05/2012'))
    #print len(result), result

    




