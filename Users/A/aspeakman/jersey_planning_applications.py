# this is a scraper of Jersey planning applications

# now based on JSON API which does not seem to work externally

# so converted to a list scraper using uids in this form X/YYYY/NNNN where X is in A,S,SSI,P,PP,RC,RP,RW

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import random
import urllib, urllib2
import json

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

#class JerseyScraper(base.DateScraper):
class JerseyScraper(base.ListScraper):

    START_SEQUENCE = 20000000 # gathering back to this record number (in YYYYNNNN format derived from the application number in this format = X/YYYY/NNNN)
    START_POINT = (date.today().year * 10000) + 1
    MAX_ID_BATCH = 200 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 150 # max application details to scrape in one go

    # old dates set up - still works
    #search_url = 'http://webapps.gov.je/Planning/PlanningApplicationSearch.aspx'
    #date_from_field = 'ApplicationDateFromHTMLInputText'
    #date_to_field = 'ApplicationDateToHTMLInputText'
    #ref_field = 'CaseNo'
    #scrape_next_link = '<a href="{{ next_link }}"> Next </a>'
    #request_date_format = '%d/%m/%Y'
    #search_form = 'Form1'

    # new dates set up - not working
    search_url = 'https://www.mygov.je/Planning/Pages/Planning.aspx'
    search_form = 'aspnetForm'
    request_date_format = '%-d/%-m/%Y'
    date_from_fields = { 'day': 'ctl00$SPWebPartManager1$g_717cf524_fe11_474e_b9ab_cc818a5fede9$ctl00$ddlFromDay', 
                        'month': 'ctl00$SPWebPartManager1$g_717cf524_fe11_474e_b9ab_cc818a5fede9$ctl00$ddlFromMonth', 
                        'year': 'ctl00$SPWebPartManager1$g_717cf524_fe11_474e_b9ab_cc818a5fede9$ctl00$ddlFromYear', }
    date_to_fields = { 'day': 'ctl00$SPWebPartManager1$g_717cf524_fe11_474e_b9ab_cc818a5fede9$ctl00$ddlToDay',
                        'month': 'ctl00$SPWebPartManager1$g_717cf524_fe11_474e_b9ab_cc818a5fede9$ctl00$ddlToMonth',
                        'year': 'ctl00$SPWebPartManager1$g_717cf524_fe11_474e_b9ab_cc818a5fede9$ctl00$ddlToYear', }
    search_fields = {
        '__EVENTTARGET': 'ctl00$SPWebPartManager1$g_717cf524_fe11_474e_b9ab_cc818a5fede9$ctl00$btnPlanningApplicationSearchSubmit',
        '__EVENTARGUMENT': '' }
    scrape_ids = """
    <table id="PlanningApplicationSearchResultASPPanel"> <table>
    {* <table>
    <tr> <td> {{ [records].uid }} </td> </tr>
    <tr> <td /> <td> <a href="{{ [records].url|abs }}"> </a> </td> </tr>
    </table> *}
    </table>
    """

    applic_url = 'https://www.mygov.je/Planning/Pages/PlanningApplicationDetail.aspx?s=1&r='
    scrape_dates_link = '<a href="{{ dates_link|abs }}"> Application timeline </a>'

    prefixes = [ 'P', 'A', 'RC', 'RP', 'RW', 'S', 'PP', 'SSI' ]
    scrape_id = '<div class="pln-maincontent"> <th> Application Reference </th> <td> {{ uid }} </td> </div>'
    scrape_data_block = '<div class="pln-maincontent"> {{ block|html }} </div>'
    scrape_dates_block = '<div class="pln-maincontent"> {{ block|html }} </div>'
    scrape_min_data = """
    <th> Application Reference </th> <td> {{ reference }} </td>
    <th> Description </th> <td> {{ description }} </td>
    <th> Property Name </th> <td> {{ [address] }} </td>
    <th> Road Name </th> <td> {{ [address] }} </td>
    <th> Parish </th> <td> {{ [address] }} </td>
    <th> Postcode </th> <td> {{ [address] }} </td>
    """
    scrape_min_dates = """
    <tr> <th> Validated Date </th> <td> {{ date_validated }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr> <th> Officer Responsible </th> <td> {{ case_officer }} </td> </tr>',
    '<tr> <th> Status </th> <td> {{ status }} </td> </tr>',
    '<tr> <th> Parish </th> <td> {{ parish }} </td> </tr>',
    '<tr> <th> Postcode </th> <td> {{ postcode }} </td> </tr>',
    '<tr> <th> Applicant </th> <td> {{ applicant_name }} , {{ applicant_address }} </td> </tr>',
    '<tr> <th> Agent </th> <td> {{ agent_name }} </td> </tr>',
    #'<tr> <th> Constraints </th> <td> {{ constraints }} </td> </tr>',
    '<tr> <th> Agent </th> <td> {{ agent_name }} , {{ agent_address }} </td> </tr>',
    ]
    scrape_optional_dates = [
    '<tr> <th> Advertised Date  </th> <td> {{ last_advertised_date }} </td> </tr>',
    '<tr> <th> End Publicity Date </th> <td> {{ consultation_end_date }} </td> </tr>',
    '<tr> <th> Committee Date  </th> <td> {{ meeting_date }} </td> </tr>',
    '<tr> <th> Decision Date </th> <td> {{ decision_date }} </td> </tr>',
    '<tr> <th> Appeal Date </th> <td> {{ appeal_date }} </td> </tr>',
    ]

    # only for dates setup - not working in list scraper
    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)
        print response.read()

        #fields = { }
        #fields [self.date_from_field] = date_from.strftime(self.request_date_format)
        #fields [self.date_to_field] = date_to.strftime(self.request_date_format)

        fields = self.search_fields
        date_from = date_from.strftime(self.request_date_format)
        date_parts = date_from.split('/')
        fields [self.date_from_fields['day']] = date_parts[0]
        fields [self.date_from_fields['month']] = date_parts[1]
        fields [self.date_from_fields['year']] = date_parts[2]
        date_to = date_to.strftime(self.request_date_format)
        date_parts = date_to.split('/')
        fields [self.date_to_fields['day']] = date_parts[0]
        fields [self.date_to_fields['month']] = date_parts[1]
        fields [self.date_to_fields['year']] = date_parts[2]

        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br)
        
        final_result = []
        while response:
            url = response.geturl()
            html = response.read()
            if self.DEBUG: print html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            else:
                break
            try:
                result = scrapemark.scrape(self.scrape_next_link, html, url)
                next_link = result['next_link']
                response = self.br.open(next_link)
            except:
                break
            
        return final_result

    # NB if both are None, it's the first ever scrape
    # NB if rec_to is None, rec_from is the highest existing record and it's a current scrape
    # NB also if rec_to is None, the default should be to try to get at least self.MIN_RECS records
    def get_id_records (self, rec_from, rec_to = None):
        final_result = []
        num_from = None
        num_to = None

        if not rec_from and not rec_to:
            rec_from = self.START_SEQUENCE
            rec_to = (date.today().year * 10000) + 9999 # last possible record of the current year        
        elif not rec_to:
            rec_to = rec_from + self.MIN_RECS # set target after highest current record to get any recent records
            min_rec_to = (date.today().year * 10000) + self.MIN_RECS # first possible record of the current year
            if rec_to < min_rec_to: rec_to = min_rec_to
            rec_from -= self.MIN_RECS

        if self.DEBUG: print 'Looking for records: ', rec_from, rec_to
        
        current_rec = rec_to
        top_page = None
        bot_page = None
        while current_rec >= rec_from and len(final_result) < self.MAX_ID_BATCH:
            current_page = str(current_rec)[4:8]
            if int(current_page) < 1900: # only testing for max 1900 applications per year (potentially there are 9999)
                
                for prefix in self.prefixes:
                    current_appno = prefix + '/' + str(current_rec)[0:4] + '/' + current_page
                    if self.DEBUG: print 'Testing page:', current_appno
                    url = self.applic_url + urllib.quote_plus(current_appno)
                    response = self.br.open(url)
                    if response:
                        html = response.read()
                        if self.DEBUG: print 'Html:', html
                        result = scrapemark.scrape(self.scrape_id, html)
                        if result and result.get('uid'):
                            if not top_page: top_page = current_appno
                            bot_page = current_appno
                            result['url'] = url
                            if self.DEBUG: print result
                            final_result.append(result)
                            break

            current_rec -= 1
                
        if final_result:
            if self.DEBUG: print bot_page, top_page
            bot_parts = bot_page.split('/')
            num_from = int(bot_parts[1])
            num_from = (num_from * 10000) + int(bot_parts[2])
            top_parts = top_page.split('/')
            num_to = int(top_parts[1])
            num_to = (num_to * 10000) + int(top_parts[2])
        return final_result, num_from, num_to

    # NB if move_forward is true, we scrape forwards from rec_start, otherwise we scrape backwards
    def get_id_records2 (self, rec_start, move_forward):
        final_result = []
        num_from = None
        num_to = None
        bad_count = 0
        find_bad = True
        current_rec = rec_start
        first_good_rec = None
        last_good_rec = None
        fields = {}
        while len(final_result) < self.MAX_ID_BATCH and bad_count < 20:
            current_year = str(current_rec)[0:4]
            current_page = str(current_rec)[4:8]
            ok_got_it = False
            for prefix in self.prefixes:
                current_appno = prefix + '/' + current_year + '/' + current_page
                if self.DEBUG: print 'Record:', current_appno
                url = self.applic_url + urllib.quote_plus(current_appno)
                response = self.br.open(url)
                if response:
                    html = response.read()
                    if self.DEBUG: print 'Html:', html
                    result = scrapemark.scrape(self.scrape_id, html)
                    if result and result.get('uid'):
                        if not first_good_rec: first_good_rec = current_rec
                        last_good_rec = current_rec
                        result['url'] = url
                        if self.DEBUG: print result
                        final_result.append(result)
                        ok_got_it = True
                        break
            if ok_got_it: 
                bad_count = 0
                find_bad = True      
            elif find_bad: 
                bad_count += 1
            if move_forward:
                if bad_count == 10: # try the next year if moving forward and we reach 10 errors
                    current_rec = (int(current_year)+1)*10000
                else:
                    current_rec += 1
            else:
                if current_page == '0000': # if moving backward, swap to next year when reach zero
                    current_rec = ((int(current_year)-1)*10000)+1900 # expecting max 1900 applications per year (potentially 9999)
                    find_bad = False
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

    def get_detail_from_uid (self, uid):
        url = self.applic_url + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

    def get_detail_from_url (self, url):
        try:
            response = self.br.open(url)
            html = response.read()
            if self.DEBUG:
                    print "Html obtained from details url:", html
            this_url = response.geturl()
            if self.DEBUG: print "Url:", this_url
        except:
            return None
        
        result = self.get_detail(html, this_url)
        if result:
            try:
                temp_result = scrapemark.scrape(self.scrape_dates_link, html, this_url)
                dates_url = temp_result['dates_link'] 
                if self.DEBUG: print dates_url
                response = self.br.open(dates_url)
                html = response.read()
                url = response.geturl()
                if self.DEBUG:
                    print "Html obtained from dates url:", html
                result2 = self.get_detail(html, url, self.scrape_dates_block, self.scrape_min_dates, self.scrape_optional_dates)
                if result2:
                    result.update(result2)
            except:
                pass
        return result

if __name__ == 'scraper':

    scraper = JerseyScraper()
    scraper.run()

    # misc test calls
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('A/2011/1163')
    #result = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('08/09/2011'))
    #print len(result), result

    #result = scraper.get_id_records(20120040, 20120050)
    #result = scraper.get_id_records(20120709)
    #print result

    # test trying to access the JSON data source directly - think the parameters are correct 
    # but does not seem to work (times out) - presumably access to external data requests is forbidden?
    #request = urllib2.Request('https://www.mygov.je/_layouts/PlanningAjaxServices/PlanningSearch.svc/Search')
    #request.add_header('Content-Type', 'application/json; charset=utf-8')
    #url = 'https://www.mygov.je/Planning/Pages/Planning.aspx'
    #data = { 'URL': url,
    #    'CommonParameters': '|05|1||49.21042016382462|-2.1445659365234633|12',
    #    'SearchParameters': '|1301||||0|All|All|8|8|2011|8|9|2011' }
    #dd = json.dumps(data)
    #print dd
    #resp = urllib2.urlopen(request, dd, 30)
    #print resp.info()
    #print json.load(resp)


    




# this is a scraper of Jersey planning applications

# now based on JSON API which does not seem to work externally

# so converted to a list scraper using uids in this form X/YYYY/NNNN where X is in A,S,SSI,P,PP,RC,RP,RW

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import random
import urllib, urllib2
import json

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

#class JerseyScraper(base.DateScraper):
class JerseyScraper(base.ListScraper):

    START_SEQUENCE = 20000000 # gathering back to this record number (in YYYYNNNN format derived from the application number in this format = X/YYYY/NNNN)
    START_POINT = (date.today().year * 10000) + 1
    MAX_ID_BATCH = 200 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 150 # max application details to scrape in one go

    # old dates set up - still works
    #search_url = 'http://webapps.gov.je/Planning/PlanningApplicationSearch.aspx'
    #date_from_field = 'ApplicationDateFromHTMLInputText'
    #date_to_field = 'ApplicationDateToHTMLInputText'
    #ref_field = 'CaseNo'
    #scrape_next_link = '<a href="{{ next_link }}"> Next </a>'
    #request_date_format = '%d/%m/%Y'
    #search_form = 'Form1'

    # new dates set up - not working
    search_url = 'https://www.mygov.je/Planning/Pages/Planning.aspx'
    search_form = 'aspnetForm'
    request_date_format = '%-d/%-m/%Y'
    date_from_fields = { 'day': 'ctl00$SPWebPartManager1$g_717cf524_fe11_474e_b9ab_cc818a5fede9$ctl00$ddlFromDay', 
                        'month': 'ctl00$SPWebPartManager1$g_717cf524_fe11_474e_b9ab_cc818a5fede9$ctl00$ddlFromMonth', 
                        'year': 'ctl00$SPWebPartManager1$g_717cf524_fe11_474e_b9ab_cc818a5fede9$ctl00$ddlFromYear', }
    date_to_fields = { 'day': 'ctl00$SPWebPartManager1$g_717cf524_fe11_474e_b9ab_cc818a5fede9$ctl00$ddlToDay',
                        'month': 'ctl00$SPWebPartManager1$g_717cf524_fe11_474e_b9ab_cc818a5fede9$ctl00$ddlToMonth',
                        'year': 'ctl00$SPWebPartManager1$g_717cf524_fe11_474e_b9ab_cc818a5fede9$ctl00$ddlToYear', }
    search_fields = {
        '__EVENTTARGET': 'ctl00$SPWebPartManager1$g_717cf524_fe11_474e_b9ab_cc818a5fede9$ctl00$btnPlanningApplicationSearchSubmit',
        '__EVENTARGUMENT': '' }
    scrape_ids = """
    <table id="PlanningApplicationSearchResultASPPanel"> <table>
    {* <table>
    <tr> <td> {{ [records].uid }} </td> </tr>
    <tr> <td /> <td> <a href="{{ [records].url|abs }}"> </a> </td> </tr>
    </table> *}
    </table>
    """

    applic_url = 'https://www.mygov.je/Planning/Pages/PlanningApplicationDetail.aspx?s=1&r='
    scrape_dates_link = '<a href="{{ dates_link|abs }}"> Application timeline </a>'

    prefixes = [ 'P', 'A', 'RC', 'RP', 'RW', 'S', 'PP', 'SSI' ]
    scrape_id = '<div class="pln-maincontent"> <th> Application Reference </th> <td> {{ uid }} </td> </div>'
    scrape_data_block = '<div class="pln-maincontent"> {{ block|html }} </div>'
    scrape_dates_block = '<div class="pln-maincontent"> {{ block|html }} </div>'
    scrape_min_data = """
    <th> Application Reference </th> <td> {{ reference }} </td>
    <th> Description </th> <td> {{ description }} </td>
    <th> Property Name </th> <td> {{ [address] }} </td>
    <th> Road Name </th> <td> {{ [address] }} </td>
    <th> Parish </th> <td> {{ [address] }} </td>
    <th> Postcode </th> <td> {{ [address] }} </td>
    """
    scrape_min_dates = """
    <tr> <th> Validated Date </th> <td> {{ date_validated }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr> <th> Officer Responsible </th> <td> {{ case_officer }} </td> </tr>',
    '<tr> <th> Status </th> <td> {{ status }} </td> </tr>',
    '<tr> <th> Parish </th> <td> {{ parish }} </td> </tr>',
    '<tr> <th> Postcode </th> <td> {{ postcode }} </td> </tr>',
    '<tr> <th> Applicant </th> <td> {{ applicant_name }} , {{ applicant_address }} </td> </tr>',
    '<tr> <th> Agent </th> <td> {{ agent_name }} </td> </tr>',
    #'<tr> <th> Constraints </th> <td> {{ constraints }} </td> </tr>',
    '<tr> <th> Agent </th> <td> {{ agent_name }} , {{ agent_address }} </td> </tr>',
    ]
    scrape_optional_dates = [
    '<tr> <th> Advertised Date  </th> <td> {{ last_advertised_date }} </td> </tr>',
    '<tr> <th> End Publicity Date </th> <td> {{ consultation_end_date }} </td> </tr>',
    '<tr> <th> Committee Date  </th> <td> {{ meeting_date }} </td> </tr>',
    '<tr> <th> Decision Date </th> <td> {{ decision_date }} </td> </tr>',
    '<tr> <th> Appeal Date </th> <td> {{ appeal_date }} </td> </tr>',
    ]

    # only for dates setup - not working in list scraper
    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)
        print response.read()

        #fields = { }
        #fields [self.date_from_field] = date_from.strftime(self.request_date_format)
        #fields [self.date_to_field] = date_to.strftime(self.request_date_format)

        fields = self.search_fields
        date_from = date_from.strftime(self.request_date_format)
        date_parts = date_from.split('/')
        fields [self.date_from_fields['day']] = date_parts[0]
        fields [self.date_from_fields['month']] = date_parts[1]
        fields [self.date_from_fields['year']] = date_parts[2]
        date_to = date_to.strftime(self.request_date_format)
        date_parts = date_to.split('/')
        fields [self.date_to_fields['day']] = date_parts[0]
        fields [self.date_to_fields['month']] = date_parts[1]
        fields [self.date_to_fields['year']] = date_parts[2]

        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br)
        
        final_result = []
        while response:
            url = response.geturl()
            html = response.read()
            if self.DEBUG: print html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            else:
                break
            try:
                result = scrapemark.scrape(self.scrape_next_link, html, url)
                next_link = result['next_link']
                response = self.br.open(next_link)
            except:
                break
            
        return final_result

    # NB if both are None, it's the first ever scrape
    # NB if rec_to is None, rec_from is the highest existing record and it's a current scrape
    # NB also if rec_to is None, the default should be to try to get at least self.MIN_RECS records
    def get_id_records (self, rec_from, rec_to = None):
        final_result = []
        num_from = None
        num_to = None

        if not rec_from and not rec_to:
            rec_from = self.START_SEQUENCE
            rec_to = (date.today().year * 10000) + 9999 # last possible record of the current year        
        elif not rec_to:
            rec_to = rec_from + self.MIN_RECS # set target after highest current record to get any recent records
            min_rec_to = (date.today().year * 10000) + self.MIN_RECS # first possible record of the current year
            if rec_to < min_rec_to: rec_to = min_rec_to
            rec_from -= self.MIN_RECS

        if self.DEBUG: print 'Looking for records: ', rec_from, rec_to
        
        current_rec = rec_to
        top_page = None
        bot_page = None
        while current_rec >= rec_from and len(final_result) < self.MAX_ID_BATCH:
            current_page = str(current_rec)[4:8]
            if int(current_page) < 1900: # only testing for max 1900 applications per year (potentially there are 9999)
                
                for prefix in self.prefixes:
                    current_appno = prefix + '/' + str(current_rec)[0:4] + '/' + current_page
                    if self.DEBUG: print 'Testing page:', current_appno
                    url = self.applic_url + urllib.quote_plus(current_appno)
                    response = self.br.open(url)
                    if response:
                        html = response.read()
                        if self.DEBUG: print 'Html:', html
                        result = scrapemark.scrape(self.scrape_id, html)
                        if result and result.get('uid'):
                            if not top_page: top_page = current_appno
                            bot_page = current_appno
                            result['url'] = url
                            if self.DEBUG: print result
                            final_result.append(result)
                            break

            current_rec -= 1
                
        if final_result:
            if self.DEBUG: print bot_page, top_page
            bot_parts = bot_page.split('/')
            num_from = int(bot_parts[1])
            num_from = (num_from * 10000) + int(bot_parts[2])
            top_parts = top_page.split('/')
            num_to = int(top_parts[1])
            num_to = (num_to * 10000) + int(top_parts[2])
        return final_result, num_from, num_to

    # NB if move_forward is true, we scrape forwards from rec_start, otherwise we scrape backwards
    def get_id_records2 (self, rec_start, move_forward):
        final_result = []
        num_from = None
        num_to = None
        bad_count = 0
        find_bad = True
        current_rec = rec_start
        first_good_rec = None
        last_good_rec = None
        fields = {}
        while len(final_result) < self.MAX_ID_BATCH and bad_count < 20:
            current_year = str(current_rec)[0:4]
            current_page = str(current_rec)[4:8]
            ok_got_it = False
            for prefix in self.prefixes:
                current_appno = prefix + '/' + current_year + '/' + current_page
                if self.DEBUG: print 'Record:', current_appno
                url = self.applic_url + urllib.quote_plus(current_appno)
                response = self.br.open(url)
                if response:
                    html = response.read()
                    if self.DEBUG: print 'Html:', html
                    result = scrapemark.scrape(self.scrape_id, html)
                    if result and result.get('uid'):
                        if not first_good_rec: first_good_rec = current_rec
                        last_good_rec = current_rec
                        result['url'] = url
                        if self.DEBUG: print result
                        final_result.append(result)
                        ok_got_it = True
                        break
            if ok_got_it: 
                bad_count = 0
                find_bad = True      
            elif find_bad: 
                bad_count += 1
            if move_forward:
                if bad_count == 10: # try the next year if moving forward and we reach 10 errors
                    current_rec = (int(current_year)+1)*10000
                else:
                    current_rec += 1
            else:
                if current_page == '0000': # if moving backward, swap to next year when reach zero
                    current_rec = ((int(current_year)-1)*10000)+1900 # expecting max 1900 applications per year (potentially 9999)
                    find_bad = False
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

    def get_detail_from_uid (self, uid):
        url = self.applic_url + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

    def get_detail_from_url (self, url):
        try:
            response = self.br.open(url)
            html = response.read()
            if self.DEBUG:
                    print "Html obtained from details url:", html
            this_url = response.geturl()
            if self.DEBUG: print "Url:", this_url
        except:
            return None
        
        result = self.get_detail(html, this_url)
        if result:
            try:
                temp_result = scrapemark.scrape(self.scrape_dates_link, html, this_url)
                dates_url = temp_result['dates_link'] 
                if self.DEBUG: print dates_url
                response = self.br.open(dates_url)
                html = response.read()
                url = response.geturl()
                if self.DEBUG:
                    print "Html obtained from dates url:", html
                result2 = self.get_detail(html, url, self.scrape_dates_block, self.scrape_min_dates, self.scrape_optional_dates)
                if result2:
                    result.update(result2)
            except:
                pass
        return result

if __name__ == 'scraper':

    scraper = JerseyScraper()
    scraper.run()

    # misc test calls
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('A/2011/1163')
    #result = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('08/09/2011'))
    #print len(result), result

    #result = scraper.get_id_records(20120040, 20120050)
    #result = scraper.get_id_records(20120709)
    #print result

    # test trying to access the JSON data source directly - think the parameters are correct 
    # but does not seem to work (times out) - presumably access to external data requests is forbidden?
    #request = urllib2.Request('https://www.mygov.je/_layouts/PlanningAjaxServices/PlanningSearch.svc/Search')
    #request.add_header('Content-Type', 'application/json; charset=utf-8')
    #url = 'https://www.mygov.je/Planning/Pages/Planning.aspx'
    #data = { 'URL': url,
    #    'CommonParameters': '|05|1||49.21042016382462|-2.1445659365234633|12',
    #    'SearchParameters': '|1301||||0|All|All|8|8|2011|8|9|2011' }
    #dd = json.dumps(data)
    #print dd
    #resp = urllib2.urlopen(request, dd, 30)
    #print resp.info()
    #print json.load(resp)


    




