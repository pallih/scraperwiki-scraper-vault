# this is a base scraper for AcolNet system planning applications for use by Openly Local

# there are 29 authorities using this system, all 29 are defined but only 14 are scraped here

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
import gc

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

systems = {
    'Babergh': 'BaberghScraper',
    'Barnet': 'BarnetScraper', # now Idox too
    #'Basingstoke': 'BasingstokeScraper', now Idox
    'Bury': 'BuryScraper',
    'Cambridgeshire': 'CambridgeshireScraper',
    'Canterbury': 'CanterburyScraper',
    'Carlisle': 'CarlisleScraper',
    'CentralBedfordshire': 'CentralBedfordshireScraper',
    'Croydon': 'CroydonScraper', # now Idox too
    'Dacorum': 'DacorumScraper',
    'Derby': 'DerbyScraper',
    'Exeter': 'ExeterScraper',
    #'Greenwich': 'GreenwichScraper', # now Idox on port 81
    'Guildford': 'GuildfordScraper',
    # following are active in the 2nd scraper
    #'Harlow': 'HarlowScraper',
    #'Havant': 'HavantScraper',
    #'Hertsmere': 'HertsmereScraper',
    #'Lewisham': 'LewishamScraper', now Idox
    #'Medway': 'MedwayScraper',
    #'NewForest': 'NewForestScraper', now Idox
    #'NewForestPark': 'NewForestParkScraper', # National Park
    #'NorthHertfordshire': 'NorthHertfordshireScraper',
    #'NorthNorfolk': 'NorthNorfolkScraper',
    #'NorthWiltshire': 'NorthWiltshireScraper',
    #'Renfrewshire': 'RenfrewshireScraper',
    #'Southwark': 'SouthwarkScraper',
    #'Stockport': 'StockportScraper',
    #'StokeOnTrent': 'StokeOnTrentScraper',
    #'SuffolkCoastal': 'SuffolkCoastalScraper',
    #'Wirral': 'WirralScraper',
     }

