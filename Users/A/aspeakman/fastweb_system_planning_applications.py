# this is a base scraper for FastWeb system planning applications for use by Openly Local

# there are 14 authorities using this system

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
    'Craven': 'CravenScraper',
    #'Eastbourne': 'EastbourneScraper', now Civica
    'Eastleigh': 'EastleighScraper',
    'Eden': 'EdenScraper',
    'Harlow': 'HarlowScraper', 
    'Mansfield': 'MansfieldScraper',
    'Neath': 'NeathScraper',
    #'Newport': 'NewportScraper', date search no longer working see separate list scraper
    'NorthDevon': 'NorthDevonScraper',
    'Plymouth': 'PlymouthScraper',
    'Rugby': 'RugbyScraper',
    'SouthLakeland': 'SouthLakelandScraper',
    'Sutton': 'SuttonScraper',
    'Welwyn': 'WelwynScraper',
    'WyreForest': 'WyreForestScraper',
     }

class FastwebScraper(base.DateScraper):

    MAX_ID_BATCH = 300 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go

    date_from_field = 'DateReceivedStart'
    date_to_field = 'DateReceivedEnd'
    search_fields = { 'ShowDecided': [] }
    search_form = 'SearchForm'
    request_date_format = '%d/%m/%Y'

    scrape_ids = """
    <body> Search Results <table>
    {* <table> <tr> 
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td> </tr>
    <tr /> <tr />
    </table> *}
    </table> </body>
    """
    next_page = 'Next'
    detail_page = 'fulldetail.asp'

    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = "<body> <h1 /> {{ block|html }} </body>"
    # the minimum acceptable valid dataset on the details page
    scrape_min_data = """
    <tr> <th> Application Number </th> <td> {{ reference }} </td> </tr>
    <tr> <th> Site Address </th> <td> {{ address }} </td> </tr>
    <tr> <th> Description </th> <td> {{ description }} </td> </tr>
    """
    # other optional parameters that can appear on the details page
    scrape_optional_data = [
    "<tr> <th> Date Received </th> <td> {{ date_received }} </td> </tr>",
    "<tr> <th> Date Valid </th> <td> {{ date_validated }} </td> </tr>",
    "<tr> <th> Application Status </th> <td> {{ status }} </td> </tr>",
    "<tr> <th> Case Officer </th> <td> {{ case_officer }} </td> </tr>",
    "<tr> <th> Decision Level/Committee </th> <td> {{ decided_by }} </td> </tr>",
    "<tr> <th> Decision Level </th> <td> {{ decided_by }} </td> </tr>",
    "<tr> <th> Application Status </th> <td> {{ status }} </td> </tr>",
    "<tr> <th> Applicant Name </th> <td> {{ applicant_name }} <br> {{ applicant_address }} </td> </tr>",
    "<tr> <th> Agent Name </th> <td> {{ agent_name }}  <br> {{ agent_address }} </td> </tr>",
    "<tr> <th> Decision Type </th> <td> {{ decision }} </td> </tr>",
    "<tr> <th> Date Valid </th> </tr> <tr> <th> Decision </th> <td> {{ decision }} </td> </tr> <tr> <th> Decision Date </th> </tr>",
    "<tr> <th> Decision </th> <td> {{ decision }} </td> </tr> <tr> <th> Decision Status </th> <td> {{ status }} </tr>",
    "<tr> <th> Decision Date </th> <td> {{ decision_date }} </td> </tr>",
    "<tr> <th> Sent Date </th> <td> {{ decision_issued_date }} </td> </tr>",
    "<tr> <th> Target Date For Decision </th> <td> {{ target_decision_date }} </td> </tr>",
    "<tr> <th> Target Date of Application </th> <td> {{ target_decision_date }} </td> </tr>",
    "<tr> <th> Agent Phone </th> <td> {{ agent_tel }} </td> </tr>",
    "<tr> <th> Ward </th> <td> {{ ward_name }} </td> </tr>",
    "<tr> <th> Parish </th> <td> {{ parish }} </td> </tr>",
    "<tr> <th> Advert Date </th> <td> {{ last_advertised_date }} </td> </tr>",
    "<tr> <th> Appeal </th> <td> {{ appeal_result }} </td> </tr>",
    #"<tr> <th> Constraints </th> <td> {{ constraints|html }} </td> </tr>",
    #"<tr> <th> Recommendation Date </th> <td> {{ target_decision_date }} </td> </tr>",
    "<tr> <th> Area Team </th> <td> {{ district }} </td> </tr>",
    "<tr> <th> Consultation Period Begins </th> <td> {{ consultation_start_date }} </td> </tr>",
    "<tr> <th> Consultation Period Ends </th> <td> {{ consultation_end_date }} </td> </tr>", 
    "<tr> <th> Consultation/Reconsultation End Date </th> <td> {{ consultation_end_date }} </td> </tr>",
    "<tr> <th> Committee Date </th> <td> {{ meeting_date }} </td> </tr>",
    '<a href="{{ comment_url|abs }}"> Comment </a>',
    ]

    def get_id_batch (self, date_from, date_to):

        if self.DEBUG: self.br.set_debug_http(True)

        response = self.br.open(self.search_url)

        fields = self.search_fields
        fields[self.date_from_field] = date_from.strftime(self.request_date_format)
        fields[self.date_to_field] = date_to.strftime(self.request_date_format)
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
            else:
                break
            try:
                response = self.br.follow_link(text=self.next_page)
            except:
                response = None
        return final_result

    def get_detail_from_uid (self, uid):
        url = urlparse.urljoin(self.search_url, self.detail_page) + "?AltRef=" + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

    # scrape detailed information on one record via its access URL
    def get_detail_from_url (self, url):
        url_parts = urlparse.urlsplit(url)
        url = urlparse.urljoin(url, self.detail_page) + '?' + url_parts.query
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

