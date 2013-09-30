# this is a base scraper for PublicAccess system planning applications for use by Openly Local

# there are approx 20 authorities using this system

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
import gc

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

systems = {
    #'Bexley': 'BexleyScraper', # now Idox too - too slow so not using this any more
    'ChesterLeStreet': 'ChesterLeStreetScraper', # now part of Durham
    'DurhamCity': 'DurhamCityScraper', # now part of Durham
    'Fenland': 'FenlandScraper',
    'Hammersmith': 'HammersmithScraper', # now Idox too
    'Knowsley': 'KnowsleyScraper',
    'Luton': 'LutonScraper',
    'Melton': 'MeltonScraper',
    #'Oadby': 'OadbyScraper', now Idox
    'OlympicDelivery': 'OlympicDeliveryScraper', # still going?
    'Sandwell': 'SandwellScraper',
    #'Southampton': 'SouthamptonScraper', # not working? now Idox as well?
    'SouthBuckinghamshire': 'SouthBuckinghamshireScraper', 
    'Southend': 'SouthendScraper',
    'StaffordshireMoorlands': 'StaffordshireMoorlandsScraper',
    #'Swindon': 'SwindonScraper', now Idox
    #'Watford': 'WatfordScraper', now Idox
    #'Waveney': 'WaveneyScraper', now Idox
    #'WestLancashire': 'WestLancashireScraper', # now Idox plural dates
    'Worcestershire': 'WorcestershireScraper',
     }

class PublicAccessScraper(base.DateScraper):

    MAX_ID_BATCH = 300 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go

    date_from_field = 'srchDateReceivedStart'
    date_to_field = 'srchDateReceivedEnd'
    search_form = 'searchform'
    request_date_format = '%d/%m/%Y'
    query_fields = { }
    ref_field = 'caseNo'
    scrape_ids = """
    <table class="cResultsForm"> <tr />
    {* <tr>
    <td> {{ [records].uid }} </td> <td> <a href="{{ [records].url|abs }}"> </a> </td>
    </tr> *}
    </table>
    """
    next_link = 'Next Page'
    scrape_max_recs = '<td class="cFormContent"> {{ max_recs }} matching </td>'

    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = '<body> {{ block|html }} </body>'
    # the minimum acceptable valid dataset on the details page
    scrape_min_data = """
    <input id="applicationno" value="{{ reference }}">
    <textarea id="address"> {{ address }} </textarea>
    <textarea id="desc"> {{ description }} </textarea>
    """
    # other optional parameters common to all scrapers can appear on the details page
    scrape_optional_data = [
    '<input id="PPReference" value="{{ planning_portal_id }}">',
    '<input id="type" value="{{ application_type }}">',
    '<input id="applicationstatus" value="{{ status }}">',
    '<input id="decision" value="{{ decision }}">',
    '<input id="decisiontype" value="{{ decided_by }}">',
    '<input id="officer" value="{{ case_officer }}">',
    '<input id="parish" value="{{ parish }}">',
    '<input id="wardname" value="{{ ward_name }}">',
    '<input id="wardnamesubmit" value="{{ ward_name }}">',
    '<input id="daterecv" value="{{ date_received }}">',
    '<input id="datevalid" value="{{ date_validated }}">',
    '<input id="targetdate" value="{{ target_decision_date }}">',
    '<input id="dateactualcommittee" value="{{ meeting_date }}">',
    '<input id="firstdcdate" value="{{ meeting_date }}">',
    '<input id="lgd" value="{{ district }}">',
    '<input id="dateneighbourconsult" value="{{ neighbour_consultation_start_date }}">',
    '<input id="dateneighbourexpiry" value="{{ neighbour_consultation_end_date }}">',
    '<input id="stconsultation" value="{{ consultation_start_date }}">',
    '<input id="consultationex" value="{{ consultation_end_date }}">',
    '<input id="dateadvert" value="{{ last_advertised_date }}">',
    '<input id="dateadvertexpiry" value="{{ latest_advertisement_expiry_date }}">',
    '<input id="datedecisionmade" value="{{ decision_date }}">',
    '<input id="datedecisionissued" value="{{ decision_issued_date }}">',
    '<input id="datepermissionexpiry" value="{{ permission_expires_date }}">',
    '<input id="datedecisionprinted" value="{{ decision_published_date }}">',
    '<input id="applicantname" value="{{ applicant_name }}">',
    '<textarea id="applicantaddress"> {{ applicant_address }} </textarea>',
    '<input id="agentname" value="{{ agent_name }}">',
    '<textarea id="agentaddress"> {{ agent_address }} </textarea>',
    '<input id="agentcondetail" value="{{ agent_tel }}">',
    '<input id="agentphonenumber" value="{{ agent_tel }}">',
    '<input id="dateexpiry" value="{{ application_expires_date }}">',
    '<input id="datesitenotice" value="{{ site_notice_start_date }}">',
    '<input id="datesitenoticeexpiry" value="{{ site_notice_end_date }}">',
    ]

    def get_id_batch (self, date_from, date_to):

        if self.DEBUG: self.br.set_debug_http(True)

        response = self.br.open(self.search_url)

        fields = {}
        fields.update(self.query_fields)
        fields[self.date_from_field] = date_from.strftime(self.request_date_format)
        fields[self.date_to_field] = date_to.strftime(self.request_date_format)
        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br)
        html = response.read()
        try:
            result = scrapemark.scrape(self.scrape_max_recs, html)
            max_recs = int(result['max_recs'])
            if self.DEBUG: print "max_recs:", max_recs
        except:
            max_recs = 0
        final_result = []
        while response and len(final_result) < max_recs:
            url = response.geturl()
            if self.DEBUG: print html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            else:
                break
            try:
                response = self.br.follow_link(text=self.next_link)
                html = response.read()
            except:
                response = None
        return final_result

    def get_detail_from_uid (self, uid):
        response = self.br.open(self.search_url)

        fields = {}
        fields.update(self.query_fields)
        fields[self.ref_field] = uid
        util.setup_form(self.br, self.search_form, fields)
        response = util.submit_form(self.br)
        try:
            html = response.read()
            if self.DEBUG: print html
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            url = result['records'][0]['url']
            if self.DEBUG: print url
        except:
            return None
        return self.get_detail_from_url(url)

