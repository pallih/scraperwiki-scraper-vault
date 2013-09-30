# this is a scraper for two authorities using E-Access systems

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
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

systems = {
    'MalvernHills': 'MalvernHillsScraper',
    'Tandridge': 'TandridgeScraper',
     }

class EAccessScraper(base.DateScraper):

    MAX_ID_BATCH = 200 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 150 # max application details to scrape in one go

    date_from_field = 'DateValidFrom'
    date_to_field = 'DateValidTo'
    ref_field = 'AppNo'
    request_date_format = '%-d/%-m/%Y'
    search_form = 'f2'
    applic_form = 'NumberSearch'
    applic_fields = { 'exactmatch': '1' }
    from_exclusive = True
    detail_form = 'form1'
    date_type = 'date_validated'

    scrape_ids = """
    <table class="MISresults"> <tr />
    {* <tr>
    <td /> <td> {{ [records].uid }} </td>
    <td> {{ [records].address }} </td> <td> {{ [records].description }} </td>
    </tr> *}
    </table>
    """

    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = '<p class="MISheader"> Planning Application Summary </p> <table> {{ block|html }} </table>'
    # the minimum acceptable valid dataset on the details page
    scrape_min_data = """
    <tr> <td> Decision </td> <td> {{ decision }} </td> </tr>
    <tr> <td> Decision date </td> <td> {{ decision_date }} </td> </tr>
    """
    # other optional parameters that can appear on the details page
    scrape_optional_data = [
    "<tr> <td> Type of application </td> <td> {{ application_type }} </td> </tr>",
    "<tr> <td> Appeal decision </td> <td> {{ appeal_result }} </td> </tr>",
    "<tr> <td> Appeal date </td> <td> {{ appeal_date }} </td> </tr>",
    "<tr> <td> Parish </td> <td> {{ parish }} </td> </tr>",
    "<tr> <td> Planning Portal Ref </td> <td> {{ planning_portal_id }} </td> </tr>",
    "<tr> <td> Ward </td> <td> {{ ward_name }} </td> </tr>",
    "<tr> <td> Officer Name </td> <td> {{ case_officer }} </td> </tr>",
    "<tr> <td> Type of development </td> <td> {{ development_type }} </td> </tr>",
    ]

    # no dates in result, so we search one day at a time and add the dates on each iteration
    def get_id_batch (self, date_from, date_to):

        this_dt = date_from
        final_result = []

        while this_dt <= date_to:

            response = self.br.open(self.search_url)
            fields = {}
            from_dt = this_dt
            if self.from_exclusive:
                from_dt = from_dt - timedelta(days=1) # from date is exclusive
            fields[self.date_from_field] = from_dt.strftime(self.request_date_format)
            fields[self.date_to_field] = this_dt.strftime(self.request_date_format)
            util.setup_form(self.br, self.search_form, fields)
            if self.DEBUG: print self.br.form
            response = util.submit_form(self.br)
            if response:
                html = response.read()
                url = response.geturl()
                if self.DEBUG: print html
                result = scrapemark.scrape(self.scrape_ids, html, url)
                if result and result.get('records'):
                    for rec in result['records']:
                        rec[self.date_type] = fields[self.date_to_field]
                    self.clean_ids(result['records'])
                    final_result.extend(result['records'])

            this_dt += timedelta(days=1)

        return final_result

    def get_detail_from_uid (self, uid):
        response = self.br.open(self.applic_url)
        fields = self.applic_fields
        fields[self.ref_field] = uid
        util.setup_form(self.br, self.applic_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br)
        try:
            util.setup_form(self.br, self.detail_form)
            response = util.submit_form(self.br)
            html = response.read()
            if self.DEBUG: print html
            url = response.geturl()
        except:
            return None
        return self.get_detail(html, url)


class MalvernHillsScraper(EAccessScraper):

    search_url = 'http://e-access.malvernhills.gov.uk/eaccess/Applicationsearch.asp'
    applic_url = 'http://e-access.malvernhills.gov.uk/eaccess/Applicationsearch.asp'
    from_exclusive = True
    date_type = 'date_received'
    scrape_ids = """
    <table class="MISresults"> <tr />
    {* <tr>
    <td /> <td> {{ [records].uid }} </td>
    <td> {{ [records].address }} </td> <td> {{ [records].description }} </td>
    </tr> *}
    </table>
    """

class TandridgeScraper(EAccessScraper):

    search_url = 'http://planning.tandridge.gov.uk/eaccess/weeklylist.asp'
    applic_url = 'http://planning.tandridge.gov.uk/eaccess/Applicationsearch.asp'
    from_exclusive = False
    date_type = 'date_validated'
    scrape_ids = """
    <table class="MISresults"> <tr />
    {* <tr>
    <td /> <td> {{ [records].uid }} </td>
    <td> {{ [records].description }} </td> <td> {{ [records].address }} </td>
    </tr> *}
    </table>
    """

if __name__ == 'scraper':

    #scraper = MalvernHillsScraper('MalvernHills')
    #scraper.run()
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
    #scraper = MalvernHillsScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/01041/TPA') # MalvernHills
    #scraper = TandridgeScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('2011/1062') # Tandridge
    
    #res = scraper.get_id_batch(util.get_dt('06/08/2011'), util.get_dt('09/08/2011'))
    #print res, len(res)
    #print scraper.get_id_batch(util.get_dt('23/03/2012'), util.get_dt('25/03/2012'))


    

