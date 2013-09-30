# this is a base scraper for SwiftLG system planning applications for use by Openly Local

# there are 20 authorities using this system, all are defined here but only the first 10 are scraped

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import random
import urllib
import urlparse
import sys

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

systems = {
    'Boston': 'BostonScraper', # fixed IP for URLs
    'CannockChase': 'CannockChaseScraper',
    'Daventry': 'DaventryScraper', # fixed IP for URLs
    'Dudley': 'DudleyScraper',
    'EastHertfordshire': 'EastHertfordshireScraper',
    'Enfield': 'EnfieldScraper',
    'Gwynedd': 'GwyneddScraper',
    #'Islington': 'IslingtonScraper', now Planning Explorer
    'LakeDistrict': 'LakeDistrictScraper', # National Park
    'Maidstone': 'MaidstoneScraper',
    # for following systems - see 2nd SwiftLG scraper
    #'MoleValley': 'MoleValleyScraper',
    #'Newport': 'NewportScraper',
    #'NorthDorset': 'NorthDorsetScraper',
    #'Oxfordshire': 'OxfordshireScraper',
    #'Pembrokeshire': 'PembrokeshireScraper',
    #'Redbridge': 'RedbridgeScraper',
    #'Rochdale': 'RochdaleScraper', # now Idox
    #'Rutland': 'RutlandScraper',
    #'Slough': 'SloughScraper',
    #'Snowdonia': 'SnowdoniaScraper', # National Park fixed IP address
    #'SouthCambridgeshire': 'SouthCambridgeshireScraper',
    #'Warrington': 'WarringtonScraper',
    #'Warwickshire': 'WarwickshireScraper',
     }

class SwiftLGScraper(base.DateScraper):

    MAX_ID_BATCH = 200 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 300 # max application details to scrape in one go

    field_dot_suffix = False
    date_from_field = 'REGFROMDATE.MAINBODY.WPACIS.1'
    date_to_field = 'REGTODATE.MAINBODY.WPACIS.1'
    search_form = '0'
    scrape_ids = """
    <form> <table> <tr />
    {* <tr>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    </tr> *}
    </table> </form>
    """
    scrape_next_link = [
        'Pages : <a href="{{ next_link }}"> </a>',
        '<p> Pages: <a href="#" /> <a href="{{ next_link }}"> </a> </p>',
        '<p> Pages: <a href="{{ next_link }}"> </a> </p>',
    ]
    detail_page = 'WPHAPPDETAIL.DisplayUrl'
    scrape_max_recs = [
        'returned {{ max_recs }} matches',
        'found {{ max_recs }} matching',
        '<p>Search results: {{ max_recs }} <br>',
        'returned {{ max_recs }} matche(s).'
    ]
    html_subs = {
    r'<a href="([^"]*?)&(?:amp;)*[bB]ackURL=[^"]*?">': r'<a href="\1">',
    }

    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = '<body> {{ block|html }} </body>'
    # flags defining field boundaries
    start_flag = '<label>'
    mid_flag = '</label>'
    end_flag = '<label/>'
    # the minimum acceptable valid dataset on the details page
    #scrape_min_dates = """
    #<div class="tabContent"> <label> Decision </label> {{ decision }} <br> <label> Decision Date </label> {{ decision_date }} <div /> </div>
    #""
    #scrape_min_appeal = """
    #<label> Appeal Lodged Date </label> {{ appeal_date }} <br> 
    #""
    # config scrape templates for all fields
    scrape_config = {
    'reference': "__start__ Application Reference __mid__ {{ __field__ }} __end__",
    'date_validated': "__start__ Registration __mid__ {{ __field__ }} __end__",
    'address': "__start__ Location __mid__ {{ __field__ }} __end__",
    'application_type': "__start__ Application Type __mid__ {{ __field__ }} __end__",
    'date_received': "__start__ Application Date __mid__ {{ __field__ }} __end__",
    'description': "__start__ Proposal __mid__ {{ __field__ }} __end__",
    'status': "__start__ Status __mid__ {{ __field__ }} __end__",
    'ward_name': "__start__ Ward __mid__ {{ __field__ }} __end__",
    'parish': "__start__ Parish __mid__ {{ __field__ }} __end__",
    'district': "__start__ Area __mid__ {{ __field__ }} __end__",
    'case_officer': "__start__ Case Officer __mid__ {{ __field__ }} __end__",
    'applicant_name': "Applicant Details __start__ Company __mid__ {{ __field__ }} __end__", 
    'agent_name': "Agent Details __start__ Company __mid__ {{ __field__ }} __end__",
    #'applicant_name': "Applicant Details {* __start__ __mid__ {{ [__field__] }} __end__ *} __start__ Address __mid__ ",
    #'agent_name': "Agent Details {* __start__ __mid__ {{ [__field__] }} __end__ *}  __start__ Address __mid__ ",
    'applicant_address': "Applicant Details __start__ Address __mid__ {{ __field__ }} __end__",
    'agent_address': "Agent Details __start__ Address __mid__ {{ __field__ }} __end__",
    'decision_date': "__start__ Decision Date __mid__ {{ __field__ }} __end__",
    'consultation_start_date': "__start__ Publicity Start Date __mid__ {{ __field__ }} __end__",
    'consultation_end_date': "__start__ Publicity End Date __mid__ {{ __field__ }} __end__",
    }
    scrape_variants = {}
    #scrape_optional_dates = [
    #"<label> Publicity Start Date </label> {{ consultation_start_date }} <br>",
    #"<label> Publicity End Date </label> {{ consultation_end_date }} <br>",
    #]
    #scrape_optional_appeal = [
    #"<label> Appeal Decision </label> {{ appeal_result }} <br> <label> Appeal Decision Date </label> {{ appeal_decision_date }} <br>",
    #]

    def __init__(self, table_name = None):
        base.DateScraper.__init__(self, table_name)
        self.scrape_config.update(self.scrape_variants)
        self.scrape_optional_data = []
        for k, v in self.scrape_config.items():
            v = v.replace('__start__', self.start_flag)
            v = v.replace('__mid__', self.mid_flag)
            v = v.replace('__end__', self.end_flag)
            v = v.replace('__field__', k)
            if k == 'reference':
                self.scrape_min_data = v
            else:
                self.scrape_optional_data.append(v)

    def get_id_batch (self, date_from, date_to):

        if self.DEBUG: self.br.set_debug_http(True)

        response = self.br.open(self.search_url)

        fields = {}
        if self.field_dot_suffix:
            fields[self.date_from_field + '.'] = date_from.strftime(self.request_date_format)
            fields[self.date_to_field + '.'] = date_to.strftime(self.request_date_format)
        else:
            fields[self.date_from_field] = date_from.strftime(self.request_date_format)
            fields[self.date_to_field] = date_to.strftime(self.request_date_format)
        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br)
        html = response.read()
        url = response.geturl()
        for k, v in self.html_subs.items():
            html = re.sub(k, v, html, 0, re.U|re.S|re.I) # unicode|dot matches new line|ignore case
        if self.DEBUG: print html
        max_recs = 0
        for scrape in self.scrape_max_recs:
            try:
                result = scrapemark.scrape(scrape, html)
                if self.DEBUG: print result
                max_recs = int(result['max_recs'])
                break
            except:
                pass
        final_result = []
        while len(final_result) < max_recs:
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            else:
                break
            if len(final_result) >= max_recs:
                break
            try:
                for scrape in self.scrape_next_link:
                    result = scrapemark.scrape(scrape, html, url)
                    if result: break
                #print result
                #next_url = self.BACK_REGEX.sub('', result['next_link'])
                next_batch = len(final_result) + 1
                replacement = '&StartIndex=' + str(next_batch) + '&SortOrder'
                next_url = re.sub(r'&StartIndex=\d+&SortOrder', replacement, result['next_link'])
                #print next_url
                response = self.br.open(next_url)
                html = response.read()
                url = response.geturl()
                for k, v in self.html_subs.items():
                    html = re.sub(k, v, html, 0, re.U|re.S|re.I) # unicode|dot matches new line|ignore case
                if self.DEBUG: print html
            except:
                break
        return final_result

    def get_detail_from_uid (self, uid):
        url = urlparse.urljoin(self.search_url, self.detail_page) + '?theApnID=' + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

    # scrape detailed information on one record via its access URL
    def get_detail_from_url (self, url):
        if self.DEBUG: print "Url:", url
        try:
            response = self.br.open(url)
            html = response.read()
            this_url = response.geturl()
            if self.DEBUG:
                print "Html obtained from details url:", html
        except:
            if self.DEBUG: raise
            else: return None
        return self.get_detail(html, this_url)