class CravenScraper(FastwebScraper):

    search_url = 'http://www.planning.cravendc.gov.uk/fastweb/search.asp'

class EastbourneScraper(FastwebScraper):

    BATCH_DAYS = 28 # batch size for each scrape - number of days to gather to produce at least one result each time
    MIN_DAYS = 35 # min number of days to get when gathering current ids

    search_url = 'http://planningapps.eastbourne.gov.uk/search.asp'
    scrape_min_data = """
    <tr> <td> Application Number </td> <td> {{ reference }} </td> </tr>
    <tr> <td> Site Address </td> <td> {{ address }} </td> </tr>
    <tr> <td> Description </td> <td> {{ description }} </td> </tr>
    """
    scrape_optional_data = [
    "<tr> <td> Date Received </td> <td> {{ date_received }} </td> </tr>",
    "<tr> <td> Date Valid </td> <td> {{ date_validated }} </td> </tr>",
    "<tr> <td> Application Status </td> <td> {{ status }} </td> </tr>",
    "<tr> <td> Case Officer </td> <td> {{ case_officer }} </td> </tr>",
    "<tr> <td> Decision Level/Committee </td> <td> {{ decided_by }} </td> </tr>",
    "<tr> <td> Decision Level </td> <td> {{ decided_by }} </td> </tr>",
    "<tr> <td> Application Status </td> <td> {{ status }} </td> </tr>",
    "<tr> <td> Applicant Name </td> <td> {{ applicant_name }} </td> </tr>",
    "<tr> <td> Agent Name </th> <td> {{ agent_name }}  <br> {{ agent_address }} </td> </tr>",
    "<tr> <td> Decision Type </td> <td> {{ decision }} </td> </tr>",
    "<tr> <td> Date Valid </td> </tr> <tr> <td> Decision </td> <td> {{ decision }} </td> </tr> <tr> <td> Decision Date </td> </tr>",
    "<tr> <td> Decision </td> <td> {{ decision }} </td> </tr> <tr> <td> Decision Status </td> <td> {{ status }} </tr>",
    "<tr> <td> Decision Date </td> <td> {{ decision_date }} </td> </tr>",
    "<tr> <td> Sent Date </td> <td> {{ decision_issued_date }} </td> </tr>",
    "<tr> <td> Target Decision Date </td> <td> {{ target_decision_date }} </td> </tr>",
    "<tr> <td> Target Date of Application </td> <td> {{ target_decision_date }} </td> </tr>",
    "<tr> <td> Agent Phone </td> <td> {{ agent_tel }} </td> </tr>",
    "<tr> <td> Ward </td> <td> {{ ward_name }} </td> </tr>",
    "<tr> <td> Parish </td> <td> {{ parish }} </td> </tr>",
    "<tr> <td> Advert Date </td> <td> {{ last_advertised_date }} </td> </tr>",
    "<tr> <td> Appeal </td> <td> {{ appeal_result }} </td> </tr>",
    #"<tr> <td> Constraints </td> <td> {{ constraints|html }} </td> </tr>",
    #"<tr> <td> Recommendation Date </td> <td> {{ target_decision_date }} </td> </tr>",
    "<tr> <td> Area Team </td> <td> {{ district }} </td> </tr>",
    "<tr> <td> Consultation Period Begins </td> <td> {{ consultation_start_date }} </td> </tr>",
    "<tr> <td> Consultation Period Ends </td> <td> {{ consultation_end_date }} </td> </tr>",
    "<tr> <td> Consultation/Reconsultation End Date </td> <td> {{ consultation_end_date }} </td> </tr>",
    "<tr> <td> Committee Date </td> <td> {{ meeting_date }} </td> </tr>",
    '<a href="{{ comment_url|abs }}"> Comment </a>',
    ]

    def get_detail_from_uid (self, uid):
        url = urlparse.urljoin(self.search_url, self.detail_page) + "?AltRef=" + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

