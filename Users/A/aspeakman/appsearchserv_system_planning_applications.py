# this is a base scraper for Application Search Servlet system planning applications for use by Openly Local

# there are 15 authorities using this system (one is a Channel Island + two are Durham County sub-regions)

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
    'Allerdale': 'AllerdaleScraper',
    'Coventry': 'CoventryScraper',
    'Crook': 'CrookScraper', # Wear Valley now part of Durham
    'Ealing': 'EalingScraper',
    'Easington': 'EasingtonScraper', # now part of Durham
    'Guernsey': 'GuernseyScraper', # Channel Island
    'Haringey': 'HaringeyScraper',
    'Hartlepool': 'HartlepoolScraper',
    'HighPeak': 'HighPeakScraper',
    'NorthWarwickshire': 'NorthWarwickshireScraper',
    'Powys': 'PowysScraper',
    'Preston': 'PrestonScraper',
    #'Rutland': 'RutlandScraper', # now SwiftLG?
    'StHelens': 'StHelensScraper',
    'Wellingborough': 'WellingboroughScraper',
     }

class AppSearchServScraper(base.DateScraper):

    MAX_ID_BATCH = 300 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go
    HEADERS = {
    'Accept-Charset': 'UTF-8,*',
    'Accept': 'text/html',
    'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
    }

    date_from_field = 'ValidDateFrom'
    date_to_field = 'ValidDateTo'
    ref_field = 'ExistingRefNo'
    search_form = 'AppSearchForm'
    request_date_format = '%d-%m-%Y'
    scrape_ids = """
    <h1 /> <table> <tr />
    {* <tr>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    </tr> *}
    </table>
    """
    scrape_no_recs = '<div id="pageCenter"> {{ no_recs }} any results </div>'
    next_page_form = 'navigationForm2' 

    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <body> {{ block|html }} </body>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <tr> Reference <td> {{ reference }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [ ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)
        #print response.read()

        fields = {}
        fields[self.date_from_field] = date_from.strftime(self.request_date_format)
        fields[self.date_to_field] = date_to.strftime(self.request_date_format)
        if self.DEBUG: print fields
        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br)
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
                util.setup_form(self.br, self.next_page_form)
                response = util.submit_form(self.br)
            except:
                response = None
        return final_result

    def get_detail_from_uid (self, uid):
        response = self.br.open(self.search_url)
        html = response.read()

        fields = {  self.ref_field: uid }
        util.setup_form(self.br, self.search_form, fields)
        response = util.submit_form(self.br)
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

