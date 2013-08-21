# this is a scraper of Isle of Wight planning applications for use by Openly Local

# works from one long sequence - no date query

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

class IsleOfWightScraper(base.ListScraper):

    START_SEQUENCE = 18000 # gathering back to this "frmId" record number
    MAX_ID_BATCH = 200 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 100 # max application details to scrape in one go
    MIN_RECS = 60
    ID_ORDER = 'url desc'
    PIN_REGEX = re.compile(r'P/\d\d\d\d\d/\d\d')
    TCP_REGEX = re.compile(r'TCP/\d\d\d\d\d/\w')

    search_form = '0'
    search_submit = None
    form_fields = { '__EVENTTARGET': 'lnkShowAll', '__EVENTARGUMENT': '', 'btnSearch': None, }
    find_fields = { '__EVENTTARGET': '', '__EVENTARGUMENT': '', 'txtPIN': '' }
    search_url = 'http://www.iwight.com/planning/planAppSearch.aspx'
    applic_url = 'http://www.iwight.com/planning/AppDetails3.aspx'
    scrape_ids = """
    <table id="dgResults"> <tr />
        {* <tr>
            <td> <a href="{{ [records].url|abs }}"> </a> </td>
         </tr> *}
    </table>
    """
    scrape_link = """
        <tr class="dbResults"> 
            <a href="{{ link|abs }}"> </a> 
        </tr>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <form id="Form1"> {{ block|html }} </form>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <span id="lblAppNo"> {{ uid }} </span>
    <span id="lblLocation"> {{ address }} </span>
    <span id="lblProposal"> {{ description }} </span>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<span id="lblTrackRecievedDate"> {{ date_received }} </span>',
    '<span id="lblTrackRegDate"> {{ date_validated }} </span>',
    '<span id="lblAppNo"> {{ reference }} </span>',
    '<span id="lblTrackConsultStart"> {{ consultation_start_date }} </span>',
    '<span id="lblTrackConsultEnd"> {{ consultation_end_date }} </span>',
    '<span id="lblofficer"> {{ case_officer }} </span>',
    '<span id="lblTrackDecisionDate"> {{ decision_date }} </span>',
    '<span id="lblTrackAppealDate"> {{ appeal_date }} </span>',
    '<span id="lblWard"> {{ ward_name }} </span>',
    '<span id="lblParish"> {{ parish }} </span>',
    '<span id="lblCurrentStatus"> {{ status|html }} </span>',
    '<span id="lblAgent"> {{ agent_name }} <br> {{ agent_address }} <br> {{ agent_tel }} </span>',
    '<span id="lblDecisionNotice"> {{ decision|html }} </span>',
    '<span id="lblTrackAppealDate"> {{ appeal_date }} </span>',
    '<span id="lblTrackAppealDecisionDate"> {{ appeal_decision_date }} </span>',
    '<span id="lblCommitteeDate"> {{ meeting_date }} </span>',
    '<span id="lblPubDate"> {{ last_advertised_date }} </span>',
    '<span id="lblcommentsby"> {{ comment_date }} </span>',
    '<span id="lblEN"> {{ easting }} / {{ northing }} </span>',
    '<a id="lnkMakeComment" href="{{ comment_url|abs }}"> </a>',
    ]

    # The search page only gets a limited list of currently active applications
    # we use it to get the maximum possible frmId value (num_recs)
    # for older records we just assume there is a continuous sequential list of "frmIds" from START_SEQUENCE up to num_recs
    # NB if both are None, it's the first ever scrape
    # NB if rec_to is None, rec_from is the highest existing record and it's a current scrape
    # NB also if rec_to is None, the default should be to try to get at least self.MIN_RECS records
    def get_id_records (self, rec_from, rec_to = None):
        final_result = []
        num_from = None
        num_to = None

        response = util.open_url(self.br, self.search_url)
        util.setup_form(self.br, self.search_form, self.form_fields)
        response = util.submit_form(self.br, self.search_submit)

        html = response.read()
        url = response.geturl()
        result = scrapemark.scrape(self.scrape_ids, html, url)
        
        if result and result.get('records'):

            num_recs = 0
            for i in result['records']:
                i['uid'] = i['url'].replace(self.applic_url+'?frmId=', '')
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
    
            if rec_to > num_recs:
                rec_to = num_recs
            if (rec_to - rec_from + 1) > self.MAX_ID_BATCH:
                rec_from = rec_to - self.MAX_ID_BATCH + 1

            for i in range(rec_from, rec_to + 1):
                final_result.append( { 'url': self.applic_url+'?frmId='+str(i), 'uid': str(i) } )
            num_from = rec_from
            num_to = rec_to

        return final_result, num_from, num_to

    # NB if move_forward is true, we scrape forwards from rec_start, otherwise we scrape backwards
    def get_id_records2 (self, rec_start, move_forward):
        final_result = []
        num_from = None
        num_to = None
        num_recs = self.get_max_sequence()
        if num_recs:
            if not rec_start:
                num_from = self.START_SEQUENCE
                num_to = num_recs
            elif move_forward:
                num_from = rec_start
                num_to = num_recs
            else:    
                num_from = self.START_SEQUENCE
                num_to = rec_start
            if num_to > num_recs:
                num_to = num_recs
            if (num_to - num_from + 1) > self.MAX_ID_BATCH:
                if not move_forward:
                    num_from = num_to - self.MAX_ID_BATCH + 1
                else:
                    num_to = num_from + self.MAX_ID_BATCH - 1
            for i in range(num_from, num_to + 1):
                final_result.append( { 'url': self.applic_url+'?frmId='+str(i), 'uid': str(i) } )
        return final_result, num_from, num_to

    def get_max_sequence (self):
        max_recs = scraperwiki.sqlite.get_var(self.DATA_END_MARKER)
        response = util.open_url(self.br, self.search_url)
        if self.DEBUG: print response.read()
        util.setup_form(self.br, self.search_form, self.form_fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br, self.search_submit)
        if response:
            html = response.read()
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                num_recs = 0
                for i in result['records']:
                    i['uid'] = i['url'].replace(self.applic_url+'?frmId=', '')
                    i['uid'] = util.GAPS_REGEX.sub('', i['uid'])
                    num = int(i['uid'])
                    if num > num_recs: num_recs = num
                if self.DEBUG: print 'Number of records', num_recs
                if num_recs > 0:
                    max_recs = num_recs
        return max_recs

    # the uid can be a numeric "frmId", a PIN number - P/-----/-- or a TCP number - TCP/-----/-
    def get_detail_from_uid (self, uid):
        if uid.isdigit():
            url = self.applic_url + '?frmId=' + urllib.quote_plus(uid)
        else:
            pin_match = self.PIN_REGEX.search(uid)
            if pin_match:
                self.find_fields['txtPIN'] = pin_match.group()
                self.find_fields['txtTCP'] = ''
            else:
                tcp_match = self.TCP_REGEX.search(uid)
                if tcp_match:
                    self.find_fields['txtPIN'] = ''
                    self.find_fields['txtTCP'] = tcp_match.group()
                else:
                    return None
            response = util.open_url(self.br, self.search_url)
            util.setup_form(self.br, self.search_form, self.find_fields)
            response = util.submit_form(self.br)
            try:
                html = response.read()
                url = response.geturl()
                result = scrapemark.scrape(self.scrape_link, html, url)
                url = result['link']
            except:
                return None
        return self.get_detail_from_url(url)


    # use the parent method to fetch and store the details of one application
    # However in this scraper the uid can change to the P/ or TCP/ form
    # so it may have to erase any previous record which has the previous frmId numeric form
    def update_application_detail(self, applic):
        old_uid = applic['uid']
        if base.BaseScraper.update_application_detail(self, applic):
            if old_uid.isdigit() and old_uid != applic['uid']:
                #print "new id:", applic['uid']
                #print "delete from " + self.TABLE_NAME + " where uid = '" + old_uid + "'"
                scraperwiki.sqlite.execute("delete from " + self.TABLE_NAME + " where uid = '" + old_uid + "'")
                scraperwiki.sqlite.commit()
            return True
        else:
            return False
            
if __name__ == 'scraper':

    scraper = IsleOfWightScraper()

    #scraper.DEBUG = True
    scraper.run()
    
    # misc tests
    #print scraper.get_detail_from_uid ('TCP/18456/H,P/00467/12')
    #print scraper.get_detail_from_uid ('24669')
    #print scraper.get_detail_from_uid ('19455')
    #result = scraper.get_id_records2(24669, True)
    #print result
    #print scraper.gather_ids(None, None)
    #scraper.gather_current_ids()
    
    #current_applications = scraperwiki.sqlite.select("uid, url from " + scraper.TABLE_NAME + " where date_scraped is not null and uid not like '%/%' limit 100")
    #print "N of old ids to be updated", len(current_applications)
    #for applic in current_applications:
    #    scraper.update_application_detail(applic)

    #util.rename_column('swdata', 'ward', 'ward_name')

