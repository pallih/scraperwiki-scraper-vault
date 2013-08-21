# this is a scraper of Telford and Wrekin / Carmarthenshire planning applications for use by Openly Local

# note currently excludes enforcement notices = development control only

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import urllib
import urlparse
import sys

base = scraperwiki.utils.swimport("openlylocal_base_scraper")
scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")

systems = {
    'Carmarthenshire': 'CarmarthenshireScraper',
    'Telford': 'TelfordScraper',
     }

class EAccessv2Scraper(base.DateScraper):

    date_from_field = 'DCdatefrom'
    date_to_field = 'DCdateto'
    start_fields = { '__EVENTTARGET': 'lnkSearchPlanning', '__EVENTARGUMENT': '', }
    search_action = 'SearchAllPCByDetailsResults.aspx'
    search_submit = 'btnSearchPlanningDetails'
    search_fields = { '__EVENTTARGET': 'btnSearchPlanningDetails', '__EVENTARGUMENT': '', }
    request_date_format = '%d-%m-%Y'
    scrape_ids = """
    <table id="TableResults"> <tr />
        {* <tr>
        <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
        <td> Development Control </td>
        </tr> *}
    </table>
    """
    link_next = 'Next'

    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div class="informationarea"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <tr> Application number {{ reference }} </tr>
    <tr> Site address {{ address }} </tr>
    <tr> Descripton of proposal {{ description }} </tr>
    <tr> Date valid {{ date_validated }} </tr>
    """ # note spelling mistake (Descripton)
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    "<tr> Application type {{ application_type }} </tr>", # OK
    '<ul id="ApplicationStatuslist"> <li class="selected"> {{ status }} </li> </ul>', # OK
    '<ul id="ApplicationStatuslist"> <li class="first selected"> {{ status }} </li> </ul>', # OK
    '<ul id="ApplicationStatuslist"> <li class="last selected"> {{ status }} </li> </ul>', # OK
    "<tr> Grid reference <span> {{ easting }} </span> <span> {{ northing }} </span> </tr>", # OK
    "<tr> Case officer {{ case_officer }} </tr>", # OK
    "<tr> Parish {{ parish }} </tr>", # OK
    "<tr> Ward {{ ward_name }} </tr>", # OK
    "<tr> Delegation level {{ decided_by }} </tr>", # OK
    """<tr> <th> Decision </th> {{ decision }} </tr>
    <tr> <th> Decision date </th> {{ decision_date }} </tr>""", # OK
    """<tr> Agent {{ [agent_name] }} </tr>
    <tr> Agent Company Name {{ [agent_name] }} </tr>""", # OK
    "<tr> Agent address {{ agent_address }} </tr>", # OK
    """<tr> Applicant {{ [applicant_name] }} </tr>
    <tr> Applicant Company Name {{ [applicant_name] }} </tr>""", #OK
    "<tr> Applicant address {{ applicant_address }} </tr>", # OK
    "<tr> <th> Appeal decision </th> {{ appeal_result }} </tr>", # OK
    "<tr> <th> Appeal decision date </th> {{ appeal_decision_date }} </tr>", # OK
    '<tr> Planning portal reference {{ planning_portal_id }} </tr>'
    ]
    # other parameters that appear on the progress page
    scrape_extra_data = [
    "<tr> Application Received {{ date_received }} </tr>", # OK
    "<tr> Consultation expiry date {{ consultation_end_date }} </tr>", # OK
    "<tr> Press notice expires {{ last_advertised_date }} </tr>", # OK
    "<tr> Site notice expires {{ site_notice_end_date }} </tr>", # OK
    "<tr> Plans board date {{ meeting_date }} </tr>", # OK
    "<tr> Application expiry date {{ permission_expires_date }} </tr>", # OK
    ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.start_url, urllib.urlencode(self.start_fields))

        self.search_fields[self.date_from_field] = date_from.strftime(self.request_date_format)
        self.search_fields[self.date_to_field] = date_to.strftime(self.request_date_format)
        #print self.search_fields
        form_ok = util.setup_form(self.br, self.search_form, self.search_fields, self.search_action )
        
        response = util.submit_form(self.br, self.search_submit)

        final_result = []
        while response:
            html = response.read()
            url = response.geturl()
            #print html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            try:
                response = self.br.follow_link(text=self.link_next)
            except:
                response = None
        return final_result

    def get_detail_from_uid (self, uid):
        url = self.applic_url + '?applicationnumber=' + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

    # scrape detailed information on one record via its access URL
    def get_detail_from_url (self, url):
        result = base.BaseScraper.get_detail_from_url (self, url)
        if result:
            try:
                response = self.br.follow_link(text='Progress')
                extra_html = response.read()
                extra_result = {}
                for i in self.scrape_extra_data:
                    next_val = scrapemark.scrape(i, extra_html)
                    if next_val:
                        extra_result.update(next_val)
                self.clean_record(extra_result)
                result.update(extra_result)
                return result
            except:
                #print "Failed to get extra detail from progress page:", url
                #return None
                return result
        else:
            return None

class CarmarthenshireScraper(EAccessv2Scraper):

    start_url = 'http://online.carmarthenshire.gov.uk/eaccessv2/search-all.aspx?Tab=Details'
    applic_url = 'http://online.carmarthenshire.gov.uk/eaccessv2/pa-applicationsummary.aspx'
    search_form = '0'

class TelfordScraper(EAccessv2Scraper):

    start_url = 'https://secure.telford.gov.uk/planning/search-all.aspx'
    applic_url = 'https://secure.telford.gov.uk/planning/pa-applicationsummary.aspx'
    search_form = 'form1'

if __name__ == 'scraper':

    #scraper = TelfordScraper('Telford')
    #scraper.replace_all_with('telford_planning_applications')
    #sys.exit()

    sys_list = []
    for k, v in systems.items(): # get latest date scraped for each system
        sys_list.append( (k, v, scraperwiki.sqlite.get_var('latest-' + k)) )
    sort_sys = sorted(sys_list, key=lambda system: system[2]) # sort so least recent are first
    for auth in sort_sys[:4]: # do max 4 per run
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
    #scraper = CarmarthenshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('W/25167') # Carmarthenshire
    #scraper = TelfordScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('TWC/2012/0233') # Telford
    #print scraper.get_detail_from_uid ('A2000/0002')
    
    #res = scraper.get_id_batch(util.get_dt('24/07/2011'), util.get_dt('29/07/2011'))
    #print res, len(res)
    #print scraper.get_id_batch(util.get_dt('23/03/2012'), util.get_dt('25/03/2012'))