class AllerdaleScraper(AppSearchServScraper):

    search_url = 'http://planning.allerdale.gov.uk/portal/servlets/ApplicationSearchServlet'
    TABLE_NAME = 'Allerdale'

    scrape_no_recs = '<div id="content"> {{ no_recs }} not return any results </div>'

    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="content"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <tr> <th> Reference </th> <td> {{ reference }} </td> </tr>
    <tr> <th> Address </th> <td> {{ address|html }} </td> 
         <th> Development </th> <td> {{ description }} </td> </tr>
    <tr> <th> Valid </th> <td> {{ date_validated }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [ 
    "<tr> <th> Application Type </th> <td> {{ application_type }} </td> </tr>",
    "<tr> <th> Committee Date </th> <td> {{ meeting_date }} </td> </tr>",
    "<tr> <th> Officer </th> <td> {{ case_officer }} </td> </tr>",
    "<tr> <th> Decision </th> <td> {{ decision }} </td> <th> Decision Date </th> <td> {{ decision_date }} </td> </tr>",
    "<tr> <th> Consultation Start Date </th> <td> {{ consultation_start_date }} </td> </tr>",
    "<tr> <th> Consultation End Date </th> <td> {{ consultation_end_date }} </td> </tr>",
    "<tr> <th> Applicant Name </th> <td> {{ applicant_name|html }} </td> </tr>",
    "<tr> <th> Agent Name </th> <td> {{ agent_name|html }} </td> </tr>",
    "<tr> <th> Applicant Address </th> <td> {{ applicant_address|html }} </td> </tr>",
    "<tr> <th> Agent Address </th> <td> {{ agent_address|html }} </td> </tr>",
    ]

class CoventryScraper(AppSearchServScraper):

    search_url = 'http://planning.coventry.gov.uk/portal/servlets/ApplicationSearchServlet'
    TABLE_NAME = 'Coventry'

    scrape_no_recs = '<h1 class="mainTitle">Sorry, but your query did not return any results {{ no_recs }} </h1>'

    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="mainPad"> <table> <table> {{ block|html }} </table> </table> </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <tr> <td> Reference </td> <td> {{ reference }} </td> </tr>
    <tr> <td> Address </td> <td> {{ address|html }} </td>
         <td> Proposal </td> <td> {{ description }} </td> </tr>
    <tr> <td> Received </td> <td> {{ date_received }} </td> 
         <td> Valid </td> <td> {{ date_validated }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    "<tr> <td> Application Description </td> <td> {{ application_type }} </td> </tr>",
    "<tr> <td> Application Status </td> <td> {{ status }} </td> </tr>",
    "<tr> <td> Determination Required </td> <td> {{ target_decision_date }} </td> </tr>",
    "<tr> <td> Committee Date </td> <td> {{ meeting_date }} </td> </tr>",
    "<tr> <td> Officer </td> <td> {{ case_officer }} </td> </tr>",
    """<tr> <td> Decision By </td> <td> {{ decided_by }} </td> <td> Committee Date </td> </tr>
    <tr> <td> Decision </td> <td> {{ decision }} </td> <td> Decision Date </td> <td> {{ decision_date }} </td> </tr>""",
    "<tr> <td> Start of Public Consultation </td> <td> {{ consultation_start_date }} </td> </tr>",
    "<tr> <td> End of Public Consultation </td> <td> {{ consultation_end_date }} </td> </tr>",
    "<tr> <td> Applicant Name </td> <td> {{ applicant_name|html }} </td> </tr>",
    "<tr> <td> Agent Name </td> <td> {{ agent_name|html }} </td> </tr>",
    "<tr> <td> Applicant Address </td> <td> {{ applicant_address|html }} </td> </tr>",
    "<tr> <td> Agent Address </td> <td> {{ agent_address|html }} </td> </tr>",
    ]

class CrookScraper(AppSearchServScraper):

    search_url = 'http://planning.wearvalley.gov.uk/portal/servlets/ApplicationSearchServlet'
    TABLE_NAME = 'Crook'

    scrape_no_recs = """<div id="bodycontent"> <strong>Sorry, but your query did not 
    return any results, {{ no_recs }} </strong> </div>"""

    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="bodycontent"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <tr> <td> Reference </td> <td> {{ reference }} </td> </tr>
    <tr> <td> Address </td> <td> {{ address|html }} </td>
         <td> Development </td> <td> {{ description }} </td> </tr>
    <tr> <td> Valid </td> <td> {{ date_validated }} </td>
        <td> Received </td> <td> {{ date_received }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    "<tr> <td> Application Type </td> <td> {{ application_type }} </td> </tr>",
    "<tr> <td> Status </td> <td> {{ status }} </td> </tr>",
    "<tr> <td> Status </td> <td> {{ decision }} </td> </tr>",
    "<tr> <td> Committee Date </td> <td> {{ meeting_date }} </td> </tr>",
    "<tr> Agent Name <td> Officer </td> <td> {{ case_officer }} </td> </tr>",
    "<tr> <td> Decision Level </td> <td> {{ decided_by }} </td> </tr>",
    "<tr> <td> Decision Date </td> <td> {{ decision_date }} </td> </tr>",
    "<tr> <td> Consultation Start Date </td> <td> {{ consultation_start_date }} </td> </tr>",
    "<tr> <td> Consultation End Date </td> <td> {{ consultation_end_date }} </td> </tr>",
    "<tr> <td> Applicant Name </td> <td> {{ applicant_name|html }} </td> </tr>",
    "<tr> <td> Agent Name </td> <td> {{ agent_name|html }} </td> </tr>",
    "<tr> <td> Applicant Address </td> <td> {{ applicant_address|html }} </td> </tr>",
    "<tr> <td> Agent Address </td> <td> {{ agent_address|html }} </td> </tr>",
    ]

class EalingScraper(AppSearchServScraper):

    search_url = 'http://www.pam.ealing.gov.uk/portal/servlets/ApplicationSearchServlet'
    TABLE_NAME = 'Ealing'

    scrape_no_recs = '<div class="innerContent"> {{ no_recs }} any results </div>'

    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="content"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <tr> <td> Reference </td> <td> {{ reference }} </td> </tr>
    <tr> <td> Address </td> <td> {{ address|html }} </td> </tr>
    <tr> <td> Description </td> <td> {{ description }} </td> </tr>
    <tr> <td> Received </td> <td> {{ date_received }} </td> </tr>
    <tr> <td> Valid </td> <td> {{ date_validated }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    "<tr> <td> Application Type </td> <td> {{ application_type }} </td> </tr>",
    "<tr> <td> Ward </td> <td> {{ ward_name }} </td> </tr>",
    "<tr> <td> Determination Required </td> <td> {{ target_decision_date }} </td> </tr>",
    "<tr> <td> Committee/Delegated Date </td> <td> {{ meeting_date }} </td> </tr>",
    "<tr> <td> Officer </td> <td> {{ case_officer }} </td> </tr>",
    "<tr> <td> Committee or Delegated </td> <td> {{ decided_by }} </td> </tr>",
    "<tr> <td> Decision </td> <td> {{ decision }} </td> </tr> <tr> <td> Decision Date </td> <td> {{ decision_date }} </td> </tr>",
    "<tr> <td> Consultation Start Date </td> <td> {{ consultation_start_date }} </td> </tr>",
    "<tr> <td> Consultation End Date </td> <td> {{ consultation_end_date }} </td> </tr>",
    "<tr> <td> Applicant Name </td> <td> {{ applicant_name|html }} </td> </tr>",
    "<tr> <td> Agent Name </td> <td> {{ agent_name|html }} </td> </tr>",
    "<tr> <td> Applicant Address </td> <td> {{ applicant_address|html }} </td> </tr>",
    "<tr> <td> Agent Address </td> <td> {{ agent_address|html }} </td> </tr>",
    '<tr> <a href="{{comment_url|abs }}"> comment on this </a> </tr>',
    ]

class EasingtonScraper(AppSearchServScraper):

    search_url = 'http://planning.easington.gov.uk/portal/servlets/ApplicationSearchServlet'
    TABLE_NAME = 'Easington'

    scrape_no_recs = """<div id="contenthome"> <strong> Sorry, but your query did 
    not return any results, {{ no_recs }} </strong> </div>"""

    scrape_ids = """
    <h1 /> <table /> <table> <tr />
    {* <tr>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    </tr> *}
    </table>
    """

    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <form name="formPLNDetails"> {{ block|html }} </form>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <input value="{{ reference }}" name="REF_NO">
    <tr> <td> Address </td> <td> {{ address }} </td>
        <td> Description </td> <td> {{ description }} </td> </tr>
    <input value="{{ date_validated }}" name="DateValid">
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<input value="{{ application_type }}" name="ApplicationType">',
    '<input value="{{ ward_name }}" name="Ward">',
    '<input value="{{ parish }}" name="ParishDescription">',
    '<input value="{{ status }}" name="CurrentStatus">',
    '<input value="{{ decision }}" name="CurrentStatus">',
    '<input value="{{ decision_date }}" name="CurrentStatusDate">',
    '<input value="{{ decided_by }}" name="CommitteeType">',
    '<input value="{{ agent_name }}" name="AgentName">',
    '<input value="{{ applicant_name }}" name="ApplicantName">',
    "<tr> Handling Officer <td> {{ case_officer }} </td> </tr>",
    '<textarea name="AGE_ADDRESS"> {{ agent_address }} </textarea>',
    '<textarea name="APP_ADDRESS"> {{ applicant_address }} </textarea>',
    ]