class BostonScraper(SwiftLGScraper): 

    # note fixed IP address was 194.72.114.25
    search_url = 'http://93.93.220.239/swiftlg/apas/run/wphappcriteria.display'
    ID_ORDER = "CASE uid WHEN substr(uid, 3, 2) < '50' THEN '20' || uid ELSE '19' || uid END desc"
    TABLE_NAME = 'Boston'
    field_dot_suffix = False
    end_flag = "<br>"
    scrape_variants = {
        'address': "__start__ Location __mid__ {{ __field__ }} <p/>",
        'case_officer': "__start__ Case Officer __mid__ {{ __field__ }} <h2/>",
    }

class CannockChaseScraper(SwiftLGScraper):

    search_url = 'http://planning.cannockchasedc.com/swiftlg/apas/run/wphappcriteria.display'
    ID_ORDER = "CASE uid WHEN substr(uid, 4, 2) < '50' THEN '20' || uid ELSE '19' || uid END desc"
    TABLE_NAME = 'CannockChase'
    scrape_variants = {
        'reference': "__start__ Application Ref __mid__ {{ __field__ }} __end__",
        'description': "__start__ Full Description __mid__ {{ __field__ }} __end__",
        'status': "__start__ Status Description __mid__ {{ __field__ }}__end__",
        'case_officer': "__start__ Case Officer __mid__ {{ __field__ }} <h2/>",
        'agent_address': "Agent Details __start__ Address __mid__ <p> {{ __field__ }} </p>",
    }

class DaventryScraper(SwiftLGScraper):

    BATCH_DAYS = 28 # batch size for each scrape - number of days to gather to produce at least one result each time
    MIN_DAYS = 28 # min number of days to get when gathering current ids
    search_url = 'http://78.25.201.88/swiftlg/apas/run/wphappcriteria.display'
    #ID_ORDER = "uid desc"
    TABLE_NAME = 'Daventry'
    field_dot_suffix = False
    end_flag = "<br>"
    scrape_variants = {
        'reference': "__start__ Reference Number __mid__ {{ __field__ }} __end__",
        'address': "__start__ Location __mid__ {{ __field__ }} <p/>",
        'applicant_name': "Applicant Details __start__ Name __mid__ {{ __field__ }} __end__ ",
        'agent_name': "Agent Details __start__ Name __mid__ {{ __field__ }} __end__ ",
        'decision': "__start__ Decision __mid__ {{ __field__ }} __end__ __start__ Decision Date __mid__ Appeal Decision", 
        'decision_date': "__start__ Decision __mid__ __start__ Decision Date __mid__ {{ __field__ }} __end__ Appeal Decision", 
        'appeal_date': "__start__ Appeal Lodged Date __mid__ {{ __field__ }} __end__",
        'appeal_result': "__start__ Appeal Decision __mid__ {{ __field__ }} __end__ __start__ Appeal Decision Date __mid__",
        'appeal_decision_date': "__start__ Appeal Decision __mid__ __start__ Appeal Decision Date __mid__ {{ __field__ }} __end__",
    }

class DudleyScraper(SwiftLGScraper):

    search_url = 'http://www2.dudley.gov.uk/swiftlg/apas/run/Wphappcriteria.display'
    TABLE_NAME = 'Dudley'
    ID_ORDER = "CASE uid WHEN substr(uid, 2, 2) < '50' THEN '20' || uid ELSE '19' || uid END desc"
    search_form = '1'
    scrape_variants = {
        'reference': "__start__ Application Ref __mid__ {{ __field__ }} __end__",
        'case_officer': "__start__ Case Officer __mid__ {{ __field__ }} <h6/>",
        'agent_address': "Agent Details__start__ Address __mid__ <p> {{ __field__ }} </p>",
    }

class EastHertfordshireScraper(SwiftLGScraper):

    search_url = 'http://online.eastherts.gov.uk/swiftlg/apas/run/wphappcriteria.display'
    TABLE_NAME = 'EastHertfordshire'
    ID_ORDER = "CASE uid WHEN substr(uid, 3, 2) < '50' THEN '20' || uid ELSE '19' || uid END desc"
    scrape_ids = """
    <form> <table /> <table> <tr />
    {* <tr>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    </tr> *}
    </table> </form>
    """
    start_flag = '<b>'
    mid_flag = '</b>'
    end_flag = '<b/>'
    scrape_variants = {
        'status': "__start__ Status __mid__ <td> {{ __field__|html }} </td>",
        'consultation_start_date': "<label> Publicity Start Date </label> {{ __field__ }} <br>",
        'consultation_end_date': "<label> Publicity End Date </label> {{ __field__ }} <br>",
        'applicant_name': "Applicant __start__ Company __mid__ <td> {{ __field__ }} </td>",
        'agent_name': "Agent __start__ Company __mid__ <td> {{ __field__ }} </td>",
        'applicant_address': "Applicant __start__ Address __mid__ <td> {{ __field__ }} </td>",
        'agent_address': "Agent __start__ Address __mid__ <td> {{ __field__ }} </td>",
    }

class EnfieldScraper(SwiftLGScraper):

    search_url = 'http://forms.enfield.gov.uk/swiftlg/apas/run/wphappcriteria.display'
    TABLE_NAME = 'Enfield'
    field_dot_suffix = True
    end_flag = "<br>"
    scrape_variants = {
        'case_officer': "__start__ Case Officer __mid__ {{ __field__ }} <h2/>",
    }
    
class GwyneddScraper(SwiftLGScraper):

    search_url = 'http://www.gwynedd.gov.uk/swiftlg/apas/run/wphappcriteria.display?langid=1'
    TABLE_NAME = 'Gwynedd'
    ID_ORDER = "CASE uid WHEN substr(uid, 2, 2) < '50' THEN '20' || uid ELSE '19' || uid END desc"
    search_form = '1'
    end_flag = '<br>'
    scrape_variants = {
        'parish': "__start__ Community __mid__ {{ __field__ }} __end__",
        'applicant_name': "<span> Applicant </span> __start__ Name __mid__ {{ __field__ }} __end__",
        'agent_name': "<span> Agent </span> __start__ Name __mid__ {{ __field__ }} __end__",
        'applicant_address': "<span> Applicant </span> __start__ Address __mid__ {{ __field__ }} __end__",
        'agent_address': "<span> Agent </span> __start__ Address __mid__ {{ __field__ }} __end__",
    }

class IslingtonScraper(SwiftLGScraper):

    search_url = 'https://www.islington.gov.uk/onlineplanning/apas/run/wphappcriteria.display'
    TABLE_NAME = 'Islington'
    field_dot_suffix = True
    html_subs = {
    r'</(t[dhr]) class=".*?">': r'</\1>',
    r"<a href='([^']*?)&(?:amp;)*[bB]ackURL=[^']*?'>": r"<a href='\1'>",
    r'<a href="([^"]*?)&(?:amp;)*[bB]ackURL=[^"]*?">': r'<a href="\1">',
    }
    scrape_variants = {
        'reference': "__start__ Application Number __mid__ {{ __field__ }} __end__",
        'date_validated': "__start__ Date Valid __mid__ {{ __field__ }} __end__",
        'status': "__start__ Status __mid__ <td> {{ __field__|html }} </td>",
        'consultation_start_date': "__start__ Consultation Start __mid__ {{ __field__ }} __end__",
        'consultation_end_date': "__start__ Consultation End __mid__ {{ __field__ }} __end__",
        'applicant_address': "Applicant Details __start__ Address __mid__ {{ __field__ }} <h2/>",
        'agent_address': "Agent Details__start__ Address __mid__ {{ __field__ }} <h2/>",
        'decision_date': "__start__ Decision Date __mid__ {{ __field__ }} __start__ Decision __mid__ Consultation",
        'decision': "__start__ Decision Date __mid__ __start__ Decision __mid__ {{ __field__ }} __end__ Consultation", 
    }

