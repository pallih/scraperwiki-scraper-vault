# this is a scraper of Weymouth planning applications for use by Openly Local

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import urllib
import sys

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

class WeymouthScraper(base.PeriodScraper):

    MAX_ID_BATCH = 250 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go
    PERIOD_TYPE = 'Year'
    ID_ORDER = 'uid desc'

    search_form = '0'
    search_url = 'http://webapps-wpbc.dorsetforyou.com/apps/development/Planregister.asp' 
    applic_url = 'http://webapps-wpbc.dorsetforyou.com/apps/development/Planregister.asp'
    scrape_ids = """
    <table class="datatablesimple">
    {* <tr> <th> Application No. {{ [records].uid }} </th> </tr> *}
    </table>
    """
    # captures HTML blocks encompassing all fields to be gathered
    scrape_sub_blocks = """
    {* <div class="tabbox"> {{ [blocks].block|html }} </div> *}
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <tag> {{ block|html }} </tag>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <input onclick="window.open('{{ url }}','mywindow','toolbar=yes,location=yes,directories=yes,status=yes,menubar=yes,scrollbars=yes,copyhistory=yes,resizable=yes')">
    <tr> <th> Application Reference </th> <td> {{ reference }} </td> </tr>
    <tr> <th> Property Address </th> <td> {{ address }} </td> </tr>
    <tr> <th> Proposal </th> <td> {{ description }} </td> </tr>
    <tr> <th> Date Valid </th> <td> {{ date_validated }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr> <th> Application Type </t> <td> {{ application_type }} </td> </tr>',
    '<tr> <th> Status </th> <td> {{ status }} </td> </tr>',
    '<tr> <th> Case Officer </th> <td> {{ case_officer }} </td> </tr>',
    '<tr> <th> Decision Type </th> <td> {{ decided_by }} </td> </tr>',
    '<input name="easting" value="{{ easting }}"><input name="northing" value="{{ northing }}">',
    # on separate page(s)
    '<tr> <th> Applicant Name </th> <td> {{ applicant_name }} </td> </tr>',
    '<tr> <th> Applicant Address </th> <td> {{ applicant_address|html }} </td> </tr>',
    '<tr> <th> Agent Name </th> <td> {{ agent_name }} </td> </tr>',
    '<tr> <th> Agent Address </th> <td> {{ agent_address|html }} </td> </tr>',
    '<tr> <th> Date Consultation Expires </th> <td> {{ consultation_end_date }} </td> </tr>',
    """<tr> <th> Decision </th> <td> {{ decision }} </td> </tr>
    <tr> <th> Date of Decision </th> <td> {{ decision_date }} </td> </tr>""",
    ]

    def get_id_period (self, this_date):

        from_dt = date(this_date.year, 1, 1)
        to_dt = date(this_date.year, 12, 31)

        response = self.br.open(self.search_url)
        if self.DEBUG: print response.read()

        fields = {}
        fields ['year'] = str(this_date.year)
        form_ok = util.setup_form(self.br, self.search_form, fields )
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br)

        final_result = []
        if response:
            html = response.read()
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
        
        if final_result:
            return final_result, from_dt, to_dt
        else:
            return [], None, None # yearly scraper - so empty result is always invalid

    def get_detail_from_uid (self, uid):

        try:
            fields = { 'count': '1', 'formaction': 'step2', 'btnsubmit': 'Details', 'refval': uid }
            response = util.open_url(self.br, self.applic_url, fields)
            html1 = response.read()
            url = response.geturl()
            if self.DEBUG: print html1

            fields = { 'count': '2', 'formaction': 'step2', 'btnsubmit': 'Dates', 'refval': uid }
            response = util.open_url(self.br, self.applic_url, fields)
            html2 = response.read()
            if self.DEBUG: print html2

            fields = { 'count': '3', 'formaction': 'step2', 'btnsubmit': 'Applicant', 'refval': uid }
            response = util.open_url(self.br, self.applic_url, fields)
            html3 = response.read()
            if self.DEBUG: print html3

            fields = { 'count': '4', 'formaction': 'step2', 'btnsubmit': 'Agent', 'refval': uid }
            response = util.open_url(self.br, self.applic_url, fields)
            html4 = response.read()
            if self.DEBUG: print html4

            data_block = ''
            result = scrapemark.scrape(self.scrape_sub_blocks, html1+html2+html3+html4)
            if result and result.get('blocks'):
                if self.DEBUG: print result['blocks']
                for b in result['blocks']:
                    data_block += " " + b['block']
            if self.DEBUG: print data_block
            
        except:
            if self.DEBUG: raise
            else: return None

        return self.get_detail('<tag>'+data_block+'</tag>', url)

if __name__ == 'scraper':

    #util.replace_vals('swdata', 'url', "'", "", 'prefix', 'yes')

    sys.exit() # no longer working so exit here

    #scraper = WeymouthScraper()
    #scraper.run()

    #scraper.DEBUG = True
    # misc tests
    #print scraper.get_detail_from_uid ('00/00001/LBC')
    #result = scraper.get_id_period(util.get_dt('01/01/2012'))
    #print result
    #print util.inc_dt('2010-02-01', util.ISO8601_DATE, 'Month')
    #print "Found " + str(len(result)) + " ids for Mar 2012"
    #print scraper.gather_ids('2010-02-01')
    #print scraper.gather_ids(None, None)
    #scraper.gather_current_ids()

    #print util.get_local_info(0.838725140673435, 53.479254164473)
    #print util.get_local_info('je3 8hg')


# this is a scraper of Weymouth planning applications for use by Openly Local

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import urllib
import sys

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

class WeymouthScraper(base.PeriodScraper):

    MAX_ID_BATCH = 250 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go
    PERIOD_TYPE = 'Year'
    ID_ORDER = 'uid desc'

    search_form = '0'
    search_url = 'http://webapps-wpbc.dorsetforyou.com/apps/development/Planregister.asp' 
    applic_url = 'http://webapps-wpbc.dorsetforyou.com/apps/development/Planregister.asp'
    scrape_ids = """
    <table class="datatablesimple">
    {* <tr> <th> Application No. {{ [records].uid }} </th> </tr> *}
    </table>
    """
    # captures HTML blocks encompassing all fields to be gathered
    scrape_sub_blocks = """
    {* <div class="tabbox"> {{ [blocks].block|html }} </div> *}
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <tag> {{ block|html }} </tag>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <input onclick="window.open('{{ url }}','mywindow','toolbar=yes,location=yes,directories=yes,status=yes,menubar=yes,scrollbars=yes,copyhistory=yes,resizable=yes')">
    <tr> <th> Application Reference </th> <td> {{ reference }} </td> </tr>
    <tr> <th> Property Address </th> <td> {{ address }} </td> </tr>
    <tr> <th> Proposal </th> <td> {{ description }} </td> </tr>
    <tr> <th> Date Valid </th> <td> {{ date_validated }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr> <th> Application Type </t> <td> {{ application_type }} </td> </tr>',
    '<tr> <th> Status </th> <td> {{ status }} </td> </tr>',
    '<tr> <th> Case Officer </th> <td> {{ case_officer }} </td> </tr>',
    '<tr> <th> Decision Type </th> <td> {{ decided_by }} </td> </tr>',
    '<input name="easting" value="{{ easting }}"><input name="northing" value="{{ northing }}">',
    # on separate page(s)
    '<tr> <th> Applicant Name </th> <td> {{ applicant_name }} </td> </tr>',
    '<tr> <th> Applicant Address </th> <td> {{ applicant_address|html }} </td> </tr>',
    '<tr> <th> Agent Name </th> <td> {{ agent_name }} </td> </tr>',
    '<tr> <th> Agent Address </th> <td> {{ agent_address|html }} </td> </tr>',
    '<tr> <th> Date Consultation Expires </th> <td> {{ consultation_end_date }} </td> </tr>',
    """<tr> <th> Decision </th> <td> {{ decision }} </td> </tr>
    <tr> <th> Date of Decision </th> <td> {{ decision_date }} </td> </tr>""",
    ]

    def get_id_period (self, this_date):

        from_dt = date(this_date.year, 1, 1)
        to_dt = date(this_date.year, 12, 31)

        response = self.br.open(self.search_url)
        if self.DEBUG: print response.read()

        fields = {}
        fields ['year'] = str(this_date.year)
        form_ok = util.setup_form(self.br, self.search_form, fields )
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br)

        final_result = []
        if response:
            html = response.read()
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
        
        if final_result:
            return final_result, from_dt, to_dt
        else:
            return [], None, None # yearly scraper - so empty result is always invalid

    def get_detail_from_uid (self, uid):

        try:
            fields = { 'count': '1', 'formaction': 'step2', 'btnsubmit': 'Details', 'refval': uid }
            response = util.open_url(self.br, self.applic_url, fields)
            html1 = response.read()
            url = response.geturl()
            if self.DEBUG: print html1

            fields = { 'count': '2', 'formaction': 'step2', 'btnsubmit': 'Dates', 'refval': uid }
            response = util.open_url(self.br, self.applic_url, fields)
            html2 = response.read()
            if self.DEBUG: print html2

            fields = { 'count': '3', 'formaction': 'step2', 'btnsubmit': 'Applicant', 'refval': uid }
            response = util.open_url(self.br, self.applic_url, fields)
            html3 = response.read()
            if self.DEBUG: print html3

            fields = { 'count': '4', 'formaction': 'step2', 'btnsubmit': 'Agent', 'refval': uid }
            response = util.open_url(self.br, self.applic_url, fields)
            html4 = response.read()
            if self.DEBUG: print html4

            data_block = ''
            result = scrapemark.scrape(self.scrape_sub_blocks, html1+html2+html3+html4)
            if result and result.get('blocks'):
                if self.DEBUG: print result['blocks']
                for b in result['blocks']:
                    data_block += " " + b['block']
            if self.DEBUG: print data_block
            
        except:
            if self.DEBUG: raise
            else: return None

        return self.get_detail('<tag>'+data_block+'</tag>', url)

if __name__ == 'scraper':

    #util.replace_vals('swdata', 'url', "'", "", 'prefix', 'yes')

    sys.exit() # no longer working so exit here

    #scraper = WeymouthScraper()
    #scraper.run()

    #scraper.DEBUG = True
    # misc tests
    #print scraper.get_detail_from_uid ('00/00001/LBC')
    #result = scraper.get_id_period(util.get_dt('01/01/2012'))
    #print result
    #print util.inc_dt('2010-02-01', util.ISO8601_DATE, 'Month')
    #print "Found " + str(len(result)) + " ids for Mar 2012"
    #print scraper.gather_ids('2010-02-01')
    #print scraper.gather_ids(None, None)
    #scraper.gather_current_ids()

    #print util.get_local_info(0.838725140673435, 53.479254164473)
    #print util.get_local_info('je3 8hg')


