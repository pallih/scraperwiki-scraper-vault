# this is a base scraper for Ocella system planning applications for use by Openly Local

# there are 12 authorities using this system

# note most sites seem to have very badly formed html

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import random
import urllib
import copy
import sys

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

systems = {
    'Arun': 'ArunScraper',
    'Breckland': 'BrecklandScraper',
    'Bridgend': 'BridgendScraper', # v2
    'CastlePoint': 'CastlePointScraper',
    'Fareham': 'FarehamScraper', # v2
    'GreatYarmouth': 'GreatYarmouthScraper',  # v2
    'Havering': 'HaveringScraper', 
    'Hillingdon': 'HillingdonScraper',  # v2
    'Middlesbrough': 'MiddlesbroughScraper',
    'NorthEastLincs': 'NorthEastLincsScraper',
    'Rother': 'RotherScraper',
    #'Uttlesford': 'UttlesfordScraper', now Idox
    'Worcester': 'WorcesterScraper',
     }

class OcellaScraper(base.DateScraper):

    MAX_ID_BATCH = 300 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go
    MIN_DAYS = 20 # min number of days to get when gathering current ids
    HEADERS = {
    'Accept-Charset': 'UTF-8,*',
    'Accept': 'text/html',
    'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
    }

    date_from_field_suffix = '.DEFAULT.START_DATE.01'
    date_to_field_suffix = '.DEFAULT.END_DATE.01'
    form_object_suffix = '.DEFAULT.SUBMIT_TOP.01'
    search_fields =  {
        'p_object_name': '',
        'p_instance': '1',
        'p_event_type': 'ON_CLICK',
        'p_user_args': '',
        }
    ref_field_suffix = '.DEFAULT.REFERENCE.01'
    search_form = '0'
    next_form = '0'
    request_date_format = '%d-%m-%Y'
    form_name = ''

    scrape_ids = """
    <table summary="Printing Table Headers"> <tr />
    {* <tr>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    </tr> *}
    </table>
    """
    next_page_fields = {  '_request': 'NEXT' }
    dates_link = 'Milestone Dates'

    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = "<body> {{ block|html }} </body>"
    scrape_dates_block = "<body> {{ block|html }} </body>"
    # the minimum acceptable valid dataset on the details page
    scrape_min_data = """
    <th> Application Number </th>
    <td> {{ reference }} </td> <td> {{ date_received }} </td>
    <th> Site </th> <td> {{ address }} </td>
    <th> Proposal </th> <td> {{ description }} </td>
    """
    # other optional parameters that can appear on the details page
    scrape_optional_data = [
    "<th> Application Number </th> <td /> <td /> <td> {{ status }} </td>",
    "<th> Applicant </th> <td> {{ applicant_name }} </td> <td> {{ agent_name }} </td>",
    "<th> Applicant </th> <td /> <td /> {* <td> {{ [applicant_address] }} </td> <td /> *} <th> Officer </th>",
    "<th> Applicant </th> <td /> <td /> {* <td /> <td> {{ [agent_address] }} </td> *} <th> Officer </th>",
    "<th> Officer </th> <td> {{ case_officer }} </td> <td> {{ consultation_start_date }} </td> <td> {{ comment_date }} </td>",
    "<th> Decision </th> <td> <font> {{ decision }} </font> </td> <td> {{ decision_date }} </td>",
    "<th> Appeal Lodged </th> <td> {{ appeal_date }} </td> <td> {{ appeal_result }} </td> <td> {{ appeal_decision_date }} </td>",
    '<a href="{{ comment_url|abs }}">Comment on this application</a>' ]
    # the minimum acceptable valid dataset on the dates page
    scrape_min_dates = """
    Received <td> {{ date_received }} </td>
    Validated <td> {{ date_validated }} </td>
    """
    # other optional parameters that can appear on the dates page
    scrape_optional_dates = [
    "Decision due by <td> {{ target_decision_date }} </td>",
    "Standard Consultation Sent <td> {{ consultation_start_date }} </td>",
    "Advertised in Press Expiry <td> {{ latest_advertisement_expiry_date }} </td>",
    "Advertised Expiry <td> {{ latest_advertisement_expiry_date }} </td>",
    "Committee Meeting <td> {{ meeting_date }} </td>",
    "Appeal Lodged On <td> {{ appeal_date }} </td>",
    "Appeal Decided On <td> {{ appeal_decision_date }} </td>",
    "Permission Expires <td> {{ permission_expires_date }} </td>",
    "Date of Decision <td> {{ decision_date }} </td>",
    "Decision Issued Date <td> {{ decision_issued_date }} </td>",
    "Neighbour Consultations Sent <td> {{ neighbour_consultation_start_date }} </td>",
    "Neighbour Comments Due By <td> {{ neighbour_consultation_end_date }} </td>",
    ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)

        fields = {}
        fields.update(self.search_fields)
        fields ['p_object_name'] = self.form_name + self.form_object_suffix
        fields[self.form_name + self.date_from_field_suffix] = date_from.strftime(self.request_date_format)
        fields[self.form_name + self.date_to_field_suffix] = date_to.strftime(self.request_date_format)
        util.setup_form(self.br, self.search_form, fields)
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
                util.setup_form(self.br, self.next_form, self.next_page_fields)
                response = util.submit_form(self.br)
            except:
                response = None
        return final_result

    def get_detail_from_uid (self, uid):
        url = self.applic_url + "?p_arg_names=reference&p_arg_values=" + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

    # scrape detailed information on one record via its access URL
    def get_detail_from_url (self, url):
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
                response = self.br.follow_link(text=self.dates_link)
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

class ArunOldScraper(OcellaScraper):

    search_url = 'http://www1.arun.gov.uk/iplanning/portal/page/portal/arun/weekly'
    form_name = 'FORM_PLANNING_LIST'
    applic_url = 'http://www1.arun.gov.uk/iplanning/portal/pls/portal/ARUNWEB.RPT_APPLICATION_DETAILS.SHOW'
    scrape_ids = """
    <table summary="Printing Table Headers"> <tr />
    {* <tr>
    <td> {{ [records].ward_name }} </td>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    </tr> *}
    </table>
    """
    
class BrecklandScraper(OcellaScraper):

    search_url = 'http://planning.breckland.gov.uk/portal/page/portal/breckland/weekly'
    TABLE_NAME = 'Breckland'
    form_name = 'FORM_PLANNING_LIST'
    applic_url = 'http://planning.breckland.gov.uk/portal/pls/portal/breckWEB.RPT_APPLICATION_DETAILS.show'
    scrape_ids = """
    <table summary="Printing Table Headers"> <tr />
    {* <tr>
    <td> {{ [records].parish }} </td>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    </tr> *}
    </table>
    """