class GuernseyScraper(AppSearchServScraper):

    search_url = 'http://planningexplorer.gov.gg/portal/servlets/ApplicationSearchServlet'
    TABLE_NAME = 'Guernsey'
    START_SEQUENCE = '2009-04-01'

    scrape_no_recs = '<div class="itemContent"> {{ no_recs }} not return any results </div>'

    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div class="itemContent"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <tr> <td> Number </td> <td> {{ reference }} </td> </tr>
    <tr> <td> Address </td> <td> {{ address|html }} </td> </tr>
    <tr> <td> Description </td> <td> {{ description }} </td> </tr>
    <tr> <td> Received </td> <td> {{ date_received }} </td> </tr>
    <tr> <td> Valid </td> <td> {{ date_validated }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    "<tr> <td> Application Type </td> <td> {{ application_type }} </td> </tr>",
    "<tr> <td> Current Status </td> <td> {{ status }} </td> </tr>",
    "<tr> <td> Current Status </td> <td> {{ decision }} </td> </tr>",
    "<tr> <td> Officer </td> <td> {{ case_officer }} </td> </tr>",
    "<tr> <td> Committee or Delegated </td> <td> {{ decided_by }} </td> </tr>",
    "<tr> <td> Decision Notification Date </td> <td> {{ decision_date }} </td> </tr>",
    "<tr> <td> Start of Consultation Date </td> <td> {{ consultation_start_date }} </td> </tr>",
    "<tr> <td> End of Consultation Date </td> <td> {{ consultation_end_date }} </td> </tr>",
    "<tr> <td> Applicant Name </td> <td> {{ applicant_name|html }} </td> </tr>",
    "<tr> <td> Agent </td> <td> {{ agent_name|html }} </td> </tr>",
    "<tr> <td> Applicant Address </td> <td> {{ applicant_address|html }} </td> </tr>",
    "<tr> <td> Agent Address </td> <td> {{ agent_address|html }} </td> </tr>",
    '<tr> <a href="{{comment_url|abs }}"> comment on this </a> </tr>',
    ]

