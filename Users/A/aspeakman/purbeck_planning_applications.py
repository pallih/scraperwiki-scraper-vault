# this is a scraper of Purbeck planning applications for use by Openly Local

# works from the sequence of record numbers 

# date box is not for searching, only limits it to records received since a date - default = 1 year ago

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import urllib
import copy

base = scraperwiki.utils.swimport("openlylocal_base_scraper")
scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")

class PurbeckScraper(base.ListScraper):

    START_SEQUENCE = 24500 # gathering back to this record number
    MAX_ID_BATCH = 175 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 125 # max application details to scrape in one go
    ID_ORDER = 'url desc'

    search_form = '1'
    date_field = 'ctl00$MainContent$dpReceivedSince$dateInput'
    request_date_format = '%Y-%m-%d-00-00-00'
    ref_field = 'ctl00$MainContent$txtAppNum'
    search_url = 'http://planningsearch.purbeck-dc.gov.uk/PlanAppSrch.aspx'
    applic_url = 'http://planningsearch.purbeck-dc.gov.uk/PlanAppDisp.aspx'
    scrape_ids = """
    <div id="news_results_list">
    {* <table> <tr>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    </tr> </table> *}
    </div>
    """
    next_button = 'ctl00$MainContent$lvResults$pager$ctl02$NextButton'
    scrape_max = """
    <div class="rdpWrap"> Page 1 of {{ max_pages }} </div>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <form id="form1"> {{ block|html }} </form>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <input id="MainContent_txtApplNum" value="{{ reference }}">
    <textarea id="MainContent_txtLocation"> {{ address }} </textarea>
    <textarea id="MainContent_txtProposal"> {{ description }} </textarea>
    <input id="MainContent_txtRegDate" value="{{ date_validated }}">
    <input id="MainContent_txtReceivedDate" value="{{ date_received }}">
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<input id="MainContent_txtCurrentStatus" value="{{ status }}">',
    '<input id="MainContent_txtEasting" value="{{ easting }}">',
    '<input id="MainContent_txtNorthing" value="{{ northing }}">',
    '<input id="MainContent_txtApplName" value="{{ applicant_name }}">',
    '<input id="MainContent_txtAgentsName" value="{{ agent_name }}">',
    '<textarea id="MainContent_txtApplicantsAddr"> {{ applicant_address }} </textarea>',
    '<textarea id="MainContent_txtAgentsAddress"> {{ agent_address }} </textarea>',
    '<input id="MainContent_txtDecisionDueBy" value="{{ target_decision_date }}">',
    '<input id="MainContent_txtApplType" value="{{ application_type }}">',
    '<input id="MainContent_txtParish" value="{{ parish }}">',
    '<input id="MainContent_txtNeighbourLettersSent" value="{{ neighbour_consultation_start_date }}">',
    '<input id="MainContent_txtNeighbourConsultationCloses" value="{{ neighbour_consultation_end_date }}">',
    '<input id="MainContent_txtDescisionOnApp" value="{{ decision }}">',
    '<input id="MainContent_txtDecisionDate" value="{{ decision_date }}">',
    '<textarea id="MainContent_txtDealtWithBy"> {{ case_officer }} </textarea>',
    '<input id="MainContent_txtPlanningBoardDate" value="{{ meeting_date }}">',
    ]

    # NB if both are None, it's the first ever scrape
    # NB if rec_to is None, rec_from is the highest existing record and it's a current scrape
    # NB also if rec_to is None, the default should be to try to get at least self.MIN_RECS records
    def get_id_records (self, rec_from, rec_to = None):
        final_result = []
        num_from = None
        num_to = None

        to_date = date.today() - timedelta(days=14)
        response = util.open_url(self.br, self.search_url)
        fields = { self.ref_field: '', self.date_field: to_date.strftime(self.request_date_format) }
        util.setup_form(self.br, self.search_form, fields)
        response = util.submit_form(self.br)
        html = response.read()
        url = response.geturl()
        result = scrapemark.scrape(self.scrape_ids, html, url)

        if result and result.get('records'):

            num_recs = 0
            for i in result['records']:
                i['uid'] = i['url'].replace(self.applic_url+'?recno=', '')
                i['uid'] = util.GAPS_REGEX.sub('', i['uid'])
                num = int(i['uid'])
                if num > num_recs: num_recs = num
            if self.DEBUG: print 'Number of records', num_recs
    
            if not rec_from and not rec_to:
                rec_from = self.START_SEQUENCE
                rec_to = num_recs       
            elif not rec_to:
                rec_to = num_recs
                rec_from -= self.MIN_RECS
    
            if self.DEBUG: print 'Looking for records: ', rec_from, rec_to
            
            current_rec = rec_to
            top_page = None
            bot_page = None
            fields = {}
            while current_rec >= rec_from and len(final_result) < self.MAX_ID_BATCH:
                current_appno = str(current_rec)
                if self.DEBUG: print 'On page:', current_appno
                this_url = self.applic_url + '?recno=' + current_appno
                response = util.open_url(self.br, this_url)
                if response:
                    html = response.read()
                    url = response.geturl()
                    if self.DEBUG: print 'Html:', html
                    result = scrapemark.scrape(self.scrape_min_data, html, url)
                    if result and result.get('reference'):
                        if not top_page: top_page = current_appno
                        bot_page = current_appno
                        if self.DEBUG: print result
                        uid = util.GAPS_REGEX.sub('', result['reference'])
                        final_result.append( { 'url': this_url, 'uid': uid } )
                        if self.DEBUG: print 'Output N: ', len(final_result)
                current_rec -= 1
                
        if final_result:
            if self.DEBUG: print bot_page, top_page
            num_from = int(bot_page)
            num_to = int(top_page)
        return final_result, num_from, num_to

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
            this_url = self.applic_url + '?recno=' + str(current_rec)
            response = util.open_url(self.br, this_url)
            if response:
                html = response.read()
                url = response.geturl()
                if self.DEBUG: print 'Html:', html
                result = scrapemark.scrape(self.scrape_min_data, html, url)
                if result and result.get('reference'):
                    if not first_good_rec: first_good_rec = current_rec
                    last_good_rec = current_rec
                    if self.DEBUG: print result
                    uid = util.GAPS_REGEX.sub('', result['reference'])
                    final_result.append( { 'url': this_url, 'uid': uid } )
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

    def get_max_sequence (self):
        max_recs = scraperwiki.sqlite.get_var(self.DATA_END_MARKER)
        to_date = date.today() - timedelta(days=14)
        response = util.open_url(self.br, self.search_url)
        fields = { self.ref_field: '', self.date_field: to_date.strftime(self.request_date_format) }
        util.setup_form(self.br, self.search_form, fields)
        response = util.submit_form(self.br)
        html = response.read()
        url = response.geturl()
        result = scrapemark.scrape(self.scrape_ids, html, url)
        if result and result.get('records'):
            num_recs = 0
            for i in result['records']:
                i['uid'] = i['url'].replace(self.applic_url+'?recno=', '')
                i['uid'] = util.GAPS_REGEX.sub('', i['uid'])
                num = int(i['uid'])
                if num > num_recs: num_recs = num
            if self.DEBUG: print 'Number of records', num_recs
            if num_recs > 0:
                max_recs = num_recs
        return max_recs

    def get_detail_from_uid (self, uid):

        response = util.open_url(self.br, self.search_url)
        fields = { self.ref_field: uid, self.date_field: '' }
        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br)

        try:
            html = response.read()
            if self.DEBUG: print html
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            self.clean_ids(result['records'])
            url = result['records'][0]['url']
        except:
            return None

        return self.get_detail_from_url(url)
            
if __name__ == 'scraper':
    
    #scraperwiki.sqlite.execute("create table swdata (`url` text, `uid` text) ")
    #scraperwiki.sqlite.commit()
    #scraperwiki.sqlite.execute("drop table if exists swdata")
    #scraperwiki.sqlite.commit()

    scraper = PurbeckScraper()
    #scraper.reset()

    #scraper.DEBUG = True
    scraper.run()
    
    # misc tests
    #print scraper.get_detail_from_uid ('6/2000/0015')
    #result = scraper.get_id_records(20050000, 20120050)
    #result = scraper.get_id_records(None)
    #print result
    
    