class BridgendOldScraper(OcellaScraper): # no longer working

    search_url = 'http://eplan.bridgend.gov.uk/portal/page/portal/bridgend/search'
    form_name = 'FORM_SEARCH'
    applic_url = 'http://eplan.bridgend.gov.uk/portal/pls/portal/BRIDGEW.RPT_APPLICATION_DETAILS.SHOW'

    scrape_min_data = """
    Reference No <td> {{ reference }} </td>
    <tr> <td> Received </td> <td> {{ date_received }} </td> </tr>
    <tr> <td> Location </td> <td> {{ address }} </td> </tr>
    <tr> <td> Proposal </td> <td> {{ description }} </td> </tr>
    """
    scrape_optional_data = [ 
    "Reference No <tr> <td> Status </td> <td> {{ status }} </td> </tr>",
    "Reference No <tr> <td> Applicant </td> <td> {{ applicant_name }} </td> </tr>",
    "Reference No <tr> <td> Agent </td> <td> {{ agent_name }} </td> </tr>",
    "Reference No <tr> <td> Advertised in Press </td> <td> {{ consultation_start_date }} </td> </tr>",
    "Reference No <tr> <td> Comments due by </td> <td> {{ comment_date }} </td> </tr>",
    "Reference No <tr> <td> Comments due by </td> <td> {{ consultation_end_date }} </td> </tr>",
    "Reference No <tr> <td> Officer </td> <td> {{ case_officer }} </td> </tr>",
    "Reference No <tr> <td> Recommendation Level </td> <td> {{ decided_by }} </td> </tr>",
    """Reference No <tr> <td> Decision </td> <td> <font> {{ decision }} </font> </td> </tr> 
    <tr> <td> Decision Date </td> <td> {{ decision_date }} </td> </tr> <tr> Appeal Decision </tr>""",
    "Reference No <tr> <td> Appeal Decision </td> <td> {{ appeal_result }} </td> <td> Appeal Decision Date </td> <td> {{ appeal_decision_date }} </td> </tr>",
    "Reference No <tr> <td> Appeal Reference </td> <td> {{ associated_application_uid }} </td> </tr>",
    '<a href="{{ comment_url|abs }}">Comment on this application</a>' ]

class CastlePointScraper(OcellaScraper):

    search_url = 'http://planning.castlepoint.gov.uk/portal/page/portal/CASTLEPOINT/weekly'
    TABLE_NAME = 'CastlePoint'
    form_name = 'FORM_WEEKLY_LIST'
    applic_url = 'http://planning.castlepoint.gov.uk/portal/pls/portal/CASTLEWEB.RPT_APPLICATION_DETAILS.SHOW'
    scrape_ids = """
    <table summary="Printing Table Headers"> <tr />
    {* <tr>
    <td> {{ [records].ward_name }} </td>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    </tr> *}
    </table>
    """

class Ocella2Scraper(base.DateScraper): # alternative form - inherits directly from DateScraper 

    MAX_ID_BATCH = 300 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go
    MIN_DAYS = 20 # min number of days to get when gathering current ids
    date_from_field = 'receivedFrom'
    date_to_field = 'receivedTo'
    search_fields = { 'showall': 'showall' }
    search_form = 'OcellaPlanningSearch'
    request_date_format = '%d-%m-%y'
    scrape_ids = """
    <table /> <table> <tr />
    {* <tr>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    <td /> <td /> <td /> <td> {{ [records].application_type }} </td>
    </tr> *}
    </table>
    """
    scrape_data_block = '<body> {{ block|html }} </body>'
    scrape_min_data = """
    <td> Reference </td> <td> {{ reference }} </td>
    <td> Proposal </td> <td> {{ description }} </td>
    <td> Location </td> <td> {{ address }} </td>
    <td> Received </td> <td> {{ date_received }} </td>
    """
    scrape_optional_data = [
    "<td> Status </td> <td> {{ status }} </td>",
    "<td> Ward </td> <td> {{ ward_name }} </td>",
    "<td> Parish </td> <td> {{ parish }} </td>",
    "<td> Applicant </td> <td> {{ applicant_address }} </td>",
    "<td> Agent </td> <td> {{ agent_address }} </td>",
    "<td> Officer </td> <td> {{ case_officer }} </td>",
    "<td> Decided </td> <td> {{ decision_date }} </td>",
    "<td> Validated </td> <td> {{ date_validated }} </td>",
    '<form name="comment" action="{{ comment_url|abs }}" />',
    ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)
        fields = {}
        fields.update(self.search_fields)
        fields[self.date_from_field] = date_from.strftime(self.request_date_format)
        fields[self.date_to_field] = date_to.strftime(self.request_date_format)
        util.setup_form(self.br, self.search_form, fields)
        response = util.submit_form(self.br)
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

    def get_detail_from_uid (self, uid):
        url = self.applic_url + "?from=planningSearch&reference=" + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

class ArunScraper(Ocella2Scraper): # changed - now inherits from Ocella2Scraper

    TABLE_NAME = 'Arun'
    MIN_DAYS = 10 # note does not want to return more than 200 records so reduce min number of days to get when gathering current ids 
    search_url = 'http://www1.arun.gov.uk/aplanning/OcellaWeb/planningSearch'
    applic_url = 'http://www1.arun.gov.uk/aplanning/OcellaWeb/planningDetails'
    scrape_ids = """
    <table /> <table> <tr> Reference </tr>
    {* <tr>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    </tr> *}
    </table>
    """
    
class BridgendScraper(Ocella2Scraper): # changed - now inherits from Ocella2Scraper

    TABLE_NAME = 'Bridgend'
    search_url = 'http://planpor.bridgend.gov.uk/OcellaWeb/planningSearch'
    applic_url = 'http://planpor.bridgend.gov.uk/OcellaWeb/planningDetails'
    scrape_ids = """
    <table /> <table> <tr />
    {* <tr>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    <td /> <td /> <td> {{ [records].application_type }} </td>
    </tr> *}
    </table>
    """