class LakeDistrictScraper(SwiftLGScraper):

    search_url = 'http://www.lakedistrict.gov.uk/swiftlg/apas/run/wphappcriteria.display'
    TABLE_NAME = 'LakeDistrict'
    ID_ORDER = 'uid desc'
    search_form = '1'
    scrape_variants = {
        'district': "__start__ District __mid__ {{ __field__ }} __end__",
        'status': "__start__ Progress __mid__ {{ __field__ }} __end__",
        'decision': "__start__ Decision __mid__ {{ __field__ }} __end__ __start__ Decision Date __mid__ Location",
        'decision_date': "__start__ Decision __mid__ __end__ __start__ Decision Date __mid__ <td> {{ __field__ }} </td> Location", 
        'applicant_name': "<strong> Applicant </strong> <td> {{ __field__ }} </td>",
        'agent_name': "<strong> Agent </strong> <td> {{ __field__ }} </td>",
        'applicant_address': "<strong> Applicant </strong> <td /> <td /> <td> {{ __field__ }} </td>",
        'agent_address': "<strong> Agent </strong> <td> <td /> <td /> {{ __field__ }} </td>",
    }

class MaidstoneScraper(SwiftLGScraper):

    search_url = 'http://www.maidstone.gov.uk/swiftlg/apas/run/wphappcriteria.display'
    TABLE_NAME = 'Maidstone'
    field_dot_suffix = True
    scrape_variants = {
        'reference': "__start__ Application Ref __mid__ {{ __field__ }} __end__",
        'description': "__start__ Full Description __mid__ {{ __field__ }} __end__",
        'status': "__start__ Status Description __mid__ {{ __field__ }} __end__",
        'case_officer': "__start__ Case Officer __mid__ {{ __field__ }} <h2/>",
        'agent_address': "Agent Details __start__ Address __mid__ <p> {{ __field__ }} </p>",
    }

class MoleValleyScraper(SwiftLGScraper):

    search_url = 'http://www.molevalley.gov.uk/swiftlg/apas/run/wphappcriteria.display'
    TABLE_NAME = 'MoleValley'
    ID_ORDER = 'uid desc'
    scrape_variants = {
        'reference': "__start__ Application Ref __mid__ {{ __field__ }} __end__",
        'description': "__start__ Full Description __mid__ {{ __field__ }} __end__",
        'status': "__start__ Status Description __mid__ {{ __field__ }} __end__",
        'case_officer': "__start__ Case Officer __mid__ {{ __field__ }} <h2/>",
        'agent_address': "Agent Details __start__ Address __mid__ <p> {{ __field__ }} </p>",
    }

class NewportScraper(SwiftLGScraper):

    search_url = 'http://planning.newport.gov.uk/swift/apas/run/wphappcriteria.display'
    TABLE_NAME = 'Newport'
    ID_ORDER = "CASE uid WHEN substr(uid, 1, 2) < '50' THEN '20' || uid ELSE '19' || uid END desc"
    scrape_variants = {
        'reference': "__start__ Application Ref __mid__ {{ __field__ }} __end__",
        'address': "__start__ Location __mid__ {{ __field__ }} <a/>",
        'description': "__start__ Application Description __mid__ {{ __field__ }} <span> Show </span>",
        'parish': "__start__ Community Council __mid__ {{ __field__ }} __end__",
        'agent_address': "Agent Details __start__ Address __mid__ <p> {{ __field__ }} </p>",
        'applicant_address': "Applicant Details __start__ Address __mid__ <p> {{ __field__ }} </p>",
        'decision': "__start__ Decision Date __mid__ __start__ Decision __mid__ {{ __field__ }} __end__", 
    }

class NorthDorsetScraper(SwiftLGScraper):

    search_url = 'http://plansearch.north-dorset.gov.uk/swiftlg/apas/run/wphappcriteria.display'
    TABLE_NAME = 'NorthDorset'
    ID_ORDER = 'uid desc'
    scrape_variants = {
        'reference': "__start__ Application Ref __mid__ {{ __field__ }} __end__",
        'description': "__start__ Full Description __mid__ {{ __field__ }} __end__",
        'status': "__start__ Status Description __mid__ <p> {{ __field__ }} </p>",
        'case_officer': "__start__ Case Officer __mid__ {{ __field__ }} <h2/>",
        'agent_address': "Agent Details __start__ Address __mid__ <p> {{ __field__ }} </p>",
    }

class OxfordshireScraper(SwiftLGScraper):

    BATCH_DAYS = 60 # batch size for each scrape - number of days to gather to produce at least one result each time
    MIN_DAYS = 42 # min number of days to get when gathering current ids
    search_url = 'http://myeplanning.oxfordshire.gov.uk/swiftlg/apas/run/Wphappcriteria.display'
    TABLE_NAME = 'Oxfordshire'
    scrape_variants = {
        'reference': "__start__ Application Ref __mid__ {{ __field__ }} __end__",
        'description': "__start__ Description __mid__ {{ __field__ }} __end__",
        'date_validated': "__start__ Valid Date __mid__ {{ __field__ }} __end__",
        'address': "__start__ Location __mid__ {{ __field__ }} (<a/>)",
        'applicant_name': "__start__ Applicant Name __mid__ {{ __field__ }} __end__",
        'agent_name': "__start__ Agent Name __mid__ {{ __field__ }} __end__",
        'decision': "Comment __start__ Decision __mid__ {{ __field__ }} __start__ Decision Date __mid__",
        'decision_date': "Comment __start__ Decision __mid__ __start__ Decision Date __mid__ {{ __field__ }} <h2/>",
    }

class PembrokeshireScraper(SwiftLGScraper):

    BATCH_DAYS = 28 # batch size for each scrape - number of days to gather to produce at least one result each time
    MIN_DAYS = 28 # min number of days to get when gathering current ids
    search_url = 'http://planning.pembrokeshire.gov.uk/swiftlg/apas/run/wphappcriteria.display'
    TABLE_NAME = 'Pembrokeshire'
    ID_ORDER = "CASE uid WHEN substr(uid, 1, 2) < '50' THEN '20' || uid ELSE '19' || uid END desc"
    scrape_variants = {
        'reference': "__start__ Application Ref __mid__ {{ __field__ }} __end__",
        'description': "__start__ Description __mid__ {{ __field__ }} __end__",
        'date_validated': "__start__ Validated Date __mid__ {{ __field__ }} __end__",
        'parish': "__start__ Community __mid__ {{ __field__ }} __end__",
        'address': "__start__ Location __mid__ {{ __field__ }} (<a/>)",
        'decision_date': "__start__ Decision Date __mid__ {{ __field__ }} __start__ Decision __mid__",
        'decision': "__start__ Decision Date __mid__ __start__ Decision __mid__ {{ __field__ }} __end__",
        'case_officer': "__start__ Case Officer __mid__ {{ __field__ }} <h2/>",
        'agent_address': "Agent Details __start__ Address __mid__ <p> {{ __field__ }} </p>",
    }

class RedbridgeScraper(SwiftLGScraper):

    search_url = 'http://planning.redbridge.gov.uk/swiftlg/apas/run/wphappcriteria.display'
    TABLE_NAME = 'Redbridge'
    search_form = '1'
    scrape_variants = {
        'reference': "__start__ Application Ref __mid__ {{ __field__ }} __end__",
        'description': "__start__ Description __mid__ {{ __field__ }} __end__",
        'agent_address': "Agent Details __start__ Address __mid__ <div> {{ __field__ }} </div>",
        'applicant_address': "Applicant Details __start__ Address __mid__ <div> {{ __field__ }} </div>",
        'applicant_name': "Applicant Details __start__ Name __mid__ {{ __field__ }} __end__",
    }

class RochdaleScraper(SwiftLGScraper): # note no applications after 28 May 2012 - it's Idox after that

    search_url = 'http://online.rochdale.gov.uk/swiftlg/apas/run/wphappcriteria.display'
    TABLE_NAME = 'Rochdale'
    field_dot_suffix = True
    end_flag = '<br>'
    scrape_variants = {
        'address': "__start__ Location __mid__ {{ __field__ }} <p/>",
        'description': "__start__ Description __mid__ {{ __field__ }} __end__",
        'case_officer': "__start__ Case Officer __mid__ {{ __field__ }} <h2/>",
    }

class RutlandScraper(SwiftLGScraper): 

    search_url = 'http://planningonline.rutland.gov.uk/swift/apas/run/wphappcriteria.display'
    TABLE_NAME = 'Rutland'
    ID_ORDER = "substr(uid, 5) desc"
    scrape_variants = {
        'reference': "__start__ Application Ref __mid__ {{ __field__ }} __end__",
        'description': "__start__ Full Description __mid__ {{ __field__ }} __end__",
        'case_officer': "__start__ Case Officer __mid__ {{ __field__ }} <h2/>",
        'agent_address': "Agent Details __start__ Address __mid__ <p> {{ __field__ }} </p>",
    }