class EastleighScraper(FastwebScraper):

    MIN_DAYS = 28 # min number of days to get when gathering current ids
    search_url = 'http://www.eastleigh.gov.uk/fastweb/search.asp'

class EdenScraper(FastwebScraper):

    search_url = 'http://eforms.eden.gov.uk/fastweb/search.asp'

class HarlowScraper(FastwebScraper):

    TABLE_NAME = 'Harlow'
    search_url = 'http://communitymap.harlow.gov.uk/fastweb/search.asp'

class MansfieldScraper(FastwebScraper):

    search_url = 'http://www.mansfield.gov.uk/Fastweb/search.asp'

class NeathScraper(FastwebScraper):

    search_url = 'https://planning.npt.gov.uk/search.asp'

#class NewportScraper(FastwebScraper): # dates in m/d/Y format?

#    BATCH_DAYS = 28 # batch size for each scrape - number of days to gather to produce at least one result each time
#    search_url = 'http://www.newport.gov.uk/fastWeb/search.asp'

class NorthDevonScraper(FastwebScraper):

    search_url = 'http://planning.northdevon.gov.uk/search.asp'

class PlymouthScraper(FastwebScraper):

    #search_url = 'http://www.plymouth.gov.uk/planningapplications2/search.asp'
    search_url = 'http://www.plymouth.gov.uk/planningapplicationsv4/search.asp'
    #search_fields = {}
    detail_page = 'detail.asp'
    scrape_ids = """
    <body> <h1 /> <table>
    {* <table> <tr>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td> </tr>
    <tr> Received Date: {{ [records].date_received }} Decision Sent Date: </tr>
    </table> *}
    </table> </body>
    """

class RugbyScraper(FastwebScraper):

    search_url = 'http://www.planningportal.rugby.gov.uk/search.asp'

class SouthLakelandScraper(FastwebScraper):

    search_url = 'http://www.southlakeland.gov.uk/fastweb/search.asp'

class SuttonScraper(FastwebScraper):

    search_url = 'http://gis.sutton.gov.uk/FASTWEB/search.asp'

class WelwynScraper(FastwebScraper):

    MIN_DAYS = 28 # min number of days to get when gathering current ids
    search_url = 'https://fastweb.welhat.gov.uk/search.asp?ApplicationNumber=&AddressPrefix=&submit1=Go'

class WyreForestScraper(FastwebScraper):

    search_url = 'http://www.wyreforest.gov.uk/fastweb/search.asp'
    

if __name__ == 'scraper':

    #scraperwiki.sqlite.execute("delete from swvariables where name = 'earliest' or name = 'latest'")
    #scraperwiki.sqlite.commit()
    #scraper = SuttonScraper('Sutton')
    #scraper.run()
    #sys.exit()

    sys_list = []
    for k, v in systems.items(): # get latest date scraped for each system
        sys_list.append( (k, v, scraperwiki.sqlite.get_var('latest-' + k)) )
    sort_sys = sorted(sys_list, key=lambda system: system[2]) # sort so least recent are first
    for auth in sort_sys[:6]: # do max 6 per run
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
    #scraper = CravenScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('30/2011/11959') # Craven OK
    #scraper = EastbourneScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('EB/2011/0493') # Eastbourne OK
    #scraper = EastleighScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('T/11/69536') # Eastleigh OK
    #scraper = EdenScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/0716') # Eden OK
    #scraper = HarlowScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('HW/PL/13/00028') # Harlow OK
    #scraper = MansfieldScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('2011/0474/ST') # Mansfield OK
    #scraper = NeathScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('P2011/0713') # Neath OK
    #scraper = NewportScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/0831') # Newport OK
    #scraper = NorthDevonScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('52673') # NorthDevon OK
    #scraper = PlymouthScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/01380/FUL') # Plymouth OK
    #scraper = RugbyScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('R11/1591') # Rugby OK
    #scraper = SouthLakelandScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('SL/2011/0700') # SouthLakeland OK
    #scraper = SuttonScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('B2011/64812') # Sutton OK
    #scraper = WelwynScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('N6/2011/1682/TP') # Welwyn OK
    #scraper = WyreForestScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/0516/FULL') # WyreForest OK

    #res = scraper.get_id_batch(util.get_dt('14/01/2013'), util.get_dt('24/01/2013'))
    #print res, len(res)
    #print scraper.get_id_batch(util.get_dt('23/03/2012'), util.get_dt('25/03/2012'))

    #util.list_url_prefixes(scraper.TABLE_NAME, 'url')
    #util.replace_vals(scraper.TABLE_NAME, 'url', 'http://www.nuneatonandbedworth.gov.uk/sys_upl/templates/', 'http://apps.nuneatonandbedworth.gov.uk/', 'prefix', 'yes')

    #sql = "delete from Eastleigh where uid = 'Next' or uid = 'Previous'"
    #scraperwiki.sqlite.execute(sql)
    #scraperwiki.sqlite.commit()
    