# this is a scraper for two authorities using E-Access systems

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
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

systems = {
    'MalvernHills': 'MalvernHillsScraper',
    'Tandridge': 'TandridgeScraper',
     }

class EAccessScraper(base.DateScraper):

    MAX_ID_BATCH = 200 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 150 # max application details to scrape in one go

    date_from_field = 'DateValidFrom'
    date_to_field = 'DateValidTo'
    ref_field = 'AppNo'
    request_date_format = '%-d/%-m/%Y'
    search_form = 'f2'
    applic_form = 'NumberSearch'
    applic_fields = { 'exactmatch': '1' }
    from_exclusive = True
    detail_form = 'form1'
    date_type = 'date_validated'

    scrape_ids = """
    <table class="MISresults"> <tr />
    {* <tr>
    <td /> <td> {{ [records].uid }} </td>
    <td> {{ [records].address }} </td> <td> {{ [records].description }} </td>
    </tr> *}
    </table>
    """

    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = '<p class="MISheader"> Planning Application Summary </p> <table> {{ block|html }} </table>'
    # the minimum acceptable valid dataset on the details page
    scrape_min_data = """
    <tr> <td> Decision </td> <td> {{ decision }} </td> </tr>
    <tr> <td> Decision date </td> <td> {{ decision_date }} </td> </tr>
    """
    # other optional parameters that can appear on the details page
    scrape_optional_data = [
    "<tr> <td> Type of application </td> <td> {{ application_type }} </td> </tr>",
    "<tr> <td> Appeal decision </td> <td> {{ appeal_result }} </td> </tr>",
    "<tr> <td> Appeal date </td> <td> {{ appeal_date }} </td> </tr>",
    "<tr> <td> Parish </td> <td> {{ parish }} </td> </tr>",
    "<tr> <td> Planning Portal Ref </td> <td> {{ planning_portal_id }} </td> </tr>",
    "<tr> <td> Ward </td> <td> {{ ward_name }} </td> </tr>",
    "<tr> <td> Officer Name </td> <td> {{ case_officer }} </td> </tr>",
    "<tr> <td> Type of development </td> <td> {{ development_type }} </td> </tr>",
    ]

    # no dates in result, so we search one day at a time and add the dates on each iteration
    def get_id_batch (self, date_from, date_to):

        this_dt = date_from
        final_result = []

        while this_dt <= date_to:

            response = self.br.open(self.search_url)
            fields = {}
            from_dt = this_dt
            if self.from_exclusive:
                from_dt = from_dt - timedelta(days=1) # from date is exclusive
            fields[self.date_from_field] = from_dt.strftime(self.request_date_format)
            fields[self.date_to_field] = this_dt.strftime(self.request_date_format)
            util.setup_form(self.br, self.search_form, fields)
            if self.DEBUG: print self.br.form
            response = util.submit_form(self.br)
            if response:
                html = response.read()
                url = response.geturl()
                if self.DEBUG: print html
                result = scrapemark.scrape(self.scrape_ids, html, url)
                if result and result.get('records'):
                    for rec in result['records']:
                        rec[self.date_type] = fields[self.date_to_field]
                    self.clean_ids(result['records'])
                    final_result.extend(result['records'])

            this_dt += timedelta(days=1)

        return final_result

    def get_detail_from_uid (self, uid):
        response = self.br.open(self.applic_url)
        fields = self.applic_fields
        fields[self.ref_field] = uid
        util.setup_form(self.br, self.applic_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br)
        try:
            util.setup_form(self.br, self.detail_form)
            response = util.submit_form(self.br)
            html = response.read()
            if self.DEBUG: print html
            url = response.geturl()
        except:
            return None
        return self.get_detail(html, url)


class MalvernHillsScraper(EAccessScraper):

    search_url = 'http://e-access.malvernhills.gov.uk/eaccess/Applicationsearch.asp'
    applic_url = 'http://e-access.malvernhills.gov.uk/eaccess/Applicationsearch.asp'
    from_exclusive = True
    date_type = 'date_received'
    scrape_ids = """
    <table class="MISresults"> <tr />
    {* <tr>
    <td /> <td> {{ [records].uid }} </td>
    <td> {{ [records].address }} </td> <td> {{ [records].description }} </td>
    </tr> *}
    </table>
    """

class TandridgeScraper(EAccessScraper):

    search_url = 'http://planning.tandridge.gov.uk/eaccess/weeklylist.asp'
    applic_url = 'http://planning.tandridge.gov.uk/eaccess/Applicationsearch.asp'
    from_exclusive = False
    date_type = 'date_validated'
    scrape_ids = """
    <table class="MISresults"> <tr />
    {* <tr>
    <td /> <td> {{ [records].uid }} </td>
    <td> {{ [records].description }} </td> <td> {{ [records].address }} </td>
    </tr> *}
    </table>
    """

if __name__ == 'scraper':

    #scraper = MalvernHillsScraper('MalvernHills')
    #scraper.run()
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
    #scraper = MalvernHillsScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/01041/TPA') # MalvernHills
    #scraper = TandridgeScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('2011/1062') # Tandridge
    
    #res = scraper.get_id_batch(util.get_dt('06/08/2011'), util.get_dt('09/08/2011'))
    #print res, len(res)
    #print scraper.get_id_batch(util.get_dt('23/03/2012'), util.get_dt('25/03/2012'))


    

