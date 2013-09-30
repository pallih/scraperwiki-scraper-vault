# this is a scraper for two systems similar to PlanningExplorer systems

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
base = scraperwiki.utils.swimport("planningexplorer_system_planning_applications")

systems = {
    #'EastStaffordshire': 'EastStaffordshireScraper', now in standard Planning Explorer scraper
    'WestOxfordshire': 'WestOxfordshireScraper',
     }

class ExploreAlikeScraper(base.PlanningExplorerScraper):

    MAX_ID_BATCH = 200 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 150 # max application details to scrape in one go

    scrape_ids = """
    <table class="ResultsTable"> <tr />
    {* <tr>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    </tr> *}
    </table>
    """
    scrape_max_recs = '<span id="lblPagePosition"> of {{ max_recs }} </span>'
    next_form = 'Template'
    next_fields = { '__EVENTTARGET': 'lnkNextTop', '__EVENTARGUMENT': '', }

    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = '<div class="layoutdiv"> {{ block|html }} </div>'
    # the minimum acceptable valid dataset on the details page
    scrape_min_data = """
    <tr> <td> Date Valid </td> <td> {{ date_validated }} </td> </tr>
    <tr> <td> Application Number </td> <td> {{ reference }} </td> </tr>
    <tr> <td> Site Address </td> <td> {{ address }} </td> </tr>
    <tr> <td> Proposal </td> <td> {{ description }} </td> </tr>
    """
    # other optional parameters that can appear on the details page
    scrape_optional_data = [
    "<tr> <td> Application Type </td> <td> {{ application_type }} </td>",
    "<tr> <td> Status Description </td> <td> {{ status }} </td>",
    "<tr> <td> Applicant Name </td> <td> {{ applicant_name }} </td>",
    "<tr> <td> Applicant Address </td> <td> {{ applicant_address }} </td>",
    "<tr> <td> Agent Name </td> <td> {{ agent_name }} </td>",
    "<tr> <td> Agent Address </td> <td> {{ agent_address }} </td>",
    "<tr> <td> Ward </td> <td> {{ ward_name }} </td>",
    "<tr> <td> Case Officer Name </td> <td> {{ case_officer }} </td>",
    "<tr> <td> Decision Date </td> <td> {{ decision_date }} </td>",
    "<tr> <td> Target Date </td> <td> {{ target_decision_date }} </td>",
    "<tr> Legal Agreement </tr> <tr> <td> Decision </td> <td> {{ decision }} </td>",
    "<tr> <td> First Advertised </td> <td> {{ latest_advertisement_expiry_date }} </td>",
    "<tr> <td> Last Advertised </td> <td> {{ last_advertised_date }} </td>",
    "<tr> <td> Consultation Period Expires </td> <td> {{ consultation_end_date }} </td>", 
    "<tr> <td> Last Consulted </td> <td> {{ consultation_start_date }} </td>",
    "<tr> <td> Date to Commitee  </td> <td> {{ meeting_date }} </td>",
    "<tr> <td> Date Appeal Submitted  </td> <td> {{ appeal_date }} </td>",
    "<tr> <td> Appeal Decision  </td> <td> {{ appeal_result }} </td>",
    "<tr> <td> Date of Appeal Decision  </td> <td> {{ appeal_decision_date }} </td>",
    ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)

        fields = self.search_fields
        fields[self.date_from_field] = date_from.strftime(self.request_date_format)
        fields[self.date_to_field] = date_to.strftime(self.request_date_format)
        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br, self.search_submit)

        html = response.read()
        if self.DEBUG: print html
        try:
            result = scrapemark.scrape(self.scrape_max_recs, html)
            if self.DEBUG: print result
            max_recs = int(result['max_recs'])
        except:
            max_recs = 0

        final_result = []
        while response and len(final_result) < max_recs:
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            else:
                break
            if len(final_result) >= max_recs: break
            try:
                util.setup_form(self.br, self.next_form, self.next_fields)
                if self.DEBUG: print self.br.form
                response = util.submit_form(self.br)
                html = response.read()
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
        return base.PlanningExplorerScraper.clean_record(self, record)

    def get_detail_from_uid (self, uid):
        response = self.br.open(self.search_url)
        fields = self.applic_fields
        fields[self.ref_field] = uid
        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
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
        return self.get_detail(html, url)