class FarehamScraper(Ocella2Scraper): # changed - now inherits from Ocella2Scraper

    TABLE_NAME = 'Fareham'
    search_url = 'http://eoc.fareham.gov.uk/OcellaWeb/planningSearch'
    applic_url = 'http://eoc.fareham.gov.uk/OcellaWeb/planningDetails'
    scrape_data_block = '<div id="pnlPageContent"> {{ block|html }} </div>'

class GreatYarmouthScraper(Ocella2Scraper): # changed - now inherits from Ocella2Scraper

    TABLE_NAME = 'GreatYarmouth'
    search_url = 'http://planning.great-yarmouth.gov.uk/OcellaWeb/planningSearch'
    applic_url = 'http://planning.great-yarmouth.gov.uk/OcellaWeb/planningDetails'
    scrape_data_block = '<div id="planningSearch"> {{ block|html }} </div>'

class HillingdonScraper(Ocella2Scraper): # changed - now inherits from Ocella2Scraper

    TABLE_NAME = 'Hillingdon'
    BATCH_DAYS = 10
    search_url = 'http://planning.hillingdon.gov.uk/OcellaWeb/planningSearch'
    #'http://www.hillingdon.gov.uk/planningsearch'
    scrape_ids = """
    <table /> <table> <tr />
    {* <tr>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    </tr> *}
    </table>
    """
    ref_field = 'reference'

    def get_detail_from_uid (self, uid):
        response = self.br.open(self.search_url)
        fields = {}
        fields.update(self.search_fields)
        fields[self.ref_field] = uid
        util.setup_form(self.br, self.search_form, fields)
        response = util.submit_form(self.br)

        try:
            html = response.read()
            if self.DEBUG: html
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            self.clean_ids(result['records'])
            url = result['records'][0]['url']
        except:
            return None

        return self.get_detail_from_url(url)

class GreatYarmouthOldScraper(OcellaScraper): # no longer working

    search_url = 'http://planning.great-yarmouth.gov.uk/OcellaWeb/planningSearch'
    form_name = 'FORM_PLANNING_LIST'
    applic_url = 'http://planning.great-yarmouth.gov.uk/OcellaWeb/planningDetails?from=planningSearch&reference='
    scrape_ids = """
    <table summary="Printing Table Headers"> <tr />
    {* <tr>
    <td> {{ [records].ward_name }} </td>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    </tr> *}
    </table>
    """

class HaveringScraper(OcellaScraper):

    TABLE_NAME = 'Havering'
    search_url = 'http://planning.havering.gov.uk/portal/page?_pageid=33,1026&_dad=portal&_schema=PORTAL'
    form_name = 'FORM_APP_SEARCH'
    search_form = '1'
    next_form = '1'
    applic_url = 'http://planning.havering.gov.uk/pls/portal/HAVERWEB.RPT_APPLICATION_DETAILS.SHOW'
    dates_link = 'Key Application Dates'
    scrape_ids = """
    <table summary="Printing Table Headers"> <tr />
    {* <tr>
    <td> {{ [records].ward_name }} </td>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    <td> {{ [records].application_type }} </td>
    </tr> *}
    </table>
    """
    
    scrape_min_data = """
    <th> Application Number </th>
    <td> {{ reference }} </td> <td> {{ date_received }} </td>
    <th> Location </th> <td> {{ address }} </td>
    <th> Proposal </th> <td> {{ description }} </td>
    """
    scrape_optional_data = [
    "<th> Application Number </th> <td /> <td /> <td> {{ status }} </td>",
    """<th> Applicant </th> <td> {{ applicant_name }} <br/> {{ applicant_address|html }} </td>
    <td> {{ agent_name }} <br/> {{ agent_address|html }} </td>""",
    "<th> Officer </th> <td> {{ case_officer }} </td> <td> {{ consultation_start_date }} </td> <td> {{ comment_date }} </td>",
    "<th> Decision </th> <td> {{ decision }} <br /> </td> <td> {{ decision_date }} </td>",
    "<th> Appeal Lodged </th> <td> {{ appeal_date }} </td> <td> {{ appeal_result }} </td> <td> {{ appeal_decision_date }} </td>",
    '<a href="{{ comment_url|abs }}">Comment on this application</a>' ]

class HillingdonOldScraper(OcellaScraper): # no longer working

    search_url = 'http://w09.hillingdon.gov.uk/pls/portal/url/page/hillingdon/APPLICATION_SEARCH'
    form_name = 'FORM_APP_SEARCH'
    applic_url = 'http://w09.hillingdon.gov.uk/pls/portal/HILLWEB.RPT_APPLICATION_DETAILS.SHOW'

    scrape_min_data = """
    <th> Application Number </th>
    <td> {{ reference }} </td> <td> {{ date_received }} </td>
    <th> Location </th> <td> {{ address }} </td>
    <th> Proposal </th> <td> {{ description }} </td>
    """
    scrape_optional_data = [
    "<th> Application Number </th> <td /> <td /> <td> {{ status }} </td>",
    "<th> Agent </th> <td> {{ agent_name }}",
    "<th> Agent </th> <td /> {* <td> {{ [agent_address] }} </td> *} <th> Officer </th>",
    "<th> Officer </th> <td> {{ case_officer }} </td>",
    "<th> Ward </th> <td> {{ ward_name }} </td>",
    "<th> Decision </th> <td> {{ decision }} <br /> </td> <td> {{ decision_date }} </td>",
    "<th> Date Appeal Received </th> <td> {{ appeal_date }} </td> <td> {{ appeal_result }} </td> <td> {{ appeal_decision_date }} </td>",
    '<a href="{{ comment_url|abs }}">Comment on this application</a>' ]

class MiddlesbroughScraper(OcellaScraper):

    TABLE_NAME = 'Middlesbrough'
    search_url = 'http://planserv.middlesbrough.gov.uk/portal/page/portal/MIDDLESBROUGH/WEEKLY'
    form_name = 'FORM_PLANNING_LIST'
    applic_url = 'http://planserv.middlesbrough.gov.uk/portal/pls/portal/MIDWEB.RPT_APPLICATION_DETAILS.SHOW'
    scrape_ids = """
    <table summary="Printing Table Headers"> <tr />
    {* <tr>
    <td> {{ [records].ward_name }} </td>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    </tr> *}
    </table>
    """

class NorthEastLincsScraper(OcellaScraper):

    TABLE_NAME = 'NorthEastLincs'
    search_url = 'http://planning.nelincs.gov.uk/portal/page/portal/NELINCS/planning'
    form_name = 'FORM_PLANNING_LIST'
    search_form = '2'
    next_form = '0'
    applic_url = 'http://planning.nelincs.gov.uk/portal/pls/portal/NLWEB.RPT_APPLICATION_DETAILS.SHOW'

