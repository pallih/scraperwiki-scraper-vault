# this is a scraper of Burnley planning applications for use by Openly Local

#also see Ribble Valley, Wyre, Rossendale

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

class BurnleyScraper(base.DateScraper):

    #ID_ORDER = 'uid desc'
    ID_ORDER = "substr(uid, 5) desc"

    result_url = 'http://www.burnley.gov.uk/custom/plnapps/index.php'
    search_fields = { 'search': 'search', 'limit': '20' }
    date_from_field = 'from_date2'
    date_to_field = 'to_date2'
    applic_url = 'http://www.burnley.gov.uk/custom/plnapps/results.php'

    scrape_ids = """
    <table id="searchresults"> 
        {* <tr> <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td> </tr> *}
    </table>"""
    scrape_max_recs = '<h3> <strong> {{ max_recs }} </strong> Results for </h3>'
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="contentContainer"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <h1> Application {{ reference }} </h1>
    <tr> <td> Proposal </td> <td> {{ description }} </td> </tr>
    <tr> <td> Development address </td> <td> {{ address }} </td> </tr>
    <tr> <td> Key dates </td> <td> <strong> Valid date </strong> {{ date_validated }} <strong /> </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    #'<p class="first"> <strong> {{ application_type }} </strong> </p>',
    #'<tr> <td> Development address </td> <td> <strong> Ward </strong> : {{ ward_name }} <br /> </td> </tr>',
    #'<tr> <td> Development address </td> <td> <strong> Parish </strong> : {{ parish }} </td> </tr>',
    '<tr> <td> Officer </td> <td> {{ case_officer }} </td> </tr>',
    '<tr> <td> Applicant </td> <td> <strong> {{ applicant_name }} </strong> {{ applicant_address }} </td> </tr>',
    '<tr> <td> Agent </td> <td> <strong> {{ agent_name }}</strong> {{ agent_address }} </td> </tr>',
    #'<tr> <td> Planning Status </td> <td> {{ status }} </td> </tr>',
    '<tr> <td> Decision </td> <td> <strong> {{ decision }} </strong> Decision level: {{ decided_by }} </td> </tr>',
    '<tr> <td> Key dates </td> <td> <strong> Committee </strong> {{ meeting_date }} <strong /> </td> </tr>',
    '<tr> <td> Key dates </td> <td> <strong> Decision date </strong> {{ decision_date }} </td> </tr>',
    '<tr> <td> Key dates </td> <td> <strong> Eight week date </strong> {{ target_decision_date }} <strong /> </td> </tr>',
    '<tr> <td> Key dates </td> <td> <strong> Consultation sent </strong> {{ consultation_start_date }} <strong /> </td> </tr>',
    '<tr> <td> Key dates </td> <td> <strong> Consultation expires </strong> {{ consultation_end_date }} </td> </tr>',
    '<tr> <td> Key dates </td> <td> <strong> Consultation expires </strong> {{ consultation_end_date }} <strong /> </td> </tr>',
    #'<tr> <td> Constraints </td> <td> {{ conditions }} </td> </tr>',
    #'<tr> <td> Last Updated </td> <td> {{ last_updated_date }} </td> </tr>',
    #'<tr> <td> Last Advertised On </td> <td> {{ last_advertised_date }} </td> </tr>',
    #'<tr> <td> Latest Advertisement Expiry </td> <td> {{ latest_advertisement_expiry_date }} </td> </tr>',
    #'<tr> <td> Neighbour Consultation Sent </td> <td> {{ neighbour_consultation_start_date }} </td> </tr>',
    #'<tr> <td> Neighbour Consultation Expiry </td> <td> {{ neighbour_consultation_end_date }} </td> </tr>',
    ]

    def get_id_batch (self, date_from, date_to):

        fields = self.search_fields
        fields[self.date_from_field] = date_from.strftime(self.request_date_format)
        fields[self.date_to_field] = date_to.strftime(self.request_date_format)
        if self.DEBUG: print "fields:", fields
        response = util.open_url(self.br, self.result_url, fields, 'GET')

        html = response.read()
        url = response.geturl()
        if self.DEBUG: print "result page:", html

        try:
            result = scrapemark.scrape(self.scrape_max_recs, html)
            max_recs = int(result['max_recs'])
        except:
            max_recs = 0
        if self.DEBUG: print "max recs:", max_recs
        
        final_result = []
        rec_count = 0
        while response and rec_count <= max_recs:
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
                rec_count += len(result['records'])
                fields['page'] = str(rec_count)
                response = util.open_url(self.br, self.result_url, fields, 'GET')
                html = response.read()
                url = response.geturl()
                if self.DEBUG: print "next page:", html
            else:
                break

        return final_result

    def get_detail_from_uid (self, uid):
        url = self.applic_url + '?ref=' + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    scraper = BurnleyScraper()
    #scraper.reset()
    #scraper.DEBUG = True
    scraper.run()

    # misc tests
    #print scraper.get_detail_from_uid ('APP/2012/0113')
    #print scraper.get_detail_from_uid ('APP/2013/0204')
    #res = scraper.get_id_batch(util.get_dt('06/04/2013'), util.get_dt('25/04/2013'))
    #res = scraper.get_id_batch(util.get_dt('28/06/2012'), date.today())
    #print len(res), res
    #print scraper.gather_ids('2012-02-01')
    #print scraper.gather_ids('2011-02-01', '2012-01-18')
    #print scraper.gather_ids(None, None)
    #scraper.gather_current_ids()

    #util.rename_column('swdata', 'ward', 'ward_name')
