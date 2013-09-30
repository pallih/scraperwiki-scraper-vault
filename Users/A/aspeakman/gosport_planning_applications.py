# this is a scraper of Gosport planning applications for use by Openly Local

# note this is a weird system where you ask for a single date and it returns applications submitted "on or close to that date"
# seems to be a 20 day window around the specified date

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import random
import urllib

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

class GosportScraper(base.PeriodScraper):

    START_SEQUENCE = '2003-10-01'
    MAX_ID_BATCH = 350 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 250 # max application details to scrape in one go
    PERIOD_TYPE = '-20' # 20 days ending on the specified date

    search_url = 'http://www.gosport.gov.uk/gbcplanning/ApplicationSearch2.aspx'
    applic_url = 'http://www.gosport.gov.uk/gbcplanning/ApplicationDetails.aspx?ID='
    date_field = 'ApplicationSearch21:tbDateSubmitted'
    request_date_format = '%d/%m/%Y'
    search_form = 'Form1'
    search_submit = 'ApplicationSearch21:btnDateSubmitted'
    scrape_ids = """
    <table id="SearchResults1_dgSearchResults"> <tr />
    {* <tr>
    <td> {{ [records].uid }} </td>
    </tr> *}
    </table>
    """
    scrape_data_block = """
    <div class="PageTitle" /> {{ block|html }} <div class="NormalBody" />
    """
    scrape_min_data = """
    <span id="ApplicationDetails1_lbApplicationRef"> {{ reference }} </span>
    <span id="ApplicationDetails1_lbSiteAddress"> {{ address }} </span>
    <span id="ApplicationDetails1_lbProposalDescription"> {{ description }} </span>
    <span id="ApplicationDetails1_lbRegistrationDate"> {{ date_validated }} </span>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<span id="ApplicationDetails1_lbApplicationType"> {{ application_type }} </span>',
    '<span id="ApplicationDetails1_lbCaseOfficerName"> {{ case_officer }} </span>',
    '<span id="ApplicationDetails1_lbDecision"> {{ decision }} </span>',
    '<span id="ApplicationDetails1_lbDecisionDate"> {{ decision_date }} </span>',
    '<span id="ApplicationDetails1_lbApplicant"> {{ applicant_name }} <br> {{ applicant_address }} </span>',
    '<span id="ApplicationDetails1_lbAgent"> {{ agent_name }} <br> {{ agent_address }} </span>',
    '<span id="ApplicationDetails1_lblComments"> {{ comment_date }} </span>',
    '<span id="ApplicationDetails1_lbApplicationStatus"> {{ status }} </span>',
    ]

    def get_id_period (self, date):

        target_date = date + timedelta(days=10)

        from_iso_dt, to_iso_dt = util.inc_dt(target_date.strftime(util.ISO8601_DATE), util.ISO8601_DATE, self.PERIOD_TYPE)
        from_dt = util.get_dt(from_iso_dt, util.ISO8601_DATE)
        to_dt = util.get_dt(to_iso_dt, util.ISO8601_DATE)

        response = self.br.open(self.search_url)

        fields = { self.date_field: date.strftime(self.request_date_format) }
        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br, self.search_submit)

        final_result = []
        if response:
            html = response.read()
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                for rec in result['records']:
                    rec['url'] = self.applic_url + urllib.quote_plus(rec['uid'])
                self.clean_ids(result['records'])
                final_result.extend(result['records'])

        if len (final_result) > 0:
            return final_result, from_dt, to_dt 
        else:
            return [], None, None   # note 20 day result assumed never to be legitimately empty

    def get_detail_from_uid (self, uid):
        url = self.applic_url + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    scraper = GosportScraper()
    scraper.run()

    # misc test calls
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('A14639/3')
    #result, dt1, dt2 = scraper.get_id_period(util.get_dt('11/08/2012'))
    #print len(result), result, dt1, dt2
    

    





# this is a scraper of Gosport planning applications for use by Openly Local

# note this is a weird system where you ask for a single date and it returns applications submitted "on or close to that date"
# seems to be a 20 day window around the specified date

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import random
import urllib

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

class GosportScraper(base.PeriodScraper):

    START_SEQUENCE = '2003-10-01'
    MAX_ID_BATCH = 350 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 250 # max application details to scrape in one go
    PERIOD_TYPE = '-20' # 20 days ending on the specified date

    search_url = 'http://www.gosport.gov.uk/gbcplanning/ApplicationSearch2.aspx'
    applic_url = 'http://www.gosport.gov.uk/gbcplanning/ApplicationDetails.aspx?ID='
    date_field = 'ApplicationSearch21:tbDateSubmitted'
    request_date_format = '%d/%m/%Y'
    search_form = 'Form1'
    search_submit = 'ApplicationSearch21:btnDateSubmitted'
    scrape_ids = """
    <table id="SearchResults1_dgSearchResults"> <tr />
    {* <tr>
    <td> {{ [records].uid }} </td>
    </tr> *}
    </table>
    """
    scrape_data_block = """
    <div class="PageTitle" /> {{ block|html }} <div class="NormalBody" />
    """
    scrape_min_data = """
    <span id="ApplicationDetails1_lbApplicationRef"> {{ reference }} </span>
    <span id="ApplicationDetails1_lbSiteAddress"> {{ address }} </span>
    <span id="ApplicationDetails1_lbProposalDescription"> {{ description }} </span>
    <span id="ApplicationDetails1_lbRegistrationDate"> {{ date_validated }} </span>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<span id="ApplicationDetails1_lbApplicationType"> {{ application_type }} </span>',
    '<span id="ApplicationDetails1_lbCaseOfficerName"> {{ case_officer }} </span>',
    '<span id="ApplicationDetails1_lbDecision"> {{ decision }} </span>',
    '<span id="ApplicationDetails1_lbDecisionDate"> {{ decision_date }} </span>',
    '<span id="ApplicationDetails1_lbApplicant"> {{ applicant_name }} <br> {{ applicant_address }} </span>',
    '<span id="ApplicationDetails1_lbAgent"> {{ agent_name }} <br> {{ agent_address }} </span>',
    '<span id="ApplicationDetails1_lblComments"> {{ comment_date }} </span>',
    '<span id="ApplicationDetails1_lbApplicationStatus"> {{ status }} </span>',
    ]

    def get_id_period (self, date):

        target_date = date + timedelta(days=10)

        from_iso_dt, to_iso_dt = util.inc_dt(target_date.strftime(util.ISO8601_DATE), util.ISO8601_DATE, self.PERIOD_TYPE)
        from_dt = util.get_dt(from_iso_dt, util.ISO8601_DATE)
        to_dt = util.get_dt(to_iso_dt, util.ISO8601_DATE)

        response = self.br.open(self.search_url)

        fields = { self.date_field: date.strftime(self.request_date_format) }
        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br, self.search_submit)

        final_result = []
        if response:
            html = response.read()
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                for rec in result['records']:
                    rec['url'] = self.applic_url + urllib.quote_plus(rec['uid'])
                self.clean_ids(result['records'])
                final_result.extend(result['records'])

        if len (final_result) > 0:
            return final_result, from_dt, to_dt 
        else:
            return [], None, None   # note 20 day result assumed never to be legitimately empty

    def get_detail_from_uid (self, uid):
        url = self.applic_url + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    scraper = GosportScraper()
    scraper.run()

    # misc test calls
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('A14639/3')
    #result, dt1, dt2 = scraper.get_id_period(util.get_dt('11/08/2012'))
    #print len(result), result, dt1, dt2
    

    