class RotherScraper(OcellaScraper):

    TABLE_NAME = 'Rother'
    search_url = 'http://ocellaweb.rother.gov.uk/portal/page/portal/rother/search'
    form_name = 'FORM_SEARCH3'
    search_form = '1'
    next_form = '1'
    applic_url = 'http://ocellaweb.rother.gov.uk/portal/pls/portal/ROTHERWEB.RPT_DETAILS.show'

    scrape_optional_data = [
    "<th> Application Number </th> <td /> <td /> <td> {{ status }} </td>",
    "<th> Applicant </th> <td> {{ applicant_name }} </td> <td> {{ agent_name }} </td>",
    "<th> Applicant </th> <td /> <td /> {* <td> {{ [applicant_address] }} </td> <td /> *} <th> Advertised </th>",
    "<th> Applicant </th> <td /> <td /> {* <td /> <td> {{ [agent_address] }} </td> *} <th> Advertised </th>",
    "<th> Advertised </th> <td> {{ consultation_start_date }} </td> <td> {{ comment_date }} </td>",
    "<th> Decision </th> <td> <font> {{ decision }} </font> </td> <td> {{ decision_date }} </td>",
    "<th> Appeal Lodged </th> <td> {{ appeal_date }} </td> <td> {{ appeal_result }} </td> <td> {{ appeal_decision_date }} </td>",
    '<a href="{{ comment_url|abs }}">Comment on this application</a>' ]
    scrape_min_dates = """
    Validated <td> {{ date_validated }} </td>
    """

class UttlesfordScraper(OcellaScraper):

    TABLE_NAME = 'Uttlesford'
    search_url = 'http://planning.uttlesford.gov.uk/portal/page/portal/plan/weekly'
    form_name = 'PLANNING_LIST'
    applic_url = 'http://planning.uttlesford.gov.uk/portal/pls/portal/UTTWEB.RPT_APPLICATION_DETAILS.show'
    scrape_ids = """
    <table summary="Printing Table Headers"> <tr />
    {* <tr>
    <td> {{ [records].parish }} </td>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    </tr> *}
    </table>
    """

class WorcesterScraper(OcellaScraper):

    TABLE_NAME = 'Worcester'
    BATCH_DAYS = 21 # batch size for each scrape - number of days to gather to produce at least one result each time
    MIN_DAYS = 28 # min number of days to get when gathering current ids
    search_url = 'http://planningapps.worcester.gov.uk/portal/page/portal/worcester/search'
    form_name = 'FORM_SEARCH'
    search_form = '2'
    next_form = '2'
    applic_url = 'http://planningapps.worcester.gov.uk/portal/pls/portal/WWEB.RPT_DETAILS2.show'

    scrape_min_data = """
    <font> Application Reference </font> <font> {{ reference }} </font>
    <font> Description </font> <font> {{ address }} </font>
    <font> {{ description }} </font>
    <font> Date Started </font> <font> {{ date_received }} </font>
    """
    scrape_optional_data = [
    "<font> Current Status </font> <font> {{ status }} </font>",
    "<font> Ward </font> <font> {{ ward_name }} </font>",
    "<font> Agent Details </font> <font> {{ applicant_name }} </font> <font> {{ agent_name }} </font>",
    "<font> Agent Details </font> <font /> <font /> {* <font> {{ [applicant_address] }} </font> <font /> *} <font> Administration Details </font>",
    "<font> Agent Details </font> <font /> <font /> {* <font /> <font> {{ [agent_address] }} </font> *} <font> Administration Details </font>",
    "<font> Officer </font> <font> {{ case_officer }} </font>",
    "<font> Decision Due By </font> <font> {{ target_decision_date }} </font>",
    "<font> End of Consultation </font> <font> {{ consultation_end_date }} </font>",
    """<font> Committee Date </font> <font> {{ meeting_date }} </font>
    <font> Decision </font> <font> {{ decision }} </font> <font> Decision Date </font> <font> {{ decision_date }} </font>""",
    "<font> Appeal Started </font> <font> {{ appeal_date }} </font>",
    "<font> Appeal Decision Date </font> <font> {{ appeal_decision_date }} </font> <font /> <font> {{ appeal_result }} </font>",
    '<a href="{{ comment_url|abs }}">Comment on this application</a>' ]

if __name__ == 'scraper':

    #scraper = ArunScraper()
    #scraper.run()
    #util.rename_column('Rother', 'appeal_decided_date', 'appeal_decision_date')
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

    # misc test calls
    #scraper = ArunScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('BR/202/12/') # Arun OK
    #scraper = BrecklandScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('3PL/2011/0917/F') # Breckland OK
    #scraper = BridgendScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('P/11/629/FUL') # Bridgend OK
    #scraper = CastlePointScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('CPT/659/12/FUL') # Castle Point OK
    #scraper = FarehamScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('P/11/0703/FP') # Fareham OK
    #scraper = GreatYarmouthScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('06/11/0529/F') # Great Yarmouth OK
    #print scraper.get_detail_from_uid ('06/03/0054/F')
    #scraper = HaveringScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('C0005.12') # Havering OK
    #scraper = HillingdonScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('64345/APP/2011/1945') # Hillingdon OK
    #print scraper.get_detail_from_url ('http://www.hillingdon.gov.uk/planningsearch?lnk=189') # should return None = OK
    #scraper = MiddlesbroughScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('M/FP/0865/11/P') # Middlesbrough OK
    #scraper = NorthEastLincsScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('DC/695/11/WOL') # North East Lincs OK
    #scraper = RotherScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('RR/2011/1789/P') # Rother OK
    #scraper = UttlesfordScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('UTT/1343/11/LB') # Uttlesford Ok
    #scraper = WorcesterScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('P11A0394') # Worcester OK

    #scraper = WorcesterScraper()
    #print scraper.scrape_optional_data
    #scraper = BrecklandScraper()
    #print scraper.scrape_optional_data

    #scraper = BrecklandScraper()
    #res = scraper.get_id_batch(util.get_dt('15/11/2012'), util.get_dt('06/02/2013'))
    #print res, len(res)
    #scraper = MiddlesbroughScraper()
    #res = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('28/08/2011'))
    #res = scraper.get_id_batch(util.get_dt('16/03/2012'), util.get_dt('30/03/2012'))
    #print res, len(res)
    

    



    

    
