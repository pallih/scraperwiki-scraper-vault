# this is a scraper of Astun system planning applications for use by Openly Local

# currently Spelthorne and Bath/ NE Somerset

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import urllib
import sys
import gc

base = scraperwiki.utils.swimport("openlylocal_base_scraper")
scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")

systems = [  'BathScraper', 'SpelthorneScraper' ]

class AstunScraper(base.DateScraper):

    MAX_ID_BATCH = 300 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go
    ck = None
    search_form = '1'
    search_fields = { 'maxrecords': '300' }
    next_link = 'Next >'
    
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div class="atSearchDetails"> {{ block|html }} </div>
    """

    def __init__(self, table_name = None):
        base.DateScraper.__init__(self, table_name)
        if self.ck:
            util.set_cookie(self.cj, self.ck['name'], self.ck['value'], self.ck.get('domain'), self.ck.get('path', '/'))   

    def get_id_batch (self, date_from, date_to):

        response = util.open_url(self.br, self.start_url)
        if self.DEBUG: print "start page:", response.read()

        fields = self.search_fields
        fields[self.date_from_field] = date_from.strftime(self.request_date_format)
        fields[self.date_to_field] = date_to.strftime(self.request_date_format)
        form_ok = util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print "form:", self.br.form
        response = util.submit_form(self.br)

        html = response.read()
        url = response.geturl()
        if self.DEBUG: print "result page:", url, html

        result = scrapemark.scrape(self.scrape_max_pages, html)
        try:
            page_list = result['max_pages'].split()
            max_pages = len(page_list)
        except:
            max_pages = 1
        if self.DEBUG: print max_pages
        
        page_count = 1
        final_result = []
        while page_count <= max_pages:
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            else:
                break
            page_count += 1
            if page_count > max_pages: break
            try:
                next_url = re.sub(r'pageno=\d*&', 'pageno=' + str(page_count) + '&', url)
                response = self.br.open(next_url)
                html = response.read()
                url = response.geturl()
            except:
                break

        """while response:
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
                try:
                    response = self.br.follow_link(text=self.next_link)
                except:
                    break
                html = response.read()
                url = response.geturl()
                if self.DEBUG: print "next page:", html
            else:
                break"""

        return final_result

    def get_detail_from_uid (self, uid):
        self.applic_fields['Filter'] = "^REFVAL^='" + uid + "'"
        url = self.applic_url + '?' + urllib.urlencode(self.applic_fields)
        if self.DEBUG: print url
        return self.get_detail_from_url(url)

class SpelthorneScraper(AstunScraper):

    TABLE_NAME = 'Spelthorne'
    ck = { 'name': 'astun:readTerms', 'value': 'true', 'domain': 'my.spelthorne.gov.uk', 'path': '/' }
    date_from_field = 'DATEAPRECV:FROM:DATE'
    date_to_field = 'DATEAPRECV:TO:DATE'
    start_url = 'http://my.spelthorne.gov.uk/planning/?requesttype=parsetemplate&template=DCSearchAdv.tmplt'
    applic_url = 'http://my.spelthorne.gov.uk/planning/default.aspx'
    applic_fields = { 'basepage': 'default.aspx', 'requesttype': 'parsetemplate', 'template': 'DCApplication.tmplt' }
    scrape_ids = """
    <div id="atResultsList">
    {* <div>
    <p> <a href="{{ [records].url|abs }}" /> </p>
    <p> Reference: {{ [records].uid }} | </p>
    </div> *}
    </div>
    """
    scrape_max_pages = '<div class="atPageNo"> {{ max_pages }} </div>'
    
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <dl> <dt> Application Reference: </dt> <dd> {{ reference }} </dd>
    <dt> Address of Proposal: </dt> <dd> {{ address }} </dd>
    <dt> Proposal: </dt> <dd> {{ description }} </dd> </dl>
    <dl> <dt> Date Application Received: </dt> <dd> {{ date_received }} </dd>
    <dt> Date Application Validated: </dt> <dd> {{ date_validated }} </dd> </dl>
    """

    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<dt> Planning Portal Reference Number </dt> <dd> {{ planning_portal_id }} </dd>',
    '<dt> Type of Application </dt> <dd> {{ application_type }} </dd>',
    '<dt> Status </dt> <dd> {{ status }} </dd>',
    """<dt> Decision </dt> <dd> {{ decision }} </dd>
    <dt> Decision Type </dt> <dd> {{ decided_by }} </dd>""",
    '<dt> Ward </dt> <dd> {{ ward_name }} </dd>',
    '<dt> Parish </dt> <dd> {{ parish }} </dd>',
    '<dt> Case Officer </dt> <dd> {{ case_officer }} </dd>',
    '<dt> Appeal Reference </dt> <dd> {{ appeal_reference }} </dd>',
    '<dt> Appeal Status </dt> <dd> {{ appeal_status }} </dd>',
    '<h4> Applicant </h4> <dt> Name </dt> <dd> {{ applicant_name }} </dd> <dt> Address </dt> <dd> {{ applicant_address }} </dd>',
    '<h4> Agent </h4> <dt> Name </dt> <dd> {{ agent_name }} </dd> <dt> Address </dt> <dd> {{ agent_address }} </dd>',
    '<dt> Target Determination Date </dt> <dd> {{ target_decision_date }} </dd>',
    '<dt> Actual Committee Date </dt> <dd> {{ meeting_date }} </dd>',
    '<dt> Neighbourhood Consultations sent on </dt> <dd> {{ consultation_start_date }} </dd>',
    '<dt> Expiry Date for Neighbour Consultations </dt><dd> {{ neighbour_consultation_end_date }} </dd>',
    '<dt> Standard Consultations sent on </dt> <dd> {{ neighbour_consultation_start_date }} </dd>',
    '<dt> Expiry Date for Standard Consultations </dt> <dd> {{ consultation_end_date }} </dd>',
    '<dt> Last Advertised on </dt> <dd> {{ last_advertised_date }} </dd>',
    '<dt> Expiry Date for Latest Advertisement </dt> <dd> {{ latest_advertisement_expiry_date }} </dd>',
    '<dt> Latest Site Notice posted on </dt> <dd> {{ site_notice_start_date }} </dd>',
    '<dt> Expiry Date for Latest Site Notice </dt> <dd>{{ site_notice_end_date }} </dd>',
    '<dt> Date Decision Made </dt> <dd> {{ decision_date }} </dd>',
    '<dt> Date Decision Issued: </dt> <dd> {{ decision_issued_date }} </dd>',
    '<dt> Permission Expiry Date </dt> <dd> {{ permission_expires_date }} </dd>',
    '<dt> Date Decision Printed </dt> <dd> {{ decision_published_date }} </dd>',
    '<a class="atComments forwardlink" href="{{ comment_url|abs }}"> Comment on this application </a>',
    ]


