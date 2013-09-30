# this is a scraper of Telford and Wrekin planning applications for use by Openly Local

# very similar to Carmarthenshire

# note currently excludes enforcement notices = development control only

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import urllib
import urlparse

base = scraperwiki.utils.swimport("openlylocal_base_scraper")
scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")

class TelfordScraper(base.DateScraper):

    date_from_field = 'DCdatefrom'
    date_to_field = 'DCdateto'
    start_fields = { '__EVENTTARGET': 'lnkSearchPlanning', '__EVENTARGUMENT': '', }
    search_form = 'form1'
    search_action = 'SearchAllPCByDetailsResults.aspx'
    search_submit = 'btnSearchPlanningDetails'
    search_fields = { '__EVENTTARGET': 'btnSearchPlanningDetails', '__EVENTARGUMENT': '', }
    request_date_format = '%d-%m-%Y'
    start_url = 'https://secure.telford.gov.uk/planning/search-all.aspx'
    applic_url = 'https://secure.telford.gov.uk/planning/pa-applicationsummary.aspx'
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
    <tr> Planning portal reference {{ planning_portal_id }} </tr>
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
    "<tr> <th> Decision </th> {{ decision }} </tr>", # OK
    "<tr> <th> Decision date </th> {{ decision_date }} </tr>", # OK
    "<tr> Agent {{ agent_name }} </tr>", # OK
    "<tr> Agent Company Name {{ agent_name }} </tr>", # OK
    "<tr> Agent address {{ agent_address }} </tr>", # OK
    "<tr> Applicant {{ applicant_name }} </tr>",
    "<tr> Applicant Company Name {{ applicant_name }} </tr>", #OK
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

if __name__ == 'scraper':

    #scraper = TelfordScraper()
    #scraper.run()

    #scraper.DEBUG = True

    # misc test calls
    #print scraper.get_detail_from_uid ('TA/2012/0398')
    #print scraper.get_more_detail_from_url(scraper.progress_url + '?applicationnumber=TA/2012/0389')
    #result = scraper.get_id_batch(util.get_dt('31/01/2011'), util.get_dt('08/02/2011'))
    #print len(result), result
    #print scraper.get_id_batch(util.get_dt('23/03/2012'), util.get_dt('25/03/2012'))


# this is a scraper of Telford and Wrekin planning applications for use by Openly Local

# very similar to Carmarthenshire

# note currently excludes enforcement notices = development control only

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import urllib
import urlparse

base = scraperwiki.utils.swimport("openlylocal_base_scraper")
scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")

class TelfordScraper(base.DateScraper):

    date_from_field = 'DCdatefrom'
    date_to_field = 'DCdateto'
    start_fields = { '__EVENTTARGET': 'lnkSearchPlanning', '__EVENTARGUMENT': '', }
    search_form = 'form1'
    search_action = 'SearchAllPCByDetailsResults.aspx'
    search_submit = 'btnSearchPlanningDetails'
    search_fields = { '__EVENTTARGET': 'btnSearchPlanningDetails', '__EVENTARGUMENT': '', }
    request_date_format = '%d-%m-%Y'
    start_url = 'https://secure.telford.gov.uk/planning/search-all.aspx'
    applic_url = 'https://secure.telford.gov.uk/planning/pa-applicationsummary.aspx'
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
    <tr> Planning portal reference {{ planning_portal_id }} </tr>
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
    "<tr> <th> Decision </th> {{ decision }} </tr>", # OK
    "<tr> <th> Decision date </th> {{ decision_date }} </tr>", # OK
    "<tr> Agent {{ agent_name }} </tr>", # OK
    "<tr> Agent Company Name {{ agent_name }} </tr>", # OK
    "<tr> Agent address {{ agent_address }} </tr>", # OK
    "<tr> Applicant {{ applicant_name }} </tr>",
    "<tr> Applicant Company Name {{ applicant_name }} </tr>", #OK
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

if __name__ == 'scraper':

    #scraper = TelfordScraper()
    #scraper.run()

    #scraper.DEBUG = True

    # misc test calls
    #print scraper.get_detail_from_uid ('TA/2012/0398')
    #print scraper.get_more_detail_from_url(scraper.progress_url + '?applicationnumber=TA/2012/0389')
    #result = scraper.get_id_batch(util.get_dt('31/01/2011'), util.get_dt('08/02/2011'))
    #print len(result), result
    #print scraper.get_id_batch(util.get_dt('23/03/2012'), util.get_dt('25/03/2012'))