class SloughScraper(SwiftLGScraper):

    search_url = 'http://www2.slough.gov.uk/swiftlg/apas/run/wphappcriteria.display'
    TABLE_NAME = 'Slough'
    scrape_variants = {
        'reference': "__start__ Application Ref __mid__ {{ __field__ }} __end__",
        'description': "__start__ Description __mid__ {{ __field__ }} __end__",
        'address': "__start__ Location __mid__ {{ __field__ }} (<a/>)",
        'agent_address': "Agent Details __start__ Address __mid__ <p> {{ __field__ }} </p>",
        'case_officer': "__start__ Case Officer __mid__ <p> {{ __field__ }} </p>",
    }

class SnowdoniaScraper(SwiftLGScraper):

    search_url = 'http://217.77.186.246:8080/swiftlg_snpa/apas/run/wphappcriteria.display'
    TABLE_NAME = 'Snowdonia'
    scrape_variants = {
        'reference': "__start__ Application Ref __mid__ {{ __field__ }} __end__",
        'description': "__start__ Description __mid__ {{ __field__ }} __end__",
        'address': "__start__ Location __mid__ {{ __field__ }} (<a/>)",
        'agent_address': "Agent Details __start__ Address __mid__ <p> {{ __field__ }} </p>",
        'case_officer': "__start__ Case Officer __mid__ {{ __field__ }} <h2/>",
    }

class SouthCambridgeshireScraper(SwiftLGScraper):

    search_url = 'http://plan.scambs.gov.uk/swiftlg/apas/run/wphappcriteria.display'
    TABLE_NAME = 'SouthCambridgeshire'
    search_form = '1'
    scrape_variants = {
        'reference': "__start__ Application Ref __mid__ {{ __field__ }} __end__",
        'description': "__start__ Description __mid__ {{ __field__ }} __end__",
        'agent_address': "Agent Details __start__ Address __mid__ <p> {{ __field__ }} </p>",
        'case_officer': "__start__ Case Officer __mid__ {{ __field__ }} <h2/>",
    }
    
class WarringtonScraper(SwiftLGScraper):

    search_url = 'http://planning.warrington.gov.uk/swiftlg/apas/run/wphappcriteria.display'
    TABLE_NAME = 'Warrington'
    ID_ORDER = 'uid desc'
    search_form = '1'
    scrape_variants = {
        'reference': "__start__ Application&#160;Number __mid__ {{ __field__ }} <p/>",
        'address': "__start__ Location __mid__ <p> {{ __field__ }} </p>",
        'applicant_name': "Applicant Details <p> <strong> Company </strong> {{ __field__ }} </p>", 
        'agent_name': "Agent Details <p> <strong> Company </strong> {{ __field__ }} </p>",
        'applicant_address': "Applicant Details <p> <strong> Address </strong> {{ __field__ }} </p>",
        'agent_address': "Agent Details <p> <strong> Address </strong> {{ __field__ }} </p>",
    }

class WarwickshireScraper(SwiftLGScraper):

    BATCH_DAYS = 60 # batch size for each scrape - number of days to gather to produce at least one result each time
    MIN_DAYS = 60 # min number of days to get when gathering current ids
    search_url = 'https://planning.warwickshire.gov.uk/swiftlg/apas/run/wphappcriteria.display'
    TABLE_NAME = 'Warwickshire'
    scrape_variants = {
        'reference': "__start__ Reference Number __mid__ {{ __field__ }} __end__",
        'description': "__start__ Description __mid__ {{ __field__ }} __end__",
        'status': "__start__ Current Position __mid__ {{ __field__ }} __end__",
        'agent_address': "Agent Details __start__ Address __mid__ <p> {{ __field__ }} </p>",
        'applicant_address': "Applicant Details __start__ Address __mid__ <p> {{ __field__ }} </p>",
        'case_officer': "__start__ Case Officer __mid__ <p> {{ __field__ }} </p>",
        'decision': "__start__ Decision __mid__ {{ __field__ }} __start__ Decision Date __mid__",
        'decision_date': "__start__ Decision __mid__ __start__ Decision Date __mid__ {{ __field__ }} __end__",
        'consultation_end_date': "__start__ Consultation Ends __mid__ {{ __field__ }} __end__",
    }

if __name__ == 'scraper':

    #scraperwiki.sqlite.execute("update Slough set date_scraped = null, address = null, status = null where uid = 'P/00162/056'")
    #scraperwiki.sqlite.commit()
    #scraper = MoleValleyScraper('MoleValley')
    #scraper = EnfieldScraper('Enfield')
    #scraper.reset('2004-07-14', '2012-11-01')
    #scraper.reset('2006-08-07', '2012-11-01')
    #scraper.DEBUG = True
    #scraper.gather_current_ids()
    #scraper.MAX_UPDATE_BATCH = 1000
    #scraper.ID_ORDER = 'rowid desc'
    #scraper.populate_missing_applications()
    #scraper.reset('2004-07-14', '2012-11-01')

    #util.rename_column('Daventry', 'appeal_decision', 'appeal_result')
    #sys.exit()

    #util.replace_vals('Boston', 'url', 'http://194.72.114.25/', 'http://93.93.220.239/', 'prefix', 'yes')
    #scraper = BostonScraper()
    #scraper.run()
    #scraper = DaventryScraper()
    #scraper.run()
    #scraper = DudleyScraper()
    #scraper.run()
    #sys.exit()

    sys_list = []
    for k, v in systems.items(): # get latest date scraped for each system
        sys_list.append( (k, v, scraperwiki.sqlite.get_var('latest-' + k)) )
    sort_sys = sorted(sys_list, key=lambda system: system[2]) # sort so least recent are first
    for auth in sort_sys[:6]: # do max 6 per run
        strexec = auth[1] + "('" + auth[0] + "')"
        print "Scraping from:", strexec
        try:
            scraper = eval(strexec)
            scraper.run()
        except Exception as err:
            print "Error - skipping this authority -", str(err)
    print "Finished"

    # misc test calls
    #scraper = BostonScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('B/11/0128') # Boston
    #print scraper.get_detail_from_uid ('B/13/0192')
    #scraper = CannockChaseScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('CH/11/0274') # CannockChase
    #scraper = DaventryScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('DA/2010/0002') # Daventry
    #scraper = DudleyScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('P13/0122 ') # Dudley
    #scraper = EastHertfordshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('3/11/1322/FP') # EastHertfordshire
    #scraper = EnfieldScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('LDC/11/0122') # Enfield
    #scraper = GwyneddScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('C11/0643/11/CT') # Gwynedd
    #scraper = IslingtonScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('P081406(MA01)') # Islington
    #scraper = LakeDistrictScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('7/2011/5414') # LakeDistrict
    #scraper = MaidstoneScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/1325') # Maidstone
    #scraper = MoleValleyScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('MO/2012/0800') # MoleValley
    #scraper = NewportScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('12/0356') # Newport
    #print scraper.get_detail_from_uid ('09/0245')
    #print scraper.get_detail_from_uid ('06/1048')
    #scraper = NorthDorsetScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('2/2011/0927/PLNG') # NorthDorset
    #scraper = OxfordshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('MW.0123/11') # Oxfordshire (low numbers)
    #scraper = PembrokeshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/0454/PA') # Pembrokeshire
    #scraper = RedbridgeScraper()
    #scraper.DEBUG = True   
    #print scraper.get_detail_from_uid ('WTPO/0082/12')
    #print scraper.get_detail_from_uid ('1631/11') # Redbridge
    #scraper = RochdaleScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/D54733') # Rochdale
    #scraper = RutlandScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('APP/2012/0923') # Rutland
    #scraper = SloughScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('P/00162/056') # Slough
    #scraper = SnowdoniaScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('NP5/66/230') # Snowdonia
    #scraper = SouthCambridgeshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('S/01021/12NM') # SouthCambridgeshire
    #scraper = WarringtonScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('2011/18599') # Warrington
    #scraper = WarwickshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('WDC/11CC015 ') # Warwickshire (low numbers)

    #res = scraper.get_id_batch(util.get_dt('01/01/2010'), util.get_dt('15/01/2010'))
    #print res, len(res)


    

