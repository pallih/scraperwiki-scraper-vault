# this is a scraper of Wyre planning applications for use by Openly Local

# does a date query to get the historical records (where a decision has been made)

# also gathers the missing recent (undecided) applications by using a list sequence based on uid

# note results say 20 per page, but site actually delivers 21 - repeats same record at end of page and beginning of next page (means records count is wrong)

#also see Burnley, Rossendale, Ribble Valley

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import urllib
import random

base = scraperwiki.utils.swimport("openlylocal_base_scraper")
scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")

class WyreScraper(base.DateScraper):

    MAX_ID_BATCH = 200 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 150 # max application details to scrape in one go
    #ID_ORDER - 'uid desc'
    ID_ORDER = "CASE uid WHEN substr(uid, 1, 2) < '50' THEN '20' || uid ELSE '19' || uid END desc"
    MIN_DAYS = 28

    applic_url = 'http://www.wyre.gov.uk/site/scripts/planx_details.php'
    result_url = 'http://www.wyre.gov.uk/planningApplication/search/results'
    search_fields = { 'location': '', 'applicant': '', 'developmentDescription': '', 'decisionType': '', 'decisionDate': '', 'advancedSearch': 'Search' }
    no_results = 'http://www.wyre.gov.uk/planningApplication/search/no_results'
    scrape_ids = """
    <form class="basic_form box"> <tr />
        {* <tr> <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td> </tr> *}
    </form>"""
    scrape_next = '<p class="center"> results | <a href="{{ next_link }}"> Next </a> </p>'
    scrape_max = '<div id="content_inner"> <h2> {{ max_recs }} results </h2> </div>'
    scrape_one_id = """
    <div id="content_inner"> 
        <h1> {{ uid }} </h1>
        <a href="{{ url|abs }}">track this application</a>
    </div>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="content_inner"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <h1> {{ reference }} </h1>
    <tr> <td> Proposal </td> <td> {{ description }} </td> </tr>
    <tr> <td> Proposal Location </td> <td> {{ address }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr> <td> Valid </td> <td> {{ date_validated }} </td> </tr>',
    '<tr> <td> Application Type </td> <td> {{ application_type }} </td> </tr>',
    '<tr> <td> Ward </td> <td> {{ ward_name }} </td> </tr>',
    '<tr> <td> Parish </td> <td> {{ parish }} </td> </tr>',
    '<tr> <td> Officer </td> <td> {{ case_officer }} </td> </tr>',
    '<tr> <td> Target </td> <td> {{ target_decision_date }} </td> </tr>',
    '<tr> <td> Agent </td> <td> {{ agent_name }} <br> {{ agent_address }} </td> </tr>',
    '<tr> <td> Applicant </td> <td> {{ applicant_name }} <br> {{ applicant_address }} </td> </tr>',
    '<tr> <td> Last Advertised On </td> <td> {{ last_advertised_date }} </td> </tr>',
    '<tr> <td> Latest Advertisement Expiry </td> <td> {{ latest_advertisement_expiry_date }} </td> </tr>',
    '<tr> <td> Standard Consultation Sent </td> <td> {{ consultation_start_date }} </td> </tr>',
    '<tr> <td> Standard Consultation Expiry </td> <td> {{ consultation_end_date }} </td> </tr>',
    '<tr> <td> Neighbour Consultation Sent </td> <td> {{ neighbour_consultation_start_date }} </td> </tr>',
    '<tr> <td> Neighbour Consultation Expiry </td> <td> {{ neighbour_consultation_end_date }} </td> </tr>',
    '<tr> <td> Last Updated </td> <td> {{ last_updated_date }} </td> </tr>',
    '<tr> <td> Planning Status </td> <td> {{ status }} </td> </tr>',
    '<tr> <td> Decision </td> <td> {{ decision }} </td> </tr>',
    '<tr> <td> Decision Date </td> <td> {{ decision_date }} </td> </tr>',
    ]

    def get_id_batch (self, date_from, date_to):

        atype_list = scraperwiki.sqlite.get_var('app_types') # stored application type suffixes
        app_types = atype_list.split(',') if atype_list else []

        fields = self.search_fields
        fields['lowerLimit'] = '0'
        fields['fromDay'] = str(date_from.day)
        fields['fromMonth'] = str(date_from.month)
        fields['fromYear'] = str(date_from.year)
        fields['toDay'] = str(date_to.day)
        fields['toMonth'] = str(date_to.month)
        fields['toYear'] = str(date_to.year)
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
                #result = scrapemark.scrape(self.scrape_next, html)
                #try:
                #    next_link = result['next_link']
                #except:
                #    break
                #response = util.open_url(self.br, next_link)
                html = response.read()
                url = response.geturl()
                if self.DEBUG: print "next page:", html
            else:
                break

        # examine the application type suffixes to see if there any new ones to be stored
        start_len = len(app_types)
        for rec in final_result:
            app_type = rec['uid'][9:]
            if app_type not in app_types:
                app_types.append(app_type)
        if len(app_types) > start_len:
            atype_list = ','.join(app_types)
            if self.DEBUG: print "app types:", atype_list
            scraperwiki.sqlite.save_var('app_types', atype_list)

        # if this is a query for the most current records, extend with any undecided applications
        if date_to == date.today():
            final_result.extend(self.get_undecided_records())

        return final_result

    # does trawl to look for the most recent applications not yet decided
    # probes for potential application uids forward from the highest existing uid 
    # uses the stored list of different application types already encountered
    def get_undecided_records (self, max = 100):

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
        
        year = int(uid_from[0:2])
        rec_from = (year * 100000) + int(uid_from[3:8])
        rec_to = rec_from + max

        atype_list = scraperwiki.sqlite.get_var('app_types') # stored application type suffixes
        app_types = atype_list.split(',') if atype_list else []
        if 'FUL' in app_types: app_types.remove('FUL') 

        fields = {}
        current_rec = rec_from + 1
        while current_rec <= rec_to:
            current_appbase = str(current_rec)[0:2] + '/' + str(current_rec)[2:7]
            if self.DEBUG: print 'Testing: ', current_appbase
            app_tests = [ 'FUL' ] # always test for full applications
            random.shuffle(app_types) # select randomly from the other types
            app_tests.extend(app_types[:6]) # only test 6 other types each time, too slow otherwise
            for atype in app_tests:
                current_appno = current_appbase + '/' + atype
                if current_appno not in taken_list: 
                    fields['appNumber'] = current_appno
                    try:
                        response = util.open_url(self.br, self.applic_url, fields, 'GET')
                        url = response.geturl()
                        if url <> self.no_results:
                            html = response.read()
                            result = scrapemark.scrape(self.scrape_one_id, html, url)
                            if result:
                                result['url'] = result['url'].replace('track?appID=', '')
                                if self.DEBUG: print 'Found:', current_appno, result
                                self.clean_ids([result])
                                final_result.append(result)
                                break
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

    scraper = WyreScraper()
    #scraper.populate_missing_applications()
    scraper.run()

    #scraper.DEBUG = True
    # misc tests
    #print scraper.get_detail_from_uid ('08/01054/DIS')
    #res = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('22/08/2011'))
    #res = scraper.get_id_batch(util.get_dt('28/06/2012'), date.today())
    #res = scraper.get_id_batch(util.get_dt('01/01/2013'))
    #print len(res), res
    #print scraper.get_undecided_records ()
    #print scraper.gather_ids('2012-02-01')
    #print scraper.gather_ids('2011-02-01', '2012-01-18')
    #print scraper.gather_ids(None, None)
    #scraper.gather_current_ids()

    #util.rename_column('swdata', 'ward', 'ward_name')