# this is a base scraper for Ocella system planning applications for use by Openly Local

# there are 12 authorities using this system

# note most sites seem to have very badly formed html

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import random
import urllib
import copy
import sys

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

systems = {
    'Arun': 'ArunScraper',
    'Breckland': 'BrecklandScraper',
    'Bridgend': 'BridgendScraper', # v2
    'CastlePoint': 'CastlePointScraper',
    'Fareham': 'FarehamScraper', # v2
    'GreatYarmouth': 'GreatYarmouthScraper',  # v2
    'Havering': 'HaveringScraper', 
    'Hillingdon': 'HillingdonScraper',  # v2
    'Middlesbrough': 'MiddlesbroughScraper',
    'NorthEastLincs': 'NorthEastLincsScraper',
    'Rother': 'RotherScraper',
    #'Uttlesford': 'UttlesfordScraper', now Idox
    'Worcester': 'WorcesterScraper',
     }

class OcellaScraper(base.DateScraper):

    MAX_ID_BATCH = 300 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go
    MIN_DAYS = 20 # min number of days to get when gathering current ids
    HEADERS = {
    'Accept-Charset': 'UTF-8,*',
    'Accept': 'text/html',
    'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
    }

    date_from_field_suffix = '.DEFAULT.START_DATE.01'
    date_to_field_suffix = '.DEFAULT.END_DATE.01'
    form_object_suffix = '.DEFAULT.SUBMIT_TOP.01'
    search_fields =  {
        'p_object_name': '',
        'p_instance': '1',
        'p_event_type': 'ON_CLICK',
        'p_user_args': '',
        }
    ref_field_suffix = '.DEFAULT.REFERENCE.01'
    search_form = '0'
    next_form = '0'
    request_date_format = '%d-%m-%Y'
    form_name = ''

    scrape_ids = """
    <table summary="Printing Table Headers"> <tr />
    {* <tr>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    </tr> *}
    </table>
    """
    next_page_fields = {  '_request': 'NEXT' }
    dates_link = 'Milestone Dates'

    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = "<body> {{ block|html }} </body>"
    scrape_dates_block = "<body> {{ block|html }} </body>"
    # the minimum acceptable valid dataset on the details page
    scrape_min_data = """
    <th> Application Number </th>
    <td> {{ reference }} </td> <td> {{ date_received }} </td>
    <th> Site </th> <td> {{ address }} </td>
    <th> Proposal </th> <td> {{ description }} </td>
    """
    # other optional parameters that can appear on the details page
    scrape_optional_data = [
    "<th> Application Number </th> <td /> <td /> <td> {{ status }} </td>",
    "<th> Applicant </th> <td> {{ applicant_name }} </td> <td> {{ agent_name }} </td>",
    "<th> Applicant </th> <td /> <td /> {* <td> {{ [applicant_address] }} </td> <td /> *} <th> Officer </th>",
    "<th> Applicant </th> <td /> <td /> {* <td /> <td> {{ [agent_address] }} </td> *} <th> Officer </th>",
    "<th> Officer </th> <td> {{ case_officer }} </td> <td> {{ consultation_start_date }} </td> <td> {{ comment_date }} </td>",
    "<th> Decision </th> <td> <font> {{ decision }} </font> </td> <td> {{ decision_date }} </td>",
    "<th> Appeal Lodged </th> <td> {{ appeal_date }} </td> <td> {{ appeal_result }} </td> <td> {{ appeal_decision_date }} </td>",
    '<a href="{{ comment_url|abs }}">Comment on this application</a>' ]
    # the minimum acceptable valid dataset on the dates page
    scrape_min_dates = """
    Received <td> {{ date_received }} </td>
    Validated <td> {{ date_validated }} </td>
    """
    # other optional parameters that can appear on the dates page
    scrape_optional_dates = [
    "Decision due by <td> {{ target_decision_date }} </td>",
    "Standard Consultation Sent <td> {{ consultation_start_date }} </td>",
    "Advertised in Press Expiry <td> {{ latest_advertisement_expiry_date }} </td>",
    "Advertised Expiry <td> {{ latest_advertisement_expiry_date }} </td>",
    "Committee Meeting <td> {{ meeting_date }} </td>",
    "Appeal Lodged On <td> {{ appeal_date }} </td>",
    "Appeal Decided On <td> {{ appeal_decision_date }} </td>",
    "Permission Expires <td> {{ permission_expires_date }} </td>",
    "Date of Decision <td> {{ decision_date }} </td>",
    "Decision Issued Date <td> {{ decision_issued_date }} </td>",
    "Neighbour Consultations Sent <td> {{ neighbour_consultation_start_date }} </td>",
    "Neighbour Comments Due By <td> {{ neighbour_consultation_end_date }} </td>",
    ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)

        fields = {}
        fields.update(self.search_fields)
        fields ['p_object_name'] = self.form_name + self.form_object_suffix
        fields[self.form_name + self.date_from_field_suffix] = date_from.strftime(self.request_date_format)
        fields[self.form_name + self.date_to_field_suffix] = date_to.strftime(self.request_date_format)
        util.setup_form(self.br, self.search_form, fields)
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
                util.setup_form(self.br, self.next_form, self.next_page_fields)
                response = util.submit_form(self.br)
            except:
                response = None
        return final_result

    def get_detail_from_uid (self, uid):
        url = self.applic_url + "?p_arg_names=reference&p_arg_values=" + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

    # scrape detailed information on one record via its access URL
    def get_detail_from_url (self, url):
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
                response = self.br.follow_link(text=self.dates_link)
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

class ArunOldScraper(OcellaScraper):

    search_url = 'http://www1.arun.gov.uk/iplanning/portal/page/portal/arun/weekly'
    form_name = 'FORM_PLANNING_LIST'
    applic_url = 'http://www1.arun.gov.uk/iplanning/portal/pls/portal/ARUNWEB.RPT_APPLICATION_DETAILS.SHOW'
    scrape_ids = """
    <table summary="Printing Table Headers"> <tr />
    {* <tr>
    <td> {{ [records].ward_name }} </td>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    </tr> *}
    </table>
    """
    
class BrecklandScraper(OcellaScraper):

    search_url = 'http://planning.breckland.gov.uk/portal/page/portal/breckland/weekly'
    TABLE_NAME = 'Breckland'
    form_name = 'FORM_PLANNING_LIST'
    applic_url = 'http://planning.breckland.gov.uk/portal/pls/portal/breckWEB.RPT_APPLICATION_DETAILS.show'
    scrape_ids = """
    <table summary="Printing Table Headers"> <tr />
    {* <tr>
    <td> {{ [records].parish }} </td>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    </tr> *}
    </table>
    """