# this is a base scraper for SwiftLG system planning applications for use by Openly Local

# there are 20 authorities using this system, all are defined here but only the first 10 are scraped

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import random
import urllib
import urlparse
import sys

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

systems = {
    'Boston': 'BostonScraper', # fixed IP for URLs
    'CannockChase': 'CannockChaseScraper',
    'Daventry': 'DaventryScraper', # fixed IP for URLs
    'Dudley': 'DudleyScraper',
    'EastHertfordshire': 'EastHertfordshireScraper',
    'Enfield': 'EnfieldScraper',
    'Gwynedd': 'GwyneddScraper',
    #'Islington': 'IslingtonScraper', now Planning Explorer
    'LakeDistrict': 'LakeDistrictScraper', # National Park
    'Maidstone': 'MaidstoneScraper',
    # for following systems - see 2nd SwiftLG scraper
    #'MoleValley': 'MoleValleyScraper',
    #'Newport': 'NewportScraper',
    #'NorthDorset': 'NorthDorsetScraper',
    #'Oxfordshire': 'OxfordshireScraper',
    #'Pembrokeshire': 'PembrokeshireScraper',
    #'Redbridge': 'RedbridgeScraper',
    #'Rochdale': 'RochdaleScraper', # now Idox
    #'Rutland': 'RutlandScraper',
    #'Slough': 'SloughScraper',
    #'Snowdonia': 'SnowdoniaScraper', # National Park fixed IP address
    #'SouthCambridgeshire': 'SouthCambridgeshireScraper',
    #'Warrington': 'WarringtonScraper',
    #'Warwickshire': 'WarwickshireScraper',
     }

class SwiftLGScraper(base.DateScraper):

    MAX_ID_BATCH = 200 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 300 # max application details to scrape in one go

    field_dot_suffix = False
    date_from_field = 'REGFROMDATE.MAINBODY.WPACIS.1'
    date_to_field = 'REGTODATE.MAINBODY.WPACIS.1'
    search_form = '0'
    scrape_ids = """
    <form> <table> <tr />
    {* <tr>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    </tr> *}
    </table> </form>
    """
    scrape_next_link = [
        'Pages : <a href="{{ next_link }}"> </a>',
        '<p> Pages: <a href="#" /> <a href="{{ next_link }}"> </a> </p>',
        '<p> Pages: <a href="{{ next_link }}"> </a> </p>',
    ]
    detail_page = 'WPHAPPDETAIL.DisplayUrl'
    scrape_max_recs = [
        'returned {{ max_recs }} matches',
        'found {{ max_recs }} matching',
        '<p>Search results: {{ max_recs }} <br>',
        'returned {{ max_recs }} matche(s).'
    ]
    html_subs = {
    r'<a href="([^"]*?)&(?:amp;)*[bB]ackURL=[^"]*?">': r'<a href="\1">',
    }

    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = '<body> {{ block|html }} </body>'
    # flags defining field boundaries
    start_flag = '<label>'
    mid_flag = '</label>'
    end_flag = '<label/>'
    # the minimum acceptable valid dataset on the details page
    #scrape_min_dates = """
    #<div class="tabContent"> <label> Decision </label> {{ decision }} <br> <label> Decision Date </label> {{ decision_date }} <div /> </div>
    #""
    #scrape_min_appeal = """
    #<label> Appeal Lodged Date </label> {{ appeal_date }} <br> 
    #""
    # config scrape templates for all fields
    scrape_config = {
    'reference': "__start__ Application Reference __mid__ {{ __field__ }} __end__",
    'date_validated': "__start__ Registration __mid__ {{ __field__ }} __end__",
    'address': "__start__ Location __mid__ {{ __field__ }} __end__",
    'application_type': "__start__ Application Type __mid__ {{ __field__ }} __end__",
    'date_received': "__start__ Application Date __mid__ {{ __field__ }} __end__",
    'description': "__start__ Proposal __mid__ {{ __field__ }} __end__",
    'status': "__start__ Status __mid__ {{ __field__ }} __end__",
    'ward_name': "__start__ Ward __mid__ {{ __field__ }} __end__",
    'parish': "__start__ Parish __mid__ {{ __field__ }} __end__",
    'district': "__start__ Area __mid__ {{ __field__ }} __end__",
    'case_officer': "__start__ Case Officer __mid__ {{ __field__ }} __end__",
    'applicant_name': "Applicant Details __start__ Company __mid__ {{ __field__ }} __end__", 
    'agent_name': "Agent Details __start__ Company __mid__ {{ __field__ }} __end__",
    #'applicant_name': "Applicant Details {* __start__ __mid__ {{ [__field__] }} __end__ *} __start__ Address __mid__ ",
    #'agent_name': "Agent Details {* __start__ __mid__ {{ [__field__] }} __end__ *}  __start__ Address __mid__ ",
    'applicant_address': "Applicant Details __start__ Address __mid__ {{ __field__ }} __end__",
    'agent_address': "Agent Details __start__ Address __mid__ {{ __field__ }} __end__",
    'decision_date': "__start__ Decision Date __mid__ {{ __field__ }} __end__",
    'consultation_start_date': "__start__ Publicity Start Date __mid__ {{ __field__ }} __end__",
    'consultation_end_date': "__start__ Publicity End Date __mid__ {{ __field__ }} __end__",
    }
    scrape_variants = {}
    #scrape_optional_dates = [
    #"<label> Publicity Start Date </label> {{ consultation_start_date }} <br>",
    #"<label> Publicity End Date </label> {{ consultation_end_date }} <br>",
    #]
    #scrape_optional_appeal = [
    #"<label> Appeal Decision </label> {{ appeal_result }} <br> <label> Appeal Decision Date </label> {{ appeal_decision_date }} <br>",
    #]

    def __init__(self, table_name = None):
        base.DateScraper.__init__(self, table_name)
        self.scrape_config.update(self.scrape_variants)
        self.scrape_optional_data = []
        for k, v in self.scrape_config.items():
            v = v.replace('__start__', self.start_flag)
            v = v.replace('__mid__', self.mid_flag)
            v = v.replace('__end__', self.end_flag)
            v = v.replace('__field__', k)
            if k == 'reference':
                self.scrape_min_data = v
            else:
                self.scrape_optional_data.append(v)

    def get_id_batch (self, date_from, date_to):

        if self.DEBUG: self.br.set_debug_http(True)

        response = self.br.open(self.search_url)

        fields = {}
        if self.field_dot_suffix:
            fields[self.date_from_field + '.'] = date_from.strftime(self.request_date_format)
            fields[self.date_to_field + '.'] = date_to.strftime(self.request_date_format)
        else:
            fields[self.date_from_field] = date_from.strftime(self.request_date_format)
            fields[self.date_to_field] = date_to.strftime(self.request_date_format)
        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br)
        html = response.read()
        url = response.geturl()
        for k, v in self.html_subs.items():
            html = re.sub(k, v, html, 0, re.U|re.S|re.I) # unicode|dot matches new line|ignore case
        if self.DEBUG: print html
        max_recs = 0
        for scrape in self.scrape_max_recs:
            try:
                result = scrapemark.scrape(scrape, html)
                if self.DEBUG: print result
                max_recs = int(result['max_recs'])
                break
            except:
                pass
        final_result = []
        while len(final_result) < max_recs:
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            else:
                break
            if len(final_result) >= max_recs:
                break
            try:
                for scrape in self.scrape_next_link:
                    result = scrapemark.scrape(scrape, html, url)
                    if result: break
                #print result
                #next_url = self.BACK_REGEX.sub('', result['next_link'])
                next_batch = len(final_result) + 1
                replacement = '&StartIndex=' + str(next_batch) + '&SortOrder'
                next_url = re.sub(r'&StartIndex=\d+&SortOrder', replacement, result['next_link'])
                #print next_url
                response = self.br.open(next_url)
                html = response.read()
                url = response.geturl()
                for k, v in self.html_subs.items():
                    html = re.sub(k, v, html, 0, re.U|re.S|re.I) # unicode|dot matches new line|ignore case
                if self.DEBUG: print html
            except:
                break
        return final_result

    def get_detail_from_uid (self, uid):
        url = urlparse.urljoin(self.search_url, self.detail_page) + '?theApnID=' + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

    # scrape detailed information on one record via its access URL
    def get_detail_from_url (self, url):
        if self.DEBUG: print "Url:", url
        try:
            response = self.br.open(url)
            html = response.read()
            this_url = response.geturl()
            if self.DEBUG:
                print "Html obtained from details url:", html
        except:
            if self.DEBUG: raise
            else: return None
        return self.get_detail(html, this_url)

