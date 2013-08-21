# this is a scraper of Bournemouth planning applications for use by Openly Local

# also see South Northamptonshire

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

class BournemouthScraper(base.DateScraper):

    date_from_field = 'ctl00$MainContent$txtDateReceivedFrom'
    date_to_field = 'ctl00$MainContent$txtDateReceivedTo'
    search_submit = 'ctl00$MainContent$btnSearch'
    search_form = '0'
    search_url = 'http://planning.bournemouth.gov.uk/RealTimeRegister/planappsrch.aspx'
    scrape_max_recs = '<div>Your search returned the following results (a total of <b> {{ max_recs }} </b> </div>'
    scrape_next_submit = '<input title="Next Page" name="{{ next_submit }}">'
    ref_field = 'ctl00$MainContent$txtAppNumber'
    scrape_ids = """
    <table id="MainContent_grdResults_ctl00"> <tbody>
    {* <tr> <td> <a href="{{ [records].url|abs }}">
    {{ [records].uid }} </a> </td>  </tr> *}
    </tbody> </table>
    """

    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="contenttext"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <input value="{{ reference }}" name="ctl00$MainContent$txtAppNo">
    <textarea name="ctl00$MainContent$txtProposal"> {{ description }} </textarea>
    <input value="{{ date_received }}" name="ctl00$MainContent$txtReceivedDate">
    <input value="{{ date_validated }}" name="ctl00$MainContent$txtValidDate">
    <textarea name="ctl00$MainContent$txtLocation"> {{ address }} </textarea>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<input value="{{ application_type }}" name="ctl00$MainContent$txtType">',
    '<input value="{{ case_officer }}" name="ctl00$MainContent$txtCaseOfficer">',
    '<input value="{{ decided_by }}" name="ctl00$MainContent$txtCommitteeDelegated">',
    '<input value="{{ meeting_date }}" name="ctl00$MainContent$txtCommitteeDelegatedDate">',
    '<input value="{{ latest_advertisement_expiry_date }}" name="ctl00$MainContent$txtAdvertExpiry">',
    '<input value="{{ neighbour_consultation_end_date }}" name="ctl00$MainContent$txtNeighbourExpiry">',
    '<input value="{{ site_notice_end_date }}" name="ctl00$MainContent$txtSiteNoticeExpiry">',
    '<input value="{{ decision_issued_date }}" name="ctl00$MainContent$txtIssueDate">',
    '<input value="{{ decision }}" name="ctl00$MainContent$txtDecision">',
    '<input value="{{ decision_date }}" name="ctl00$MainContent$txtDecisionDate">',
    '<input value="{{ ward_name }}" name="ctl00$MainContent$txtWard">',
    '<input value="{{ parish }}" name="ctl00$MainContent$txtParish">',
    '<input value="{{ uprn }}" name="ctl00$MainContent$txtUprn">',
    '<input value="{{ easting }}" name="ctl00$MainContent$txtEasting">',
    '<input value="{{ northing }}" name="ctl00$MainContent$txtNorthing">',
    '<td id="MainContent_tdCommentsWelcomeBy"> Comments Welcome By <br> {{ consultation_end_date }} </td>',
    ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)

        fields = { }
        fields[self.date_from_field] = date_from.strftime(self.request_date_format)
        fields[self.date_to_field] = date_to.strftime(self.request_date_format)
        util.setup_form(self.br, self.search_form, fields )
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br, self.search_submit)

        html = response.read()
        if self.DEBUG: print html
            
        try:
            result = scrapemark.scrape(self.scrape_max_recs, html)
            max_recs = int(result['max_recs'])
        except:
            max_recs = 0
        if self.DEBUG: print "max recs:", max_recs

        final_result = []
        while response and len(final_result) < max_recs:
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            else:
                break
            if len(final_result) >= max_recs:
                break
            try:
                result = scrapemark.scrape(self.scrape_next_submit, html)
                util.setup_form(self.br, self.search_form )
                if self.DEBUG: print self.br.form
                response = util.submit_form(self.br, result['next_submit'])
                html = response.read()
            except:
                break
        return final_result

    def get_detail_from_uid (self, uid):
        try:
            response = self.br.open(self.search_url)
            fields = { self.ref_field: uid }
            util.setup_form(self.br, self.search_form, fields)
            if self.DEBUG: print self.br.form
            response = util.submit_form(self.br, self.search_submit)
            html = response.read()
            url = response.geturl()
            if self.DEBUG: print html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            return self.get_detail_from_url(result['records'][0]['url'])
        except:
            return None

if __name__ == 'scraper':

    scraper = BournemouthScraper()
    #scraper.clear_all()
    scraper.run()

    #scraper.DEBUG = True

    # misc test calls
    #print scraper.get_detail_from_uid ('7-2012-24945')
    #result = scraper.get_id_batch(util.get_dt('08/10/2012'), util.get_dt('11/10/2012'))
    #print len(result), result
    #print scraper.get_id_batch(util.get_dt('23/03/2012'), util.get_dt('25/03/2012'))



