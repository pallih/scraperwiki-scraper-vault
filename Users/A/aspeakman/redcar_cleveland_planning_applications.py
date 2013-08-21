# this is a scraper of Redcar and Cleveland planning applications for use by Openly Local

# also see Vale of Glamorgan

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

class RedcarClevelandScraper(base.DateScraper):

    HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:8.0) Gecko/20100101 Firefox/8.0',
    'Accept-Charset': 'UTF-8,*',
    'Accept': 'text/html',
    'Accept-Language': 'en-gb,en',
    }

    date_from_field = 'ctl00$ContentPlaceHolder1$txtRecFrom'
    date_to_field = 'ctl00$ContentPlaceHolder1$txtRecTo'
    search_form = '1'
    request_date_format = '%d/%m/%Y'
    start_link = "Planning Search"
    search_fields = { '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$RadButton1', '__EVENTARGUMENT': '' }
    start_url = 'https://planning.redcar-cleveland.gov.uk/'
    applic_url = 'https://planning.redcar-cleveland.gov.uk/PlaRecord.aspx'
    scrape_next = '<input class="rgPageNext" name="{{ next_submit }}">'
    scrape_max = '<div class="rgWrap rgInfoPart"> <strong> {{ max_recs }} </strong> items </div>'
    scrape_ids = """
    <table id="ctl00_ContentPlaceHolder1_RadGrid1_ctl00"> <tr /> <tr />
    {* <tr>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    </tr> *}
    </table>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <form id="form1"> {{ block|html }} </form>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <span id="ContentPlaceHolder1_lblTitle"> Planning Application Details for : {{ reference }} </span>
    <textarea id="ContentPlaceHolder1_TabContainer1_tabDetails_txtLocation"> {{ address }} </textarea>
    <textarea id="ContentPlaceHolder1_TabContainer1_tabDetails_txtProposal"> {{ description }} </textarea>
    <input id="ContentPlaceHolder1_TabContainer1_tabOtherDetails_txtRec" value="{{ date_received }}" /> 
    <input id="ContentPlaceHolder1_TabContainer1_tabOtherDetails_txtComplete" value="{{ date_validated }}" />
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<input id="ContentPlaceHolder1_TabContainer1_tabDetails_txtParish" value="{{ parish }}" />',
    '<input id="ContentPlaceHolder1_TabContainer1_tabDetails_txtAppType" value="{{ application_type }}" />',
    '<input id="ContentPlaceHolder1_TabContainer1_tabDetails_txtStatus" value="{{ status }}" />',
    '<input id="ContentPlaceHolder1_TabContainer1_tabDetails_txtAppName" value="{{ applicant_name }}" />',
    '<input id="ContentPlaceHolder1_TabContainer1_tabDetails_txtAgtName" value="{{ agent_name }}" />',
    '<textarea id="ContentPlaceHolder1_TabContainer1_tabDetails_txtAppAddress"> {{ applicant_address }} </textarea>',
    '<textarea id="ContentPlaceHolder1_TabContainer1_tabDetails_txtAgtAddress"> {{ agent_address }} </textarea>',
    '<input id="ContentPlaceHolder1_TabContainer1_tabOtherDetails_txtOffName" value="{{ case_officer }}" />',
    '<input id="ContentPlaceHolder1_TabContainer1_tabOtherDetails_txtExpiry" value="{{ application_expires_date }}" />',
    '<input id="ContentPlaceHolder1_TabContainer1_tabOtherDetails_txtpubconsultstartdate" value="{{ consultation_start_date }}" />',
    '<input id="ContentPlaceHolder1_TabContainer1_tabOtherDetails_txtpubconsultenddate" value="{{ consultation_end_date }}" />',
    '<input id="ContentPlaceHolder1_TabContainer1_tabDecision_txtDecision" value="{{ decision }}" />',
    '<input id="ContentPlaceHolder1_TabContainer1_tabDecision_txtDecisionType" value="{{ decided_by }}" />',
    '<input id="ContentPlaceHolder1_TabContainer1_tabDecision_txtDecDate" value="{{ decision_date }}" />',
    '<table id="ContentPlaceHolder1_TabContainer1_tabDecision_gvCondits"> <tr /> {{ conditions }} </table>',
    ]

    def get_id_batch (self, date_from, date_to):

        response = util.open_url(self.br, self.start_url)
        if self.DEBUG: print "start page:", response.read()
        self.br.follow_link(text=self.start_link)

        #form_ok = util.setup_form(self.br, self.search_form, self.start_fields)
        #if self.DEBUG: print "form:", self.br.form
        #response = util.submit_form(self.br)
        #if self.DEBUG: print "search page:", response.read()

        fields = self.search_fields
        fields[self.date_from_field] = date_from.strftime(self.request_date_format)
        fields[self.date_to_field] = date_to.strftime(self.request_date_format)
        form_ok = util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print "form:", self.br.form
        response = util.submit_form(self.br)

        html = response.read()
        url = response.geturl()
        if self.DEBUG: print "result page:", html
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

        return final_result

    def get_detail_from_uid (self, uid):
        url = self.applic_url + '?AppNo=' + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    scraper = RedcarClevelandScraper()
    scraper.run()

    # misc tests
    #scraper.DEBUG = True
    #scraper.br.set_debug_http(True)
    #print scraper.get_detail_from_uid ('R/2011/0554/CL')
    #res = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('22/08/2011'))
    #print len(res), res
    #print scraper.gather_ids('2012-02-01')
    #print scraper.gather_ids('2011-02-01', '2012-01-18')