class AcolNetScraper(base.DateScraper):

    MAX_ID_BATCH = 300 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go

    date_from_field = 'regdate1'
    date_to_field = 'regdate2'
    search_form = 'frmSearch'
    request_date_format = '%d/%m/%Y'
    ref_field = 'casefullref'
    scrape_ids = """
    <div id="contentcol">
    {* <table class="results-table">
    <tr> <td class="casenumber"> <a href="{{ [records].url|abs }}">
    {{ [records].uid }} </a> </td> </tr>
    </table> *}
    </div>
    """
    scrape_next = '<a id="lnkPageNext" href="{{ next_link }}"> </a>'
    scrape_ref_link = '<td class="casenumber"> <a href="{{ ref_link|abs }}"> </a> </td>'
    html_subs = { 
    r'<script\s.*?</script>': r'',
    r'<form\s[^>]*?WebMetric[^>]*?>.*?</form>': r''
    }

    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = '<body> {{ block|html }} </body>'
    # the minimum acceptable valid dataset on the details page
    scrape_min_data = """
    <th> Location </th> <td> {{ address }} </td>
    <th> Proposal </th> <td> {{ description }} </td>
    """
    # other optional parameters common to all scrapers can appear on the details page
    scrape_optional_data = [
    '<th> Date Received </th> <td> {{ date_received }} </td>',
    "<th> Application Number </th> <td> {{ reference }} </td>",
    "<th> Registration </th> <td> {{ date_validated }} </td>",
    "<th> Statutory Start </th> <td> {{ date_validated }} </td>",
    "<th> Application Type </th> <td> {{ application_type }} </td>",
    "<th> Case Officer </th> <td> {{ case_officer }} </td>",
    "<th> Decision Level </th> <td> {{ decided_by }} </td>",
    "Expected Decision Level <th> Decision Level </th> <td> {{ decided_by }} </td>",
    "<th> Appeal Received Date </th> <td> {{ appeal_date }} </td>",
    "<th> Date Appeal Recieved </th> <td> {{ appeal_date }} </td>", # NB spelling mistake is deliberate - Stoke on Trent
    "<th> Target Date for Decision </th> <td> {{ target_decision_date }} </td>",
    "<th> Appeal Decision </th> <td> {{ appeal_result }} </td>",
    "<th> Earliest Decision Date </th> <td> {{ consultation_end_date }} </td>",
    "<th> Consultation Period Expires </th> <td> {{ consultation_end_date }} </td>",
    "<th> Consultation Period Ends </th> <td> {{ consultation_end_date }} </td>",
    "<th> Status </th> <td> {{ status }} </td>",
    "<th> Parish </th> <td> {{ parish }} </td>",
    "<th> Ward </th> <td> {{ ward_name }} </td>",
    "<th> Comments </th> <td> {{ comment_date }} </td>",
    "<th> Applicant </th> <td> {{ applicant_name }} </td>",
    "<th> Consultation Start Date </th> <td> {{ consultation_start_date }} </td>",
    "<th> Consultation Period Starts </th> <td> {{ consultation_start_date }} </td>",
    "<th> Date from when comments </th> <td> {{ consultation_start_date }} </td>",
    "<th> Date Decision Made </th> <td> {{ decision_date }} </td>",
    "<th> Agent </th> <td> {{ agent_name }} </td>",
    "<th> Date Decision Despatched </th> <td> {{ decision_issued_date }} </td>",
    "<th> Decision Issued </th> <td> {{ decision_issued_date }} </td>",
    "<th> Meeting Date </th> <td> {{ meeting_date }} </td>",
    "<th> Committee </th> <td> {{ meeting_date }} </td>",
    "<tr> <th> Easting/Northing </th> <td> {{ easting }}/{{ northing }} </td> </tr>",
    "<th> Appeal Decision </th> <td> {{ appeal_result }} </td> <th> Appeal Decision Date </th> <td> {{ appeal_decision_date }} </td>",
    ]
    # optional parameters that can be replaced by versions in child scrapers
    scrape_variants = [
    "<th> Agent </th> <td /> {* <td> {{ [agent_address] }} </td> *} <th> Applicant </th>",
    "<th> Applicant </th> <td /> {* <td> {{ [applicant_address] }} </td> *} <th> Date </th>",
    "Decision Despatched <th> Decision </th> <td> {{ decision }} </td>",
    ]

    def __init__(self, table_name = None):
        self.br, self.handler, self.cj = util.get_browser(self.HEADERS)
        if table_name:
            self.TABLE_NAME = table_name
            self.DATA_START_MARKER = 'earliest-' + table_name
            self.DATA_END_MARKER = 'latest-' + table_name
        self.scrape_optional_data.extend(self.scrape_variants)

    def get_id_batch (self, date_from, date_to):

        if self.DEBUG: self.br.set_debug_http(True)

        response = self.br.open(self.search_url)

        response = self.br.response()  # this is a copy of the current browser response
        html = response.get_data()
        for k, v in self.html_subs.items(): # fix html which breaks form processing (nested SELECTS)
            html = re.sub(k, v, html, 0, re.U|re.S|re.I) # unicode|dot matches new line|ignore case
        response.set_data(html)
        self.br.set_response(response)

        fields = {}
        fields[self.date_from_field] = date_from.strftime(self.request_date_format)
        fields[self.date_to_field] = date_to.strftime(self.request_date_format)
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
                if 'next_link' in self.scrape_next:
                    result = scrapemark.scrape(self.scrape_next, html, url)
                    response = self.br.open(result['next_link'])
                else:
                    util.setup_form(self.br, self.scrape_next)
                    response = util.submit_form(self.br)
            except:
                response = None
        return final_result

    def get_detail_from_uid (self, uid):
        response = self.br.open(self.search_url)

        response = self.br.response()  # this is a copy of the current browser response
        html = response.get_data()
        for k, v in self.html_subs.items(): # fix html which breaks form processing (nested SELECTS)
            html = re.sub(k, v, html, 0, re.U|re.S|re.I) # unicode|dot matches new line|ignore case
        response.set_data(html)
        self.br.set_response(response)

        fields = {}
        fields[self.ref_field] = uid
        util.setup_form(self.br, self.search_form, fields)
        response = util.submit_form(self.br)
        try:
            html = response.read()
            if self.DEBUG: print html
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ref_link, html, url)
            url = result['ref_link']
            if self.DEBUG: print url
        except:
            return None
        return self.get_detail_from_url(url)