class HaringeyScraper(AppSearchServScraper):

    search_url = 'http://www.planningservices.haringey.gov.uk/portal/servlets/ApplicationSearchServlet'
    TABLE_NAME = 'Haringey'

    scrape_no_recs = '<h2> {{ no_recs }} not return any results </h2>'

    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <form name="formPLNDetails"> {{ block|html }} </form>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <input value="{{ reference }}" name="REF_NO">
    <tr> <td> Location </td> <td> {{ address }} </td>
        <td> Development </td> <td> {{ description }} </td> </tr>
    <input value="{{ date_received }}" name="DateReceived">
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<input value="{{ application_type }}" name="ApplicationType">',
    '<input value="{{ planning_portal_id }}" name="PORTAL_REF">',
    '<input value="{{ ward_name }}" name="Ward">',
    '<input value="{{ easting }}" name="Eastings"> <input value="{{ northing }}" name="Northings">',
    '<input value="{{ status }}" name="CurrentStatus">',
    '<input value="{{ decision }}" name="CurrentStatus">',
    '<input value="{{ decision_date }}" name="CurrentStatusDate">',
    '<input value="{{ decided_by }}" name="CommitteeType">',
    '<input value="{{ agent_name }}" name="AgentName">',
    '<input value="{{ agent_tel }}" name="AG_Telephone">',
    '<input value="{{ meeting_date }}" name="CommitteeDate">',
    '<input value="{{ applicant_name }}" name="ApplicantName">',
    "<tr> <td> Officer </td> <td> {{ case_officer }} </td> </tr>",
    "<tr> <td> Agent Address </td> <td> {{ agent_address }} </td> </tr>",
    "<tr> <td> Applicant Address </td> <td> {{ applicant_address }} </td> </tr>",
    ]

class HartlepoolScraper(AppSearchServScraper):

    search_url = 'http://eforms.hartlepool.gov.uk:7777/portal/servlets/ApplicationSearchServlet'
    TABLE_NAME = 'Hartlepool'

    scrape_no_recs = """<h1>Search Results List</h1>
    <strong>Sorry, but your query did not return any results {{ no_recs }} </strong>"""

    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div class="box3"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <tr> <td> Reference </td> <td> {{ reference }} </td> </tr>
    <tr> <td> Development </td> </tr> <tr> <td> {{ description }} </td> </tr>
    <tr> <td> Address </td> <td> {{ address|html }} </td> 
         <td> Valid </td> <td> {{ date_validated }} </td> </tr>
    <tr> <td> Received </td> <td> {{ date_received }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    "<tr> <td> Application Type </td> <td> {{ application_type }} </td> </tr>",
    "<tr> <td> Target Date </td> <td> {{ target_decision_date }} </td> </tr>",
    "<tr> <td> Officer </td> <td> {{ case_officer }} </td> </tr>",
    "<tr> <td> Decision </td> <td> {{ decision }} </td> <td> Decision Date </td> <td> {{ decision_date }} </td> </tr>",
    "<tr> <td> Applicant Name </td> <td> {{ applicant_name|html }} </td> </tr>",
    "<tr> <td> Agent Details </td> <td> {{ agent_name|html }} <br> {{ agent_address|html }} </td> </tr>",
    "<tr> <td> Applicant Address </td> <td> {{ applicant_address|html }} </td> </tr>",
    ]

