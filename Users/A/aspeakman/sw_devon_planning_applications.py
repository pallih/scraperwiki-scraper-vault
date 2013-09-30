# this is a scraper of South Hams and West Devon planning applications for use by Openly Local

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

systems = {
    'SouthHams': 'SouthHamsScraper',
    'WestDevon': 'WestDevonScraper',
     }

class SWDevonScraper(base.DateScraper):

    MAX_ID_BATCH = 200 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 150 # max application details to scrape in one go

    advanced_tab = 'ctl00$BodyContent$tab2'
    date_from_field = {
        'day': 'ctl00$BodyContent$start_date_day',
        'month': 'ctl00$BodyContent$start_date_month',
        'year': 'ctl00$BodyContent$start_date_year',
        }
    date_to_field = {
        'day': 'ctl00$BodyContent$end_date_day',
        'month': 'ctl00$BodyContent$end_date_month',
        'year': 'ctl00$BodyContent$end_date_year',
        }
    request_date_format = '%-d/%-m/%Y'
    search_form = '0'
    scrape_ids = """
    <fieldset title="Search Results">
    {* <div class="resultItemAdvanced">
    <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a>
    </div *}
    </fieldset>
    """
    scrape_next = '<input type="submit" name="{{ next_submit }}" value="Next">'
    dates_tab = 'ctl00$BodyContent$sub3'
    names_tab = 'ctl00$BodyContent$sub4'
    scrape_data_block = """
    <div id="divContent"> {{ block|html }} </div>
    """
    scrape_min_data = """
    <span id="BodyContent_lblNumber1"> {{ reference }} </span>
    <div id="BodyContent_basicDescriptionData"> {{ description }} </div>
    <div id="BodyContent_basicAddressData"> {{ address }} </div>
    """
    scrape_min_names = """
    <div id="BodyContent_basicApplicantNameData"> {{ applicant_name }} </div>
    """
    scrape_min_dates = """
    <div id="BodyContent_basicDateReceivedData"> {{ date_received }} </div>
    <div id="BodyContent_basicDateRegisteredData"> {{ date_validated }} </div>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<div id="BodyContent_basicDecisionData"> {{ decision }} </div>',
    '<div id="BodyContent_basicDecisionDateData"> {{ decision_date }} </div>',
    '<div id="BodyContent_basicCaseOfficerData"> {{ case_officer }} </div>',
    ]
    scrape_optional_dates = [
    '<div id="BodyContent_basicDateTargetData"> {{ target_decision_date }} </div>',
    '<div id="BodyContent_basicDateCommentsData"> {{ comment_date }} </div>',
    '<div id="BodyContent_basicDateDecisionData"> {{ decision_date }} </div>',
    '<div id="BodyContent_basicDateAdvertData"> {{ last_advertised_date }} </div>',
    ]
    scrape_optional_names = [
    '<div id="BodyContent_basicApplicantAddressData"> {{ applicant_address }} </div>',
    '<div id="BodyContent_basicAgentNameData"> {{ agent_name }} </div>',
    '<div id="BodyContent_basicAgentAddressData"> {{ agent_address }} </div>',
    ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)
        if self.DEBUG:
            print "Html obtained from search url:", response.read()

        fields = { '__EVENTTARGET': self.advanced_tab, '__EVENTARGUMENT': '', 'ctl00$BodyContent$btnSimpleSearch': None}
        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br)
        if self.DEBUG:
            print "Html obtained from advanced url:", response.read()

        fields = {}
        date_from = date_from.strftime(self.request_date_format)
        date_parts = date_from.split('/')
        fields [self.date_from_field['day']] = date_parts[0]
        fields [self.date_from_field['month']] = date_parts[1]
        fields [self.date_from_field['year']] = date_parts[2]
        date_to = date_to.strftime(self.request_date_format)
        date_parts = date_to.split('/')
        fields [self.date_to_field['day']] = date_parts[0]
        fields [self.date_to_field['month']] = date_parts[1]
        fields [self.date_to_field['year']] = date_parts[2]

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
                result = scrapemark.scrape(self.scrape_next, html)
                try:
                    next_submit = result['next_submit']
                except:
                    break
                form_ok = util.setup_form(self.br, self.search_form)
                if self.DEBUG: print "form:", self.br.form
                response = util.submit_form(self.br, next_submit)
            else:
                break

        return final_result

    def get_detail_from_uid (self, uid):
        url = self.applic_url + urllib.quote_plus(uid)
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
                #response = self.br.follow_link(text=self.dates_link)
                fields = { '__EVENTTARGET': self.dates_tab, '__EVENTARGUMENT': ''}
                util.setup_form(self.br, self.search_form, fields)
                response = util.submit_form(self.br)
                html = response.read()
                url = response.geturl()
                if self.DEBUG:
                    print "Html obtained from dates url:", html
                result2 = self.get_detail(html, url, self.scrape_data_block, self.scrape_min_dates, self.scrape_optional_dates)
                if result2:
                    result.update(result2)
            except:
                pass  
            try:
                fields = { '__EVENTTARGET': self.names_tab, '__EVENTARGUMENT': ''}
                util.setup_form(self.br, self.search_form, fields)
                response = util.submit_form(self.br)
                #response = self.br.follow_link(text=self.names_link)
                html = response.read()
                url = response.geturl()
                if self.DEBUG:
                    print "Html obtained from names url:", html
                result3 = self.get_detail(html, url, self.scrape_data_block, self.scrape_min_names, self.scrape_optional_names)
                if result3:
                    result.update(result3)
            except:
                pass  
        return result

class SouthHamsScraper(SWDevonScraper):

    search_url = 'http://apps.southhams.gov.uk/planningSearch/default.aspx'
    applic_url = 'http://apps.southhams.gov.uk/planningSearch/default.aspx?shortid='

class WestDevonScraper(SWDevonScraper):

    search_url = 'http://apps.westdevon.gov.uk/planningSearch/default.aspx'
    applic_url = 'http://apps.westdevon.gov.uk/planningsearch/default.aspx?shortid='

if __name__ == 'scraper':

    #scraper = SouthHamsScraper('SouthHams')
    #scraper.replace_all_with('south_hams_planning_applications')
    #scraper = WestDevonScraper('WestDevon')
    #scraper.replace_all_with('west_devon_planning_applications')
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
    #scraper = SouthHamsScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('2036/11/F')
    #print scraper.get_detail_from_uid ('0770/11/F') # SouthHams
    #scraper = WestDevonScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('03187/2012') # WestDevon
    
    #res = scraper.get_id_batch(util.get_dt('17/02/2011'), util.get_dt('19/02/2011'))
    #print res, len(res)
    #print scraper.get_id_batch(util.get_dt('23/03/2012'), util.get_dt('25/03/2012'))

# this is a scraper of South Hams and West Devon planning applications for use by Openly Local

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

systems = {
    'SouthHams': 'SouthHamsScraper',
    'WestDevon': 'WestDevonScraper',
     }

class SWDevonScraper(base.DateScraper):

    MAX_ID_BATCH = 200 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 150 # max application details to scrape in one go

    advanced_tab = 'ctl00$BodyContent$tab2'
    date_from_field = {
        'day': 'ctl00$BodyContent$start_date_day',
        'month': 'ctl00$BodyContent$start_date_month',
        'year': 'ctl00$BodyContent$start_date_year',
        }
    date_to_field = {
        'day': 'ctl00$BodyContent$end_date_day',
        'month': 'ctl00$BodyContent$end_date_month',
        'year': 'ctl00$BodyContent$end_date_year',
        }
    request_date_format = '%-d/%-m/%Y'
    search_form = '0'
    scrape_ids = """
    <fieldset title="Search Results">
    {* <div class="resultItemAdvanced">
    <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a>
    </div *}
    </fieldset>
    """
    scrape_next = '<input type="submit" name="{{ next_submit }}" value="Next">'
    dates_tab = 'ctl00$BodyContent$sub3'
    names_tab = 'ctl00$BodyContent$sub4'
    scrape_data_block = """
    <div id="divContent"> {{ block|html }} </div>
    """
    scrape_min_data = """
    <span id="BodyContent_lblNumber1"> {{ reference }} </span>
    <div id="BodyContent_basicDescriptionData"> {{ description }} </div>
    <div id="BodyContent_basicAddressData"> {{ address }} </div>
    """
    scrape_min_names = """
    <div id="BodyContent_basicApplicantNameData"> {{ applicant_name }} </div>
    """
    scrape_min_dates = """
    <div id="BodyContent_basicDateReceivedData"> {{ date_received }} </div>
    <div id="BodyContent_basicDateRegisteredData"> {{ date_validated }} </div>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<div id="BodyContent_basicDecisionData"> {{ decision }} </div>',
    '<div id="BodyContent_basicDecisionDateData"> {{ decision_date }} </div>',
    '<div id="BodyContent_basicCaseOfficerData"> {{ case_officer }} </div>',
    ]
    scrape_optional_dates = [
    '<div id="BodyContent_basicDateTargetData"> {{ target_decision_date }} </div>',
    '<div id="BodyContent_basicDateCommentsData"> {{ comment_date }} </div>',
    '<div id="BodyContent_basicDateDecisionData"> {{ decision_date }} </div>',
    '<div id="BodyContent_basicDateAdvertData"> {{ last_advertised_date }} </div>',
    ]
    scrape_optional_names = [
    '<div id="BodyContent_basicApplicantAddressData"> {{ applicant_address }} </div>',
    '<div id="BodyContent_basicAgentNameData"> {{ agent_name }} </div>',
    '<div id="BodyContent_basicAgentAddressData"> {{ agent_address }} </div>',
    ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)
        if self.DEBUG:
            print "Html obtained from search url:", response.read()

        fields = { '__EVENTTARGET': self.advanced_tab, '__EVENTARGUMENT': '', 'ctl00$BodyContent$btnSimpleSearch': None}
        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br)
        if self.DEBUG:
            print "Html obtained from advanced url:", response.read()

        fields = {}
        date_from = date_from.strftime(self.request_date_format)
        date_parts = date_from.split('/')
        fields [self.date_from_field['day']] = date_parts[0]
        fields [self.date_from_field['month']] = date_parts[1]
        fields [self.date_from_field['year']] = date_parts[2]
        date_to = date_to.strftime(self.request_date_format)
        date_parts = date_to.split('/')
        fields [self.date_to_field['day']] = date_parts[0]
        fields [self.date_to_field['month']] = date_parts[1]
        fields [self.date_to_field['year']] = date_parts[2]

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
                result = scrapemark.scrape(self.scrape_next, html)
                try:
                    next_submit = result['next_submit']
                except:
                    break
                form_ok = util.setup_form(self.br, self.search_form)
                if self.DEBUG: print "form:", self.br.form
                response = util.submit_form(self.br, next_submit)
            else:
                break

        return final_result

    def get_detail_from_uid (self, uid):
        url = self.applic_url + urllib.quote_plus(uid)
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
                #response = self.br.follow_link(text=self.dates_link)
                fields = { '__EVENTTARGET': self.dates_tab, '__EVENTARGUMENT': ''}
                util.setup_form(self.br, self.search_form, fields)
                response = util.submit_form(self.br)
                html = response.read()
                url = response.geturl()
                if self.DEBUG:
                    print "Html obtained from dates url:", html
                result2 = self.get_detail(html, url, self.scrape_data_block, self.scrape_min_dates, self.scrape_optional_dates)
                if result2:
                    result.update(result2)
            except:
                pass  
            try:
                fields = { '__EVENTTARGET': self.names_tab, '__EVENTARGUMENT': ''}
                util.setup_form(self.br, self.search_form, fields)
                response = util.submit_form(self.br)
                #response = self.br.follow_link(text=self.names_link)
                html = response.read()
                url = response.geturl()
                if self.DEBUG:
                    print "Html obtained from names url:", html
                result3 = self.get_detail(html, url, self.scrape_data_block, self.scrape_min_names, self.scrape_optional_names)
                if result3:
                    result.update(result3)
            except:
                pass  
        return result

class SouthHamsScraper(SWDevonScraper):

    search_url = 'http://apps.southhams.gov.uk/planningSearch/default.aspx'
    applic_url = 'http://apps.southhams.gov.uk/planningSearch/default.aspx?shortid='

class WestDevonScraper(SWDevonScraper):

    search_url = 'http://apps.westdevon.gov.uk/planningSearch/default.aspx'
    applic_url = 'http://apps.westdevon.gov.uk/planningsearch/default.aspx?shortid='

if __name__ == 'scraper':

    #scraper = SouthHamsScraper('SouthHams')
    #scraper.replace_all_with('south_hams_planning_applications')
    #scraper = WestDevonScraper('WestDevon')
    #scraper.replace_all_with('west_devon_planning_applications')
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
    #scraper = SouthHamsScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('2036/11/F')
    #print scraper.get_detail_from_uid ('0770/11/F') # SouthHams
    #scraper = WestDevonScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('03187/2012') # WestDevon
    
    #res = scraper.get_id_batch(util.get_dt('17/02/2011'), util.get_dt('19/02/2011'))
    #print res, len(res)
    #print scraper.get_id_batch(util.get_dt('23/03/2012'), util.get_dt('25/03/2012'))