class BostonScraper(SwiftLGScraper): 

    # note fixed IP address was 194.72.114.25
    search_url = 'http://93.93.220.239/swiftlg/apas/run/wphappcriteria.display'
    ID_ORDER = "CASE uid WHEN substr(uid, 3, 2) < '50' THEN '20' || uid ELSE '19' || uid END desc"
    TABLE_NAME = 'Boston'
    field_dot_suffix = False
    end_flag = "<br>"
    scrape_variants = {
        'address': "__start__ Location __mid__ {{ __field__ }} <p/>",
        'case_officer': "__start__ Case Officer __mid__ {{ __field__ }} <h2/>",
    }

class CannockChaseScraper(SwiftLGScraper):

    search_url = 'http://planning.cannockchasedc.com/swiftlg/apas/run/wphappcriteria.display'
    ID_ORDER = "CASE uid WHEN substr(uid, 4, 2) < '50' THEN '20' || uid ELSE '19' || uid END desc"
    TABLE_NAME = 'CannockChase'
    scrape_variants = {
        'reference': "__start__ Application Ref __mid__ {{ __field__ }} __end__",
        'description': "__start__ Full Description __mid__ {{ __field__ }} __end__",
        'status': "__start__ Status Description __mid__ {{ __field__ }}__end__",
        'case_officer': "__start__ Case Officer __mid__ {{ __field__ }} <h2/>",
        'agent_address': "Agent Details __start__ Address __mid__ <p> {{ __field__ }} </p>",
    }

class DaventryScraper(SwiftLGScraper):

    BATCH_DAYS = 28 # batch size for each scrape - number of days to gather to produce at least one result each time
    MIN_DAYS = 28 # min number of days to get when gathering current ids
    search_url = 'http://78.25.201.88/swiftlg/apas/run/wphappcriteria.display'
    #ID_ORDER = "uid desc"
    TABLE_NAME = 'Daventry'
    field_dot_suffix = False
    end_flag = "<br>"
    scrape_variants = {
        'reference': "__start__ Reference Number __mid__ {{ __field__ }} __end__",
        'address': "__start__ Location __mid__ {{ __field__ }} <p/>",
        'applicant_name': "Applicant Details __start__ Name __mid__ {{ __field__ }} __end__ ",
        'agent_name': "Agent Details __start__ Name __mid__ {{ __field__ }} __end__ ",
        'decision': "__start__ Decision __mid__ {{ __field__ }} __end__ __start__ Decision Date __mid__ Appeal Decision", 
        'decision_date': "__start__ Decision __mid__ __start__ Decision Date __mid__ {{ __field__ }} __end__ Appeal Decision", 
        'appeal_date': "__start__ Appeal Lodged Date __mid__ {{ __field__ }} __end__",
        'appeal_result': "__start__ Appeal Decision __mid__ {{ __field__ }} __end__ __start__ Appeal Decision Date __mid__",
        'appeal_decision_date': "__start__ Appeal Decision __mid__ __start__ Appeal Decision Date __mid__ {{ __field__ }} __end__",
    }

class DudleyScraper(SwiftLGScraper):

    search_url = 'http://www2.dudley.gov.uk/swiftlg/apas/run/Wphappcriteria.display'
    TABLE_NAME = 'Dudley'
    ID_ORDER = "CASE uid WHEN substr(uid, 2, 2) < '50' THEN '20' || uid ELSE '19' || uid END desc"
    search_form = '1'
    scrape_variants = {
        'reference': "__start__ Application Ref __mid__ {{ __field__ }} __end__",
        'case_officer': "__start__ Case Officer __mid__ {{ __field__ }} <h6/>",
        'agent_address': "Agent Details__start__ Address __mid__ <p> {{ __field__ }} </p>",
    }

class EastHertfordshireScraper(SwiftLGScraper):

    search_url = 'http://online.eastherts.gov.uk/swiftlg/apas/run/wphappcriteria.display'
    TABLE_NAME = 'EastHertfordshire'
    ID_ORDER = "CASE uid WHEN substr(uid, 3, 2) < '50' THEN '20' || uid ELSE '19' || uid END desc"
    scrape_ids = """
    <form> <table /> <table> <tr />
    {* <tr>
    <td> <a href="{{ [records].url|abs }}"> {{ [records].uid }} </a> </td>
    </tr> *}
    </table> </form>
    """
    start_flag = '<b>'
    mid_flag = '</b>'
    end_flag = '<b/>'
    scrape_variants = {
        'status': "__start__ Status __mid__ <td> {{ __field__|html }} </td>",
        'consultation_start_date': "<label> Publicity Start Date </label> {{ __field__ }} <br>",
        'consultation_end_date': "<label> Publicity End Date </label> {{ __field__ }} <br>",
        'applicant_name': "Applicant __start__ Company __mid__ <td> {{ __field__ }} </td>",
        'agent_name': "Agent __start__ Company __mid__ <td> {{ __field__ }} </td>",
        'applicant_address': "Applicant __start__ Address __mid__ <td> {{ __field__ }} </td>",
        'agent_address': "Agent __start__ Address __mid__ <td> {{ __field__ }} </td>",
    }

class EnfieldScraper(SwiftLGScraper):

    search_url = 'http://forms.enfield.gov.uk/swiftlg/apas/run/wphappcriteria.display'
    TABLE_NAME = 'Enfield'
    field_dot_suffix = True
    end_flag = "<br>"
    scrape_variants = {
        'case_officer': "__start__ Case Officer __mid__ {{ __field__ }} <h2/>",
    }
    
class GwyneddScraper(SwiftLGScraper):

    search_url = 'http://www.gwynedd.gov.uk/swiftlg/apas/run/wphappcriteria.display?langid=1'
    TABLE_NAME = 'Gwynedd'
    ID_ORDER = "CASE uid WHEN substr(uid, 2, 2) < '50' THEN '20' || uid ELSE '19' || uid END desc"
    search_form = '1'
    end_flag = '<br>'
    scrape_variants = {
        'parish': "__start__ Community __mid__ {{ __field__ }} __end__",
        'applicant_name': "<span> Applicant </span> __start__ Name __mid__ {{ __field__ }} __end__",
        'agent_name': "<span> Agent </span> __start__ Name __mid__ {{ __field__ }} __end__",
        'applicant_address': "<span> Applicant </span> __start__ Address __mid__ {{ __field__ }} __end__",
        'agent_address': "<span> Agent </span> __start__ Address __mid__ {{ __field__ }} __end__",
    }

class IslingtonScraper(SwiftLGScraper):

    search_url = 'https://www.islington.gov.uk/onlineplanning/apas/run/wphappcriteria.display'
    TABLE_NAME = 'Islington'
    field_dot_suffix = True
    html_subs = {
    r'</(t[dhr]) class=".*?">': r'</\1>',
    r"<a href='([^']*?)&(?:amp;)*[bB]ackURL=[^']*?'>": r"<a href='\1'>",
    r'<a href="([^"]*?)&(?:amp;)*[bB]ackURL=[^"]*?">': r'<a href="\1">',
    }
    scrape_variants = {
        'reference': "__start__ Application Number __mid__ {{ __field__ }} __end__",
        'date_validated': "__start__ Date Valid __mid__ {{ __field__ }} __end__",
        'status': "__start__ Status __mid__ <td> {{ __field__|html }} </td>",
        'consultation_start_date': "__start__ Consultation Start __mid__ {{ __field__ }} __end__",
        'consultation_end_date': "__start__ Consultation End __mid__ {{ __field__ }} __end__",
        'applicant_address': "Applicant Details __start__ Address __mid__ {{ __field__ }} <h2/>",
        'agent_address': "Agent Details__start__ Address __mid__ {{ __field__ }} <h2/>",
        'decision_date': "__start__ Decision Date __mid__ {{ __field__ }} __start__ Decision __mid__ Consultation",
        'decision': "__start__ Decision Date __mid__ __start__ Decision __mid__ {{ __field__ }} __end__ Consultation", 
    }