class HighPeakScraper(AppSearchServScraper):

    search_url = 'http://planning.highpeak.gov.uk/portal/servlets/ApplicationSearchServlet'
    TABLE_NAME = 'HighPeak'

    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="pageCenter"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <tr> <th> Reference </th> <td> {{ reference }} </td> </tr>
    <tr> <th> Address </th> <td> {{ address|html }} </td> </tr>
    <tr> <th> Description </th> <td> {{ description }} </td> </tr>
    <tr> <th> Received </th> <td> {{ date_received }} </td> </tr>
    <tr> <th> Valid </th> <td> {{ date_validated }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    "<tr> <th> Application Type </th> <td> {{ application_type }} </td> </tr>",
    "<tr> <th> Ward </th> <td> {{ ward_name }} </td> </tr>",
    "<tr> <th> Parish </th> <td> {{ parish }} </td> </tr>",
    "<tr> <th> Officer </th> <td> {{ case_officer }} </td> </tr>",
    "<tr> <th> Committee Type </th> <td> {{ decided_by }} </td> </tr>",
    "<tr> <th> Committee Date </th> <td> {{ meeting_date }} </td> </tr>",
    "<tr> <th> Decision </th> <td> {{ decision }} </td> </tr> <tr> <th> Decision Date </th> <td> {{ decision_date }} </td> </tr>",
    "<tr> <th> Consultation Start Date </th> <td> {{ consultation_start_date }} </td> </tr>",
    "<tr> <th> Consultation End Date </th> <td> {{ consultation_end_date }} </td> </tr>",
    "<tr> <th> Applicant Name </th> <td> {{ applicant_name|html }} </td> </tr>",
    "<tr> <th> Agent Name </th> <td> {{ agent_name|html }} </td> </tr>",
    "<tr> <th> Applicant Address </th> <td> {{ applicant_address|html }} </td> </tr>",
    "<tr> <th> Agent Address </th> <td> {{ agent_address|html }} </td> </tr>",
    ]


class NorthWarwickshireScraper(AppSearchServScraper):

    search_url = 'http://www.northwarks.gov.uk/info/200296/development_control/883/planning_application_search/2'
    TABLE_NAME = 'NorthWarwickshire'

    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="central"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <tr> <td> Reference </td> <td> {{ reference }} </td> </tr>
    <tr> <td> Location </td> <td> {{ address|html }} </td> </tr>
    <tr> <td> Proposal </td> <td> {{ description }} </td> </tr>
    <tr> <td> Received </td> <td> {{ date_received }} </td> </tr>
    <tr> <td> Valid </td> <td> {{ date_validated }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    "<tr> <td> Eastings </td> <td> {{ easting }} </td> </tr> <tr> <td> Northings </td> <td> {{ northing }} </td> </tr>",
    "<tr> <td> Ward </td> <td> {{ ward_name }} </td> </tr>",
    "<tr> <td> Parish </td> <td> {{ parish }} </td> </tr>",
    "<tr> <td> Case Officer </td> <td> {{ case_officer }} </td> </tr>",
    "<tr> <td> Decision Level </td> <td> {{ decided_by }} </td> </tr>",
    "<tr> <td> Decision </td> <td> {{ decision }} </td> </tr> <tr> <td> Decision Date </td> <td> {{ decision_date }} </td> </tr>",
    "<tr> <td> Consultation Start Date </td> <td> {{ consultation_start_date }} </td> </tr>",
    "<tr> <td> Consultation End Date </td> <td> {{ consultation_end_date }} </td> </tr>",
    "<tr> <td> Applicant Name </td> <td> {{ applicant_name|html }} </td> </tr>",
    "<tr> <td> Agent Name </td> <td> {{ agent_name|html }} </td> </tr>",
    "<tr> <td> Applicant Address </td> <td> {{ applicant_address|html }} </td> </tr>",
    "<tr> <td> Agent Address </td> <td> {{ agent_address|html }} </td> </tr>",
    ]