#class EastStaffordshireScraper(ExploreAlikeScraper):

#    search_url = 'http://www2.eaststaffsbc.gov.uk/Northgate/PlanningExplorer/GeneralSearch.aspx'
#    date_from_field = 'ctl07_input'
#    date_to_field = 'ctl08_input'
#    search_fields = { 'rbGroup': ['ctl05'] }
#    applic_fields = { 'rbGroup': ['ctl06'] }
#    ref_field = 'txtAlternativeApplicationNumber'

class WestOxfordshireScraper(ExploreAlikeScraper): 

    search_url = 'http://planning.westoxon.gov.uk/MVM/Online/PL/GeneralSearch.aspx'
    date_from_field = '_ctl7_hidden'
    date_to_field = '_ctl8_hidden'
    search_fields = { 'rbGroup': ['_ctl5'] }
    applic_fields = { 'rbGroup': ['_ctl6'] }
    ref_field = 'txtApplicationNumber'
    request_date_format = '%%3CDateChooser%%20Value%%3D%%22%Y%%252C%-m%%252C%-d%%22%%3E%%3CExpandEffects%%3E%%3C/ExpandEffects%%3E%%3C/DateChooser%%3E'


if __name__ == 'scraper':

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
    #scraper = EastStaffordshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('P/2012/01244') # EastStaffordshire
    #scraper = WestOxfordshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/1205/P/FP') # WestOxfordshire
    
    #res = scraper.get_id_batch(util.get_dt('24/07/2011'), util.get_dt('28/07/2011'))
    #print res, len(res)
    #print scraper.get_id_batch(util.get_dt('23/03/2012'), util.get_dt('25/03/2012'))


    

# this is a scraper for two systems similar to PlanningExplorer systems

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
base = scraperwiki.utils.swimport("planningexplorer_system_planning_applications")

systems = {
    #'EastStaffordshire': 'EastStaffordshireScraper', now in standard Planning Explorer scraper
    'WestOxfordshire': 'WestOxfordshireScraper',
     }