# this is a scraper of Burnley planning applications for use by Openly Local

#also see Ribble Valley, Wyre, Rossendale

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

class BurnleyScraper(base.DateScraper):

    #ID_ORDER = 'uid desc'
    ID_ORDER = "substr(uid, 5) desc"

    result_url = 'http://www.burnley.gov.uk/custom/plnapps/index.php'
    search_fields = { 'search': 'search', 'limit': '20' }
    date_from_field = 'from_date2'
    date_to_field = 'to_date2'
    applic_url = 'http://www.burnley.gov.uk/custom/plnapps/results.php'

    scrape_ids = """
    <table id="searchresults"> 
        {* <tr> <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td> </tr> *}
    </table>"""
    scrape_max_recs = '<h3> <strong> {{ max_recs }} </strong> Results for </h3>'
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="contentContainer"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <h1> Application {{ reference }} </h1>
    <tr> <td> Proposal </td> <td> {{ description }} </td> </tr>
    <tr> <td> Development address </td> <td> {{ address }} </td> </tr>
    <tr> <td> Key dates </td> <td> <strong> Valid date </strong> {{ date_validated }} <strong /> </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    #'<p class="first"> <strong> {{ application_type }} </strong> </p>',
    #'<tr> <td> Development address </td> <td> <strong> Ward </strong> : {{ ward_name }} <br /> </td> </tr>',
    #'<tr> <td> Development address </td> <td> <strong> Parish </strong> : {{ parish }} </td> </tr>',
    '<tr> <td> Officer </td> <td> {{ case_officer }} </td> </tr>',
    '<tr> <td> Applicant </td> <td> <strong> {{ applicant_name }} </strong> {{ applicant_address }} </td> </tr>',
    '<tr> <td> Agent </td> <td> <strong> {{ agent_name }}</strong> {{ agent_address }} </td> </tr>',
    #'<tr> <td> Planning Status </td> <td> {{ status }} </td> </tr>',
    '<tr> <td> Decision </td> <td> <strong> {{ decision }} </strong> Decision level: {{ decided_by }} </td> </tr>',
    '<tr> <td> Key dates </td> <td> <strong> Committee </strong> {{ meeting_date }} <strong /> </td> </tr>',
    '<tr> <td> Key dates </td> <td> <strong> Decision date </strong> {{ decision_date }} </td> </tr>',
    '<tr> <td> Key dates </td> <td> <strong> Eight week date </strong> {{ target_decision_date }} <strong /> </td> </tr>',
    '<tr> <td> Key dates </td> <td> <strong> Consultation sent </strong> {{ consultation_start_date }} <strong /> </td> </tr>',
    '<tr> <td> Key dates </td> <td> <strong> Consultation expires </strong> {{ consultation_end_date }} </td> </tr>',
    '<tr> <td> Key dates </td> <td> <strong> Consultation expires </strong> {{ consultation_end_date }} <strong /> </td> </tr>',
    #'<tr> <td> Constraints </td> <td> {{ conditions }} </td> </tr>',
    #'<tr> <td> Last Updated </td> <td> {{ last_updated_date }} </td> </tr>',
    #'<tr> <td> Last Advertised On </td> <td> {{ last_advertised_date }} </td> </tr>',
    #'<tr> <td> Latest Advertisement Expiry </td> <td> {{ latest_advertisement_expiry_date }} </td> </tr>',
    #'<tr> <td> Neighbour Consultation Sent </td> <td> {{ neighbour_consultation_start_date }} </td> </tr>',
    #'<tr> <td> Neighbour Consultation Expiry </td> <td> {{ neighbour_consultation_end_date }} </td> </tr>',
    ]

    def get_id_batch (self, date_from, date_to):

        fields = self.search_fields
        fields[self.date_from_field] = date_from.strftime(self.request_date_format)
        fields[self.date_to_field] = date_to.strftime(self.request_date_format)
        if self.DEBUG: print "fields:", fields
        response = util.open_url(self.br, self.result_url, fields, 'GET')

        html = response.read()
        url = response.geturl()
        if self.DEBUG: print "result page:", html

        try:
            result = scrapemark.scrape(self.scrape_max_recs, html)
            max_recs = int(result['max_recs'])
        except:
            max_recs = 0
        if self.DEBUG: print "max recs:", max_recs
        
        final_result = []
        rec_count = 0
        while response and rec_count <= max_recs:
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
                rec_count += len(result['records'])
                fields['page'] = str(rec_count)
                response = util.open_url(self.br, self.result_url, fields, 'GET')
                html = response.read()
                url = response.geturl()
                if self.DEBUG: print "next page:", html
            else:
                break

        return final_result

    def get_detail_from_uid (self, uid):
        url = self.applic_url + '?ref=' + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    scraper = BurnleyScraper()
    #scraper.reset()
    #scraper.DEBUG = True
    scraper.run()

    # misc tests
    #print scraper.get_detail_from_uid ('APP/2012/0113')
    #print scraper.get_detail_from_uid ('APP/2013/0204')
    #res = scraper.get_id_batch(util.get_dt('06/04/2013'), util.get_dt('25/04/2013'))
    #res = scraper.get_id_batch(util.get_dt('28/06/2012'), date.today())
    #print len(res), res
    #print scraper.gather_ids('2012-02-01')
    #print scraper.gather_ids('2011-02-01', '2012-01-18')
    #print scraper.gather_ids(None, None)
    #scraper.gather_current_ids()

    #util.rename_column('swdata', 'ward', 'ward_name')
