# this is a scraper of Surrey Heath planning applications for use by Openly Local

# AcolNet with Javascript front end - date query results not accessible

# so works from the sequence of thesystemkey record numbers 

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import urllib, urllib2
import mimetools, mimetypes
import os, stat
from cStringIO import StringIO

base = scraperwiki.utils.swimport("openlylocal_base_scraper")
scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")

class SurreyHeathScraper(base.ListScraper):

    START_SEQUENCE = 1 # gathering back to this record number
    START_POINT = 31200
    MAX_ID_BATCH = 250 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go
    ID_ORDER = "uid desc"
    MIN_RECS = 70

    HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:8.0) Gecko/20100101 Firefox/8.0',
    'Accept-Charset': 'UTF-8,*',
    'Accept': 'text/html',
    'Accept-Language': 'en-gb,en',
    'Connection': 'Keep-Alive'
    }
    ck = { 'name': 'WhlScheduledLogoff', 'value': 'False', 'domain': 'www.public.surreyheath-online.gov.uk', 'path': '/'}

    date_from_field = 'regdate1'
    date_to_field = 'regdate2'
    ref_field = 'casefullref'
    search_form = 'frmSearch'
    search_fields = { 'casefullref': '', 'locaddress1': '', 'appname': '', 'agtname': '', 'wardname': '', 'parishname': '',    
        'appntype': '', 'dcndate1': '', 'dcndate2': '', 'aplrecdate1': '', 'aplrecdate2': '', 'apldcndate1': '', 'apldcndate2': '', 'regdate1': '', 'regdate2': '',}
    #search_fields = { 'edtappno': '',  'edtlocation': '',  'edtappname': '',  'edtagtname': '',  'edtwardname': '',  
    #    'edtdcndate1': '',  'edtdcndate2': '',  'edtaplrecdate1': '',  'edtaplrecdate2': '', 'edtapldcndate1': '',  'edtapldcndate2': '',  }
    start_url = 'https://www.public.surreyheath-online.gov.uk/whalecom60b1ef305f59f921/whalecom0/Scripts/PlanningPagesOnline/acolnetcgi.gov?ACTION=UNWRAP&RIPNAME=Root.PgeApplications'
    search_url = 'https://www.public.surreyheath-online.gov.uk/whalecom60b1ef305f59f921/whalecom0/Scripts/PlanningPagesOnline/acolnetcgi.gov?ACTION=UNWRAP&RIPNAME=Root.pgesearch'
    applic_url = 'https://www.public.surreyheath-online.gov.uk/whalecom60b1ef305f59f921/whalecom0/Scripts/PlanningPagesOnline/acolnetcgi.gov?ACTION=UNWRAP&RIPNAME=Root.PgeResultDetail'

    first_page = True # only first page access requires page replace
    scrape_replace = 'window.location.replace(" {{ replace }} ");'
    scrape_action = ' action="{{ action|abs }}" '
    subs = {
        r'<script\s.*?</script>': r'',
        r'onSubmit=""return ValidateSearch\(\)""': r'onSubmit="return ValidateSearch()"',
        }
    scrape_next = '<a id="lnkPageNext" href=" {{ next_link }} "> </a>'
    scrape_max = '<table class="pagetitle"> {{ max_recs }} Results </table>'
    scrape_ids = """
    <div id="contentcol">
    {* <table class="results-table">
    <tr> <td class="casenumber"> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td> </tr>
    </table> *}
    </div>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <table id="details-table"> {{ block|html }} </table>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <th> Application Number </th> <td> {{ uid }} </td>
    <th> Registration (Validation) Date </th> <td> {{ date_validated }} </td>
    <th> Location </th> <td> {{ address }} </td>
    <th> Proposal </th> <td> {{ description }} </td>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<th> Date Received </th> <td> {{ date_received }} </td>',
    "<th> Application Number </th> <td> {{ reference }} </td>",
    "<th> Registration </th> <td> {{ date_validated }} </td>",
    "<th> Statutory Start </th> <td> {{ date_validated }} </td>",
    "<th> Application Type </th> <td> {{ application_type }} </td>",
    "<th> Case Officer </th> <td> {{ case_officer }} </td>",
    "<th> Decision Level </th> <td> {{ decided_by }} </td>",
    "<th> Appeal Received Date </th> <td> {{ appeal_date }} </td>",
    "<th> Target Date for Decision </th> <td> {{ target_decision_date }} </td>",
    "<th> Appeal Decision </th> <td> {{ appeal_result }} </td>",
    "<th> Earliest Decision Date </th> <td> {{ consultation_end_date }} </td>",
    "<th> Consultation Period Expires </th> <td> {{ consultation_end_date }} </td>",
    "<th> Consultation Period Ends </th> <td> {{ consultation_end_date }} </td>",
    "<th> Status </th> <td> {{ status }} </td>",
    "<th> Parish </th> <td> {{ parish }} </td>",
    "<th> Ward </th> <td> {{ ward_name }} </td>",
    "<th> Comments </th> <td> {{ comment_date }} </td>",
    "<th> Applicant </th> <td> {{ applicant_name }} </td>",
    "<th> Consultation Start Date </th> <td> {{ consultation_start_date }} </td>",
    "<th> Consultation Period Starts </th> <td> {{ consultation_start_date }} </td>",
    "<th> Date from when comments </th> <td> {{ consultation_start_date }} </td>",
    "<th> Site Notice Date </th> <td> {{ site_notice_start_date }} </td>",
    "<th> Date Decision Made </th> <td> {{ decision_date }} </td>",
    "<th> Agent </th> <td> {{ agent_name }} </td>",
    "<th> Date Decision Despatched </th> <td> {{ decision_issued_date }} </td> <th> Decision </th> <td> {{ decision }} </td>",
    "<th> Decision Issued </th> <td> {{ decision_issued_date }} </td>",
    "<th> Meeting Date </th> <td> {{ meeting_date }} </td>",
    "<th> Committee </th> <td> {{ meeting_date }} </td>",
    "<th> Appeal Received Date </th> <td> {{ appeal_date }} </td>",
    "<tr> <th> Easting/Northing </th> <td> {{ easting }}/{{ northing }} </td> </tr>",
    "<th> Agent </th> <td /> {* <td> {{ [agent_address] }} </td> *} <th> Applicant </th>",
    "<th> Applicant </th> <td /> {* <td> {{ [applicant_address] }} </td> *} <th> Date </th>",
    ]

    def __init__(self, table_name = None):
        base.ListScraper.__init__(self, table_name)
        if self.ck:
            util.set_cookie(self.cj, self.ck['name'], self.ck['value'], self.ck.get('domain'), self.ck.get('path', '/'))   

    """def get_id_batch (self, date_from, date_to): 

        response = util.open_url(self.br, self.search_url)
        html = response.read()
        if self.DEBUG: print "search page:", html

        result = scrapemark.scrape(self.scrape_replace, html)
        response = util.open_url(self.br, result['replace'], )
        response = self.br.response()  # adjust bad html
        html = response.get_data()
        if self.DEBUG: print "html pre sub:", html
        for k, v in self.subs.items():
            html = re.sub(k, v, html, 0, re.U|re.S|re.I) # unicode|dot matches new line|ignore case
        if self.DEBUG: print "html post sub:", html
        response.set_data(html)
        self.br.set_response(response)

        html = response.read()
        url = response.geturl()
        if self.DEBUG: print "form page:", html
        result = scrapemark.scrape(self.scrape_action, html, url)
        print result

        #self.br.set_handle_referer(False)
        #self.HEADERS['Referer'] = self.start_url
        #self.br.addheaders = self.HEADERS.items()

        #fields = self.search_fields
        fields = {}
        fields[self.date_from_field] = date_from.strftime(self.request_date_format)
        fields[self.date_to_field] = date_to.strftime(self.request_date_format)
        util.setup_form(self.br, self.search_form, fields)

        #response = util.open_url(self.br, result['action'], fields)
        #request = urllib2.Request(result['action'])
        #request.add_header('Accept', 'text/html')
        #opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj), MultipartPostHandler)
        #response = opener.open(request, urllib.urlencode(fields))

        if self.DEBUG: print "form:", self.br.form
        response = util.submit_form(self.br)

        html = response.read()
        url = response.geturl()
        if self.DEBUG: print "result page:", url, html
        result = scrapemark.scrape(self.scrape_max, html, url)
        try:
            max_recs = int(result['max_recs'])
        except:
            max_recs = 0
        
        final_result = []
        while response and len(final_result) < max_recs:
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
                html = response.read()
                url = response.geturl()
                if self.DEBUG: print "next page:", html
            else:
                break

        return final_result"""

    # NB if move_forward is true, we scrape forwards from rec_start, otherwise we scrape backwards
    def get_id_records2 (self, rec_start, move_forward):
        final_result = []
        num_from = None
        num_to = None
        bad_count = 0
        current_rec = rec_start
        fields = {}
        first_good_rec = None
        last_good_rec = None
        while len(final_result) < self.MAX_ID_BATCH and bad_count < 10:
            if self.DEBUG: print 'Record:', current_rec
            this_url = self.applic_url + '&TheSystemkey=' + str(current_rec)
            response = util.open_url(self.br, this_url)
            if response:
                html = response.read()
                if self.DEBUG: print 'Html:', html
                if self.first_page:
                    result = scrapemark.scrape(self.scrape_replace, html)
                    response = util.open_url(self.br, result['replace'], )
                    html = response.read()
                    self.first_page = False
                result = scrapemark.scrape(self.scrape_min_data, html)
                if result and result.get('uid'):
                    if not first_good_rec: first_good_rec = current_rec
                    last_good_rec = current_rec
                    if self.DEBUG: print result
                    final_result.append( { 'url': this_url, 'uid': str(current_rec) } ) # temporarily sets uid to thesystemkey
                    bad_count = 0
                else:
                    bad_count += 1
            else:
                bad_count += 1
            if move_forward:
                current_rec += 1
            else:
                current_rec -= 1
        if final_result:
            self.clean_ids(final_result)
            if move_forward:
                num_from = first_good_rec
                num_to = last_good_rec
            else:
                num_to = first_good_rec
                num_from = last_good_rec
        return final_result, num_from, num_to

    def get_detail_from_url (self, url):
        try: 
            response = util.open_url(self.br, url)
            html = response.read()
            if self.DEBUG: print "start page:", html
    
            if self.first_page:
                result = scrapemark.scrape(self.scrape_replace, html)
                response = util.open_url(self.br, result['replace'], )
                html = response.read()
                self.first_page = False

            url = response.geturl()
        except:
            if self.DEBUG: raise
            else: return None
        return self.get_detail(html, url)

    # note only works if the 'uid' is set temporarily to the systemkey
    def get_detail_from_uid (self, uid):
        url = self.applic_url + '&TheSystemkey=' + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

class Callable:
    def __init__(self, anycallable):
        self.__call__ = anycallable

# Controls how sequences are uncoded. If true, elements may be given multiple values by
#  assigning a sequence.
doseq = 1

class MultipartPostHandler(urllib2.BaseHandler):

    handler_order = urllib2.HTTPHandler.handler_order - 10 # needs to run first

    def http_request(self, request):
        data = request.get_data()
        if data is not None and type(data) != str:
            v_files = []
            v_vars = []
            try:
                 for(key, value) in data.items():
                    if type(value) == file:
                         v_files.append((key, value))
                    else:
                         v_vars.append((key, value))
            except TypeError:
                systype, value, traceback = sys.exc_info()
                raise TypeError, "not a valid non-string sequence or mapping object", traceback

            if len(v_files) == 0:
                data = urllib.urlencode(v_vars, doseq)
            else:
                boundary, data = self.multipart_encode(v_vars, v_files)

                contenttype = 'multipart/form-data; boundary=%s' % boundary
                if(request.has_header('Content-Type')
                   and request.get_header('Content-Type').find('multipart/form-data') != 0):
                    print "Replacing %s with %s" % (request.get_header('content-type'), 'multipart/form-data')
                request.add_unredirected_header('Content-Type', contenttype)

            request.add_data(data)
        
        return request

    def multipart_encode(vars, files, boundary = None, buf = None):
        if boundary is None:
            boundary = mimetools.choose_boundary()
        if buf is None:
            buf = StringIO()
        for(key, value) in vars:
            buf.write('--%s\r\n' % boundary)
            buf.write('Content-Disposition: form-data; name="%s"' % key)
            buf.write('\r\n\r\n' + value + '\r\n')
        for(key, fd) in files:
            file_size = os.fstat(fd.fileno())[stat.ST_SIZE]
            filename = fd.name.split('/')[-1]
            contenttype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
            buf.write('--%s\r\n' % boundary)
            buf.write('Content-Disposition: form-data; name="%s"; filename="%s"\r\n' % (key, filename))
            buf.write('Content-Type: %s\r\n' % contenttype)
            # buffer += 'Content-Length: %s\r\n' % file_size
            fd.seek(0)
            buf.write('\r\n' + fd.read() + '\r\n')
        buf.write('--' + boundary + '--\r\n\r\n')
        buf = buf.getvalue()
        return boundary, buf

    multipart_encode = Callable(multipart_encode)

    https_request = http_request

if __name__ == 'scraper':

    scraper = SurreyHeathScraper()
    scraper.run()

    # misc tests
    #scraper.DEBUG = True
    #scraper.br.set_debug_http(True)
    #print scraper.get_detail_from_uid ('12/0111')
    #print scraper.get_detail_from_uid('29743')
    #print scraper.get_detail_from_uid ('31391')
    #print scraper.get_detail_from_uid ('31372')
    #res = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('18/08/2011'))
    #print len(res), res
    #result = scraper.get_id_records2(15000, True)
    #print result, len(result)
    #print scraper.gather_ids('2012-02-01')
    #print scraper.gather_ids('2011-02-01', '2012-01-18')

# this is a scraper of Surrey Heath planning applications for use by Openly Local

# AcolNet with Javascript front end - date query results not accessible

# so works from the sequence of thesystemkey record numbers 

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import urllib, urllib2
import mimetools, mimetypes
import os, stat
from cStringIO import StringIO

base = scraperwiki.utils.swimport("openlylocal_base_scraper")
scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")

class SurreyHeathScraper(base.ListScraper):

    START_SEQUENCE = 1 # gathering back to this record number
    START_POINT = 31200
    MAX_ID_BATCH = 250 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go
    ID_ORDER = "uid desc"
    MIN_RECS = 70

    HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:8.0) Gecko/20100101 Firefox/8.0',
    'Accept-Charset': 'UTF-8,*',
    'Accept': 'text/html',
    'Accept-Language': 'en-gb,en',
    'Connection': 'Keep-Alive'
    }
    ck = { 'name': 'WhlScheduledLogoff', 'value': 'False', 'domain': 'www.public.surreyheath-online.gov.uk', 'path': '/'}

    date_from_field = 'regdate1'
    date_to_field = 'regdate2'
    ref_field = 'casefullref'
    search_form = 'frmSearch'
    search_fields = { 'casefullref': '', 'locaddress1': '', 'appname': '', 'agtname': '', 'wardname': '', 'parishname': '',    
        'appntype': '', 'dcndate1': '', 'dcndate2': '', 'aplrecdate1': '', 'aplrecdate2': '', 'apldcndate1': '', 'apldcndate2': '', 'regdate1': '', 'regdate2': '',}
    #search_fields = { 'edtappno': '',  'edtlocation': '',  'edtappname': '',  'edtagtname': '',  'edtwardname': '',  
    #    'edtdcndate1': '',  'edtdcndate2': '',  'edtaplrecdate1': '',  'edtaplrecdate2': '', 'edtapldcndate1': '',  'edtapldcndate2': '',  }
    start_url = 'https://www.public.surreyheath-online.gov.uk/whalecom60b1ef305f59f921/whalecom0/Scripts/PlanningPagesOnline/acolnetcgi.gov?ACTION=UNWRAP&RIPNAME=Root.PgeApplications'
    search_url = 'https://www.public.surreyheath-online.gov.uk/whalecom60b1ef305f59f921/whalecom0/Scripts/PlanningPagesOnline/acolnetcgi.gov?ACTION=UNWRAP&RIPNAME=Root.pgesearch'
    applic_url = 'https://www.public.surreyheath-online.gov.uk/whalecom60b1ef305f59f921/whalecom0/Scripts/PlanningPagesOnline/acolnetcgi.gov?ACTION=UNWRAP&RIPNAME=Root.PgeResultDetail'

    first_page = True # only first page access requires page replace
    scrape_replace = 'window.location.replace(" {{ replace }} ");'
    scrape_action = ' action="{{ action|abs }}" '
    subs = {
        r'<script\s.*?</script>': r'',
        r'onSubmit=""return ValidateSearch\(\)""': r'onSubmit="return ValidateSearch()"',
        }
    scrape_next = '<a id="lnkPageNext" href=" {{ next_link }} "> </a>'
    scrape_max = '<table class="pagetitle"> {{ max_recs }} Results </table>'
    scrape_ids = """
    <div id="contentcol">
    {* <table class="results-table">
    <tr> <td class="casenumber"> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td> </tr>
    </table> *}
    </div>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <table id="details-table"> {{ block|html }} </table>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <th> Application Number </th> <td> {{ uid }} </td>
    <th> Registration (Validation) Date </th> <td> {{ date_validated }} </td>
    <th> Location </th> <td> {{ address }} </td>
    <th> Proposal </th> <td> {{ description }} </td>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<th> Date Received </th> <td> {{ date_received }} </td>',
    "<th> Application Number </th> <td> {{ reference }} </td>",
    "<th> Registration </th> <td> {{ date_validated }} </td>",
    "<th> Statutory Start </th> <td> {{ date_validated }} </td>",
    "<th> Application Type </th> <td> {{ application_type }} </td>",
    "<th> Case Officer </th> <td> {{ case_officer }} </td>",
    "<th> Decision Level </th> <td> {{ decided_by }} </td>",
    "<th> Appeal Received Date </th> <td> {{ appeal_date }} </td>",
    "<th> Target Date for Decision </th> <td> {{ target_decision_date }} </td>",
    "<th> Appeal Decision </th> <td> {{ appeal_result }} </td>",
    "<th> Earliest Decision Date </th> <td> {{ consultation_end_date }} </td>",
    "<th> Consultation Period Expires </th> <td> {{ consultation_end_date }} </td>",
    "<th> Consultation Period Ends </th> <td> {{ consultation_end_date }} </td>",
    "<th> Status </th> <td> {{ status }} </td>",
    "<th> Parish </th> <td> {{ parish }} </td>",
    "<th> Ward </th> <td> {{ ward_name }} </td>",
    "<th> Comments </th> <td> {{ comment_date }} </td>",
    "<th> Applicant </th> <td> {{ applicant_name }} </td>",
    "<th> Consultation Start Date </th> <td> {{ consultation_start_date }} </td>",
    "<th> Consultation Period Starts </th> <td> {{ consultation_start_date }} </td>",
    "<th> Date from when comments </th> <td> {{ consultation_start_date }} </td>",
    "<th> Site Notice Date </th> <td> {{ site_notice_start_date }} </td>",
    "<th> Date Decision Made </th> <td> {{ decision_date }} </td>",
    "<th> Agent </th> <td> {{ agent_name }} </td>",
    "<th> Date Decision Despatched </th> <td> {{ decision_issued_date }} </td> <th> Decision </th> <td> {{ decision }} </td>",
    "<th> Decision Issued </th> <td> {{ decision_issued_date }} </td>",
    "<th> Meeting Date </th> <td> {{ meeting_date }} </td>",
    "<th> Committee </th> <td> {{ meeting_date }} </td>",
    "<th> Appeal Received Date </th> <td> {{ appeal_date }} </td>",
    "<tr> <th> Easting/Northing </th> <td> {{ easting }}/{{ northing }} </td> </tr>",
    "<th> Agent </th> <td /> {* <td> {{ [agent_address] }} </td> *} <th> Applicant </th>",
    "<th> Applicant </th> <td /> {* <td> {{ [applicant_address] }} </td> *} <th> Date </th>",
    ]

    def __init__(self, table_name = None):
        base.ListScraper.__init__(self, table_name)
        if self.ck:
            util.set_cookie(self.cj, self.ck['name'], self.ck['value'], self.ck.get('domain'), self.ck.get('path', '/'))   

    """def get_id_batch (self, date_from, date_to): 

        response = util.open_url(self.br, self.search_url)
        html = response.read()
        if self.DEBUG: print "search page:", html

        result = scrapemark.scrape(self.scrape_replace, html)
        response = util.open_url(self.br, result['replace'], )
        response = self.br.response()  # adjust bad html
        html = response.get_data()
        if self.DEBUG: print "html pre sub:", html
        for k, v in self.subs.items():
            html = re.sub(k, v, html, 0, re.U|re.S|re.I) # unicode|dot matches new line|ignore case
        if self.DEBUG: print "html post sub:", html
        response.set_data(html)
        self.br.set_response(response)

        html = response.read()
        url = response.geturl()
        if self.DEBUG: print "form page:", html
        result = scrapemark.scrape(self.scrape_action, html, url)
        print result

        #self.br.set_handle_referer(False)
        #self.HEADERS['Referer'] = self.start_url
        #self.br.addheaders = self.HEADERS.items()

        #fields = self.search_fields
        fields = {}
        fields[self.date_from_field] = date_from.strftime(self.request_date_format)
        fields[self.date_to_field] = date_to.strftime(self.request_date_format)
        util.setup_form(self.br, self.search_form, fields)

        #response = util.open_url(self.br, result['action'], fields)
        #request = urllib2.Request(result['action'])
        #request.add_header('Accept', 'text/html')
        #opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj), MultipartPostHandler)
        #response = opener.open(request, urllib.urlencode(fields))

        if self.DEBUG: print "form:", self.br.form
        response = util.submit_form(self.br)

        html = response.read()
        url = response.geturl()
        if self.DEBUG: print "result page:", url, html
        result = scrapemark.scrape(self.scrape_max, html, url)
        try:
            max_recs = int(result['max_recs'])
        except:
            max_recs = 0
        
        final_result = []
        while response and len(final_result) < max_recs:
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
                html = response.read()
                url = response.geturl()
                if self.DEBUG: print "next page:", html
            else:
                break

        return final_result"""

    # NB if move_forward is true, we scrape forwards from rec_start, otherwise we scrape backwards
    def get_id_records2 (self, rec_start, move_forward):
        final_result = []
        num_from = None
        num_to = None
        bad_count = 0
        current_rec = rec_start
        fields = {}
        first_good_rec = None
        last_good_rec = None
        while len(final_result) < self.MAX_ID_BATCH and bad_count < 10:
            if self.DEBUG: print 'Record:', current_rec
            this_url = self.applic_url + '&TheSystemkey=' + str(current_rec)
            response = util.open_url(self.br, this_url)
            if response:
                html = response.read()
                if self.DEBUG: print 'Html:', html
                if self.first_page:
                    result = scrapemark.scrape(self.scrape_replace, html)
                    response = util.open_url(self.br, result['replace'], )
                    html = response.read()
                    self.first_page = False
                result = scrapemark.scrape(self.scrape_min_data, html)
                if result and result.get('uid'):
                    if not first_good_rec: first_good_rec = current_rec
                    last_good_rec = current_rec
                    if self.DEBUG: print result
                    final_result.append( { 'url': this_url, 'uid': str(current_rec) } ) # temporarily sets uid to thesystemkey
                    bad_count = 0
                else:
                    bad_count += 1
            else:
                bad_count += 1
            if move_forward:
                current_rec += 1
            else:
                current_rec -= 1
        if final_result:
            self.clean_ids(final_result)
            if move_forward:
                num_from = first_good_rec
                num_to = last_good_rec
            else:
                num_to = first_good_rec
                num_from = last_good_rec
        return final_result, num_from, num_to

    def get_detail_from_url (self, url):
        try: 
            response = util.open_url(self.br, url)
            html = response.read()
            if self.DEBUG: print "start page:", html
    
            if self.first_page:
                result = scrapemark.scrape(self.scrape_replace, html)
                response = util.open_url(self.br, result['replace'], )
                html = response.read()
                self.first_page = False

            url = response.geturl()
        except:
            if self.DEBUG: raise
            else: return None
        return self.get_detail(html, url)

    # note only works if the 'uid' is set temporarily to the systemkey
    def get_detail_from_uid (self, uid):
        url = self.applic_url + '&TheSystemkey=' + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