class BaberghScraper(AcolNetScraper):

    search_url = 'http://planning.babergh.gov.uk/dcdatav2/AcolNetCGI.gov?ACTION=UNWRAP&RIPNAME=Root.pgesearch'
    search_form = 'frmSearchByParish'
    TABLE_NAME = 'Babergh'

class BarnetScraper(AcolNetScraper):

    search_url = 'http://planningcases.barnet.gov.uk/planning-cases/acolnetcgi.exe?ACTION=UNWRAP&RIPNAME=Root.pgesearch'
    search_form = 'frmSearchByWard'
    TABLE_NAME = 'Barnet'

class BasingstokeScraper(AcolNetScraper):

    search_url = 'http://planning.basingstoke.gov.uk/DCOnline2/AcolNetCGI.dcgov?ACTION=UNWRAP&RIPNAME=Root.pgesearch'
    TABLE_NAME = 'Basingstoke'

class BuryScraper(AcolNetScraper):

    search_url = 'http://e-planning.bury.gov.uk/DCWebPages/acolnetcgi.gov?ACTION=UNWRAP&RIPNAME=Root.pgesearch'
    TABLE_NAME = 'Bury'

class CambridgeshireScraper(AcolNetScraper):

    BATCH_DAYS = 28 # batch size for each scrape - number of days to gather to produce at least one result each time
    MIN_DAYS = 28 # min number of days to get when gathering current ids
    search_url = 'http://planapps2.cambridgeshire.gov.uk/DCWebPages/AcolNetCGI.gov?ACTION=UNWRAP&RIPNAME=Root.pgesearch'
    TABLE_NAME = 'Cambridgeshire'
    search_form = 'frmSearchByParish'
    scrape_variants = [
    "<th> Agent </th> <td /> {* <td> {{ [agent_address] }} </td> *} <th> Case Type </th>",
    "<th> Applicant </th> <td /> {* <td> {{ [applicant_address] }} </td> *} <th> Date </th>",
    "Decision Despatched <th> Decision </th> <td> {{ decision }} </td>",
    ]

class CanterburyScraper(AcolNetScraper):

    search_url = 'http://www2.canterbury.gov.uk/planning/acolnetcgi.cgi?ACTION=UNWRAP&RIPNAME=Root.PgeSearch'
    TABLE_NAME = 'Canterbury'
    date_from_field = 'edtregdate1'
    date_to_field = 'edtregdate2'
    ref_field = 'edtappno'
    scrape_ids = """
    <div id="contentcol"> <table> <tr />
    {* <tr> <td> <a href="{{ [records].url|abs }}">
    {{ [records].uid }} </a> </td> </tr> *}
    </table> </div>
    """
    scrape_next = 'frmNextPage'
    scrape_ref_link = '<div id="contentcol"> <td> <a href="{{ ref_link|abs }}"> </a> </td> </div>'
    scrape_variants = [
    "<th> Agent </th> <td /> {* <td> {{ [agent_address] }} </td> *} <th> Applicant </th>",
    "<th> Applicant </th> <td /> {* <td> {{ [applicant_address] }} </td> *} <th> Decision </th>",
    "Level <th> Decision Date </th> <td> {{ decision_date }} </td> <th> Decision </th> <td> {{ decision }} </td>",
    ]

