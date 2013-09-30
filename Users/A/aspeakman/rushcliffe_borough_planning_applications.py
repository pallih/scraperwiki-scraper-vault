# this is a scraper of Rushcliffe planning applications for use by Openly Local

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

class RushcliffeScraper(base.DateScraper):

    #ID_ORDER = 'uid desc'
    ID_ORDER = "CASE uid WHEN substr(uid, 1, 2) < '50' THEN '20' || uid ELSE '19' || uid END desc"
    BATCH_DAYS = 10 # batch size for each scrape - note max 100 returned so reduce days
    date_from_field = 'advDaten3'
    date_to_field = 'advDaten4'
    search_form = 'advDate'
    search_fields = { 'Apps': 'Rec', 'advDaten3': 'Rec', 'AppType': 'DC', 'locality': 'All', 'street': 'All streets'}
    search_url = 'http://www.document1.co.uk/blueprint/AdvSearch.asp'
    accept = "I have read and accept the copyright notice and disclaimer - please select this link to view the plans that match your search results"
    next_link = "Next"
    ref_form = '0'
    ref_field = 'appNumSearchn1'
    scrape_ids = """
    <h2> Search Results </h2> <div>
    {* <ul> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </ul>
    *}
    </div>
    """

    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="innercolumn"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <h2> Application number: {{ reference }} </h2> 
    <li> <strong> Date received </strong> {{ date_received }} </li>
    <li> <strong> Date registered </strong> {{ date_validated }} </li>
    <li> <strong> Address of proposal </strong> {{ address }} <br /> </li>
    <li> <strong> Proposal </strong> {{ description }} </li>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<li> <strong> Type of application </strong> {{ application_type }} </li>',
    '<h3> agent details </h3> <li> <strong> Type of application </strong> {{ application_type }} </li>',
    '<li> <strong> Date neighbours consulted </strong> {{ neighbour_consultation_start_date }} </li>',
    """<li> <strong> Decision </strong> {{ decision }} </li>
    <li> <strong> Date of decision </strong> {{ decision_date }} </li>""",
    '<li> <strong> Case officer </strong> {{ case_officer }} </li>',
    '<li> <strong> Parish </strong> {{ parish }} </li>',
    '<li> <strong> Ward </strong> {{ ward_name }} ( <a /> ) </li>',
    '<li> <strong> OS map references </strong> Easting {{ easting }}; Northing {{ northing }}; Map {{ os_grid_ref }} </li>',
    '<li> <strong> Name of applicant </strong> {{ applicant_name }} </li>',
    '<li> <strong> Address of applicant </strong> {{ applicant_address }} </li>',
    '<li> <strong> Name of agent </strong> {{ agent_name }} </li>',
    '<li> <strong> Address of agent </strong> {{ agent_address }} </li>',
    '<li> <strong> Current status </strong> {{ status }} </li>',
    '<li> <strong> Consultation period expected to end </strong> {{ consultation_end_date }} </li>',
    '<a href="{{ comment_url|abs }}"> <img src="graphics/comments.gif"> </a>'
    ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)

        self.search_fields[self.date_from_field] = date_from.strftime(self.request_date_format)
        self.search_fields[self.date_to_field] = date_to.strftime(self.request_date_format)
        util.setup_form(self.br, self.search_form, self.search_fields )
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br)

        if self.DEBUG: print "accept page:", response.read()
        response = self.br.follow_link(text=self.accept)
        
        #print html
        #sys.exit()
        #try:
        #    result = scrapemark.scrape(self.scrape_max, html)
        #    max_recs = int(result['max_recs'])
        #except:
        #    max_recs = 0
        #if self.DEBUG: print "max recs:", max_recs

        final_result = []
        while response:
            html = response.read()
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            try:
                response = self.br.follow_link(text=self.next_link)
            except:
                break
        return final_result

    def get_detail_from_uid (self, uid):

        try:
            response = self.br.open(self.search_url)

            fields = { self.ref_field: uid }
            util.setup_form(self.br, self.ref_form, fields )
            if self.DEBUG: print self.br.form
            response = util.submit_form(self.br)
    
            if self.DEBUG: print "accept page:", response.read()
            response = self.br.follow_link(text=self.accept)
            html = response.read()
            url = response.geturl()

            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                return self.get_detail_from_url(result['records'][0]['url'])
            else:
                return None
        except:
            if self.DEBUG: raise
            else: return None

if __name__ == 'scraper':

    scraper = RushcliffeScraper()
    #scraper.clear_all()
    scraper.run()

    #scraper.DEBUG = True

    # misc test calls
    #print scraper.get_detail_from_uid ('12/01622/FUL')
    #print scraper.get_detail_from_uid ('13/00407/FUL')
    #result = scraper.get_id_batch(util.get_dt('08/10/2012'), util.get_dt('10/10/2012'))
    #print len(result), result
    #print scraper.get_id_batch(util.get_dt('23/03/2012'), util.get_dt('25/03/2012'))


