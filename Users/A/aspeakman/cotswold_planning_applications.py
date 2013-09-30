# this is a scraper of Cotswold planning applications for use by Openly Local

# weekly current list covers last 5-6 weeks only

# otherwise has monthly lists of applications decided going back to March 2004

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import urllib
import copy

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

class CotswoldScraper(base.PeriodScraper):

    START_SEQUENCE = '2004-03-01' # gathers id data by working backwards from the current date towards this one
    MAX_ID_BATCH = 200 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 150 # max application details to scrape in one go
    #ID_ORDER = 'uid desc'
    ID_ORDER = "CASE uid WHEN substr(uid, 1, 2) < '50' THEN '20' || uid ELSE '19' || uid END desc"
    
    ref_field = 'ctl00$mainContent$appnum'
    detail_submit = 'ctl00$mainContent$butAppnum'
    applic_url = 'http://www.cotswold.gov.uk/nqcontent.cfm?a_id=2297&step=2'
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="content"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <tr> <td> Application </td> <td> {{ reference }} </td> </tr>
    <tr> <td> Proposal </td> <td> {{ description }} </td> </tr>
    <tr> <td> Location </td> <td> {{ address }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr> <td> Ward </td> <td> {{ ward_name }} </td> </tr>',
    '<tr> <td> Case Officer </td> <td> {{ case_officer }} </td> </tr>',
    '<tr> <td> Parish </td> <td> {{ parish }} </td> </tr>',
    '<tr> <td> Application Type </td> <td> {{ application_type }} </td> </tr>',
    '<tr> <td> Application Status </td> <td> {{ status }} </td> </tr>',
    '<tr> <td> Easting / Northing </td> <td> {{ easting }} / {{ northing }} </td> </tr>',
    '<tr> <td> Applicant </td> <td> {{ applicant_name }} <br> {{ applicant_address|html }} </td> </tr>',
    '<tr> <td> Agent </td> <td> {{ agent_name }} <br> {{ agent_address|html }} </td> </tr>',
    '<a href="{{ comment_url|abs }}"> Comments </a>',
    ]
    # other parameters that appear on the dates page
    scrape_extra_data = [
    "<tr> <td> Application Received </td> <td> {{ date_received }} </td> </tr>", 
    "<tr> <td> Comments by </td> <td> {{ comment_date }} </td> </tr>", 
    ]

    def get_id_period (self, date):

        # first get the monthly list of applications decided
        self.search_url = 'http://www.cotswold.gov.uk/nqcontent.cfm?a_id=8899'
        self.PERIOD_TYPE = 'Month'
        self.search_form = 'WeeklyListLookup'
        self.date_field = 'ChosenMonthlyList'
        self.request_date_format = '%Y-%m'
        self.scrape_ids = """
        <h2> Monthly list </h2>
        <table> <tr />
        {* <tr>
        <td> {{ [records].decision_date }} </td>
        <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
        <td /> <td /> <td> {{ [records].date_received }} </td>
        </tr> *}
        </table>
        """
        month_records, month_from_dt, month_to_dt = self.get_id_period_internal (date)

        # now get any current weekly list
        self.search_url = 'http://www.cotswold.gov.uk/nqcontent.cfm?a_id=8199'
        self.PERIOD_TYPE = 'Sunday'
        self.search_form = 'WeeklyListLookup'
        self.date_field = '#ChosenWeeklyList'
        self.request_date_format = 'Week ending %d %B %Y'
        self.scrape_ids = """
        <div class="plainBox" />
        <table> <tr />
        {* <tr>
        <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
        <td> {{ [records].date_received }} </td>
        </tr> *}
        </table>
        """
        week_records, week_from_dt, week_to_dt = self.get_id_period_internal (date)

        if week_from_dt and week_to_dt: # if there are current records, use those values updated with any decision dates from the current month
            month_uids = {}
            for map in month_records:
                month_uids[map['uid']] = map
            for i in week_records:
                if i['uid'] in month_uids:
                    i['decision_date'] = month_uids[i['uid']]['decision_date']
            return week_records, week_from_dt, week_to_dt
        else: # otherwise just use monthly values
            return month_records, month_from_dt, month_to_dt

    def get_id_period_internal (self, date):

        from_iso_dt, to_iso_dt = util.inc_dt(date.strftime(util.ISO8601_DATE), util.ISO8601_DATE, self.PERIOD_TYPE)
        from_dt = util.get_dt(from_iso_dt, util.ISO8601_DATE)
        to_dt = util.get_dt(to_iso_dt, util.ISO8601_DATE)

        response = self.br.open(self.search_url)
        fields = { self.date_field: to_dt.strftime(self.request_date_format) }
        try:
            util.setup_form(self.br, self.search_form, fields)
            if self.DEBUG: print self.br.form
            response = util.submit_form(self.br)
        except:
            response = None

        final_result = []
        if response:
            html = response.read()
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
        else:
            return [], None, None

        return final_result, from_dt, to_dt # note weekly result could be legitimately empty
        
    def get_detail_from_uid (self, uid):
        url = self.applic_url + '&myID=' + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

    # scrape detailed information on one record via its access URL
    def get_detail_from_url (self, url):
        result = base.BaseScraper.get_detail_from_url (self, url)
        if result:
            try:
                response = self.br.follow_link(text='Dates')
                extra_html = response.read()
                extra_result = {}
                for i in self.scrape_extra_data:
                    next_val = scrapemark.scrape(i, extra_html)
                    if next_val:
                        extra_result.update(next_val)
                self.clean_record(extra_result)
                result.update(extra_result)
            except:
                if self.DEBUG:
                    print "Failed to get extra detail from dates page:", url
                    raise
                #return None
            return result
        else:
            return None