class CarlisleScraper(AcolNetScraper):

    search_url = 'http://planning.carlisle.gov.uk/applications/AcolNetCGI.gov?ACTION=UNWRAP&RIPNAME=Root.pgesearch'
    TABLE_NAME = 'Carlisle'

class CentralBedfordshireScraper(AcolNetScraper):

    search_url = 'http://www.centralbedfordshire.gov.uk/PLANTECH/DCWebPages/acolnetcgi.gov?ACTION=UNWRAP&RIPNAME=Root.pgesearch'
    TABLE_NAME = 'CentralBedfordshire'
    search_form = 'frmSearchByParish'
    scrape_ids = """
    <div id="contentcol">
    {* <table class="results-table">
    <tr> <td class="casenumber"> <a href="{{ [records].url|abs }}">
    {{ [records].uid }} (click for more details) </a> </td> </tr>
    </table> *}
    </div>
    """
    scrape_min_data = """
    <th> Location </th> <td> {{ address }} </td>
    <th> Description </th> <td> {{ description }} </td>
    """
    scrape_variants = [
    "<th> Agent </th> <td /> {* <td> {{ [agent_address] }} </td> *} <th> Date </th>",
    "<th> Applicant </th> <td /> {* <td> {{ [applicant_address] }} </td> *} <th> Agent </th>",
    "Decision Despatched <th> Decision </th> <td> {{ decision }} </td>",
    ]

class CroydonScraper(AcolNetScraper):

    search_url = 'http://planning.croydon.gov.uk/DCWebPages/acolnetcgi.gov?ACTION=UNWRAP&RIPNAME=Root.pgesearch'
    TABLE_NAME = 'Croydon'

class DacorumScraper(AcolNetScraper):

    search_url = 'http://212.44.10.240/planonline/AcolNetCGI.gov?ACTION=UNWRAP&RIPNAME=Root.pgesearch'
    TABLE_NAME = 'Dacorum'
    search_form = 'frmSearchByWard'
    html_subs = {
        r'<form name="aspnetForm"[^>]*>': r'',
    }
    scrape_variants = [
    "<th> Agent </th> <td /> {* <td> {{ [agent_address] }} </td> *} <th> Case Type </th>",
    "<th> Applicant </th> <td /> {* <td> {{ [applicant_address] }} </td> *} <th> Date </th>",
    "Decision Despatched <th> Decision </th> <td> {{ decision }} </td>",
    ]

class DerbyScraper(AcolNetScraper):

    search_url = 'http://eplanning.derby.gov.uk/acolnet/planningpages02/acolnetcgi.exe?ACTION=UNWRAP&RIPNAME=Root.pgesearch'
    TABLE_NAME = 'Derby'
    scrape_ids = """
    <div id="contentcol">
    {* <table class="results-table">
    <tr> <td class="casenumber"> <a href="{{ [records].url|abs }}">
    {{ [records].uid }} - link to more details </a> </td> </tr>
    </table> *}
    </div>
    """
    scrape_variants = [
    "<th> Agent </th> <td> <p> {{ agent_name }} </p> {* <p> {{ [agent_address] }} </p> *} </td> <th> Applicant </th>",
    "<th> Applicant </th> <td> <p> {{ applicant_name }} </p> {* <p> {{ [applicant_address] }} </p> *} </td> <th> Date </th>",
    "Decision Made <th> Decision </th> <td> {{ decision }} </td>",
    ]

class ExeterScraper(AcolNetScraper):

    search_url = 'http://pub.exeter.gov.uk/scripts/acolnet/planning/AcolnetCGI.gov?ACTION=UNWRAP&RIPNAME=Root.pgesearch'
    TABLE_NAME = 'Exeter'
    search_form = 'frmSearchByWard'
    scrape_variants = [
    "<th> Agent </th> <td /> {* <td> {{ [agent_address] }} </td> *} <th> Case Type </th>",
    "<th> Applicant </th> <td /> {* <td> {{ [applicant_address] }} </td> *} <th> Date </th>",
    "Decision Despatched <th> Decision </th> <td> {{ decision }} </td>",
    ]