# this is a scraper of Rushcliffe planning applications for use by Openly Local

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

class RushcliffeScraper(base.DateScraper):

    #ID_ORDER = 'uid desc'
    ID_ORDER = "CASE uid WHEN substr(uid, 1, 2) < '50' THEN '20' || uid ELSE '19' || uid END desc"
    BATCH_DAYS = 10 # batch size for each scrape - note max 100 returned so reduce days
    date_from_field = 'advDaten3'
    date_to_field = 'advDaten4'
    search_form = 'advDate'
    search_fields = { 'Apps': 'Rec', 'advDaten3': 'Rec', 'AppType': 'DC', 'locality': 'All', 'street': 'All streets'}
    search_url = 'http://www.document1.co.uk/blueprint/AdvSearch.asp'
    accept = "I have read and accept the copyright notice and disclaimer - please select this link to view the plans that match your search results"
    next_link = "Next"
    ref_form = '0'
    ref_field = 'appNumSearchn1'
    scrape_ids = """
    <h2> Search Results </h2> <div>
    {* <ul> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </ul>
    *}
    </div>
    """

    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="innercolumn"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <h2> Application number: {{ reference }} </h2> 
    <li> <strong> Date received </strong> {{ date_received }} </li>
    <li> <strong> Date registered </strong> {{ date_validated }} </li>
    <li> <strong> Address of proposal </strong> {{ address }} <br /> </li>
    <li> <strong> Proposal </strong> {{ description }} </li>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<li> <strong> Type of application </strong> {{ application_type }} </li>',
    '<h3> agent details </h3> <li> <strong> Type of application </strong> {{ application_type }} </li>',
    '<li> <strong> Date neighbours consulted </strong> {{ neighbour_consultation_start_date }} </li>',
    """<li> <strong> Decision </strong> {{ decision }} </li>
    <li> <strong> Date of decision </strong> {{ decision_date }} </li>""",
    '<li> <strong> Case officer </strong> {{ case_officer }} </li>',
    '<li> <strong> Parish </strong> {{ parish }} </li>',
    '<li> <strong> Ward </strong> {{ ward_name }} ( <a /> ) </li>',
    '<li> <strong> OS map references </strong> Easting {{ easting }}; Northing {{ northing }}; Map {{ os_grid_ref }} </li>',
    '<li> <strong> Name of applicant </strong> {{ applicant_name }} </li>',
    '<li> <strong> Address of applicant </strong> {{ applicant_address }} </li>',
    '<li> <strong> Name of agent </strong> {{ agent_name }} </li>',
    '<li> <strong> Address of agent </strong> {{ agent_address }} </li>',
    '<li> <strong> Current status </strong> {{ status }} </li>',
    '<li> <strong> Consultation period expected to end </strong> {{ consultation_end_date }} </li>',
    '<a href="{{ comment_url|abs }}"> <img src="graphics/comments.gif"> </a>'
    ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)

        self.search_fields[self.date_from_field] = date_from.strftime(self.request_date_format)
        self.search_fields[self.date_to_field] = date_to.strftime(self.request_date_format)
        util.setup_form(self.br, self.search_form, self.search_fields )
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br)

        if self.DEBUG: print "accept page:", response.read()
        response = self.br.follow_link(text=self.accept)
        
        #print html
        #sys.exit()
        #try:
        #    result = scrapemark.scrape(self.scrape_max, html)
        #    max_recs = int(result['max_recs'])
        #except:
        #    max_recs = 0
        #if self.DEBUG: print "max recs:", max_recs

        final_result = []
        while response:
            html = response.read()
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            try:
                response = self.br.follow_link(text=self.next_link)
            except:
                break
        return final_result

    def get_detail_from_uid (self, uid):

        try:
            response = self.br.open(self.search_url)

            fields = { self.ref_field: uid }
            util.setup_form(self.br, self.ref_form, fields )
            if self.DEBUG: print self.br.form
            response = util.submit_form(self.br)
    
            if self.DEBUG: print "accept page:", response.read()
            response = self.br.follow_link(text=self.accept)
            html = response.read()
            url = response.geturl()

            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                return self.get_detail_from_url(result['records'][0]['url'])
            else:
                return None
        except:
            if self.DEBUG: raise
            else: return None

if __name__ == 'scraper':

    scraper = RushcliffeScraper()
    #scraper.clear_all()
    scraper.run()

    #scraper.DEBUG = True

    # misc test calls
    #print scraper.get_detail_from_uid ('12/01622/FUL')
    #print scraper.get_detail_from_uid ('13/00407/FUL')
    #result = scraper.get_id_batch(util.get_dt('08/10/2012'), util.get_dt('10/10/2012'))
    #print len(result), result
    #print scraper.get_id_batch(util.get_dt('23/03/2012'), util.get_dt('25/03/2012'))