class BridgendOldScraper(OcellaScraper): # no longer working

    search_url = 'http://eplan.bridgend.gov.uk/portal/page/portal/bridgend/search'
    form_name = 'FORM_SEARCH'
    applic_url = 'http://eplan.bridgend.gov.uk/portal/pls/portal/BRIDGEW.RPT_APPLICATION_DETAILS.SHOW'

    scrape_min_data = """
    Reference No <td> {{ reference }} </td>
    <tr> <td> Received </td> <td> {{ date_received }} </td> </tr>
    <tr> <td> Location </td> <td> {{ address }} </td> </tr>
    <tr> <td> Proposal </td> <td> {{ description }} </td> </tr>
    """
    scrape_optional_data = [ 
    "Reference No <tr> <td> Status </td> <td> {{ status }} </td> </tr>",
    "Reference No <tr> <td> Applicant </td> <td> {{ applicant_name }} </td> </tr>",
    "Reference No <tr> <td> Agent </td> <td> {{ agent_name }} </td> </tr>",
    "Reference No <tr> <td> Advertised in Press </td> <td> {{ consultation_start_date }} </td> </tr>",
    "Reference No <tr> <td> Comments due by </td> <td> {{ comment_date }} </td> </tr>",
    "Reference No <tr> <td> Comments due by </td> <td> {{ consultation_end_date }} </td> </tr>",
    "Reference No <tr> <td> Officer </td> <td> {{ case_officer }} </td> </tr>",
    "Reference No <tr> <td> Recommendation Level </td> <td> {{ decided_by }} </td> </tr>",
    """Reference No <tr> <td> Decision </td> <td> <font> {{ decision }} </font> </td> </tr> 
    <tr> <td> Decision Date </td> <td> {{ decision_date }} </td> </tr> <tr> Appeal Decision </tr>""",
    "Reference No <tr> <td> Appeal Decision </td> <td> {{ appeal_result }} </td> <td> Appeal Decision Date </td> <td> {{ appeal_decision_date }} </td> </tr>",
    "Reference No <tr> <td> Appeal Reference </td> <td> {{ associated_application_uid }} </td> </tr>",
    '<a href="{{ comment_url|abs }}">Comment on this application</a>' ]

class CastlePointScraper(OcellaScraper):

    search_url = 'http://planning.castlepoint.gov.uk/portal/page/portal/CASTLEPOINT/weekly'
    TABLE_NAME = 'CastlePoint'
    form_name = 'FORM_WEEKLY_LIST'
    applic_url = 'http://planning.castlepoint.gov.uk/portal/pls/portal/CASTLEWEB.RPT_APPLICATION_DETAILS.SHOW'
    scrape_ids = """
    <table summary="Printing Table Headers"> <tr />
    {* <tr>
    <td> {{ [records].ward_name }} </td>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    </tr> *}
    </table>
    """

class Ocella2Scraper(base.DateScraper): # alternative form - inherits directly from DateScraper 

    MAX_ID_BATCH = 300 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go
    MIN_DAYS = 20 # min number of days to get when gathering current ids
    date_from_field = 'receivedFrom'
    date_to_field = 'receivedTo'
    search_fields = { 'showall': 'showall' }
    search_form = 'OcellaPlanningSearch'
    request_date_format = '%d-%m-%y'
    scrape_ids = """
    <table /> <table> <tr />
    {* <tr>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    <td /> <td /> <td /> <td> {{ [records].application_type }} </td>
    </tr> *}
    </table>
    """
    scrape_data_block = '<body> {{ block|html }} </body>'
    scrape_min_data = """
    <td> Reference </td> <td> {{ reference }} </td>
    <td> Proposal </td> <td> {{ description }} </td>
    <td> Location </td> <td> {{ address }} </td>
    <td> Received </td> <td> {{ date_received }} </td>
    """
    scrape_optional_data = [
    "<td> Status </td> <td> {{ status }} </td>",
    "<td> Ward </td> <td> {{ ward_name }} </td>",
    "<td> Parish </td> <td> {{ parish }} </td>",
    "<td> Applicant </td> <td> {{ applicant_address }} </td>",
    "<td> Agent </td> <td> {{ agent_address }} </td>",
    "<td> Officer </td> <td> {{ case_officer }} </td>",
    "<td> Decided </td> <td> {{ decision_date }} </td>",
    "<td> Validated </td> <td> {{ date_validated }} </td>",
    '<form name="comment" action="{{ comment_url|abs }}" />',
    ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)
        fields = {}
        fields.update(self.search_fields)
        fields[self.date_from_field] = date_from.strftime(self.request_date_format)
        fields[self.date_to_field] = date_to.strftime(self.request_date_format)
        util.setup_form(self.br, self.search_form, fields)
        response = util.submit_form(self.br)
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

    def get_detail_from_uid (self, uid):
        url = self.applic_url + "?from=planningSearch&reference=" + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

class ArunScraper(Ocella2Scraper): # changed - now inherits from Ocella2Scraper

    TABLE_NAME = 'Arun'
    MIN_DAYS = 10 # note does not want to return more than 200 records so reduce min number of days to get when gathering current ids 
    search_url = 'http://www1.arun.gov.uk/aplanning/OcellaWeb/planningSearch'
    applic_url = 'http://www1.arun.gov.uk/aplanning/OcellaWeb/planningDetails'
    scrape_ids = """
    <table /> <table> <tr> Reference </tr>
    {* <tr>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    </tr> *}
    </table>
    """
    
class BridgendScraper(Ocella2Scraper): # changed - now inherits from Ocella2Scraper

    TABLE_NAME = 'Bridgend'
    search_url = 'http://planpor.bridgend.gov.uk/OcellaWeb/planningSearch'
    applic_url = 'http://planpor.bridgend.gov.uk/OcellaWeb/planningDetails'
    scrape_ids = """
    <table /> <table> <tr />
    {* <tr>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    <td /> <td /> <td> {{ [records].application_type }} </td>
    </tr> *}
    </table>
    """

class FarehamScraper(Ocella2Scraper): # changed - now inherits from Ocella2Scraper

    TABLE_NAME = 'Fareham'
    search_url = 'http://eoc.fareham.gov.uk/OcellaWeb/planningSearch'
    applic_url = 'http://eoc.fareham.gov.uk/OcellaWeb/planningDetails'
    scrape_data_block = '<div id="pnlPageContent"> {{ block|html }} </div>'