class BexleyScraper(PublicAccessScraper):

    search_url = 'http://publicaccess.bexley.gov.uk/publicaccess/tdc/DcApplication/application_searchform.aspx'

class DurhamCityScraper(PublicAccessScraper):

    search_url = 'http://publicaccess.durhamcity.gov.uk/publicaccess/tdc/DcApplication/application_searchform.aspx'

class ChesterLeStreetScraper(PublicAccessScraper):

    BATCH_DAYS = 28 # batch size for each scrape - number of days to gather to produce at least one result each time
    MIN_DAYS = 28 # min number of days to get when gathering current ids
    search_url = 'http://planning.chester-le-street.gov.uk/publicaccess/tdc/DcApplication/application_searchform.aspx'

class FenlandScraper(PublicAccessScraper):

    search_url = 'http://www.fenland.gov.uk/publicaccess/tdc/DcApplication/application_searchform.aspx'

class HammersmithScraper(PublicAccessScraper):

    search_url = 'http://www.apps.lbhf.gov.uk/PublicAccess/tdc/DcApplication/application_searchform.aspx'

class KnowsleyScraper(PublicAccessScraper):

    search_url = 'http://publicaccess.knowsley.gov.uk/PublicAccess/tdc/DcApplication/application_searchform.aspx'

class LutonScraper(PublicAccessScraper):

    search_url = 'http://www.eplan.luton.gov.uk/PublicAccess/tdc/DcApplication/application_searchform.aspx'

class MeltonScraper(PublicAccessScraper):

    search_url = 'http://publicaccess.melton.gov.uk/PALiveSystem77/tdc/DcApplication/application_searchform.aspx'

class OadbyScraper(PublicAccessScraper):

    BATCH_DAYS = 36 # batch size for each scrape - number of days to gather to produce at least one result each time
    MIN_DAYS = 36 # min number of days to get when gathering current ids
    search_url = 'http://pa.owbc.net/PublicAccess/tdc/DcApplication/application_searchform.aspx'

