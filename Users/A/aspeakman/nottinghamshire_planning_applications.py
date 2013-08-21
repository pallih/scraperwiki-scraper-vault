# this is a scraper of Nottinghamshire planning applications for use by Openly Local

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

class NottinghamshireScraper(base.DateScraper):

    MAX_ID_BATCH = 200 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 150 # max application details to scrape in one go
    BATCH_DAYS = 28 # batch size for each scrape - number of days to gather to produce at least one result each time
    MIN_DAYS = 14 # min number of days to get when gathering current ids

    date_from_field = 'ctl00_MainContent_txtDateReceivedFrom_dateInput_ClientState'
    date_to_field = 'ctl00_MainContent_txtDateReceivedTo_dateInput_ClientState'
    request_date_format = '{"enabled":true,"emptyMessage":"","validationText":"%Y-%m-%d-00-00-00","valueAsString":"%Y-%m-%d-00-00-00","minDateStr":"01/01/1900","maxDateStr":"12/31/2099"}'
    #date_from_field2 = 'ctl00$MainContent$txtDateReceivedFrom'
    #date_to_field2 = 'ctl00$MainContent$txtDateReceivedTo'
    #request_date_format2 = '%Y-%m-%d'
    search_fields = { '__EVENTTARGET': '', '__EVENTARGUMENT': '' } 
    search_form = '1'
    start_fields = { 'ctl00$MainContent$radSearchType': 'ADV' }
    submit_continue = "ctl00$MainContent$btnContinue"
    submit_control = 'ctl00$MainContent$btnSearch'
    submit_next = 'ctl00$MainContent$lvResults$pager$ctl02$NextButton'
    
    start_url = 'http://www.nottinghamshire.gov.uk/planningsearch/planhome.aspx'
    applic_url = 'http://www.nottinghamshire.gov.uk/planningsearch/plandisp.aspx'
    
    scrape_max = '<div> Your search returned the following results (a total of {{ max_recs }}). Click on an application number to view its case file. </div>'
    scrape_ids = """
    <div id="news_results_list">
        {* <div> <div class="SearchResultRow">
        <div> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </div> <div> {{ [records].reference }} </div> 
        </div> </div> *}
    </div>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="ncc-content"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <textarea name="ctl00$MainContent$txtLocation"> {{ address }} </textarea>
    <textarea name="ctl00$MainContent$txtProposal"> {{ description }} </textarea>
    <input value="{{ date_received }}" name="ctl00$MainContent$txtReceivedDate">
    <input value="{{ date_validated }}" name="ctl00$MainContent$txtValidDate">
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<select name="ctl00$MainContent$listDistricts"> {{ district }} </select>',
    '<select name="ctl00$MainContent$listParishes"> {{ parish }} </select>', 
    '<textarea name="ctl00$MainContent$txtAppName"> {{ applicant_name }} </textarea>',
    '<textarea name="ctl00$MainContent$txtAgentsName"> {{ agent_name }} </textarea>',
    '<input value="{{ case_officer }}" name="ctl00$MainContent$txtCaseOfficer">', 
    '<input value="{{ decision }}" name="ctl00$MainContent$txtDecision">',
    '<input value="{{ decision_date }}" name="ctl00$MainContent$txtDecisionDate2">',
    '<input value="{{ appeal_by_date }}" name="ctl00$MainContent$txtAppealDeadline">',
    '<table id="ctl00_MainContent_gridConstraints_ctl00"> <tr /> {{ conditions }} </table>',
    '<tr> <td> Site Notice </td> <td /> <td> {{ site_notice_start_date }} </td> <td> {{ site_notice_end_date }} </td> </tr>',
    '<tr> <td> Press Advert </td> <td /> <td> {{ consultation_start_date }} </td> <td> {{ consultation_end_date }} </td> </tr>',
    ]

    def get_id_batch (self, date_from, date_to):

        final_result = []

        response = util.open_url(self.br, self.start_url)
        if self.DEBUG: print "start page:", response.read()

        form_ok = util.setup_form(self.br, self.search_form, self.start_fields)
        if self.DEBUG: print "form:", self.br.form
        response = util.submit_form(self.br, self.submit_continue)

        fields = self.search_fields
        fields[self.date_from_field] = date_from.strftime(self.request_date_format)
        #fields[self.date_from_field2] = date_from.strftime(self.request_date_format2)
        fields[self.date_to_field] = date_to.strftime(self.request_date_format)
        #fields[self.date_to_field2] = date_to.strftime(self.request_date_format2)
        form_ok = util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print "form:", self.br.form
        response = util.submit_form(self.br, self.submit_control)

        html = response.read()
        if self.DEBUG: print "result page:", html
        result = scrapemark.scrape(self.scrape_max, html)
        try:
            num_recs = int(result['max_recs'])
        except:
            num_recs = 0
        if self.DEBUG: print "max_recs:", num_recs

        while len(final_result) < num_recs:
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
                if self.DEBUG: print 'Output N: ', len(final_result)
            else:
                break
            if len(final_result) < num_recs:
                try:
                    form_ok = util.setup_form(self.br, self.search_form)
                    if self.DEBUG: print "form:", self.br.form
                    response = util.submit_form(self.br, self.submit_next)
                    html = response.read()
                except:
                    break
            
        return final_result

    def get_detail_from_uid (self, uid):
        url = self.applic_url + '?AppNo=' + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    scraper = NottinghamshireScraper()
    scraper.run()

    # misc tests
    #scraper.DEBUG = True
    #scraper.br.set_debug_http(True)
    #print scraper.get_detail_from_uid ('T/2297')
    #result = scraper.get_id_batch(util.get_dt('01/08/2011'), util.get_dt('22/08/2011'))
    #print len(result), result
    #print scraper.gather_ids('2012-02-01')
    #print scraper.gather_ids('2011-02-01', '2012-01-18')
    