class PowysScraper(AppSearchServScraper):

    search_url = 'http://planning.powys.gov.uk/portal/servlets/ApplicationSearchServlet'
    TABLE_NAME = 'Powys'

    scrape_no_recs = '<div id="col-middle"> {{ no_recs }} not return any results </div>'

    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="col-middle"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <tr> <th> Reference </th> <td> {{ reference }} </td>
         <th> Received </th> <td> {{ date_received }} </td> </tr>
    <tr> <th> Address </th> <td> {{ address|html }} </td>
         <th> Development </th> <td> {{ description }} </td> </tr>
    <tr> <th> Valid </th> <td> {{ date_validated }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    "<tr> <th> Eastings </th> <td> {{ easting }} </td> <th> Northings </th> <td> {{ northing }} </td> </tr>",
    "<tr> <th> Community Council </th> <td> {{ district }} </td> </tr>",
    "<tr> <th> Officer </th> <td> {{ case_officer }} </td> </tr>",
    "<tr> <th> Committee Type </th> <td> {{ decided_by }} </td> </tr>",
    "<tr> <th> Committee Date </th> <td> {{ meeting_date }} </td> </tr>",
    "<tr> <th> Decision </th> <td> {{ decision }} </td> <th> Decision Date </th> <td> {{ decision_date }} </td> </tr>",
    "<tr> <th> Consultation Start Date </th> <td> {{ consultation_start_date }} </td> </tr>",
    "<tr> <th> Consultation End Date </th> <td> {{ consultation_end_date }} </td> </tr>",
    "<tr> <th> Applicant Name </th> <td> {{ applicant_name|html }} </td> </tr>",
    "<tr> <th> Agent Name </th> <td> {{ agent_name|html }} </td> </tr>",
    "<tr> <th> Applicant Address </th> <td> {{ applicant_address|html }} </td> </tr>",
    "<tr> <th> Agent Address </th> <td> {{ agent_address|html }} </td> </tr>",
    ]

class PrestonScraper(AppSearchServScraper): 

    search_url = 'http://publicaccess.preston.gov.uk/portal/servlets/ApplicationSearchServlet'
    TABLE_NAME = 'Preston'

    scrape_no_recs = '<h1> </h1> <p>Sorry, but your query did not return any results, {{ no_recs }} </p>'

    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div class="table"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <tr> <td> Reference </td> <td> {{ reference }} </td> </tr>
    <tr> <td> Address </td> <td> {{ address|html }} </td> </tr>
    <tr> <td> Description </td> <td> {{ description }} </td> </tr>
    <tr> <td> Received </td> <td> {{ date_received }} </td> </tr>
    <tr> <td> Valid </td> <td> {{ date_validated }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    "<tr> <td> Application Type </td> <td> {{ application_type }} </td> </tr>",
    "<tr> <td> Ward </td> <td> {{ ward_name }} </td> </tr>",
    "<tr> <td> Parish </td> <td> {{ parish }} </td> </tr>",
    "<tr> <td> Committee Date </td> <td> {{ meeting_date }} </td> </tr>",
    "<tr> <td> Case Officer </td> <td> {{ case_officer }} </td> </tr>",
    "<tr> <td> Committee Type </td> <td> {{ decided_by }} </td> </tr>",
    "<tr> <td> Decision </td> <td> {{ decision }} </td> </tr> <tr> <td> Decision Date </td> <td> {{ decision_date }} </td> </tr>",
    "<tr> <td> Consultation Start Date </td> <td> {{ consultation_start_date }} </td> </tr>",
    "<tr> <td> Consultation End Date </td> <td> {{ consultation_end_date }} </td> </tr>",
    "<tr> <td> Applicant Name </td> <td> {{ applicant_name|html }} </td> </tr>",
    "<tr> <td> Agent Name </td> <td> {{ agent_name|html }} </td> </tr>",
    "<tr> <td> Applicant Address </td> <td> {{ applicant_address|html }} </td> </tr>",
    "<tr> <td> Agent Address </td> <td> {{ agent_address|html }} </td> </tr>",
    ]