class OlympicDeliveryScraper(PublicAccessScraper):

    START_SEQUENCE = '2006-09-01'
    BATCH_DAYS = 28 # batch size for each scrape - number of days to gather to produce at least one result each time
    MIN_DAYS = 28 # min number of days to get when gathering current ids
    search_url = 'http://planning.london2012.com/publicaccess/tdc/DcApplication/application_searchform.aspx'

class SandwellScraper(PublicAccessScraper):

    search_url = 'http://webcaps.sandwell.gov.uk/PublicAccess/tdc/DcApplication/application_searchform.aspx'

class SouthamptonScraper(PublicAccessScraper):

    search_url = 'http://publicaccess.southampton.gov.uk/PublicAccess/tdc/DcApplication/application_searchform.aspx'
    
class SouthBuckinghamshireScraper(PublicAccessScraper):

    search_url = 'http://sbdc-paweb.southbucks.gov.uk/publicaccess/tdc/DcApplication/application_searchform.aspx'

class SouthendScraper(PublicAccessScraper):

    search_url = 'http://planning.southend.gov.uk/PublicAccess/tdc/DcApplication/application_searchform.aspx'

class StaffordshireMoorlandsScraper(PublicAccessScraper):

    search_url = 'http://publicaccess.staffsmoorlands.gov.uk/publicaccess/tdc/DcApplication/application_searchform.aspx'

class SwindonScraper(PublicAccessScraper):

    search_url = 'http://195.89.201.121/PublicAccess77/tdc/DcApplication/application_searchform.aspx'

class WatfordScraper(PublicAccessScraper):

    search_url = 'http://ww3.watford.gov.uk/publicaccess/tdc/DcApplication/application_searchform.aspx'

class WaveneyScraper(PublicAccessScraper):

    search_url = 'http://publicaccess.waveney.gov.uk/PASystem77/tdc/DcApplication/application_searchform.aspx'

class WestLancashireScraper(PublicAccessScraper):

    search_url = 'http://publicaccess.westlancsdc.gov.uk/PublicAccess/tdc/DcApplication/application_searchform.aspx'
    
class WorcestershireScraper(PublicAccessScraper):

    BATCH_DAYS = 42 # batch size for each scrape - number of days to gather to produce at least one result each time
    MIN_DAYS = 28 # min number of days to get when gathering current ids
    search_url = 'http://www.worcestershire.gov.uk/PublicAccess/tdc/DcApplication/application_searchform.aspx'
    scrape_ids = """
    <table class="whubTable"> <tr />
    {* <tr>
    <td> {{ [records].uid }} </td> <td> <a href="{{ [records].url|abs }}"> </a> </td>
    </tr> *}
    </table>
    """
    scrape_max_recs = '<p>A total of {{ max_recs }} matching applications were found.</p>'
    scrape_min_data = """
    <input id="idApplicationReferenceValue" value="{{ reference }}">
    <textarea id="idLocationValue"> {{ address }} </textarea>
    <textarea id="idProposalValue"> {{ description }} </textarea>
    """
    scrape_optional_data = [
    '<input id="idPlanningPortalReferenceValue" value="{{ planning_portal_id }}">',
    '<input id="idTypeValue" value="{{ application_type }}">',
    '<input id="idStatusValue" value="{{ status }}">',
    '<input id="idDecisionTakenValue" value="{{ decision }}">',
    '<input id="idDecisionLevelValue" value="{{ decided_by }}">',
    '<input id="idCaseOfficerValue" value="{{ case_officer }}">',
    '<input id="idParishValue" value="{{ parish }}">',
    '<input id="idElectoralDivisionCurrentValue" value="{{ ward_name }}">',
    '<input id="idElectoralDivisionCurrentDistrictValue" value="{{ district }}">',
    
    '<input id="idDateReceivedValue" value="{{ date_received }}">',
    '<input id="idDateValidatedValue" value="{{ date_validated }}">',
    '<input id="idDateTargetDeterminationValue" value="{{ target_decision_date }}">',
    '<input id="idDateCommitteeValue" value="{{ meeting_date }}">',
    '<input id="idDateNeighbourConsultationsSentValue" value="{{ neighbour_consultation_start_date }}">',
    '<input id="idDateNeighbourConsultationsExpiryValue" value="{{ neighbour_consultation_end_date }}">',
    '<input id="idDateStandardConsultationsSentValue" value="{{ consultation_start_date }}">',
    '<input id="idDateStandardConsultationsExpiryValue" value="{{ consultation_end_date }}">',
    '<input id="idDateLatestAdvertisementPostedValue" value="{{ last_advertised_date }}">',
    '<input id="idDateLatestAdvertisementExpiryValue" value="{{ latest_advertisement_expiry_date }}">',
    '<input id="idDateOverallExpiryValue" value="{{ application_expires_date }}">',
    '<input id="idDateLatestPublicNoticePostedValue" value="{{ site_notice_start_date }}">',
    '<input id="idDateLatestPublicNoticeExpiryValue" value="{{ site_notice_end_date }}">',

    '<input id="idDateDecisionTakenValue" value="{{ decision_date }}">',
    '<input id="idDateDecisionIssuedValue" value="{{ decision_issued_date }}">',
    '<input id="idDatePermissionExpiryValue" value="{{ permission_expires_date }}">',
    '<input id="idDateDecisionPrintedValue" value="{{ decision_published_date }}">',

    '<input id="idApplicantNameValue" value="{{ applicant_name }}">',
    '<textarea id="idApplicantAddressValue"> {{ applicant_address }} </textarea>',
    '<input id="idAgentNameValue" value="{{ agent_name }}">',
    '<textarea id="idAgentAddressValue"> {{ agent_address }} </textarea>',
    '<input id="idAgentPhoneValue" value="{{ agent_tel }}">',
    ]