class Callable:
    def __init__(self, anycallable):
        self.__call__ = anycallable

# Controls how sequences are uncoded. If true, elements may be given multiple values by
#  assigning a sequence.
doseq = 1

class MultipartPostHandler(urllib2.BaseHandler):

    handler_order = urllib2.HTTPHandler.handler_order - 10 # needs to run first

    def http_request(self, request):
        data = request.get_data()
        if data is not None and type(data) != str:
            v_files = []
            v_vars = []
            try:
                 for(key, value) in data.items():
                    if type(value) == file:
                         v_files.append((key, value))
                    else:
                         v_vars.append((key, value))
            except TypeError:
                systype, value, traceback = sys.exc_info()
                raise TypeError, "not a valid non-string sequence or mapping object", traceback

            if len(v_files) == 0:
                data = urllib.urlencode(v_vars, doseq)
            else:
                boundary, data = self.multipart_encode(v_vars, v_files)

                contenttype = 'multipart/form-data; boundary=%s' % boundary
                if(request.has_header('Content-Type')
                   and request.get_header('Content-Type').find('multipart/form-data') != 0):
                    print "Replacing %s with %s" % (request.get_header('content-type'), 'multipart/form-data')
                request.add_unredirected_header('Content-Type', contenttype)

            request.add_data(data)
        
        return request

    def multipart_encode(vars, files, boundary = None, buf = None):
        if boundary is None:
            boundary = mimetools.choose_boundary()
        if buf is None:
            buf = StringIO()
        for(key, value) in vars:
            buf.write('--%s\r\n' % boundary)
            buf.write('Content-Disposition: form-data; name="%s"' % key)
            buf.write('\r\n\r\n' + value + '\r\n')
        for(key, fd) in files:
            file_size = os.fstat(fd.fileno())[stat.ST_SIZE]
            filename = fd.name.split('/')[-1]
            contenttype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
            buf.write('--%s\r\n' % boundary)
            buf.write('Content-Disposition: form-data; name="%s"; filename="%s"\r\n' % (key, filename))
            buf.write('Content-Type: %s\r\n' % contenttype)
            # buffer += 'Content-Length: %s\r\n' % file_size
            fd.seek(0)
            buf.write('\r\n' + fd.read() + '\r\n')
        buf.write('--' + boundary + '--\r\n\r\n')
        buf = buf.getvalue()
        return boundary, buf

    multipart_encode = Callable(multipart_encode)

    https_request = http_request

if __name__ == 'scraper':

    scraper = SurreyHeathScraper()
    scraper.run()

    # misc tests
    #scraper.DEBUG = True
    #scraper.br.set_debug_http(True)
    #print scraper.get_detail_from_uid ('12/0111')
    #print scraper.get_detail_from_uid('29743')
    #print scraper.get_detail_from_uid ('31391')
    #print scraper.get_detail_from_uid ('31372')
    #res = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('18/08/2011'))
    #print len(res), res
    #result = scraper.get_id_records2(15000, True)
    #print result, len(result)
    #print scraper.gather_ids('2012-02-01')
    #print scraper.gather_ids('2011-02-01', '2012-01-18')