class ExploreAlikeScraper(base.PlanningExplorerScraper):

    MAX_ID_BATCH = 200 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 150 # max application details to scrape in one go

    scrape_ids = """
    <table class="ResultsTable"> <tr />
    {* <tr>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    </tr> *}
    </table>
    """
    scrape_max_recs = '<span id="lblPagePosition"> of {{ max_recs }} </span>'
    next_form = 'Template'
    next_fields = { '__EVENTTARGET': 'lnkNextTop', '__EVENTARGUMENT': '', }

    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = '<div class="layoutdiv"> {{ block|html }} </div>'
    # the minimum acceptable valid dataset on the details page
    scrape_min_data = """
    <tr> <td> Date Valid </td> <td> {{ date_validated }} </td> </tr>
    <tr> <td> Application Number </td> <td> {{ reference }} </td> </tr>
    <tr> <td> Site Address </td> <td> {{ address }} </td> </tr>
    <tr> <td> Proposal </td> <td> {{ description }} </td> </tr>
    """
    # other optional parameters that can appear on the details page
    scrape_optional_data = [
    "<tr> <td> Application Type </td> <td> {{ application_type }} </td>",
    "<tr> <td> Status Description </td> <td> {{ status }} </td>",
    "<tr> <td> Applicant Name </td> <td> {{ applicant_name }} </td>",
    "<tr> <td> Applicant Address </td> <td> {{ applicant_address }} </td>",
    "<tr> <td> Agent Name </td> <td> {{ agent_name }} </td>",
    "<tr> <td> Agent Address </td> <td> {{ agent_address }} </td>",
    "<tr> <td> Ward </td> <td> {{ ward_name }} </td>",
    "<tr> <td> Case Officer Name </td> <td> {{ case_officer }} </td>",
    "<tr> <td> Decision Date </td> <td> {{ decision_date }} </td>",
    "<tr> <td> Target Date </td> <td> {{ target_decision_date }} </td>",
    "<tr> Legal Agreement </tr> <tr> <td> Decision </td> <td> {{ decision }} </td>",
    "<tr> <td> First Advertised </td> <td> {{ latest_advertisement_expiry_date }} </td>",
    "<tr> <td> Last Advertised </td> <td> {{ last_advertised_date }} </td>",
    "<tr> <td> Consultation Period Expires </td> <td> {{ consultation_end_date }} </td>", 
    "<tr> <td> Last Consulted </td> <td> {{ consultation_start_date }} </td>",
    "<tr> <td> Date to Commitee  </td> <td> {{ meeting_date }} </td>",
    "<tr> <td> Date Appeal Submitted  </td> <td> {{ appeal_date }} </td>",
    "<tr> <td> Appeal Decision  </td> <td> {{ appeal_result }} </td>",
    "<tr> <td> Date of Appeal Decision  </td> <td> {{ appeal_decision_date }} </td>",
    ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)

        fields = self.search_fields
        fields[self.date_from_field] = date_from.strftime(self.request_date_format)
        fields[self.date_to_field] = date_to.strftime(self.request_date_format)
        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br, self.search_submit)

        html = response.read()
        if self.DEBUG: print html
        try:
            result = scrapemark.scrape(self.scrape_max_recs, html)
            if self.DEBUG: print result
            max_recs = int(result['max_recs'])
        except:
            max_recs = 0

        final_result = []
        while response and len(final_result) < max_recs:
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            else:
                break
            if len(final_result) >= max_recs: break
            try:
                util.setup_form(self.br, self.next_form, self.next_fields)
                if self.DEBUG: print self.br.form
                response = util.submit_form(self.br)
                html = response.read()
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
        return base.PlanningExplorerScraper.clean_record(self, record)

    def get_detail_from_uid (self, uid):
        response = self.br.open(self.search_url)
        fields = self.applic_fields
        fields[self.ref_field] = uid
        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
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
        return self.get_detail(html, url)


#class EastStaffordshireScraper(ExploreAlikeScraper):

#    search_url = 'http://www2.eaststaffsbc.gov.uk/Northgate/PlanningExplorer/GeneralSearch.aspx'
#    date_from_field = 'ctl07_input'
#    date_to_field = 'ctl08_input'
#    search_fields = { 'rbGroup': ['ctl05'] }
#    applic_fields = { 'rbGroup': ['ctl06'] }
#    ref_field = 'txtAlternativeApplicationNumber'

class WestOxfordshireScraper(ExploreAlikeScraper): 

    search_url = 'http://planning.westoxon.gov.uk/MVM/Online/PL/GeneralSearch.aspx'
    date_from_field = '_ctl7_hidden'
    date_to_field = '_ctl8_hidden'
    search_fields = { 'rbGroup': ['_ctl5'] }
    applic_fields = { 'rbGroup': ['_ctl6'] }
    ref_field = 'txtApplicationNumber'
    request_date_format = '%%3CDateChooser%%20Value%%3D%%22%Y%%252C%-m%%252C%-d%%22%%3E%%3CExpandEffects%%3E%%3C/ExpandEffects%%3E%%3C/DateChooser%%3E'


if __name__ == 'scraper':

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
    #scraper = EastStaffordshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('P/2012/01244') # EastStaffordshire
    #scraper = WestOxfordshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/1205/P/FP') # WestOxfordshire
    
    #res = scraper.get_id_batch(util.get_dt('24/07/2011'), util.get_dt('28/07/2011'))
    #print res, len(res)
    #print scraper.get_id_batch(util.get_dt('23/03/2012'), util.get_dt('25/03/2012'))


    