if __name__ == 'scraper':

    #scraper = OlympicDeliveryScraper('OlympicDelivery')
    #scraper.run()
    #sys.exit()

    #sql = 'UPDATE Oadby SET application_expires_date = application_expiry_date WHERE application_expires_date is null'
    #scraperwiki.sqlite.execute(sql)
    #scraperwiki.sqlite.commit()
    #util.rename_column('Oadby', 'application_expiry_date', None)
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
            scraper = None
            gc.collect()
        except Exception as err:
            print "Error - skipping this authority -", str(err)
    print "Finished"

    # misc test calls
    #scraper = BexleyScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/01303/FUL') # Bexley OK
    #scraper = DurhamCityScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/00676/FPA') # DurhamCity
    #scraper = ChesterLeStreetScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('2/11/00214/FUL') # ChesterLeStreet
    #scraper = FenlandScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('F/YR11/2012/CCC') # Fenland OK
    #scraper = HammersmithScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('2011/02637/FUL') # Hammersmith and Fulham
    #scraper = KnowsleyScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/00422/DEMCON') # Knowsley OK
    #scraper = LutonScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/00941/FUL') # Luton OK
    #scraper = MeltonScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/00630/FUL') # Melton OK
    #scraper = OadbyScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/00310/FUL') # Oadby
    #scraper = OlympicDeliveryScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/90510/AODODA') # OlympicDelivery
    #scraper = SandwellScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('DC/11/53727') # Sandwell
    #scraper = SouthamptonScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('12/01883/FUL') # Southampton NOT WORKING
    #scraper = SouthBuckinghamshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/01303/FUL') # SouthBuckinghamshire OK
    #scraper = SouthendScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/01119/FUL') # Southend OK
    #scraper = StaffordshireMoorlandsScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/00749/FUL') # StaffordshireMoorlands OK
    #scraper = SwindonScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('S/11/1140') # Swindon OK
    #scraper = WatfordScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/00815/CM') # Watford OK
    #scraper = WaveneyScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('DC/11/0926/FUL') # Waveney OK
    #scraper = WestLancashireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('2011/0898/FUL') # WestLancashire OK
    #scraper = WorcestershireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/000051/REG3') # Worcestershire OK

    #res = scraper.get_id_batch(util.get_dt('10/08/2011'), util.get_dt('10/08/2011'))
    #print res, len(res)


    

# this is a base scraper for PublicAccess system planning applications for use by Openly Local