class RutlandScraper(AppSearchServScraper):

    search_url = 'http://planningonline.rutland.gov.uk:7777/portal/servlets/ApplicationSearchServlet'
    TABLE_NAME = 'Rutland'

    scrape_no_recs = '<div id="mainContent"> {{ no_recs }} not return any results, </div>'

    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="mainContent"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <tr> <th> Reference </th> <td> {{ reference }} </td> </tr>
    <tr> <th> Address </th> <td> {{ address|html }} </td>
         <th> Proposal </th> <td> {{ description }} </td> </tr>
    <tr> <th> Received </th> <td> {{ date_received }} </td>
         <th> Valid </th> <td> {{ date_validated }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    "<tr> <th> Application Type </th> <td> {{ application_type }} </td> </tr>",
    "<tr> <th> Eastings </th> <td> {{ easting }} </td> <th> Northings </th> <td> {{ northing }} </td> </tr>",
    "<tr> <th> Parish </th> <td> {{ parish }} </td> </tr>",
    "<tr> <th> Officer </th> <td> {{ case_officer }} </td> </tr>",
    "<tr> <th> Committee Type </th> <td> {{ decided_by }} </td> </tr>",
    "<tr> <th> Committee Date </th> <td> {{ meeting_date }} </td> </tr>",
    "<tr> <th> Status </th> <td> {{ status }} </td> </tr>",
    "<tr> <th> Status </th> <td> {{ decision }} </td> </tr>",
    "<tr> <th> Decision Date </th> <td> {{ decision_date }} </td> </tr>",
    "<tr> <th> Consultation Start Date </th> <td> {{ consultation_start_date }} </td> </tr>",
    "<tr> <th> Consultation End Date </th> <td> {{ consultation_end_date }} </td> </tr>",
    "<tr> <th> Applicant Name </th> <td> {{ applicant_name|html }} </td> </tr>",
    "<tr> <th> Agent Name </th> <td> {{ agent_name|html }} </td> </tr>",
    "<tr> <th> Applicant Address </th> <td> {{ applicant_address|html }} </td> </tr>",
    "<tr> <th> Agent Address </th> <td> {{ agent_address|html }} </td> </tr>",
    ]

class StHelensScraper(AppSearchServScraper):

    search_url = 'http://llpgport.oltps.sthelens.gov.uk:8080/portal/servlets/ApplicationSearchServlet'
    TABLE_NAME = 'StHelens'

    scrape_no_recs = '<p> Sorry, {{ no_recs }} not return any results </p>'

     # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div class="article"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <tr> <td> Reference </td> <td> {{ reference }} </td> </tr>
    <tr> <td> Address </td> <td> {{ address|html }} </td> </tr>
    <tr> <td> Received </td> <td> {{ date_received }} </td> 
         <td> Valid </td> <td> {{ date_validated }} </td> </tr>
    <tr> <td> Development </td> </tr> <tr> <td> {{ description }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    "<tr> <td> Application Type </td> <td> {{ application_type }} </td> </tr>",
    "<tr> <td> Eastings </td> <td> {{ easting }} <br> {{ northing }} </td> </tr>",
    "<tr> <td> Committee Date </td> <td> {{ meeting_date }} </td> </tr>",
    "<tr> <td> Officer </td> <td> {{ case_officer }} </td> </tr>",
    "<tr> <td> Decision Level </td> <td> {{ decided_by }} </td> </tr>",
    "<tr> <td> Decision </td> <td> {{ decision }} </td> <td> Decision Date </td> <td> {{ decision_date }} </td> </tr>",
    "<tr> <td> Consultation Start Date </td> <td> {{ consultation_start_date }} </td> </tr>",
    "<tr> <td> Consultation End Date </td> <td> {{ consultation_end_date }} </td> </tr>",
    "<tr> <td> Applicant Name </td> <td> {{ applicant_name|html }} </td> </tr>",
    "<tr> <td> Agent Name </td> <td> {{ agent_name|html }} </td> </tr>",
    "<tr> <td> Applicant Address </td> <td> {{ applicant_address|html }} </td> </tr>",
    "<tr> <td> Agent Address </td> <td> {{ agent_address|html }} </td> </tr>",
    ]