class GreatYarmouthScraper(Ocella2Scraper): # changed - now inherits from Ocella2Scraper

    TABLE_NAME = 'GreatYarmouth'
    search_url = 'http://planning.great-yarmouth.gov.uk/OcellaWeb/planningSearch'
    applic_url = 'http://planning.great-yarmouth.gov.uk/OcellaWeb/planningDetails'
    scrape_data_block = '<div id="planningSearch"> {{ block|html }} </div>'

class HillingdonScraper(Ocella2Scraper): # changed - now inherits from Ocella2Scraper

    TABLE_NAME = 'Hillingdon'
    BATCH_DAYS = 10
    search_url = 'http://planning.hillingdon.gov.uk/OcellaWeb/planningSearch'
    #'http://www.hillingdon.gov.uk/planningsearch'
    scrape_ids = """
    <table /> <table> <tr />
    {* <tr>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    </tr> *}
    </table>
    """
    ref_field = 'reference'

    def get_detail_from_uid (self, uid):
        response = self.br.open(self.search_url)
        fields = {}
        fields.update(self.search_fields)
        fields[self.ref_field] = uid
        util.setup_form(self.br, self.search_form, fields)
        response = util.submit_form(self.br)

        try:
            html = response.read()
            if self.DEBUG: html
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            self.clean_ids(result['records'])
            url = result['records'][0]['url']
        except:
            return None

        return self.get_detail_from_url(url)

class GreatYarmouthOldScraper(OcellaScraper): # no longer working

    search_url = 'http://planning.great-yarmouth.gov.uk/OcellaWeb/planningSearch'
    form_name = 'FORM_PLANNING_LIST'
    applic_url = 'http://planning.great-yarmouth.gov.uk/OcellaWeb/planningDetails?from=planningSearch&reference='
    scrape_ids = """
    <table summary="Printing Table Headers"> <tr />
    {* <tr>
    <td> {{ [records].ward_name }} </td>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    </tr> *}
    </table>
    """

class HaveringScraper(OcellaScraper):

    TABLE_NAME = 'Havering'
    search_url = 'http://planning.havering.gov.uk/portal/page?_pageid=33,1026&_dad=portal&_schema=PORTAL'
    form_name = 'FORM_APP_SEARCH'
    search_form = '1'
    next_form = '1'
    applic_url = 'http://planning.havering.gov.uk/pls/portal/HAVERWEB.RPT_APPLICATION_DETAILS.SHOW'
    dates_link = 'Key Application Dates'
    scrape_ids = """
    <table summary="Printing Table Headers"> <tr />
    {* <tr>
    <td> {{ [records].ward_name }} </td>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    <td> {{ [records].application_type }} </td>
    </tr> *}
    </table>
    """
    
    scrape_min_data = """
    <th> Application Number </th>
    <td> {{ reference }} </td> <td> {{ date_received }} </td>
    <th> Location </th> <td> {{ address }} </td>
    <th> Proposal </th> <td> {{ description }} </td>
    """
    scrape_optional_data = [
    "<th> Application Number </th> <td /> <td /> <td> {{ status }} </td>",
    """<th> Applicant </th> <td> {{ applicant_name }} <br/> {{ applicant_address|html }} </td>
    <td> {{ agent_name }} <br/> {{ agent_address|html }} </td>""",
    "<th> Officer </th> <td> {{ case_officer }} </td> <td> {{ consultation_start_date }} </td> <td> {{ comment_date }} </td>",
    "<th> Decision </th> <td> {{ decision }} <br /> </td> <td> {{ decision_date }} </td>",
    "<th> Appeal Lodged </th> <td> {{ appeal_date }} </td> <td> {{ appeal_result }} </td> <td> {{ appeal_decision_date }} </td>",
    '<a href="{{ comment_url|abs }}">Comment on this application</a>' ]

class HillingdonOldScraper(OcellaScraper): # no longer working

    search_url = 'http://w09.hillingdon.gov.uk/pls/portal/url/page/hillingdon/APPLICATION_SEARCH'
    form_name = 'FORM_APP_SEARCH'
    applic_url = 'http://w09.hillingdon.gov.uk/pls/portal/HILLWEB.RPT_APPLICATION_DETAILS.SHOW'

    scrape_min_data = """
    <th> Application Number </th>
    <td> {{ reference }} </td> <td> {{ date_received }} </td>
    <th> Location </th> <td> {{ address }} </td>
    <th> Proposal </th> <td> {{ description }} </td>
    """
    scrape_optional_data = [
    "<th> Application Number </th> <td /> <td /> <td> {{ status }} </td>",
    "<th> Agent </th> <td> {{ agent_name }}",
    "<th> Agent </th> <td /> {* <td> {{ [agent_address] }} </td> *} <th> Officer </th>",
    "<th> Officer </th> <td> {{ case_officer }} </td>",
    "<th> Ward </th> <td> {{ ward_name }} </td>",
    "<th> Decision </th> <td> {{ decision }} <br /> </td> <td> {{ decision_date }} </td>",
    "<th> Date Appeal Received </th> <td> {{ appeal_date }} </td> <td> {{ appeal_result }} </td> <td> {{ appeal_decision_date }} </td>",
    '<a href="{{ comment_url|abs }}">Comment on this application</a>' ]

class MiddlesbroughScraper(OcellaScraper):

    TABLE_NAME = 'Middlesbrough'
    search_url = 'http://planserv.middlesbrough.gov.uk/portal/page/portal/MIDDLESBROUGH/WEEKLY'
    form_name = 'FORM_PLANNING_LIST'
    applic_url = 'http://planserv.middlesbrough.gov.uk/portal/pls/portal/MIDWEB.RPT_APPLICATION_DETAILS.SHOW'
    scrape_ids = """
    <table summary="Printing Table Headers"> <tr />
    {* <tr>
    <td> {{ [records].ward_name }} </td>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    </tr> *}
    </table>
    """

class NorthEastLincsScraper(OcellaScraper):

    TABLE_NAME = 'NorthEastLincs'
    search_url = 'http://planning.nelincs.gov.uk/portal/page/portal/NELINCS/planning'
    form_name = 'FORM_PLANNING_LIST'
    search_form = '2'
    next_form = '0'
    applic_url = 'http://planning.nelincs.gov.uk/portal/pls/portal/NLWEB.RPT_APPLICATION_DETAILS.SHOW'