# there are approx 20 authorities using this system

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
import gc

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

systems = {
    #'Bexley': 'BexleyScraper', # now Idox too - too slow so not using this any more
    'ChesterLeStreet': 'ChesterLeStreetScraper', # now part of Durham
    'DurhamCity': 'DurhamCityScraper', # now part of Durham
    'Fenland': 'FenlandScraper',
    'Hammersmith': 'HammersmithScraper', # now Idox too
    'Knowsley': 'KnowsleyScraper',
    'Luton': 'LutonScraper',
    'Melton': 'MeltonScraper',
    #'Oadby': 'OadbyScraper', now Idox
    'OlympicDelivery': 'OlympicDeliveryScraper', # still going?
    'Sandwell': 'SandwellScraper',
    #'Southampton': 'SouthamptonScraper', # not working? now Idox as well?
    'SouthBuckinghamshire': 'SouthBuckinghamshireScraper', 
    'Southend': 'SouthendScraper',
    'StaffordshireMoorlands': 'StaffordshireMoorlandsScraper',
    #'Swindon': 'SwindonScraper', now Idox
    #'Watford': 'WatfordScraper', now Idox
    #'Waveney': 'WaveneyScraper', now Idox
    #'WestLancashire': 'WestLancashireScraper', # now Idox plural dates
    'Worcestershire': 'WorcestershireScraper',
     }

class PublicAccessScraper(base.DateScraper):

    MAX_ID_BATCH = 300 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 200 # max application details to scrape in one go

    date_from_field = 'srchDateReceivedStart'
    date_to_field = 'srchDateReceivedEnd'
    search_form = 'searchform'
    request_date_format = '%d/%m/%Y'
    query_fields = { }
    ref_field = 'caseNo'
    scrape_ids = """
    <table class="cResultsForm"> <tr />
    {* <tr>
    <td> {{ [records].uid }} </td> <td> <a href="{{ [records].url|abs }}"> </a> </td>
    </tr> *}
    </table>
    """
    next_link = 'Next Page'
    scrape_max_recs = '<td class="cFormContent"> {{ max_recs }} matching </td>'

    # captures HTML block encompassing all fields to be gathered
    scrape_data_block = '<body> {{ block|html }} </body>'
    # the minimum acceptable valid dataset on the details page
    scrape_min_data = """
    <input id="applicationno" value="{{ reference }}">
    <textarea id="address"> {{ address }} </textarea>
    <textarea id="desc"> {{ description }} </textarea>
    """
    # other optional parameters common to all scrapers can appear on the details page
    scrape_optional_data = [
    '<input id="PPReference" value="{{ planning_portal_id }}">',
    '<input id="type" value="{{ application_type }}">',
    '<input id="applicationstatus" value="{{ status }}">',
    '<input id="decision" value="{{ decision }}">',
    '<input id="decisiontype" value="{{ decided_by }}">',
    '<input id="officer" value="{{ case_officer }}">',
    '<input id="parish" value="{{ parish }}">',
    '<input id="wardname" value="{{ ward_name }}">',
    '<input id="wardnamesubmit" value="{{ ward_name }}">',
    '<input id="daterecv" value="{{ date_received }}">',
    '<input id="datevalid" value="{{ date_validated }}">',
    '<input id="targetdate" value="{{ target_decision_date }}">',
    '<input id="dateactualcommittee" value="{{ meeting_date }}">',
    '<input id="firstdcdate" value="{{ meeting_date }}">',
    '<input id="lgd" value="{{ district }}">',
    '<input id="dateneighbourconsult" value="{{ neighbour_consultation_start_date }}">',
    '<input id="dateneighbourexpiry" value="{{ neighbour_consultation_end_date }}">',
    '<input id="stconsultation" value="{{ consultation_start_date }}">',
    '<input id="consultationex" value="{{ consultation_end_date }}">',
    '<input id="dateadvert" value="{{ last_advertised_date }}">',
    '<input id="dateadvertexpiry" value="{{ latest_advertisement_expiry_date }}">',
    '<input id="datedecisionmade" value="{{ decision_date }}">',
    '<input id="datedecisionissued" value="{{ decision_issued_date }}">',
    '<input id="datepermissionexpiry" value="{{ permission_expires_date }}">',
    '<input id="datedecisionprinted" value="{{ decision_published_date }}">',
    '<input id="applicantname" value="{{ applicant_name }}">',
    '<textarea id="applicantaddress"> {{ applicant_address }} </textarea>',
    '<input id="agentname" value="{{ agent_name }}">',
    '<textarea id="agentaddress"> {{ agent_address }} </textarea>',
    '<input id="agentcondetail" value="{{ agent_tel }}">',
    '<input id="agentphonenumber" value="{{ agent_tel }}">',
    '<input id="dateexpiry" value="{{ application_expires_date }}">',
    '<input id="datesitenotice" value="{{ site_notice_start_date }}">',
    '<input id="datesitenoticeexpiry" value="{{ site_notice_end_date }}">',
    ]

    def get_id_batch (self, date_from, date_to):

        if self.DEBUG: self.br.set_debug_http(True)

        response = self.br.open(self.search_url)

        fields = {}
        fields.update(self.query_fields)
        fields[self.date_from_field] = date_from.strftime(self.request_date_format)
        fields[self.date_to_field] = date_to.strftime(self.request_date_format)
        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br)
        html = response.read()
        try:
            result = scrapemark.scrape(self.scrape_max_recs, html)
            max_recs = int(result['max_recs'])
            if self.DEBUG: print "max_recs:", max_recs
        except:
            max_recs = 0
        final_result = []
        while response and len(final_result) < max_recs:
            url = response.geturl()
            if self.DEBUG: print html
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            else:
                break
            try:
                response = self.br.follow_link(text=self.next_link)
                html = response.read()
            except:
                response = None
        return final_result

    def get_detail_from_uid (self, uid):
        response = self.br.open(self.search_url)

        fields = {}
        fields.update(self.query_fields)
        fields[self.ref_field] = uid
        util.setup_form(self.br, self.search_form, fields)
        response = util.submit_form(self.br)
        try:
            html = response.read()
            if self.DEBUG: print html
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            url = result['records'][0]['url']
            if self.DEBUG: print url
        except:
            return None
        return self.get_detail_from_url(url)