class GreenwichScraper(AcolNetScraper):

    search_url = 'http://onlineplanning.greenwich.gov.uk/acolnet/planningonline/acolnetcgi.gov?ACTION=UNWRAP&RIPNAME=Root.pgesearch'
    TABLE_NAME = 'Greenwich'
    search_form = 'frmSearchByWard'

class GuildfordScraper(AcolNetScraper):

    search_url = 'http://www2.guildford.gov.uk/DLDC_Version_2/acolnetcgi.gov?ACTION=UNWRAP&RIPNAME=Root.pgesearch'
    TABLE_NAME = 'Guildford'
    scrape_variants = [
    "<th> Agent </th> <td /> {* <td> {{ [agent_address] }} </td> *} <th> Case Type </th>",
    "<th> Applicant </th> <td /> {* <td> {{ [applicant_address] }} </td> *} <th> Neighbours </th>",
    "Level <th> Decision Date </th> <td> {{ decision_date }} </td> <th> Decision </th> <td> {{ decision }} </td>",
    "<th> Location </th> <td> {{ address }} <a/> </td>",
    ]

class HarlowScraper(AcolNetScraper):

    search_url = 'http://planning.harlow.gov.uk/DLDC_Version_2/acolnetcgi.exe?ACTION=UNWRAP&RIPNAME=Root.pgesearch'
    TABLE_NAME = 'Harlow'

class HavantScraper(AcolNetScraper):

    search_url = 'http://www5.havant.gov.uk/ACOLNETDCOnline/acolnetcgi.gov?ACTION=UNWRAP&RIPNAME=Root.pgesearch'
    TABLE_NAME = 'Havant'

class HertsmereScraper(AcolNetScraper):

    search_url = 'http://www2.hertsmere.gov.uk/ACOLNET/DCOnline//acolnetcgi.gov?ACTION=UNWRAP&RIPNAME=Root.pgesearch'
    TABLE_NAME = 'Hertsmere'

class LewishamScraper(AcolNetScraper):

    search_url = 'http://acolnet.lewisham.gov.uk/lewis-xslpagesdc/acolnetcgi.exe?ACTION=UNWRAP&RIPNAME=Root.pgesearch'
    TABLE_NAME = 'Lewisham'
    date_from_field = 'edtregdate1'
    date_to_field = 'edtregdate2'
    ref_field = 'edtappno'

class MedwayScraper(AcolNetScraper):

    search_url = 'http://planning.medway.gov.uk/DCOnline/AcolNetCGI.gov?ACTION=UNWRAP&RIPNAME=Root.pgesearch'
    TABLE_NAME = 'Medway'
    search_form = 'frmSearchByWard'

class NewForestScraper(AcolNetScraper):

    search_url = 'http://web3.newforest.gov.uk/planningonline/acolnetcgi.gov?ACTION=UNWRAP&RIPNAME=Root.pgesearch'
    TABLE_NAME = 'NewForest'
    search_form = 'frmSearchByParish'
    scrape_variants = [
    "<th> Agent </th> <td /> {* <td> {{ [agent_address] }} </td> *} <th> Applicant </th>",
    "<th> Applicant </th> <td /> {* <td> {{ [applicant_address] }} </td> *} <th> Date </th>",
    "Level <th> Decision Date </th> <td> {{ decision_date }} </td> <th> Decision </th> <td> {{ decision }} </td>",
    "<th> Case Officer </th> <td> {{ case_officer }} Return to Search Page </td>",
    ]

