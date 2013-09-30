# this is a scraper of planning applications for three district systems on DorsetForYou for use by Openly Local

# Christchurch, West Dorset and Weymouth

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import random
import urllib
import sys

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

systems = {
    'Christchurch': 'ChristchurchScraper',
    'WestDorset': 'WestDorsetScraper',
    'Weymouth': 'WeymouthScraper',
     }

class DorsetForYouScraper(base.DateScraper):

    MAX_ID_BATCH = 200 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 150 # max application details to scrape in one go

    request_date_format = '%d/%m/%Y'
    scrape_ids = """
    <table id="MatchingApplications_DataGrid_ResultSet"> <tr />
    {* <tr> <td> {{ [records].uid }} </td> </tr>  *}
    </table>
    """
    scrape_max_recs = '<span id="MatchingApplications_Label_CountResults"> list - {{ max_recs }} matching </span>'

    scrape_min_data = """
    <input id="DetailsOfProposal_Textbox_ApplicationNumber" value="{{ reference }}">
    <textarea id="DetailsOfProposal_Textbox_SiteAddress"> {{ address }} </textarea>
    <textarea id="DetailsOfProposal_Textbox_ProposedDevelopment"> {{ description }} </textarea>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<input id="DetailsOfProposal_Textbox_RegistrationDate" value="{{ date_validated }}">',
    '<textarea id="DetailsOfProposal_Textbox_ApplicationStatus"> {{ status }} </textarea>',
    '<input id="DetailsOfProposal_Textbox_ApplicationType" value="{{ application_type }}">',
    '<input id="DetailsOfProposal_Textbox_Decision" value="{{ decision }}">',
    '<input id="DetailsOfProposal_Textbox_DecisionDate" value="{{ decision_date }}">',
    '<input id="DetailsOfProposal_Textbox_CaseOfficer" value="{{ case_officer }}">',
    '<input id="DetailsOfProposal_Textbox_GridReference" value="{{ easting }}/{{ northing }}">',
    '<span id="ProgressBar_Label_PressAdDate"> Comments Welcome <br> By {{ consultation_end_date }} </span',
    '<span id="ProgressBar_Label_AppealLodged"> Appeal Lodged <br> {{ appeal_date }} </span>',
    '<span id="ProgressBar_Label_AppealOutcome"> Appeal Outcome <br> {{ appeal_decision_date }} </span>',
    ]
    # on separate page
    scrape_applic_data = '<input id="ApplicantAgentDetail_Textbox_ApplicantName" value="{{ applicant_name }}">'
    scrape_optional_applic = [
    '<textarea id="ApplicantAgentDetail_Textbox_ApplicantAddress"> {{ applicant_address }} </textarea>',
    '<input id="ApplicantAgentDetail_Textbox_AgentName" value="{{ agent_name }}">',
    '<textarea id="ApplicantAgentDetail_Textbox_AgentAddress"> {{ agent_address }} </textarea>',
    '<input id="ApplicantAgentDetail_Textbox_AgentTelephone" value="{{ agent_tel }}">'
    ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)

        fields = {}
        fields [self.date_from_field] = date_from.strftime(self.request_date_format)
        fields [self.date_to_field] = date_to.strftime(self.request_date_format)
        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br, self.search_submit)

        html = response.read()
        if self.DEBUG: print html
        try:
            result = scrapemark.scrape(self.scrape_max_recs, html)
            max_recs = int(result['max_recs'])
        except:
            max_recs = 0

        final_result = []
        while response and len(final_result) < max_recs:
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                for record in result['records']:
                    record['url'] = self.applic_url + urllib.quote_plus(record['uid'])
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            if len(final_result) >= max_recs: break
            fields = { '__EVENTARGUMENT': '', '__EVENTTARGET': self.next_field }
            util.setup_form(self.br, self.search_form, fields)
            for control in self.br.form.controls:
                if control.type == "submit":
                    control.disabled = True
            if self.DEBUG: print self.br.form
            response = util.submit_form(self.br)
            html = response.read()
            if self.DEBUG: print html

        return final_result

    def get_detail_from_uid (self, uid):
        url = self.applic_url + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

    # scrape detailed information on one record via its access URL
    def get_detail_from_url (self, url):
        if self.DEBUG: print "Url:", url
        try:
            response = self.br.open(url)
            html = response.read()
            url = response.geturl()
            if self.DEBUG:
                print "Html obtained from details url:", html
        except:
            return None
        final_result = self.get_detail(html, url)
        if final_result:
            try:
                fields = { '__EVENTARGUMENT': '', '__EVENTTARGET': self.applic_field }
                util.setup_form(self.br, self.detail_form, fields)
                for control in self.br.form.controls:
                    if control.type == "submit" or control.type == "image":
                        control.disabled = True
                if self.DEBUG: print self.br.form
                response = util.submit_form(self.br)
                html = response.read()
                url = response.geturl()
                if self.DEBUG:
                    print "Html obtained from applicant link:", html
                result = self.get_detail(html, url, self.scrape_data_block, self.scrape_applic_data, self.scrape_optional_applic)
                final_result.update(result)
            except:
                pass
            return final_result
        else:
            return None

class ChristchurchScraper(DorsetForYouScraper):

    TABLE_NAME = 'Christchurch'
    search_url = 'http://webapps.christchurch.gov.uk/PlanningApplications/pages/ApplicationSearch.aspx'
    applic_url = 'http://webapps.christchurch.gov.uk/PlanningApplications/pages/ApplicationDetails.aspx?Authority=Christchurch%20Borough%20Council&Application='
    search_form = 'ApplicationSearch'
    detail_form = 'ApplicationDetails'
    search_submit = 'DetailedSearch:Button_DetailedSearch'
    date_from_field = 'DetailedSearch:TextBox_DateRaisedFrom'
    date_to_field = 'DetailedSearch:TextBox_DateRaisedTo'
    next_field = 'MatchingApplications:ResultsNavigationBottom:LinkButton_Next'
    applic_field = 'PlanningNavigation:Button_ApplicantAgentDetails'
    scrape_data_block = '<form id="ApplicationDetails"> {{ block|html }} </form>'

    def __init__(self, table_name = None):
        DorsetForYouScraper.__init__(self, table_name)
        self.scrape_optional_data.append('<input id="DetailsOfProposal_Textbox_Parish" value="{{ ward_name }}">')

class WestDorsetScraper(DorsetForYouScraper):

    TABLE_NAME = 'WestDorset'
    search_url = 'http://eforms.dorsetforyou.com/planningapplications/%28S%28vrbfvgjy02hpcy55ybgzrh35%29%29/pages/applicationsearch.aspx'
    applic_url = 'http://eforms.dorsetforyou.com/planningapplications/(S(szto2rrxaciq1je5ozqnmnre))/pages/ApplicationDetails.aspx?Authority=West%20Dorset%20District%20Council&Application='
    search_form = 'ctl00'
    detail_form = 'ctl00'
    search_submit = 'DetailedSearch$Button_DetailedSearch'
    date_from_field = 'DetailedSearch$TextBox_DateRaisedFrom'
    date_to_field = 'DetailedSearch$TextBox_DateRaisedTo'
    next_field = 'MatchingApplications$ResultsNavigationTop$LinkButton_Next'
    applic_field = 'PlanningNavigation$Button_ApplicantAgentDetails'
    scrape_data_block = '<form id="ctl00"> {{ block|html }} </form>'

    def __init__(self, table_name = None):
        DorsetForYouScraper.__init__(self, table_name)
        self.scrape_optional_data.append('<input id="DetailsOfProposal_Textbox_Parish" value="{{ parish }}">')

class WeymouthScraper(DorsetForYouScraper):

    TABLE_NAME = 'Weymouth'
    search_url = 'http://webapps-wpbc.dorsetforyou.com/apps/development/Planregister.asp'
    applic_url = 'http://webapps.westdorset-dc.gov.uk/PlanAppsWPBC/(S(zsd2gm45uvpsxcjmmgn5cbyl))/pages/ApplicationDetails.aspx?Authority=Weymouth+and+Portland+Borough+Council&Application='
    search_form = 'ctl00'
    detail_form = 'ctl00'
    ref_field = 'QuickSearchApplicationNumber$TextBox_ApplicationNumber'
    ref_submit = 'QuickSearchApplicationNumber$Button_SearchApplicationNumber'
    search_submit = 'DetailedSearch$Button_DetailedSearch'
    date_from_field = 'DetailedSearch$TextBox_DateRaisedFrom'
    date_to_field = 'DetailedSearch$TextBox_DateRaisedTo'
    next_field = 'MatchingApplications$ResultsNavigationTop$LinkButton_Next'
    applic_field = 'PlanningNavigation$Button_ApplicantAgentDetails'
    scrape_data_block = '<form id="ctl00"> {{ block|html }} </form>'

    def __init__(self, table_name = None):
        DorsetForYouScraper.__init__(self, table_name)
        self.scrape_optional_data.append('<input id="DetailsOfProposal_Textbox_Parish" value="{{ parish }}">')

    def get_detail_from_uid (self, uid):
        try:
            response = self.br.open(self.search_url)
            fields = { self.ref_field: uid }
            util.setup_form(self.br, self.search_form, fields)
            if self.DEBUG: print self.br.form
            response = util.submit_form(self.br, self.ref_submit)
            html = response.read()
            url = response.geturl()
            if self.DEBUG:
                print "Html obtained from details via uid:", html
        except:
            return None
        final_result = self.get_detail(html, url)
        if final_result:
            try:
                fields = { '__EVENTARGUMENT': '', '__EVENTTARGET': self.applic_field }
                util.setup_form(self.br, self.detail_form, fields)
                for control in self.br.form.controls:
                    if control.type == "submit" or control.type == "image":
                        control.disabled = True
                if self.DEBUG: print self.br.form
                response = util.submit_form(self.br)
                html = response.read()
                url = response.geturl()
                if self.DEBUG:
                    print "Html obtained from applicant link:", html
                result = self.get_detail(html, url, self.scrape_data_block, self.scrape_applic_data, self.scrape_optional_applic)
                final_result.update(result)
            except:
                pass
            return final_result
        else:
            return None
    

if __name__ == 'scraper':

    #scraperwiki.sqlite.attach('weymouth_planning_applications', 'weymouth')
    #scraperwiki.sqlite.execute("create table Weymouth as select * from weymouth.swdata")
    #scraperwiki.sqlite.commit()
    #util.replace_vals('Weymouth', 'url', "'", "", 'prefix', 'yes')
    #sys.exit()

    sys_list = []
    for k, v in systems.items(): # get latest date scraped for each system
        sys_list.append( (k, v, scraperwiki.sqlite.get_var('latest-' + k)) )
    sort_sys = sorted(sys_list, key=lambda system: system[2]) # sort so least recent are first
    for auth in sort_sys[:4]: # do max 4 per run
        strexec = auth[1] + "('" + auth[0] + "')"
        print "Scraping from:", strexec
        try:
            scraper = eval(strexec)
            scraper.run()
        except Exception as err:
            print "Error - skipping this authority -", str(err)
    print "Finished"

    # misc test calls
    #scraper = WestDorsetScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('1/D/12/001362') # WestDorset
    #scraper = ChristchurchScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('8/11/0324') # Christchurch
    #scraper = WeymouthScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/00688/FUL')
    #print scraper.get_detail_from_uid ('00/00001/LBC') # Weymouth
    #print scraper.get_detail_from_uid ('10/00001/BHUTS')
    #result = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('19/08/2011'))
    #print len(result), result

    




# this is a scraper of planning applications for three district systems on DorsetForYou for use by Openly Local

# Christchurch, West Dorset and Weymouth

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import re
import dateutil.parser
import random
import urllib
import sys

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

systems = {
    'Christchurch': 'ChristchurchScraper',
    'WestDorset': 'WestDorsetScraper',
    'Weymouth': 'WeymouthScraper',
     }

class DorsetForYouScraper(base.DateScraper):

    MAX_ID_BATCH = 200 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 150 # max application details to scrape in one go

    request_date_format = '%d/%m/%Y'
    scrape_ids = """
    <table id="MatchingApplications_DataGrid_ResultSet"> <tr />
    {* <tr> <td> {{ [records].uid }} </td> </tr>  *}
    </table>
    """
    scrape_max_recs = '<span id="MatchingApplications_Label_CountResults"> list - {{ max_recs }} matching </span>'

    scrape_min_data = """
    <input id="DetailsOfProposal_Textbox_ApplicationNumber" value="{{ reference }}">
    <textarea id="DetailsOfProposal_Textbox_SiteAddress"> {{ address }} </textarea>
    <textarea id="DetailsOfProposal_Textbox_ProposedDevelopment"> {{ description }} </textarea>
    """
    # other optional parameters that can appear on an application page
    scrape_optional_data = [
    '<input id="DetailsOfProposal_Textbox_RegistrationDate" value="{{ date_validated }}">',
    '<textarea id="DetailsOfProposal_Textbox_ApplicationStatus"> {{ status }} </textarea>',
    '<input id="DetailsOfProposal_Textbox_ApplicationType" value="{{ application_type }}">',
    '<input id="DetailsOfProposal_Textbox_Decision" value="{{ decision }}">',
    '<input id="DetailsOfProposal_Textbox_DecisionDate" value="{{ decision_date }}">',
    '<input id="DetailsOfProposal_Textbox_CaseOfficer" value="{{ case_officer }}">',
    '<input id="DetailsOfProposal_Textbox_GridReference" value="{{ easting }}/{{ northing }}">',
    '<span id="ProgressBar_Label_PressAdDate"> Comments Welcome <br> By {{ consultation_end_date }} </span',
    '<span id="ProgressBar_Label_AppealLodged"> Appeal Lodged <br> {{ appeal_date }} </span>',
    '<span id="ProgressBar_Label_AppealOutcome"> Appeal Outcome <br> {{ appeal_decision_date }} </span>',
    ]
    # on separate page
    scrape_applic_data = '<input id="ApplicantAgentDetail_Textbox_ApplicantName" value="{{ applicant_name }}">'
    scrape_optional_applic = [
    '<textarea id="ApplicantAgentDetail_Textbox_ApplicantAddress"> {{ applicant_address }} </textarea>',
    '<input id="ApplicantAgentDetail_Textbox_AgentName" value="{{ agent_name }}">',
    '<textarea id="ApplicantAgentDetail_Textbox_AgentAddress"> {{ agent_address }} </textarea>',
    '<input id="ApplicantAgentDetail_Textbox_AgentTelephone" value="{{ agent_tel }}">'
    ]

    def get_id_batch (self, date_from, date_to):

        response = self.br.open(self.search_url)

        fields = {}
        fields [self.date_from_field] = date_from.strftime(self.request_date_format)
        fields [self.date_to_field] = date_to.strftime(self.request_date_format)
        util.setup_form(self.br, self.search_form, fields)
        if self.DEBUG: print self.br.form
        response = util.submit_form(self.br, self.search_submit)

        html = response.read()
        if self.DEBUG: print html
        try:
            result = scrapemark.scrape(self.scrape_max_recs, html)
            max_recs = int(result['max_recs'])
        except:
            max_recs = 0

        final_result = []
        while response and len(final_result) < max_recs:
            url = response.geturl()
            result = scrapemark.scrape(self.scrape_ids, html, url)
            if result and result.get('records'):
                for record in result['records']:
                    record['url'] = self.applic_url + urllib.quote_plus(record['uid'])
                self.clean_ids(result['records'])
                final_result.extend(result['records'])
            if len(final_result) >= max_recs: break
            fields = { '__EVENTARGUMENT': '', '__EVENTTARGET': self.next_field }
            util.setup_form(self.br, self.search_form, fields)
            for control in self.br.form.controls:
                if control.type == "submit":
                    control.disabled = True
            if self.DEBUG: print self.br.form
            response = util.submit_form(self.br)
            html = response.read()
            if self.DEBUG: print html

        return final_result

    def get_detail_from_uid (self, uid):
        url = self.applic_url + urllib.quote_plus(uid)
        return self.get_detail_from_url(url)

    # scrape detailed information on one record via its access URL
    def get_detail_from_url (self, url):
        if self.DEBUG: print "Url:", url
        try:
            response = self.br.open(url)
            html = response.read()
            url = response.geturl()
            if self.DEBUG:
                print "Html obtained from details url:", html
        except:
            return None
        final_result = self.get_detail(html, url)
        if final_result:
            try:
                fields = { '__EVENTARGUMENT': '', '__EVENTTARGET': self.applic_field }
                util.setup_form(self.br, self.detail_form, fields)
                for control in self.br.form.controls:
                    if control.type == "submit" or control.type == "image":
                        control.disabled = True
                if self.DEBUG: print self.br.form
                response = util.submit_form(self.br)
                html = response.read()
                url = response.geturl()
                if self.DEBUG:
                    print "Html obtained from applicant link:", html
                result = self.get_detail(html, url, self.scrape_data_block, self.scrape_applic_data, self.scrape_optional_applic)
                final_result.update(result)
            except:
                pass
            return final_result
        else:
            return None

class ChristchurchScraper(DorsetForYouScraper):

    TABLE_NAME = 'Christchurch'
    search_url = 'http://webapps.christchurch.gov.uk/PlanningApplications/pages/ApplicationSearch.aspx'
    applic_url = 'http://webapps.christchurch.gov.uk/PlanningApplications/pages/ApplicationDetails.aspx?Authority=Christchurch%20Borough%20Council&Application='
    search_form = 'ApplicationSearch'
    detail_form = 'ApplicationDetails'
    search_submit = 'DetailedSearch:Button_DetailedSearch'
    date_from_field = 'DetailedSearch:TextBox_DateRaisedFrom'
    date_to_field = 'DetailedSearch:TextBox_DateRaisedTo'
    next_field = 'MatchingApplications:ResultsNavigationBottom:LinkButton_Next'
    applic_field = 'PlanningNavigation:Button_ApplicantAgentDetails'
    scrape_data_block = '<form id="ApplicationDetails"> {{ block|html }} </form>'

    def __init__(self, table_name = None):
        DorsetForYouScraper.__init__(self, table_name)
        self.scrape_optional_data.append('<input id="DetailsOfProposal_Textbox_Parish" value="{{ ward_name }}">')

class WestDorsetScraper(DorsetForYouScraper):

    TABLE_NAME = 'WestDorset'
    search_url = 'http://eforms.dorsetforyou.com/planningapplications/%28S%28vrbfvgjy02hpcy55ybgzrh35%29%29/pages/applicationsearch.aspx'
    applic_url = 'http://eforms.dorsetforyou.com/planningapplications/(S(szto2rrxaciq1je5ozqnmnre))/pages/ApplicationDetails.aspx?Authority=West%20Dorset%20District%20Council&Application='
    search_form = 'ctl00'
    detail_form = 'ctl00'
    search_submit = 'DetailedSearch$Button_DetailedSearch'
    date_from_field = 'DetailedSearch$TextBox_DateRaisedFrom'
    date_to_field = 'DetailedSearch$TextBox_DateRaisedTo'
    next_field = 'MatchingApplications$ResultsNavigationTop$LinkButton_Next'
    applic_field = 'PlanningNavigation$Button_ApplicantAgentDetails'
    scrape_data_block = '<form id="ctl00"> {{ block|html }} </form>'

    def __init__(self, table_name = None):
        DorsetForYouScraper.__init__(self, table_name)
        self.scrape_optional_data.append('<input id="DetailsOfProposal_Textbox_Parish" value="{{ parish }}">')

class WeymouthScraper(DorsetForYouScraper):

    TABLE_NAME = 'Weymouth'
    search_url = 'http://webapps-wpbc.dorsetforyou.com/apps/development/Planregister.asp'
    applic_url = 'http://webapps.westdorset-dc.gov.uk/PlanAppsWPBC/(S(zsd2gm45uvpsxcjmmgn5cbyl))/pages/ApplicationDetails.aspx?Authority=Weymouth+and+Portland+Borough+Council&Application='
    search_form = 'ctl00'
    detail_form = 'ctl00'
    ref_field = 'QuickSearchApplicationNumber$TextBox_ApplicationNumber'
    ref_submit = 'QuickSearchApplicationNumber$Button_SearchApplicationNumber'
    search_submit = 'DetailedSearch$Button_DetailedSearch'
    date_from_field = 'DetailedSearch$TextBox_DateRaisedFrom'
    date_to_field = 'DetailedSearch$TextBox_DateRaisedTo'
    next_field = 'MatchingApplications$ResultsNavigationTop$LinkButton_Next'
    applic_field = 'PlanningNavigation$Button_ApplicantAgentDetails'
    scrape_data_block = '<form id="ctl00"> {{ block|html }} </form>'

    def __init__(self, table_name = None):
        DorsetForYouScraper.__init__(self, table_name)
        self.scrape_optional_data.append('<input id="DetailsOfProposal_Textbox_Parish" value="{{ parish }}">')

    def get_detail_from_uid (self, uid):
        try:
            response = self.br.open(self.search_url)
            fields = { self.ref_field: uid }
            util.setup_form(self.br, self.search_form, fields)
            if self.DEBUG: print self.br.form
            response = util.submit_form(self.br, self.ref_submit)
            html = response.read()
            url = response.geturl()
            if self.DEBUG:
                print "Html obtained from details via uid:", html
        except:
            return None
        final_result = self.get_detail(html, url)
        if final_result:
            try:
                fields = { '__EVENTARGUMENT': '', '__EVENTTARGET': self.applic_field }
                util.setup_form(self.br, self.detail_form, fields)
                for control in self.br.form.controls:
                    if control.type == "submit" or control.type == "image":
                        control.disabled = True
                if self.DEBUG: print self.br.form
                response = util.submit_form(self.br)
                html = response.read()
                url = response.geturl()
                if self.DEBUG:
                    print "Html obtained from applicant link:", html
                result = self.get_detail(html, url, self.scrape_data_block, self.scrape_applic_data, self.scrape_optional_applic)
                final_result.update(result)
            except:
                pass
            return final_result
        else:
            return None
    

if __name__ == 'scraper':

    #scraperwiki.sqlite.attach('weymouth_planning_applications', 'weymouth')
    #scraperwiki.sqlite.execute("create table Weymouth as select * from weymouth.swdata")
    #scraperwiki.sqlite.commit()
    #util.replace_vals('Weymouth', 'url', "'", "", 'prefix', 'yes')
    #sys.exit()

    sys_list = []
    for k, v in systems.items(): # get latest date scraped for each system
        sys_list.append( (k, v, scraperwiki.sqlite.get_var('latest-' + k)) )
    sort_sys = sorted(sys_list, key=lambda system: system[2]) # sort so least recent are first
    for auth in sort_sys[:4]: # do max 4 per run
        strexec = auth[1] + "('" + auth[0] + "')"
        print "Scraping from:", strexec
        try:
            scraper = eval(strexec)
            scraper.run()
        except Exception as err:
            print "Error - skipping this authority -", str(err)
    print "Finished"

    # misc test calls
    #scraper = WestDorsetScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('1/D/12/001362') # WestDorset
    #scraper = ChristchurchScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('8/11/0324') # Christchurch
    #scraper = WeymouthScraper()
    #scraper.DEBUG = True
    #print scraper.get_detail_from_uid ('11/00688/FUL')
    #print scraper.get_detail_from_uid ('00/00001/LBC') # Weymouth
    #print scraper.get_detail_from_uid ('10/00001/BHUTS')
    #result = scraper.get_id_batch(util.get_dt('08/08/2011'), util.get_dt('19/08/2011'))
    #print len(result), result

    