class BexleyScraper(PublicAccessScraper):

    search_url = 'http://publicaccess.bexley.gov.uk/publicaccess/tdc/DcApplication/application_searchform.aspx'

class DurhamCityScraper(PublicAccessScraper):

    search_url = 'http://publicaccess.durhamcity.gov.uk/publicaccess/tdc/DcApplication/application_searchform.aspx'

class ChesterLeStreetScraper(PublicAccessScraper):

    BATCH_DAYS = 28 # batch size for each scrape - number of days to gather to produce at least one result each time
    MIN_DAYS = 28 # min number of days to get when gathering current ids
    search_url = 'http://planning.chester-le-street.gov.uk/publicaccess/tdc/DcApplication/application_searchform.aspx'

class FenlandScraper(PublicAccessScraper):

    search_url = 'http://www.fenland.gov.uk/publicaccess/tdc/DcApplication/application_searchform.aspx'

class HammersmithScraper(PublicAccessScraper):

    search_url = 'http://www.apps.lbhf.gov.uk/PublicAccess/tdc/DcApplication/application_searchform.aspx'

class KnowsleyScraper(PublicAccessScraper):

    search_url = 'http://publicaccess.knowsley.gov.uk/PublicAccess/tdc/DcApplication/application_searchform.aspx'

class LutonScraper(PublicAccessScraper):

    search_url = 'http://www.eplan.luton.gov.uk/PublicAccess/tdc/DcApplication/application_searchform.aspx'

class MeltonScraper(PublicAccessScraper):

    search_url = 'http://publicaccess.melton.gov.uk/PALiveSystem77/tdc/DcApplication/application_searchform.aspx'

class OadbyScraper(PublicAccessScraper):

    BATCH_DAYS = 36 # batch size for each scrape - number of days to gather to produce at least one result each time
    MIN_DAYS = 36 # min number of days to get when gathering current ids
    search_url = 'http://pa.owbc.net/PublicAccess/tdc/DcApplication/application_searchform.aspx'