class NewForestParkScraper(AcolNetScraper): # this is the national park, not the local authority

    search_url = 'http://web01.newforestnpa.gov.uk/Pages3/AcolNetCGI.dcgov?ACTION=UNWRAP&RIPNAME=Root.pgesearch'
    TABLE_NAME = 'NewForestPark'
    search_form = 'frmSearchByParish'
    scrape_variants = [
    "<th> Agent </th> <td /> {* <td> {{ [agent_address] }} </td> *} <th> Applicant </th>",
    "<th> Applicant </th> <td /> {* <td> {{ [applicant_address] }} </td> *} <th> Date </th>",
    "Site Visit <th> Decision </th> <td> {{ decision }} </td>",
    ]

class NorthHertfordshireScraper(AcolNetScraper):

    search_url = 'http://www.north-herts.gov.uk/dcdataonline/Pages/AcolNetCGI.gov?ACTION=UNWRAP&RIPNAME=Root.pgesearch'
    TABLE_NAME = 'NorthHertfordshire'

class NorthNorfolkScraper(AcolNetScraper):

    search_url = 'http://planweb.north-norfolk.gov.uk/Planning/AcolNetCGI.exe?ACTION=UNWRAP&RIPNAME=Root.pgesearch'
    TABLE_NAME = 'NorthNorfolk'
    search_form = 'frmSearchByParish'
    scrape_variants = [
    "<th> Agent </th> <td /> {* <td> {{ [agent_address] }} </td> *} <th> Case Type </th>",
    "<th> Applicant </th> <td /> {* <td> {{ [applicant_address] }} </td> *} <th> Date </th>",
    "Decision Despatched <th> Decision </th> <td> {{ decision }} </td>",
    ]

class NorthWiltshireScraper(AcolNetScraper):

    search_url = 'http://northplanning.wiltshire.gov.uk/DCOnline/acolnetcgi.gov?ACTION=UNWRAP&RIPNAME=Root.pgesearch'
    TABLE_NAME = 'NorthWiltshire'

class RenfrewshireScraper(AcolNetScraper):

    search_url = 'http://planning.renfrewshire.gov.uk/dcwebpages02/acolnetcgi.gov?ACTION=UNWRAP&RIPNAME=Root.pgesearch'
    TABLE_NAME = 'Renfrewshire'
    date_from_field = 'recdate1'
    date_to_field = 'recdate2'
    scrape_variants = [
    "<th> Agent </th> <td /> {* <td> {{ [agent_address] }} </td> *} <th> Applicant </th>",
    "<th> Applicant </th> <td /> {* <td> {{ [applicant_address] }} </td> *} <th> Decision </th>",
    "Applicant <th> Decision </th> <td> {{ decision }} </td>",
    "<th> Community Council </th> <td> {{ parish }} </td>",
    ]

class SouthwarkScraper(AcolNetScraper):

    search_url = 'http://planningonline.southwarksites.com/planningonline2/AcolNetCGI.exe?ACTION=UNWRAP&RIPNAME=Root.pgesearch'
    TABLE_NAME = 'Southwark'
    scrape_variants = [
    "<th> Agent </th> <td /> {* <td> {{ [agent_address] }} </td> *} <th> Ward </th>",
    "<th> Applicant </th> <td /> {* <td> {{ [applicant_address] }} </td> *} <th> Agent </th>",
    "Applicant <th> Decision Made </th> <td> {{ decision_date }} </td> <th> Decision </th> <td> {{ decision }} </td>",
    "<th> Community Council </th> <td> {{ parish }} </td>",
    ]

class StockportScraper(AcolNetScraper):

    search_url = 'http://planning.stockport.gov.uk/PlanningData/AcolNetCGI.gov?ACTION=UNWRAP&RIPNAME=Root.pgesearch'
    TABLE_NAME = 'Stockport'
    search_form = 'frmSearchByWard'

class StokeOnTrentScraper(AcolNetScraper):

    search_url = 'http://www.planning.stoke.gov.uk/dataonlineplanning/AcolNetCGI.exe?ACTION=UNWRAP&RIPNAME=Root.pgesearch'
    TABLE_NAME = 'StokeOnTrent'

