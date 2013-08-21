# this is a scraper of National Infrastructure Planning applications for use by Openly Local

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

class NIPScraper(base.PeriodScraper):

    START_SEQUENCE = '2011-01-01'
    MAX_ID_BATCH = 50 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 20 # max application details to scrape in one go
    PERIOD_TYPE = 'Fixed'

    applic_url = 'http://infrastructure.planningportal.gov.uk/projects/'
    search_url = 'http://infrastructure.planningportal.gov.uk/projects/register-of-applications/'
    html_subs = { r'zoom=\d+"': r'zoom="', r'<i>\s*by ': r'<i>' }
    scrape_ids = """
    <table> <tr /> 
    {* <tr> <td> <a href="{{ [records].url|abs }}"> {{ [records].description }} </a> </td>
    <td> {{ [records].address }} </td>
    <td> {{ [records].applicant_name }} </td>
    <td> {{ [records].date_received }} </td>
    <td> {{ [records].date_validated }} </td>
    <td /> <td> {{ [records].status }} </td>
    </tr> *}
    </table>
    """
    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = """
    <div id="page"> {{ block|html }} </div>
    """
    # the minimum acceptable valid dataset on an application page
    scrape_min_data = """
    <div id="projecthead"> <h1> {{ description }} </h1> </div>
    <h3> Location </h3> <div class="textwidget"> <p> {{ address }} </p> </div>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<div class="ipc_project_about"> <h2 /> {{ details }} <p /> </div>',
    '<h1 /> <i> {{ applicant_name }} </i>',
    '<p> Developer: <a> {{ agent_name }} </a> </p>',
    """<div id="projectmap">
    <div style="position: absolute;">
    <a href="http://www.openstreetmap.org/?lat={{ lat }}&amp;lon={{ lng }}&amp;zoom="> </a>
    </div> </div>""",
    ]

    def get_id_period (self, this_date):

        from_dt = this_date
        to_dt = date.today()

        response = self.br.open(self.search_url) # one fixed page of records
        
        final_result = []
        if response:
            html = response.read()
            url = response.geturl()
            if self.DEBUG: print html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if self.DEBUG: print self.scrape_ids
            if self.DEBUG: print result
            if result and result.get('records'):
                for r in result['records']:
                    r['uid'] = r['url'].replace(self.applic_url, '')
                    try:
                        dt = dateutil.parser.parse(r['date_received'], dayfirst=True).date()
                        r['date_received'] = dt.strftime(util.ISO8601_DATE)
                        if dt < from_dt:
                            from_dt = dt
                    except:
                        del r['date_received'] # badly formatted dates are removed
                    try:
                        dt = dateutil.parser.parse(r['date_validated'], dayfirst=True).date()
                        r['date_validated'] = dt.strftime(util.ISO8601_DATE)
                    except:
                        del r['date_validated'] # badly formatted dates are removed
                self.clean_ids(result['records'])
                final_result.extend(result['records'])

        if final_result:
            return final_result, from_dt, to_dt
        else:
            return [], None, None # yearly scraper - so empty result is always invalid

    def get_detail_from_uid (self, uid):
        url = self.applic_url + uid
        return self.get_detail_from_url(url)

    def get_detail_from_url (self, url):

        try:
            response = self.br.open(url)
            html = response.read()
            url = response.geturl()

            for k, v in self.html_subs.items(): # adjust html to make match
                html = re.sub(k, v, html, 0, re.U|re.S|re.I) # unicode|dot matches new line|ignore case

            if self.DEBUG: print html
            
        except:
            if self.DEBUG: raise
            else: return None

        result = self.get_detail(html, url)
        if result:
            if result.get('details'):
                result['description'] = result['description'] + ' ' + result['details']
                del result['details']

        #    if result.get('lat') and result.get('lng'):
        #        info = util.get_local_info(result['lng'], result['lat'])
        #        result['postcode'] = info['postcode']
        #        result['region'] = info['region']
        #        if len(info['councils']) > 1:
        #            for c in info['councils']:
        #                result[c['type']] = c['name']
        #        else:
        #            result['district'] = info['councils'][0]['name']
        #            result['county'] = info['councils'][0]['name']
                
        return result
            
if __name__ == 'scraper':

    scraper = NIPScraper()
    scraper.run()

    #scraper.DEBUG = True
    # misc tests
    #print scraper.get_detail_from_uid ('north-east/port-blyth-new-biomass-plant/')
    #print scraper.get_detail_from_uid ('wales/brig-y-cwm-energy-from-waste-generating-station/')
    #result = scraper.get_id_period(util.get_dt('01/01/2012'))
    #print result
    #print util.inc_dt('2010-02-01', util.ISO8601_DATE, 'Month')
    #print "Found " + str(len(result)) + " ids for Mar 2012"
    #print scraper.gather_ids('2010-02-01')
    #print scraper.gather_ids(None, None)
    #scraper.gather_current_ids()

    #util.rename_column('swdata', 'council', 'district')
    #scraperwiki.sqlite.save_var('latest', 20120800)

    #print util.get_local_info('IP2 0UB')