class OlympicDeliveryScraper(PublicAccessScraper):

    START_SEQUENCE = '2006-09-01'
    BATCH_DAYS = 28 # batch size for each scrape - number of days to gather to produce at least one result each time
    MIN_DAYS = 28 # min number of days to get when gathering current ids
    search_url = 'http://planning.london2012.com/publicaccess/tdc/DcApplication/application_searchform.aspx'

class SandwellScraper(PublicAccessScraper):

    search_url = 'http://webcaps.sandwell.gov.uk/PublicAccess/tdc/DcApplication/application_searchform.aspx'

class SouthamptonScraper(PublicAccessScraper):

    search_url = 'http://publicaccess.southampton.gov.uk/PublicAccess/tdc/DcApplication/application_searchform.aspx'
    
class SouthBuckinghamshireScraper(PublicAccessScraper):

    search_url = 'http://sbdc-paweb.southbucks.gov.uk/publicaccess/tdc/DcApplication/application_searchform.aspx'

class SouthendScraper(PublicAccessScraper):

    search_url = 'http://planning.southend.gov.uk/PublicAccess/tdc/DcApplication/application_searchform.aspx'

class StaffordshireMoorlandsScraper(PublicAccessScraper):

    search_url = 'http://publicaccess.staffsmoorlands.gov.uk/publicaccess/tdc/DcApplication/application_searchform.aspx'

class SwindonScraper(PublicAccessScraper):

    search_url = 'http://195.89.201.121/PublicAccess77/tdc/DcApplication/application_searchform.aspx'

class WatfordScraper(PublicAccessScraper):

    search_url = 'http://ww3.watford.gov.uk/publicaccess/tdc/DcApplication/application_searchform.aspx'

class WaveneyScraper(PublicAccessScraper):

    search_url = 'http://publicaccess.waveney.gov.uk/PASystem77/tdc/DcApplication/application_searchform.aspx'

class WestLancashireScraper(PublicAccessScraper):

    search_url = 'http://publicaccess.westlancsdc.gov.uk/PublicAccess/tdc/DcApplication/application_searchform.aspx'
    
class WorcestershireScraper(PublicAccessScraper):

    BATCH_DAYS = 42 # batch size for each scrape - number of days to gather to produce at least one result each time
    MIN_DAYS = 28 # min number of days to get when gathering current ids
    search_url = 'http://www.worcestershire.gov.uk/PublicAccess/tdc/DcApplication/application_searchform.aspx'
    scrape_ids = """
    <table class="whubTable"> <tr />
    {* <tr>
    <td> {{ [records].uid }} </td> <td> <a href="{{ [records].url|abs }}"> </a> </td>
    </tr> *}
    </table>
    """
    scrape_max_recs = '<p>A total of {{ max_recs }} matching applications were found.</p>'
    scrape_min_data = """
    <input id="idApplicationReferenceValue" value="{{ reference }}">
    <textarea id="idLocationValue"> {{ address }} </textarea>
    <textarea id="idProposalValue"> {{ description }} </textarea>
    """
    scrape_optional_data = [
    '<input id="idPlanningPortalReferenceValue" value="{{ planning_portal_id }}">',
    '<input id="idTypeValue" value="{{ application_type }}">',
    '<input id="idStatusValue" value="{{ status }}">',
    '<input id="idDecisionTakenValue" value="{{ decision }}">',
    '<input id="idDecisionLevelValue" value="{{ decided_by }}">',
    '<input id="idCaseOfficerValue" value="{{ case_officer }}">',
    '<input id="idParishValue" value="{{ parish }}">',
    '<input id="idElectoralDivisionCurrentValue" value="{{ ward_name }}">',
    '<input id="idElectoralDivisionCurrentDistrictValue" value="{{ district }}">',
    
    '<input id="idDateReceivedValue" value="{{ date_received }}">',
    '<input id="idDateValidatedValue" value="{{ date_validated }}">',
    '<input id="idDateTargetDeterminationValue" value="{{ target_decision_date }}">',
    '<input id="idDateCommitteeValue" value="{{ meeting_date }}">',
    '<input id="idDateNeighbourConsultationsSentValue" value="{{ neighbour_consultation_start_date }}">',
    '<input id="idDateNeighbourConsultationsExpiryValue" value="{{ neighbour_consultation_end_date }}">',
    '<input id="idDateStandardConsultationsSentValue" value="{{ consultation_start_date }}">',
    '<input id="idDateStandardConsultationsExpiryValue" value="{{ consultation_end_date }}">',
    '<input id="idDateLatestAdvertisementPostedValue" value="{{ last_advertised_date }}">',
    '<input id="idDateLatestAdvertisementExpiryValue" value="{{ latest_advertisement_expiry_date }}">',
    '<input id="idDateOverallExpiryValue" value="{{ application_expires_date }}">',
    '<input id="idDateLatestPublicNoticePostedValue" value="{{ site_notice_start_date }}">',
    '<input id="idDateLatestPublicNoticeExpiryValue" value="{{ site_notice_end_date }}">',

    '<input id="idDateDecisionTakenValue" value="{{ decision_date }}">',
    '<input id="idDateDecisionIssuedValue" value="{{ decision_issued_date }}">',
    '<input id="idDatePermissionExpiryValue" value="{{ permission_expires_date }}">',
    '<input id="idDateDecisionPrintedValue" value="{{ decision_published_date }}">',

    '<input id="idApplicantNameValue" value="{{ applicant_name }}">',
    '<textarea id="idApplicantAddressValue"> {{ applicant_address }} </textarea>',
    '<input id="idAgentNameValue" value="{{ agent_name }}">',
    '<textarea id="idAgentAddressValue"> {{ agent_address }} </textarea>',
    '<input id="idAgentPhoneValue" value="{{ agent_tel }}">',
    ]