class SuffolkCoastalScraper(AcolNetScraper):

    search_url = 'http://apps3.suffolkcoastal.gov.uk/DCDataV2/acolnetcgi.gov?ACTION=UNWRAP&RIPNAME=Root.pgesearch'
    TABLE_NAME = 'SuffolkCoastal'

class WirralScraper(AcolNetScraper):

    search_url = 'http://www.wirral.gov.uk/planning/DC/AcolNetCGI.gov?ACTION=UNWRAP&RIPNAME=Root.pgesearch'
    TABLE_NAME = 'Wirral'
    search_form = 'frmSearchByWard'
    scrape_variants = [
    "<th> Agent </th> <td /> {* <td> {{ [agent_address] }} </td> *} <th> Case Type </th>",
    "<th> Applicant </th> <td /> {* <td> {{ [applicant_address] }} </td> *} <th> Neighbours </th>",
    "Decision Despatched <th> Decision </th> <td> {{ decision }} </td>",
    ]

if __name__ == 'scraper':

    #scraperwiki.sqlite.execute("update Canterbury set date_scraped = null, address = null, status = null, applicant_name = null where length(applicant_name) > 1024")
    #scraperwiki.sqlite.commit()
    #sys.exit()
    #scraper = DacorumScraper() 
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
            scraper = None
            gc.collect()
        except Exception as err:
            print "Error - skipping this authority -", str(err)
    print "Finished"

    # misc test calls
    #scraper = BaberghScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('B/11/00894') # Babergh OK
    #scraper = BarnetScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('B/03361/11') # Barnet OK
    #scraper = BasingstokeScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('BDB/74875') # Basingstoke OK
    #scraper = BuryScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('54341') # Bury OK
    #scraper = CambridgeshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('S/01521/11/CC') # Cambridgeshire low numbers OK
    #scraper = CanterburyScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('CA//12/00751') # Canterbury OK
    #scraper = CarlisleScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/0667') # Carlisle OK
    #scraper = CentralBedfordshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('CB/11/02642/ADV') # CentralBedfordshire OK
    #scraper = CroydonScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/01369/P') # Croydon OK
    #scraper = DacorumScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('4/01130/11/FUL') # Dacorum OK
    #scraper = DerbyScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('08/11/00983') # Derby OK
    #scraper = ExeterScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/1409/07') # Exeter OK slow
    #scraper = GreenwichScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/1968/F') # Greenwich OK
    #scraper = GuildfordScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/T/00179') # Guildford OK
    #scraper = HarlowScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('HW/TP/11/10022') # Harlow OK
    #scraper = HavantScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('APP/11/01323') # Havant OK
    #scraper = HertsmereScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('TP/11/1511') # Hertsmere OK
    #scraper = LewishamScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('DC/11/76704/X') # Lewisham OK
    #scraper = MedwayScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('MC/11/2155') # Medway OK
    #scraper = NewForestScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/97541') # NewForest OK
    #scraper = NewForestParkScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/96734') # NewForestPark OK
    #scraper = NorthHertfordshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/01995/1HH') # NorthHertfordshire OK
    #scraper = NorthNorfolkScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('NMA1/10/1453') # NorthNorfolk OK
    #scraper = NorthWiltshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/02822/FUL') # NorthWiltshire OK
    #scraper = RenfrewshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/0580/PP') # Renfrewshire slow OK
    #scraper = SouthwarkScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/AP/2280') # Southwark OK
    #scraper = StockportScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('DC/047899') # Stockport OK
    #scraper = StokeOnTrentScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('52503/FUL') # StokeOnTrent OK
    #scraper = SuffolkCoastalScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('C/11/1884') # SuffolkCoastal OK
    #scraper = WirralScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('APP/11/00967') # Wirral OK


    #res = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('18/08/2011'))
    #print res, len(res)


    