if __name__ == 'scraper':

    #scraperwiki.sqlite.execute("delete from swdata")
    #scraperwiki.sqlite.commit()

    scraper = CotswoldScraper()
    #scraper.reset()
    scraper.run()

    #scraper.DEBUG = True
    # misc tests
    #print scraper.get_detail_from_uid ('12/03329/FUL')
    #result, dt1, dt2 = scraper.get_id_period(util.get_dt('01/08/2012'))
    #print len(result), result, dt1, dt2
    
# this is a scraper of Cotswold planning applications for use by Openly Local

# weekly current list covers last 5-6 weeks only

# otherwise has monthly lists of applications decided going back to March 2004

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import urllib
import copy

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

class CotswoldScraper(base.PeriodScraper):

    START_SEQUENCE = '2004-03-01' # gathers id data by working backwards from the current date towards this one
    MAX_ID_BATCH = 200 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 150 # max application details to scrape in one go
    #ID_ORDER = 'uid desc'
    ID_ORDER = "CASE uid WHEN substr(uid, 1, 2) < '50' THEN '20' || uid ELSE '19' || uid END desc"
    
    ref_field = 'ctl00$mainContent$appnum'
    detail_submit = 'ctl00$mainContent$butAppnum'
    applic_url = 'http://www.cotswold.gov.uk/nqcontent.cfm?a_id=2297&step=2'
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="content"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <tr> <td> Application </td> <td> {{ reference }} </td> </tr>
    <tr> <td> Proposal </td> <td> {{ description }} </td> </tr>
    <tr> <td> Location </td> <td> {{ address }} </td> </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr> <td> Ward </td> <td> {{ ward_name }} </td> </tr>',
    '<tr> <td> Case Officer </td> <td> {{ case_officer }} </td> </tr>',
    '<tr> <td> Parish </td> <td> {{ parish }} </td> </tr>',
    '<tr> <td> Application Type </td> <td> {{ application_type }} </td> </tr>',
    '<tr> <td> Application Status </td> <td> {{ status }} </td> </tr>',
    '<tr> <td> Easting / Northing </td> <td> {{ easting }} / {{ northing }} </td> </tr>',
    '<tr> <td> Applicant </td> <td> {{ applicant_name }} <br> {{ applicant_address|html }} </td> </tr>',
    '<tr> <td> Agent </td> <td> {{ agent_name }} <br> {{ agent_address|html }} </td> </tr>',
    '<a href="{{ comment_url|abs }}"> Comments </a>',
    ]
    # other parameters that appear on the dates page
    scrape_extra_data = [
    "<tr> <td> Application Received </td> <td> {{ date_received }} </td> </tr>", 
    "<tr> <td> Comments by </td> <td> {{ comment_date }} </td> </tr>", 
    ]

    def get_id_period (self, date):

        # first get the monthly list of applications decided
        self.search_url = 'http://www.cotswold.gov.uk/nqcontent.cfm?a_id=8899'
        self.PERIOD_TYPE = 'Month'
        self.search_form = 'WeeklyListLookup'
        self.date_field = 'ChosenMonthlyList'
        self.request_date_format = '%Y-%m'
        self.scrape_ids = """
        <h2> Monthly list </h2>
        <table> <tr />
        {* <tr>
        <td> {{ [records].decision_date }} </td>
        <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
        <td /> <td /> <td> {{ [records].date_received }} </td>
        </tr> *}
        </table>
        """
        month_records, month_from_dt, month_to_dt = self.get_id_period_internal (date)

        # now get any current weekly list
        self.search_url = 'http://www.cotswold.gov.uk/nqcontent.cfm?a_id=8199'
        self.PERIOD_TYPE = 'Sunday'
        self.search_form = 'WeeklyListLookup'
        self.date_field = '#ChosenWeeklyList'
        self.request_date_format = 'Week ending %d %B %Y'
        self.scrape_ids = """
        <div class="plainBox" />
        <table> <tr />
        {* <tr>
        <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
        <td> {{ [records].date_received }} </td>
        </tr> *}
        </table>
        """
        week_records, week_from_dt, week_to_dt = self.get_id_period_internal (date)

        if week_from_dt and week_to_dt: # if there are current records, use those values updated with any decision dates from the current month
            month_uids = {}
            for map in month_records:
                month_uids[map['uid']] = map
            for i in week_records:
                if i['uid'] in month_uids:
                    i['decision_date'] = month_uids[i['uid']]['decision_date']
            return week_records, week_from_dt, week_to_dt
        else: # otherwise just use monthly values
            return month_records, month_from_dt, month_to_dt

    def get_id_period_internal (self, date):

        from_iso_dt, to_iso_dt = util.inc_dt(date.strftime(util.ISO8601_DATE), util.ISO8601_DATE, self.PERIOD_TYPE)
        from_dt = util.get_dt(from_iso_dt, util.ISO8601_DATE)
        to_dt = util.get_dt(to_iso_dt, util.ISO8601_DATE)

        response = self.br.open(self.search_url)
        fields = { self.date_field: to_dt.strftime(self.request_date_format) }
        try:
            util.setup_form(self.br, self.search_form, fields)
            if self.DEBUG: print self.br.form
            response = util.submit_form(self.br)
        except:
            response = None

        final_result = []
        if response:
            html = response.read()
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
        else:
            return [], None, None

        return final_result, from_dt, to_dt # note weekly result could be legitimately empty
        
    def get_detail_from_uid (self, uid):
        url = self.applic_url + '&myID=' + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

    # scrape detailed information on one record via its access URL
    def get_detail_from_url (self, url):
        result = base.BaseScraper.get_detail_from_url (self, url)
        if result:
            try:
                response = self.br.follow_link(text='Dates')
                extra_html = response.read()
                extra_result = {}
                for i in self.scrape_extra_data:
                    next_val = scrapemark.scrape(i, extra_html)
                    if next_val:
                        extra_result.update(next_val)
                self.clean_record(extra_result)
                result.update(extra_result)
            except:
                if self.DEBUG:
                    print "Failed to get extra detail from dates page:", url
                    raise
                #return None
            return result
        else:
            return None

if __name__ == 'scraper':

    #scraperwiki.sqlite.execute("delete from swdata")
    #scraperwiki.sqlite.commit()

    scraper = CotswoldScraper()
    #scraper.reset()
    scraper.run()

    #scraper.DEBUG = True
    # misc tests
    #print scraper.get_detail_from_uid ('12/03329/FUL')
    #result, dt1, dt2 = scraper.get_id_period(util.get_dt('01/08/2012'))
    #print len(result), result, dt1, dt2
    