if __name__ == 'scraper':

    #scraper = OlympicDeliveryScraper('OlympicDelivery')
    #scraper.run()
    #sys.exit()

    #sql = 'UPDATE Oadby SET application_expires_date = application_expiry_date WHERE application_expires_date is null'
    #scraperwiki.sqlite.execute(sql)
    #scraperwiki.sqlite.commit()
    #util.rename_column('Oadby', 'application_expiry_date', None)
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
            scraper = None
            gc.collect()
        except Exception as err:
            print "Error - skipping this authority -", str(err)
    print "Finished"

    # misc test calls
    #scraper = BexleyScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/01303/FUL') # Bexley OK
    #scraper = DurhamCityScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/00676/FPA') # DurhamCity
    #scraper = ChesterLeStreetScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('2/11/00214/FUL') # ChesterLeStreet
    #scraper = FenlandScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('F/YR11/2012/CCC') # Fenland OK
    #scraper = HammersmithScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('2011/02637/FUL') # Hammersmith and Fulham
    #scraper = KnowsleyScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/00422/DEMCON') # Knowsley OK
    #scraper = LutonScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/00941/FUL') # Luton OK
    #scraper = MeltonScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/00630/FUL') # Melton OK
    #scraper = OadbyScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/00310/FUL') # Oadby
    #scraper = OlympicDeliveryScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/90510/AODODA') # OlympicDelivery
    #scraper = SandwellScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('DC/11/53727') # Sandwell
    #scraper = SouthamptonScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('12/01883/FUL') # Southampton NOT WORKING
    #scraper = SouthBuckinghamshireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/01303/FUL') # SouthBuckinghamshire OK
    #scraper = SouthendScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/01119/FUL') # Southend OK
    #scraper = StaffordshireMoorlandsScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/00749/FUL') # StaffordshireMoorlands OK
    #scraper = SwindonScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('S/11/1140') # Swindon OK
    #scraper = WatfordScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/00815/CM') # Watford OK
    #scraper = WaveneyScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('DC/11/0926/FUL') # Waveney OK
    #scraper = WestLancashireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('2011/0898/FUL') # WestLancashire OK
    #scraper = WorcestershireScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/000051/REG3') # Worcestershire OK

    #res = scraper.get_id_batch(util.get_dt('10/08/2011'), util.get_dt('10/08/2011'))
    #print res, len(res)


    