class WellingboroughScraper(AppSearchServScraper):

    search_url = 'http://planning.wellingborough.gov.uk/portal/servlets/ApplicationSearchServlet'
    TABLE_NAME = 'Wellingborough'

    scrape_no_recs = '<h1>Search Results List</h1> Sorry, but your query did not return any results, {{ no_recs }}'

    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <tr> <td> Reference </td> <td> {{ reference }} </td> </tr>
    <tr> <td> Address </td> <td> {{ address|html }} </td> </tr>
    <tr> <td> Description </td> <td> {{ description }} </td> </tr>
    <tr> <td> Received </td> <td> {{ date_received }} </td> </tr>
    <tr> <td> Valid </td> <td> {{ date_validated }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    "<tr> <td> Application Type </td> <td> {{ application_type }} </td> </tr>",
    "<tr> <td> Ward </td> <td> {{ ward_name }} </td> </tr>",
    "<tr> <td> Parish </td> <td> {{ parish }} </td> </tr>",
    "<tr> <td> Committee Date </td> <td> {{ meeting_date }} </td> </tr>",
    "<tr> <td> Officer </td> <td> {{ case_officer }} </td> </tr>",
    "<tr> <td> Committee Type </td> <td> {{ decided_by }} </td> </tr>",
    "<tr> <td> Decision </td> <td> {{ decision }} </td> </tr> <tr> <td> Decision Date </td> <td> {{ decision_date }} </td> </tr>",
    "<tr> <td> Consultation Start Date </td> <td> {{ consultation_start_date }} </td> </tr>",
    "<tr> <td> Consultation End Date </td> <td> {{ consultation_end_date }} </td> </tr>",
    "<tr> <td> Applicant Name </td> <td> {{ applicant_name|html }} </td> </tr>",
    "<tr> <td> Agent Name </td> <td> {{ agent_name|html }} </td> </tr>",
    "<tr> <td> Applicant Address </td> <td> {{ applicant_address|html }} </td> </tr>",
    "<tr> <td> Agent Address </td> <td> {{ agent_address|html }} </td> </tr>",
    '<a href="{{comment_url|abs }}"> comment on this </a>',
    ]


if __name__ == 'scraper':

    #scraper = PrestonScraper('Preston') # NB issue on web site = says can only view current applications and pre 2009 applications
    #scraper = EalingScraper() 
    #scraper.DEBUG = True
    ##scraper.reset()
    #scraper.run()
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
    #scraper = AllerdaleScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('2/2011/0608') # Allerdale OK
    #scraper = CoventryScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('FUL/2012/0660') # Coventry OK
    #scraper = EalingScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('P/2012/4146') # Ealing OK
    #print scraper.get_detail_from_uid ('P/2011/1170')
    #scraper = PrestonScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('06/2012/0630') # Preston OK
    #scraper = WellingboroughScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('WP/2011/0373') # Wellingborough OK
    #scraper = StHelensScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('P/2011/0664') # St Helens OK
    #scraper = NorthWarwickshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('PAP/2011/0396') # North Warwickshire OK
    #scraper = HighPeakScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('HPK/2011/0381') # High Peak OK
    #scraper = HartlepoolScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('H/2011/0408') # Hartlepool OK
    #scraper = PowysScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('P/2011/0800') # Powys OK
    #scraper = RutlandScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('APP/2011/0540') # Rutland OK
    #scraper = GuernseyScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('FULL/2011/2233') # Guernsey OK
    #scraper = HaringeyScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('HGY/2012/1554') # Haringey OK
    #scraper = EasingtonScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('PL/5/2011/0260') # Easington OK
    #scraper = CrookScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('3/2012/0259') # Crook OK

    #res = scraper.get_id_batch(util.get_dt('07/05/2013'), util.get_dt('20/05/2013'))
    #res = scraper.get_id_batch(util.get_dt('14/05/2009'), util.get_dt('27/05/2009'))
    #print res, len(res)
    #print scraper.get_id_batch(util.get_dt('23/03/2012'), util.get_dt('25/03/2012'))

    #util.list_url_prefixes(scraper.TABLE_NAME, 'url')
    #util.replace_vals(scraper.TABLE_NAME, 'url', 'http://www.nuneatonandbedworth.gov.uk/sys_upl/templates/', 'http://apps.nuneatonandbedworth.gov.uk/', 'prefix', 'yes')
    