class LakeDistrictScraper(SwiftLGScraper):

    search_url = 'http://www.lakedistrict.gov.uk/swiftlg/apas/run/wphappcriteria.display'
    TABLE_NAME = 'LakeDistrict'
    ID_ORDER = 'uid desc'
    search_form = '1'
    scrape_variants = {
        'district': "__start__ District __mid__ {{ __field__ }} __end__",
        'status': "__start__ Progress __mid__ {{ __field__ }} __end__",
        'decision': "__start__ Decision __mid__ {{ __field__ }} __end__ __start__ Decision Date __mid__ Location",
        'decision_date': "__start__ Decision __mid__ __end__ __start__ Decision Date __mid__ <td> {{ __field__ }} </td> Location", 
        'applicant_name': "<strong> Applicant </strong> <td> {{ __field__ }} </td>",
        'agent_name': "<strong> Agent </strong> <td> {{ __field__ }} </td>",
        'applicant_address': "<strong> Applicant </strong> <td /> <td /> <td> {{ __field__ }} </td>",
        'agent_address': "<strong> Agent </strong> <td> <td /> <td /> {{ __field__ }} </td>",
    }

class MaidstoneScraper(SwiftLGScraper):

    search_url = 'http://www.maidstone.gov.uk/swiftlg/apas/run/wphappcriteria.display'
    TABLE_NAME = 'Maidstone'
    field_dot_suffix = True
    scrape_variants = {
        'reference': "__start__ Application Ref __mid__ {{ __field__ }} __end__",
        'description': "__start__ Full Description __mid__ {{ __field__ }} __end__",
        'status': "__start__ Status Description __mid__ {{ __field__ }} __end__",
        'case_officer': "__start__ Case Officer __mid__ {{ __field__ }} <h2/>",
        'agent_address': "Agent Details __start__ Address __mid__ <p> {{ __field__ }} </p>",
    }

class MoleValleyScraper(SwiftLGScraper):

    search_url = 'http://www.molevalley.gov.uk/swiftlg/apas/run/wphappcriteria.display'
    TABLE_NAME = 'MoleValley'
    ID_ORDER = 'uid desc'
    scrape_variants = {
        'reference': "__start__ Application Ref __mid__ {{ __field__ }} __end__",
        'description': "__start__ Full Description __mid__ {{ __field__ }} __end__",
        'status': "__start__ Status Description __mid__ {{ __field__ }} __end__",
        'case_officer': "__start__ Case Officer __mid__ {{ __field__ }} <h2/>",
        'agent_address': "Agent Details __start__ Address __mid__ <p> {{ __field__ }} </p>",
    }

class NewportScraper(SwiftLGScraper):

    search_url = 'http://planning.newport.gov.uk/swift/apas/run/wphappcriteria.display'
    TABLE_NAME = 'Newport'
    ID_ORDER = "CASE uid WHEN substr(uid, 1, 2) < '50' THEN '20' || uid ELSE '19' || uid END desc"
    scrape_variants = {
        'reference': "__start__ Application Ref __mid__ {{ __field__ }} __end__",
        'address': "__start__ Location __mid__ {{ __field__ }} <a/>",
        'description': "__start__ Application Description __mid__ {{ __field__ }} <span> Show </span>",
        'parish': "__start__ Community Council __mid__ {{ __field__ }} __end__",
        'agent_address': "Agent Details __start__ Address __mid__ <p> {{ __field__ }} </p>",
        'applicant_address': "Applicant Details __start__ Address __mid__ <p> {{ __field__ }} </p>",
        'decision': "__start__ Decision Date __mid__ __start__ Decision __mid__ {{ __field__ }} __end__", 
    }

class NorthDorsetScraper(SwiftLGScraper):

    search_url = 'http://plansearch.north-dorset.gov.uk/swiftlg/apas/run/wphappcriteria.display'
    TABLE_NAME = 'NorthDorset'
    ID_ORDER = 'uid desc'
    scrape_variants = {
        'reference': "__start__ Application Ref __mid__ {{ __field__ }} __end__",
        'description': "__start__ Full Description __mid__ {{ __field__ }} __end__",
        'status': "__start__ Status Description __mid__ <p> {{ __field__ }} </p>",
        'case_officer': "__start__ Case Officer __mid__ {{ __field__ }} <h2/>",
        'agent_address': "Agent Details __start__ Address __mid__ <p> {{ __field__ }} </p>",
    }

class OxfordshireScraper(SwiftLGScraper):

    BATCH_DAYS = 60 # batch size for each scrape - number of days to gather to produce at least one result each time
    MIN_DAYS = 42 # min number of days to get when gathering current ids
    search_url = 'http://myeplanning.oxfordshire.gov.uk/swiftlg/apas/run/Wphappcriteria.display'
    TABLE_NAME = 'Oxfordshire'
    scrape_variants = {
        'reference': "__start__ Application Ref __mid__ {{ __field__ }} __end__",
        'description': "__start__ Description __mid__ {{ __field__ }} __end__",
        'date_validated': "__start__ Valid Date __mid__ {{ __field__ }} __end__",
        'address': "__start__ Location __mid__ {{ __field__ }} (<a/>)",
        'applicant_name': "__start__ Applicant Name __mid__ {{ __field__ }} __end__",
        'agent_name': "__start__ Agent Name __mid__ {{ __field__ }} __end__",
        'decision': "Comment __start__ Decision __mid__ {{ __field__ }} __start__ Decision Date __mid__",
        'decision_date': "Comment __start__ Decision __mid__ __start__ Decision Date __mid__ {{ __field__ }} <h2/>",
    }

class PembrokeshireScraper(SwiftLGScraper):

    BATCH_DAYS = 28 # batch size for each scrape - number of days to gather to produce at least one result each time
    MIN_DAYS = 28 # min number of days to get when gathering current ids
    search_url = 'http://planning.pembrokeshire.gov.uk/swiftlg/apas/run/wphappcriteria.display'
    TABLE_NAME = 'Pembrokeshire'
    ID_ORDER = "CASE uid WHEN substr(uid, 1, 2) < '50' THEN '20' || uid ELSE '19' || uid END desc"
    scrape_variants = {
        'reference': "__start__ Application Ref __mid__ {{ __field__ }} __end__",
        'description': "__start__ Description __mid__ {{ __field__ }} __end__",
        'date_validated': "__start__ Validated Date __mid__ {{ __field__ }} __end__",
        'parish': "__start__ Community __mid__ {{ __field__ }} __end__",
        'address': "__start__ Location __mid__ {{ __field__ }} (<a/>)",
        'decision_date': "__start__ Decision Date __mid__ {{ __field__ }} __start__ Decision __mid__",
        'decision': "__start__ Decision Date __mid__ __start__ Decision __mid__ {{ __field__ }} __end__",
        'case_officer': "__start__ Case Officer __mid__ {{ __field__ }} <h2/>",
        'agent_address': "Agent Details __start__ Address __mid__ <p> {{ __field__ }} </p>",
    }

class RedbridgeScraper(SwiftLGScraper):

    search_url = 'http://planning.redbridge.gov.uk/swiftlg/apas/run/wphappcriteria.display'
    TABLE_NAME = 'Redbridge'
    search_form = '1'
    scrape_variants = {
        'reference': "__start__ Application Ref __mid__ {{ __field__ }} __end__",
        'description': "__start__ Description __mid__ {{ __field__ }} __end__",
        'agent_address': "Agent Details __start__ Address __mid__ <div> {{ __field__ }} </div>",
        'applicant_address': "Applicant Details __start__ Address __mid__ <div> {{ __field__ }} </div>",
        'applicant_name': "Applicant Details __start__ Name __mid__ {{ __field__ }} __end__",
    }

class RochdaleScraper(SwiftLGScraper): # note no applications after 28 May 2012 - it's Idox after that

    search_url = 'http://online.rochdale.gov.uk/swiftlg/apas/run/wphappcriteria.display'
    TABLE_NAME = 'Rochdale'
    field_dot_suffix = True
    end_flag = '<br>'
    scrape_variants = {
        'address': "__start__ Location __mid__ {{ __field__ }} <p/>",
        'description': "__start__ Description __mid__ {{ __field__ }} __end__",
        'case_officer': "__start__ Case Officer __mid__ {{ __field__ }} <h2/>",
    }

class RutlandScraper(SwiftLGScraper): 

    search_url = 'http://planningonline.rutland.gov.uk/swift/apas/run/wphappcriteria.display'
    TABLE_NAME = 'Rutland'
    ID_ORDER = "substr(uid, 5) desc"
    scrape_variants = {
        'reference': "__start__ Application Ref __mid__ {{ __field__ }} __end__",
        'description': "__start__ Full Description __mid__ {{ __field__ }} __end__",
        'case_officer': "__start__ Case Officer __mid__ {{ __field__ }} <h2/>",
        'agent_address': "Agent Details __start__ Address __mid__ <p> {{ __field__ }} </p>",
    }