class BathScraper(AstunScraper):

    TABLE_NAME = 'Bath'
    date_from_field = 'DATEAPVAL:FROM:DATE'
    date_to_field = 'DATEAPVAL:TO:DATE'
    start_url = 'http://isharemaps.bathnes.gov.uk/projects/bathnes/developmentcontrol/default.aspx?requesttype=parsetemplate&template=DevelopmentControlSearchAdvanced.tmplt'
    applic_url = 'http://isharemaps.bathnes.gov.uk/projects/bathnes/developmentcontrol/default.aspx'
    applic_fields = { 'basepage': 'default.aspx', 'requesttype': 'parsetemplate', 
        'template': 'DevelopmentControlApplication.tmplt', 'SearchLayer': 'DCApplications', 'SearchField': 'REFVAL' }
    scrape_ids = """
    <div class="atSearchResults">
    {* <div>
    <p> <a href="{{ [records].url|abs }}" /> </p>
    <p> Application reference: {{ [records].uid }} received </p>
    </div> *}
    </div>
    """
    scrape_max_pages = '<div class="atPageNo"> Pages: {{ max_pages }} </div>'
    
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <h3> (Reference:{{ reference }}) </h3>
    <tr> <td> Address of Proposal: </td> <td> {{ address }} </td> </tr>
    <tr> <td> Proposal: </td> <td> {{ description }} </td> </tr>
    <tr> <td> Date Application Received: </td> <td> {{ date_received }} </td> </tr>
    <tr> <td> Date Application Validated: </td> <td> {{ date_validated }} </td> </tr>
    """

    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr> <td> Planning Portal Reference Number </td> <td> {{ planning_portal_id }} </td> </tr>',
    '<tr> <td> Type of Application </td> <td> {{ application_type }} </td> </tr>',
    '<tr> <td> Status </td> <td> {{ status }} </td> </tr>',
    """<tr> <td> Decision </td> <td> {{ decision }} </td> </tr>
    <tr> <td> Decision Type </td> <td> {{ decided_by }} </td> </tr>""",
    '<tr> <td> Ward </td> <td> {{ ward_name }} </td> </tr>',
    '<tr> <td> Parish </td> <td> {{ parish }} </td> </tr>',
    '<tr> <td> Case Officer </td> <td> {{ case_officer }} </td> </tr>',
    '<tr> <td> Appeal Reference </td> <td> {{ appeal_reference }} </td> </tr>',
    '<tr> <td> Appeal Status </td> <td> {{ appeal_status }} </td> </tr>',
    '<tr> <td> Applicant Name </td> <td> {{ applicant_name }} </td> </tr>',
    '<tr> <td> Agent Name </td> <td> {{ agent_name }} </td> </tr>',
    '<tr> <td> Agent Address </td> <td> {{ agent_address }} </td> </tr>',
    '<tr> <td> Target Decision Date </td> <td> {{ target_decision_date }} </td> </tr>',
    '<tr> <td> Actual Committee Date </td> <td> {{ meeting_date }} </td> </tr>',
    '<tr> <td> Neighbourhood Consultations sent on </td> <td> {{ consultation_start_date }} </td> </tr>',
    '<tr> <td> Expiry Date for Neighbour Consultations </td> <td> {{ neighbour_consultation_end_date }} </td> </tr>',
    '<tr> <td> Standard Consultations sent on </td> <td> {{ neighbour_consultation_start_date }} </td> </tr>',
    '<tr> <td> Expiry Date for Consultation </td> <td> {{ consultation_end_date }} <div /> </td> </tr>',
    '<tr> <td> Last Advertised on </td> <td> {{ last_advertised_date }} </td> </tr>',
    '<tr> <td> Expiry Date for Latest Advertisement </td> <td> {{ latest_advertisement_expiry_date }} </td> </tr>',
    '<tr> <td> Latest Site Notice posted on </td> <td> {{ site_notice_start_date }} </td> </tr>',
    '<tr> <td> Expiry Date for Latest Site Notice </td> <td>{{ site_notice_end_date }} </td> </tr>',
    '<tr> <td> Date Decision Made </td> <td> {{ decision_date }} </td> </tr>',
    '<tr> <td> Date Decision Issued </td> <td> {{ decision_issued_date }} </td> </tr>',
    '<tr> <td> Permission Expiry Date </td> <td> {{ permission_expires_date }} </td> </tr>',
    '<tr> <td> Date Decision Printed </td> <td> {{ decision_published_date }} </td> </tr>',
    '<a class="atComments forwardlink" href="{{ comment_url|abs }}"> Comment on this application </a>',
    ]
    
if __name__ == 'scraper':

    #scraper = SpelthorneScraper()
    #scraper.replace_all_with('spelthorne_planning_applications', 'swdata')
    #scraper.run()
    #scraper = BathScraper()
    #scraper.run()
    #sys.exit()

    sys_list = []
    for k in systems: # get latest date scraped for each system
        try:
            scraper = eval(k + "()")
            latest_val = scraperwiki.sqlite.get_var('latest-' + scraper.TABLE_NAME)
            scraper = None
            gc.collect()
        except:
            latest_val = None
        sys_list.append( (k, latest_val) )
    sort_sys = sorted(sys_list, key=lambda system: system[1]) # sort so least recent are first
    for auth in sort_sys[:3]: # limit max per run
        strexec = auth[0] + "()"
        print "Scraping from:", strexec
        try:
            scraper = eval(strexec)
            scraper.run()
            scraper = None
            gc.collect()
        except Exception as err:
            print "Error - skipping this authority -", str(err)
    print "Finished"

    # misc test calls
    #scraper = BathScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('13/00683/FUL') # Bath
    #scraper = SpelthorneScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('12/00779/ADV') # Spelthorne
    
    #res = scraper.get_id_batch(util.get_dt('03/03/2013'), util.get_dt('10/03/2013'))
    #print res, len(res)
    #print scraper.get_id_batch(util.get_dt('23/03/2012'), util.get_dt('25/03/2012'))

