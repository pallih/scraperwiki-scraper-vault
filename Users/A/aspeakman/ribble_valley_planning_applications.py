# this is a scraper of Ribble Valley planning applications for use by Openly Local

# does a date query to get the historical records (where a decision has been made)

# also gathers the missing recent (undecided) applications by using a list sequence based on uid

# note results paging is up the spout, says 10 on page but site actually delivers 11 - and next page links are all wrong - so do paging ourselves

#also see Burnley, Wyre, Rossendale

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

class RibbleValleyScraper(base.DateScraper):

    ID_ORDER = 'uid desc'

    applic_url = 'http://www.ribblevalley.gov.uk/planningApplication'
    result_url = 'http://www.ribblevalley.gov.uk/planningApplication/search/results'
    search_fields = { 'location': '', 'applicant': '', 'developmentDescription': '', 'decisionType': '', 'decisionDate': '', 'advancedSearch': 'Search' }
    no_results = 'http://www.ribblevalley.gov.uk/planningApplication/search/no_results'
    scrape_ids = """
    <div id="content"> <tr />
        {* <tr> <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td> <td /> </tr> *}
    </div>"""
    scrape_max = '<h2> {{ max_recs }} results for </h2>'
    scrape_one_id = """
    <div id="content">
        <h1> Application {{ uid }} </h1>
    </div>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="content"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <h1> Application {{ reference }} </h1>
    <p class="first"> <span /> {{ description }} </p>
    <tr> <td> Development address </td> <td> <strong> {{ address }} </strong> </td> </tr>
    <tr> <td> Key dates </td> <td> <strong> Received </strong> : {{ date_received }} <br>
     <strong> Valid </strong> : {{ date_validated }} <br> </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<p class="first"> <strong> {{ application_type }} </strong> </p>',
    '<tr> <td> Development address </td> <td> <strong> Ward </strong> : {{ ward_name }} <br /> </td> </tr>',
    '<tr> <td> Development address </td> <td> <strong> Parish </strong> : {{ parish }} </td> </tr>',
    '<tr> <td> Officer </td> <td> <strong> {{ case_officer }} </strong> </td> </tr>',
    '<tr> <td> Applicant </td> <td> <strong> {{ applicant_name }} </strong> {{ applicant_address }} </td> </tr>',
    '<tr> <td> Agent </td> <td> <strong> {{ agent_name }}</strong> {{ agent_address }} </td> </tr>',
    '<tr> <td> Planning Status </td> <td> {{ status }} </td> </tr>',
    '<tr> <td> Decision </td> <td> <strong> {{ decision }} </strong> Date : {{ decision_date }} </td> </tr>',
    '<tr> <td> Key dates </td> <td> <strong> Committee </strong> : {{ meeting_date }} </td> </tr>',
    '<tr> <td> Constraints </td> <td> {{ conditions }} </td> </tr>',
    #'<tr> <td> Target </td> <td> {{ target_decision_date }} </td> </tr>',
    #'<tr> <td> Last Updated </td> <td> {{ last_updated_date }} </td> </tr>',
    #'<tr> <td> Last Advertised On </td> <td> {{ last_advertised_date }} </td> </tr>',
    #'<tr> <td> Latest Advertisement Expiry </td> <td> {{ latest_advertisement_expiry_date }} </td> </tr>',
    #'<tr> <td> Standard Consultation Sent </td> <td> {{ consultation_start_date }} </td> </tr>',
    #'<tr> <td> Standard Consultation Expiry </td> <td> {{ consultation_end_date }} </td> </tr>',
    #'<tr> <td> Neighbour Consultation Sent </td> <td> {{ neighbour_consultation_start_date }} </td> </tr>',
    #'<tr> <td> Neighbour Consultation Expiry </td> <td> {{ neighbour_consultation_end_date }} </td> </tr>',
    ]

    def get_id_batch (self, date_from, date_to):

        fields = self.search_fields
        fields['lowerLimit'] = '0'
        fields['fromDay'] = str(date_from.day)
        fields['fromMonth'] = str(date_from.month)
        fields['fromYear'] = str(date_from.year)
        fields['toDay'] = str(date_to.day)
        fields['toMonth'] = str(date_to.month)
        fields['toYear'] = str(date_to.year)
        if self.DEBUG: print "fields:", fields
        response = util.open_url(self.br, self.result_url, fields, 'GET')

        html = response.read()
        url = response.geturl()
        if self.DEBUG: print "result page:", html

        try:
            result = scrapemark.scrape(self.scrape_max, html, url)
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
                fields['lowerLimit'] = str(rec_count)
                response = util.open_url(self.br, self.result_url, fields, 'GET')
                html = response.read()
                url = response.geturl()
                if self.DEBUG: print "next page:", html
            else:
                break

        # if this is a query for the most current records, extend with any undecided applications
        if date_to == date.today():
            final_result.extend(self.get_undecided_records())

        return final_result

    # does trawl to look for the most recent applications not yet decided
    # probes for potential application uids forward from the highest existing uid
    # uses the stored list of different application types already encountered
    def get_undecided_records (self, max = 50):

        final_result = []

        try:
            # get the uid of the latest fully filled out application
            latest_apps = scraperwiki.sqlite.select("uid, start_date from " + self.TABLE_NAME + " where start_date is not null order by start_date desc limit " + str(max))
        except:
            return final_result
        if self.DEBUG: print latest_apps
        if not latest_apps: return final_result
        

        # select the first one at least self.BATCH_DAYS old
        thresh_date = date.today() - timedelta(days=self.BATCH_DAYS)
        if self.DEBUG: print "Thresh date:", thresh_date
        uid_from = None
        for app in latest_apps:
            this_date = util.get_dt(app['start_date'], util.ISO8601_DATE)
            if this_date <= thresh_date:
                uid_from = app['uid']   
                break
        if self.DEBUG: print "Start app:", uid_from
        if not uid_from: return final_result

        # get the list of any uids already fully gathered above that uid number
        taken_apps = scraperwiki.sqlite.select("uid from " + self.TABLE_NAME + " where start_date is not null and uid > '" + uid_from + "'")
        if self.DEBUG: print "Ids taken:", taken_apps
        taken_list = []
        for i in taken_apps:
            taken_list.append(i['uid'])
        if self.DEBUG: print taken_list
        
        year = int(uid_from[2:6])
        rec_from = (year * 10000) + int(uid_from[7:11])
        rec_to = rec_from + max

        fields = {}
        current_rec = rec_from + 1
        while current_rec <= rec_to:
            current_appno = '3/' + str(current_rec)[0:4] + '/' + str(current_rec)[4:8]
            if self.DEBUG: print 'Testing: ', current_appno
            if current_appno not in taken_list:
                fields['appNumber'] = current_appno
                try:
                    response = util.open_url(self.br, self.applic_url, fields, 'GET')
                    url = response.geturl()
                    if url <> self.no_results:
                        html = response.read()
                        result = scrapemark.scrape(self.scrape_one_id, html, url)
                        if result:
                            result['url'] = url
                            if self.DEBUG: print 'Found:', current_appno, result
                            self.clean_ids([result])
                            final_result.append(result)
                except:
                    pass
            else:
                if self.DEBUG: print 'Taken:', current_appno
            current_rec += 1
                
        return final_result

    def get_detail_from_uid (self, uid):
        url = self.applic_url + '?appNumber=' + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

if __name__ == 'scraper':

    scraper = RibbleValleyScraper()
    #scraper.DEBUG = True
    scraper.run()

    # misc tests
    #print scraper.get_detail_from_uid ('3/2000/013N')
    #res = scraper.get_id_batch(util.get_dt('22/02/2012'), util.get_dt('07/03/2012'))
    #res = scraper.get_id_batch(util.get_dt('28/06/2012'), date.today())
    #print len(res), res
    #print scraper.get_undecided_records ()
    #print scraper.gather_ids('2012-02-01')
    #print scraper.gather_ids('2011-02-01', '2012-01-18')
    #print scraper.gather_ids(None, None)
    #scraper.gather_current_ids()

    #util.rename_column('swdata', 'ward', 'ward_name')