class SloughScraper(SwiftLGScraper):

    search_url = 'http://www2.slough.gov.uk/swiftlg/apas/run/wphappcriteria.display'
    TABLE_NAME = 'Slough'
    scrape_variants = {
        'reference': "__start__ Application Ref __mid__ {{ __field__ }} __end__",
        'description': "__start__ Description __mid__ {{ __field__ }} __end__",
        'address': "__start__ Location __mid__ {{ __field__ }} (<a/>)",
        'agent_address': "Agent Details __start__ Address __mid__ <p> {{ __field__ }} </p>",
        'case_officer': "__start__ Case Officer __mid__ <p> {{ __field__ }} </p>",
    }

class SnowdoniaScraper(SwiftLGScraper):

    search_url = 'http://217.77.186.246:8080/swiftlg_snpa/apas/run/wphappcriteria.display'
    TABLE_NAME = 'Snowdonia'
    scrape_variants = {
        'reference': "__start__ Application Ref __mid__ {{ __field__ }} __end__",
        'description': "__start__ Description __mid__ {{ __field__ }} __end__",
        'address': "__start__ Location __mid__ {{ __field__ }} (<a/>)",
        'agent_address': "Agent Details __start__ Address __mid__ <p> {{ __field__ }} </p>",
        'case_officer': "__start__ Case Officer __mid__ {{ __field__ }} <h2/>",
    }

class SouthCambridgeshireScraper(SwiftLGScraper):

    search_url = 'http://plan.scambs.gov.uk/swiftlg/apas/run/wphappcriteria.display'
    TABLE_NAME = 'SouthCambridgeshire'
    search_form = '1'
    scrape_variants = {
        'reference': "__start__ Application Ref __mid__ {{ __field__ }} __end__",
        'description': "__start__ Description __mid__ {{ __field__ }} __end__",
        'agent_address': "Agent Details __start__ Address __mid__ <p> {{ __field__ }} </p>",
        'case_officer': "__start__ Case Officer __mid__ {{ __field__ }} <h2/>",
    }
    
class WarringtonScraper(SwiftLGScraper):

    search_url = 'http://planning.warrington.gov.uk/swiftlg/apas/run/wphappcriteria.display'
    TABLE_NAME = 'Warrington'
    ID_ORDER = 'uid desc'
    search_form = '1'
    scrape_variants = {
        'reference': "__start__ Application&#160;Number __mid__ {{ __field__ }} <p/>",
        'address': "__start__ Location __mid__ <p> {{ __field__ }} </p>",
        'applicant_name': "Applicant Details <p> <strong> Company </strong> {{ __field__ }} </p>", 
        'agent_name': "Agent Details <p> <strong> Company </strong> {{ __field__ }} </p>",
        'applicant_address': "Applicant Details <p> <strong> Address </strong> {{ __field__ }} </p>",
        'agent_address': "Agent Details <p> <strong> Address </strong> {{ __field__ }} </p>",
    }

class WarwickshireScraper(SwiftLGScraper):

    BATCH_DAYS = 60 # batch size for each scrape - number of days to gather to produce at least one result each time
    MIN_DAYS = 60 # min number of days to get when gathering current ids
    search_url = 'https://planning.warwickshire.gov.uk/swiftlg/apas/run/wphappcriteria.display'
    TABLE_NAME = 'Warwickshire'
    scrape_variants = {
        'reference': "__start__ Reference Number __mid__ {{ __field__ }} __end__",
        'description': "__start__ Description __mid__ {{ __field__ }} __end__",
        'status': "__start__ Current Position __mid__ {{ __field__ }} __end__",
        'agent_address': "Agent Details __start__ Address __mid__ <p> {{ __field__ }} </p>",
        'applicant_address': "Applicant Details __start__ Address __mid__ <p> {{ __field__ }} </p>",
        'case_officer': "__start__ Case Officer __mid__ <p> {{ __field__ }} </p>",
        'decision': "__start__ Decision __mid__ {{ __field__ }} __start__ Decision Date __mid__",
        'decision_date': "__start__ Decision __mid__ __start__ Decision Date __mid__ {{ __field__ }} __end__",
        'consultation_end_date': "__start__ Consultation Ends __mid__ {{ __field__ }} __end__",
    }

if __name__ == 'scraper':

    #scraperwiki.sqlite.execute("update Slough set date_scraped = null, address = null, status = null where uid = 'P/00162/056'")
    #scraperwiki.sqlite.commit()
    #scraper = MoleValleyScraper('MoleValley')
    #scraper = EnfieldScraper('Enfield')
    #scraper.reset('2004-07-14', '2012-11-01')
    #scraper.reset('2006-08-07', '2012-11-01')
    #scraper.DEBUG = True
    #scraper.gather_current_ids()
    #scraper.MAX_UPDATE_BATCH = 1000
    #scraper.ID_ORDER = 'rowid desc'
    #scraper.populate_missing_applications()
    #scraper.reset('2004-07-14', '2012-11-01')

    #util.rename_column('Daventry', 'appeal_decision', 'appeal_result')
    #sys.exit()

    #util.replace_vals('Boston', 'url', 'http://194.72.114.25/', 'http://93.93.220.239/', 'prefix', 'yes')
    #scraper = BostonScraper()
    #scraper.run()
    #scraper = DaventryScraper()
    #scraper.run()
    #scraper = DudleyScraper()
    #scraper.run()
    #sys.exit()

    sys_list = []
    for k, v in systems.items(): # get latest date scraped for each system
        sys_list.append( (k, v, scraperwiki.sqlite.get_var('latest-' + k)) )
    sort_sys = sorted(sys_list, key=lambda system: system[2]) # sort so least recent are first
    for auth in sort_sys[:6]: # do max 6 per run
        strexec = auth[1] + "('" + auth[0] + "')"
        print "Scraping from:", strexec
        try:
            scraper = eval(strexec)
            scraper.run()
        except Exception as err:
            print "Error - skipping this authority -", str(err)
    print "Finished"

    # misc test calls
    #scraper = BostonScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('B/11/0128') # Boston
    #print scraper.get_detail_from_uid ('B/13/0192')
    #scraper = CannockChaseScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('CH/11/0274') # CannockChase
    #scraper = DaventryScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('DA/2010/0002') # Daventry
    #scraper = DudleyScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('P13/0122 ') # Dudley
    #scraper = EastHertfordshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('3/11/1322/FP') # EastHertfordshire
    #scraper = EnfieldScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('LDC/11/0122') # Enfield
    #scraper = GwyneddScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('C11/0643/11/CT') # Gwynedd
    #scraper = IslingtonScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('P081406(MA01)') # Islington
    #scraper = LakeDistrictScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('7/2011/5414') # LakeDistrict
    #scraper = MaidstoneScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/1325') # Maidstone
    #scraper = MoleValleyScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('MO/2012/0800') # MoleValley
    #scraper = NewportScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('12/0356') # Newport
    #print scraper.get_detail_from_uid ('09/0245')
    #print scraper.get_detail_from_uid ('06/1048')
    #scraper = NorthDorsetScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('2/2011/0927/PLNG') # NorthDorset
    #scraper = OxfordshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('MW.0123/11') # Oxfordshire (low numbers)
    #scraper = PembrokeshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/0454/PA') # Pembrokeshire
    #scraper = RedbridgeScraper()
    #scraper.DEBUG = True   
    #print scraper.get_detail_from_uid ('WTPO/0082/12')
    #print scraper.get_detail_from_uid ('1631/11') # Redbridge
    #scraper = RochdaleScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/D54733') # Rochdale
    #scraper = RutlandScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('APP/2012/0923') # Rutland
    #scraper = SloughScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('P/00162/056') # Slough
    #scraper = SnowdoniaScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('NP5/66/230') # Snowdonia
    #scraper = SouthCambridgeshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('S/01021/12NM') # SouthCambridgeshire
    #scraper = WarringtonScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('2011/18599') # Warrington
    #scraper = WarwickshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('WDC/11CC015 ') # Warwickshire (low numbers)

    #res = scraper.get_id_batch(util.get_dt('01/01/2010'), util.get_dt('15/01/2010'))
    #print res, len(res)


    

