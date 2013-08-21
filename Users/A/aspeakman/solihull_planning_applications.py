# this is a scraper of Solihull planning applications for use by Openly Local

# note now converted to a weekly period scraper

# NO LONGER works from one long sequence - no date query
# For each previous year we have to work backwards through the ID sequence to find the max application number for that year
# For the current year we work forward to find the most recent applications


import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import urllib
from BeautifulSoup import BeautifulSoup

base = scraperwiki.utils.swimport("openlylocal_base_scraper")
scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")

class SolihullScraper(base.PeriodScraper):

    #START_SEQUENCE = 20000001 # gathering back to this uid (first application in year 2000)
    MAX_ID_BATCH = 300 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 250 # max application details to scrape in one go
    ID_ORDER = 'uid desc'
    UID_REGEX = re.compile(r'(\d\d\d\d)/(\d+)')
    PERIOD_TYPE = 'Sunday'

    search_form = '1'
    search_submit = None
    search_fields = { 'ward': 'ALL' }
    search_url = 'http://www.solihull.gov.uk/planning/dc/weeklist.asp'
    applic_url = 'http://www.solihull.gov.uk/planning/dc/ViewAppDetail.asp'
    date_select = "SD"
    scrape_not_found = """
        <p align="center"> <strong>Nothing found {{ not_found }} application reference</strong> </p>
    """
    scrape_ids = """
    <h5 />
    {* <table class="subTab">
        <tr> <td /> <td> <strong> {{ [records].uid }} </strong>
        <a href="{{ [records].url|abs }}"> </a> </td> </tr>
    </table> *}
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div class="main"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <tr> <td class="label">Application</td> {{ uid }} </tr>
    <tr> <td class="label">Location</td> {{ address|html }} </tr>
    <tr> <td class="label">Application</td> <td> {{ date_validated }} </td> </tr>
    <tr> <td class="label">Proposal</td> {{ description }} </tr>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<tr> <td class="label">Application</td> <td width="70%"> {{ reference }} </td> </tr>',
    '<tr> <td class="label">Application</td> <td /> <td width="50%"> {{ application_type }} </tr>',
    '<tr> <td class="label">Neighbour Notification for a planning application</td> <td> {{ consultation_start_date }} </td> </tr>',
    '<tr> <td class="label">Decision</td> <td> {{ decision_date }} </td> <td> {{ decision }} </td> </td>',
    '<tr> <td class="label">DeadLine</td> {{ target_decision_date }} </td>',
    '<tr> <td class="label">Ward</td> {{ ward_name }} </tr>',
    '<tr> <td class="label">Press notice</td> <td /> <td> Expires {{ last_advertised_date }} </td> </tr>',
    '<a target="ComWin" title="You can make comments online" href="{{ comment_url|abs }}"> </a>',
    ]

    # NOT USED ANY MORE
    # NB if both are None, it's the first ever scrape
    # NB if rec_to is None, rec_from is the highest existing record and it's a current scrape
    # NB also if rec_to is None, the default should be to try to get at least self.MIN_RECS records
    def get_id_records (self, rec_from, rec_to = None):
        final_result = []
        num_from = None
        num_to = None

        if not rec_to:
            response = util.open_url(self.br, self.search_url)
            self.br.select_form(nr=1)
            control = self.br.find_control(name=self.date_select)
            items = control.get_items()
            i = 0; result = None
            while True:
                #print items[i].name
                control.value = [ items[i].name ]
                response = util.submit_form(self.br, self.search_submit)
                html = response.read()
                url = response.geturl()
                result = scrapemark.scrape(self.scrape_ids, html, url)
                if result and result.get('records'): break
                self.br.select_form(nr=1)
                control = self.br.find_control(name=self.date_select)
                i = i + 1
            records = result['records']
            num_recs = len(records)
            max_uid = records[num_recs-1]['uid']
            #print max_uid
            num_recs = self.get_ref_from_uid(max_uid)

        if not rec_from and not rec_to:
            rec_from = self.START_SEQUENCE
            rec_to = num_recs
        elif not rec_to:
            rec_to = num_recs
            rec_from -= self.MIN_RECS

        num = 0; i = rec_to; last_i = 0
        while num < self.MAX_ID_BATCH and i >= rec_from: # work backwards and stop when MAX_ID_BATCH is reached
            stri = str(i)
            Y = int(stri[:4])
            R = int(stri[4:])
            if R == 0:
                Y = Y - 1
                R = self.get_year_max_ref (Y)
                if not R: break
                i = (Y * 10000) + R
            final_result.append( { 'url': self.applic_url + '?Y='+str(Y)+'&R='+str(R), 'uid': str(Y)+'/'+str(R) } )
            num = num + 1
            last_i = i
            i = i - 1

        if num > 0:
            num_from = last_i
            num_to = rec_to
        return final_result, num_from, num_to

    def get_detail_from_uid (self, uid):
        Y, R = self.get_yr_from_uid (uid)
        if Y and R:
            url = self.applic_url + '?Y='+str(Y)+'&R='+str(R)
            #print url
            return self.get_detail_from_url(url)
        else:
            return None

    # is this a uid that doesn't lead anywhere?
    def is_zombie (self, uid):
        retval = False
        Y, R = self.get_yr_from_uid (uid)
        if Y and R:
            url = self.applic_url + '?Y='+str(Y)+'&R='+str(R)
            try:
                response = self.br.open(url)
                html = response.read()
                result = scrapemark.scrape(self.scrape_not_found, html)
                if result and result.get('not_found'):
                    retval = True
            except:
                pass
        return retval

    def get_yr_from_uid (self, uid):
        uid_match = self.UID_REGEX.match(uid.strip())
        if uid_match and len(uid_match.groups()) == 2:
            Y = uid_match.group(1)
            R = uid_match.group(2)
            return int(Y), int(R)
        else:
            return None, None

    # NOT USED ANY MORE
    def get_ref_from_uid (self, uid):
        Y, R = self.get_yr_from_uid (uid)
        if Y and R:
            return (Y * 10000) + R
        else:
            return None

    # NOT USED ANY MORE
    def get_year_max_ref (self, year, ascending = False, target = 3000):
        ret = None
        if ascending:
            start = 1;  end = target + 1; step = 1
        else:
            start = target; step = -1; end = 0
        for i in range(start,end,step):
            url = self.applic_url + '?Y='+str(year)+'&R='+str(i)
            #print url
            try:
                response = self.br.open(url)
                html = response.read()
                result = scrapemark.scrape(self.scrape_not_found, html)
                if ascending and result and result.get('not_found'):
                    ret = i - 1
                    break
                elif not ascending and (not result or not result.get('not_found')): 
                    ret = i
                    break
            except:
                return None
        return ret

    def get_id_period (self, date):

        fields = self.search_fields
        from_iso_dt, to_iso_dt = util.inc_dt(date.strftime(util.ISO8601_DATE), util.ISO8601_DATE, self.PERIOD_TYPE)
        from_dt = util.get_dt(from_iso_dt, util.ISO8601_DATE)
        to_dt = util.get_dt(to_iso_dt, util.ISO8601_DATE)
        fields [self.date_select] = to_dt.strftime(self.request_date_format)

        final_result = []
        
        response = util.open_url(self.br, self.search_url, fields, 'POST')
        if response:
            html = response.read()
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
        else:
            return [], None, None

        return final_result, from_dt, to_dt # note weekly result might some times be legitimately empty
            
if __name__ == 'scraper':

    scraper = SolihullScraper()

    #scraper.populate_missing_applications()
    #scraper.DEBUG = True
    #scraper.reset('2010-12-31', '2013-04-26')
    scraper.run()

    # misc tests
    #print "Max id in 2011 = ", scraper.get_year_max_ref(2011)
    #print "Max id in 2011 = ", scraper.get_year_max_ref(2011, True)
    #print scraper.get_detail_from_uid ('2009/500')
    #print scraper.get_detail_from_uid ('2012/1')
    #result = scraper.get_id_records(20000001, 20110100)
    #result = scraper.get_id_records(20110500)
    #print result
    #print scraper.gather_ids(None, None)
    #scraper.gather_current_ids()
    
    #current_applications = scraperwiki.sqlite.select("uid, url from " + scraper.TABLE_NAME + " where date_scraped is not null and uid not like '%/%' limit 100")
    #print "N of old ids to be updated", len(current_applications)
    #for applic in current_applications:
    #    scraper.update_application_detail(applic)

    #util.rename_column('swdata', 'ward', 'ward_name')

    
    #print scraper.get_id_period(util.get_dt('27/03/2013'))
    #print scraper.is_zombie('2008/787')