class RotherScraper(OcellaScraper):

    TABLE_NAME = 'Rother'
    search_url = 'http://ocellaweb.rother.gov.uk/portal/page/portal/rother/search'
    form_name = 'FORM_SEARCH3'
    search_form = '1'
    next_form = '1'
    applic_url = 'http://ocellaweb.rother.gov.uk/portal/pls/portal/ROTHERWEB.RPT_DETAILS.show'

    scrape_optional_data = [
    "<th> Application Number </th> <td /> <td /> <td> {{ status }} </td>",
    "<th> Applicant </th> <td> {{ applicant_name }} </td> <td> {{ agent_name }} </td>",
    "<th> Applicant </th> <td /> <td /> {* <td> {{ [applicant_address] }} </td> <td /> *} <th> Advertised </th>",
    "<th> Applicant </th> <td /> <td /> {* <td /> <td> {{ [agent_address] }} </td> *} <th> Advertised </th>",
    "<th> Advertised </th> <td> {{ consultation_start_date }} </td> <td> {{ comment_date }} </td>",
    "<th> Decision </th> <td> <font> {{ decision }} </font> </td> <td> {{ decision_date }} </td>",
    "<th> Appeal Lodged </th> <td> {{ appeal_date }} </td> <td> {{ appeal_result }} </td> <td> {{ appeal_decision_date }} </td>",
    '<a href="{{ comment_url|abs }}">Comment on this application</a>' ]
    scrape_min_dates = """
    Validated <td> {{ date_validated }} </td>
    """

class UttlesfordScraper(OcellaScraper):

    TABLE_NAME = 'Uttlesford'
    search_url = 'http://planning.uttlesford.gov.uk/portal/page/portal/plan/weekly'
    form_name = 'PLANNING_LIST'
    applic_url = 'http://planning.uttlesford.gov.uk/portal/pls/portal/UTTWEB.RPT_APPLICATION_DETAILS.show'
    scrape_ids = """
    <table summary="Printing Table Headers"> <tr />
    {* <tr>
    <td> {{ [records].parish }} </td>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    </tr> *}
    </table>
    """

class WorcesterScraper(OcellaScraper):

    TABLE_NAME = 'Worcester'
    BATCH_DAYS = 21 # batch size for each scrape - number of days to gather to produce at least one result each time
    MIN_DAYS = 28 # min number of days to get when gathering current ids
    search_url = 'http://planningapps.worcester.gov.uk/portal/page/portal/worcester/search'
    form_name = 'FORM_SEARCH'
    search_form = '2'
    next_form = '2'
    applic_url = 'http://planningapps.worcester.gov.uk/portal/pls/portal/WWEB.RPT_DETAILS2.show'

    scrape_min_data = """
    <font> Application Reference </font> <font> {{ reference }} </font>
    <font> Description </font> <font> {{ address }} </font>
    <font> {{ description }} </font>
    <font> Date Started </font> <font> {{ date_received }} </font>
    """
    scrape_optional_data = [
    "<font> Current Status </font> <font> {{ status }} </font>",
    "<font> Ward </font> <font> {{ ward_name }} </font>",
    "<font> Agent Details </font> <font> {{ applicant_name }} </font> <font> {{ agent_name }} </font>",
    "<font> Agent Details </font> <font /> <font /> {* <font> {{ [applicant_address] }} </font> <font /> *} <font> Administration Details </font>",
    "<font> Agent Details </font> <font /> <font /> {* <font /> <font> {{ [agent_address] }} </font> *} <font> Administration Details </font>",
    "<font> Officer </font> <font> {{ case_officer }} </font>",
    "<font> Decision Due By </font> <font> {{ target_decision_date }} </font>",
    "<font> End of Consultation </font> <font> {{ consultation_end_date }} </font>",
    """<font> Committee Date </font> <font> {{ meeting_date }} </font>
    <font> Decision </font> <font> {{ decision }} </font> <font> Decision Date </font> <font> {{ decision_date }} </font>""",
    "<font> Appeal Started </font> <font> {{ appeal_date }} </font>",
    "<font> Appeal Decision Date </font> <font> {{ appeal_decision_date }} </font> <font /> <font> {{ appeal_result }} </font>",
    '<a href="{{ comment_url|abs }}">Comment on this application</a>' ]

if __name__ == 'scraper':

    #scraper = ArunScraper()
    #scraper.run()
    #util.rename_column('Rother', 'appeal_decided_date', 'appeal_decision_date')
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

    # misc test calls
    #scraper = ArunScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('BR/202/12/') # Arun OK
    #scraper = BrecklandScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('3PL/2011/0917/F') # Breckland OK
    #scraper = BridgendScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('P/11/629/FUL') # Bridgend OK
    #scraper = CastlePointScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('CPT/659/12/FUL') # Castle Point OK
    #scraper = FarehamScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('P/11/0703/FP') # Fareham OK
    #scraper = GreatYarmouthScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('06/11/0529/F') # Great Yarmouth OK
    #print scraper.get_detail_from_uid ('06/03/0054/F')
    #scraper = HaveringScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('C0005.12') # Havering OK
    #scraper = HillingdonScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('64345/APP/2011/1945') # Hillingdon OK
    #print scraper.get_detail_from_url ('http://www.hillingdon.gov.uk/planningsearch?lnk=189') # should return None = OK
    #scraper = MiddlesbroughScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('M/FP/0865/11/P') # Middlesbrough OK
    #scraper = NorthEastLincsScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('DC/695/11/WOL') # North East Lincs OK
    #scraper = RotherScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('RR/2011/1789/P') # Rother OK
    #scraper = UttlesfordScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('UTT/1343/11/LB') # Uttlesford Ok
    #scraper = WorcesterScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('P11A0394') # Worcester OK

    #scraper = WorcesterScraper()
    #print scraper.scrape_optional_data
    #scraper = BrecklandScraper()
    #print scraper.scrape_optional_data

    #scraper = BrecklandScraper()
    #res = scraper.get_id_batch(util.get_dt('15/11/2012'), util.get_dt('06/02/2013'))
    #print res, len(res)
    #scraper = MiddlesbroughScraper()
    #res = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('28/08/2011'))
    #res = scraper.get_id_batch(util.get_dt('16/03/2012'), util.get_dt('30/03/2012'))
    #print res, len(res)
    

    



    

    
