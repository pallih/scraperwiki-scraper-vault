# this is a scraper of Ceredigion planning applications for use by Openly Local

# also see Stevenage

# currently designed to work backwards collecting applications from the current date to 1/1/2000

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import urllib

base = scraperwiki.utils.swimport("openlylocal_base_scraper")
scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")

class CeredigionScraper(base.DateScraper):

    MAX_ID_BATCH = 300 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go
    HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
    'Accept-Charset': 'UTF-8,*',
    'Accept': 'text/html',
    'Accept-Language': 'en-gb,en',
    }

    date_from_field = 'CTRL:61:_:A'
    date_to_field = 'CTRL:62:_:A'
    appno_field = 'CTRL:49:_:A'
    search_form = 'RW'
    submit_control = 'CTRL:68:_:B'
    next_control = 'CTRL:74:_:K:' 
    detail_control = 'CTRL:75:_:D:0'
    back_control = 'CTRL:126:_'
    request_date_format = '%d/%m/%Y'
    start_url = 'http://forms.ceredigion.gov.uk/ufs/ufsmain?formid=DESH_PLANNING_APPS&LANGUAGE=EN'
    scrape_no_details = '<td> No details were found by this search. {{ no_details }} </td>'
    first_search = True
    scrape_ids = """
    <table title="Search Results"> <tr />
    {* <tr>
    <td> <input value="{{ [records].uid }}"> </td>
    </tr> *}
    </table>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <table summary="GRIDCONTROL1"> {{ block|html }} </table>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <div id="CTID-8-_-A"> {{ reference }} </div>
    <div id="CTID-11-_-A"> {{ description }} </div>
    <div id="CTID-20-_-A"> {{ address }} </div>
    <div id="CTID-25-_-A"> {{ date_received }} </div>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<div id="CTID-26-_-A"> {{ date_validated }} </div>',
    '<div id="CTID-10-_-A"> {{ application_type }} </div>',
    '<div id="CTID-14-_-A"> {{ decision }} </div>',
    '<div id="CTID-16-_-A"> {{ agent_name }} </div>',
    '<div id="CTID-17-_-A"> {{ applicant_name }} </div>',
    '<div id="CTID-21-_-A"> {{ ward_name }} </div>',
    '<div id="CTID-33-_-A"> {{ case_officer }} </div>',
    '<div id="CTID-28-_-A"> {{ meeting_date }} </div>',
    '<div id="CTID-29-_-A"> {{ decision_date }} </div>',
    ]

    def get_id_batch (self, date_from, date_to):

        response = util.open_url(self.br, self.start_url)
        if self.first_search: # launch search facility page with button appears only on first opening of this url
            util.setup_form(self.br)
            response = util.submit_form(self.br)
            self.first_search = False
        if self.DEBUG: print "start page:", response.read()

        fields = {}
        date_from = date_from.strftime(self.request_date_format)
        date_to = date_to.strftime(self.request_date_format)
        fields[self.date_from_field] = date_from
        fields[self.date_to_field] = date_to

        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print "form:", self.br.form
        response = util.submit_form(self.br, self.submit_control)
        
        final_result = []
        while response:
            html = response.read()
            url = response.geturl()
            if self.DEBUG: print "result page:", html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
                try: # has to break out on the last page
                    util.setup_form(self.br, self.search_form)
                    if self.DEBUG: print "form:", self.br.form
                    response = util.submit_form(self.br, self.next_control + str(len(final_result)))
                except:
                    break
            else:
                break

        return final_result

    def get_detail_from_uid (self, uid):
        try:
            response = util.open_url(self.br, self.start_url)
            if self.first_search: # launch search facility page with button appears only on first opening of this url
                util.setup_form(self.br)
                response = util.submit_form(self.br)
                self.first_search = False
            if self.DEBUG: print "start page:", response.read()

            fields = {}
            fields[self.appno_field] = uid
            util.setup_form(self.br, self.search_form, fields)
            if self.DEBUG: print "form:", self.br.form
            response = util.submit_form(self.br, self.submit_control)
            html1 = response.read()
            if self.DEBUG: print "result page:", html1

            util.setup_form(self.br, self.search_form) 
            if self.DEBUG: print "form:", self.br.form
            response = util.submit_form(self.br, self.detail_control)
            html = response.read()
            url = response.geturl()
            if self.DEBUG: print "detail page:", html

            if self.DEBUG: print "OK:", uid
        
        except:
            if self.DEBUG: print "Failed to get details for:", uid
            return None
        return self.get_detail(html, url)

if __name__ == 'scraper':

    scraper = CeredigionScraper() 
    scraper.run()

    # misc tests
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('8/12/0004')
    #print scraper.get_detail_from_uid ('A120299')
    #print scraper.get_detail_from_uid ('A110805')
    #print scraper.get_detail_from_uid ('A110389')
    #res = scraper.get_id_batch(util.get_dt('08/02/2013'), util.get_dt('12/03/2013'))
    #print len(res), res
    #print scraper.gather_ids('2012-02-01')
    #print scraper.gather_ids('2011-02-01', '2012-01-18')
    #print scraper.update_current_applications()
    #scraper.gather_current_ids()
    #scraper.populate_missing_applications()

# this is a scraper of Ceredigion planning applications for use by Openly Local

# also see Stevenage

# currently designed to work backwards collecting applications from the current date to 1/1/2000

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import urllib

base = scraperwiki.utils.swimport("openlylocal_base_scraper")
scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")

class CeredigionScraper(base.DateScraper):

    MAX_ID_BATCH = 300 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go
    HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
    'Accept-Charset': 'UTF-8,*',
    'Accept': 'text/html',
    'Accept-Language': 'en-gb,en',
    }

    date_from_field = 'CTRL:61:_:A'
    date_to_field = 'CTRL:62:_:A'
    appno_field = 'CTRL:49:_:A'
    search_form = 'RW'
    submit_control = 'CTRL:68:_:B'
    next_control = 'CTRL:74:_:K:' 
    detail_control = 'CTRL:75:_:D:0'
    back_control = 'CTRL:126:_'
    request_date_format = '%d/%m/%Y'
    start_url = 'http://forms.ceredigion.gov.uk/ufs/ufsmain?formid=DESH_PLANNING_APPS&LANGUAGE=EN'
    scrape_no_details = '<td> No details were found by this search. {{ no_details }} </td>'
    first_search = True
    scrape_ids = """
    <table title="Search Results"> <tr />
    {* <tr>
    <td> <input value="{{ [records].uid }}"> </td>
    </tr> *}
    </table>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <table summary="GRIDCONTROL1"> {{ block|html }} </table>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <div id="CTID-8-_-A"> {{ reference }} </div>
    <div id="CTID-11-_-A"> {{ description }} </div>
    <div id="CTID-20-_-A"> {{ address }} </div>
    <div id="CTID-25-_-A"> {{ date_received }} </div>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<div id="CTID-26-_-A"> {{ date_validated }} </div>',
    '<div id="CTID-10-_-A"> {{ application_type }} </div>',
    '<div id="CTID-14-_-A"> {{ decision }} </div>',
    '<div id="CTID-16-_-A"> {{ agent_name }} </div>',
    '<div id="CTID-17-_-A"> {{ applicant_name }} </div>',
    '<div id="CTID-21-_-A"> {{ ward_name }} </div>',
    '<div id="CTID-33-_-A"> {{ case_officer }} </div>',
    '<div id="CTID-28-_-A"> {{ meeting_date }} </div>',
    '<div id="CTID-29-_-A"> {{ decision_date }} </div>',
    ]

    def get_id_batch (self, date_from, date_to):

        response = util.open_url(self.br, self.start_url)
        if self.first_search: # launch search facility page with button appears only on first opening of this url
            util.setup_form(self.br)
            response = util.submit_form(self.br)
            self.first_search = False
        if self.DEBUG: print "start page:", response.read()

        fields = {}
        date_from = date_from.strftime(self.request_date_format)
        date_to = date_to.strftime(self.request_date_format)
        fields[self.date_from_field] = date_from
        fields[self.date_to_field] = date_to

        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print "form:", self.br.form
        response = util.submit_form(self.br, self.submit_control)
        
        final_result = []
        while response:
            html = response.read()
            url = response.geturl()
            if self.DEBUG: print "result page:", html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
                try: # has to break out on the last page
                    util.setup_form(self.br, self.search_form)
                    if self.DEBUG: print "form:", self.br.form
                    response = util.submit_form(self.br, self.next_control + str(len(final_result)))
                except:
                    break
            else:
                break

        return final_result

    def get_detail_from_uid (self, uid):
        try:
            response = util.open_url(self.br, self.start_url)
            if self.first_search: # launch search facility page with button appears only on first opening of this url
                util.setup_form(self.br)
                response = util.submit_form(self.br)
                self.first_search = False
            if self.DEBUG: print "start page:", response.read()

            fields = {}
            fields[self.appno_field] = uid
            util.setup_form(self.br, self.search_form, fields)
            if self.DEBUG: print "form:", self.br.form
            response = util.submit_form(self.br, self.submit_control)
            html1 = response.read()
            if self.DEBUG: print "result page:", html1

            util.setup_form(self.br, self.search_form) 
            if self.DEBUG: print "form:", self.br.form
            response = util.submit_form(self.br, self.detail_control)
            html = response.read()
            url = response.geturl()
            if self.DEBUG: print "detail page:", html

            if self.DEBUG: print "OK:", uid
        
        except:
            if self.DEBUG: print "Failed to get details for:", uid
            return None
        return self.get_detail(html, url)

if __name__ == 'scraper':

    scraper = CeredigionScraper() 
    scraper.run()

    # misc tests
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('8/12/0004')
    #print scraper.get_detail_from_uid ('A120299')
    #print scraper.get_detail_from_uid ('A110805')
    #print scraper.get_detail_from_uid ('A110389')
    #res = scraper.get_id_batch(util.get_dt('08/02/2013'), util.get_dt('12/03/2013'))
    #print len(res), res
    #print scraper.gather_ids('2012-02-01')
    #print scraper.gather_ids('2011-02-01', '2012-01-18')
    #print scraper.update_current_applications()
    #scraper.gather_current_ids()
    #scraper.populate_missing_applications()

