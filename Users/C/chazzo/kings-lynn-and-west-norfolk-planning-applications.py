###############################################################################
# Scrape planning applications to King's Lynn and West Norfolk Borough Council

# Based on the new PublicAccess (Idox version) scraper referenced at:
# http://code.google.com/p/planningalerts/issues/detail?id=49#c0

# Doesn't work because I haven't the faintest idea what I'm doing.

# Charles Butcher 2012-02-01

###############################################################################

import urllib, urllib2
import urlparse
import datetime
import re
import mechanize
import sys
import string
import BeautifulSoup
import cookielib
import scraperwiki

cookie_jar = cookielib.CookieJar()

PlanningUtils = scraperwiki.utils.swimport("planningalertscom-planningutils-library")
fixNewlines = PlanningUtils.fixNewlines
getPostcodeFromText = PlanningUtils.getPostcodeFromText
PlanningAuthorityResults = PlanningUtils.PlanningAuthorityResults
PlanningApplication = PlanningUtils.PlanningApplication

# ignore robots.txt, which for this council is set to disallow all bots:
# http://online.west-norfolk.gov.uk/robots.txt

br = mechanize.Browser()
br.set_handle_robots(False)

class NewPublicAccessParser(object):
    """This is the class which parses the PublicAccess search results page.
    """

    search_form_url_end = "search.do?action=advanced"
    search_results_url_end = "advancedSearchResults.do?action=firstPage"

# Form fields checked correct against the website on 2012-02-01

    data_template = (
            ("searchType", "Application"),
            ("caseAddressType", "Application"),
            ("searchCriteria.reference", ""),
            ("searchCriteria.planningPortalReference", ""),
            ("searchCriteria.alternativeReference", ""),
            ("searchCriteria.description", ""),
            ("searchCriteria.applicantName", ""),
            ("searchCriteria.caseType", ""),
            ("searchCriteria.ward", ""),
            ("searchCriteria.parish", ""),
            ("searchCriteria.agent", ""),
            ("searchCriteria.caseStatus", ""),
            ("searchCriteria.caseDecision", ""),
            ("searchCriteria.appealStatus", ""),
            ("searchCriteria.appealDecision", ""),
            ("searchCriteria.developmentType", ""),
            ("searchCriteria.address", ""),
            ("dates(applicationReceivedStart)", "%(day)02d/%(month)02d/%(year)04d"),
            ("dates(applicationReceivedEnd)", "%(day)02d/%(month)02d/%(year)04d"),
            ("dates(applicationValidatedStart)", ""),
            ("dates(applicationValidatedEnd)", ""),
            ("date(applicationCommitteeStart)", ""),
            ("date(applicationCommitteeEnd)", ""),
            ("date(applicationDecisionStart)", ""),
            ("date(applicationDecisionEnd)", ""),
            ("date(appealDecisionStart)", ""),
            ("date(appealDecisionEnd)", ""),
            ("date(applicationDeterminedStart)", ""),
            ("date(applicationDeterminedEnd)", ""),
            )

    def __init__(self,
                 authority_name,
                 authority_short_name,
                 base_url,
                 debug=False):
        
        self.authority_name = authority_name
        self.authority_short_name = authority_short_name
        self.base_url = base_url
        self.debug = debug

        # The object which stores our set of planning application results
        self._results = PlanningAuthorityResults(self.authority_name, self.authority_short_name)

    def fetch_setting_cookie(self, url, data=None):
        request = urllib2.Request(url, data)
        
        if self.debug:
            print >>sys.stderr, "Request URL: " + url
            if request.has_data():
                print >>sys.stderr, "Request data: " + request.get_data()
        cookie_jar.add_cookie_header(request)
        response = urllib2.urlopen(request)
        cookie_jar.extract_cookies(response, request)

        if self.debug:
            print >>sys.stderr, "vvvv Response"
            print >>sys.stderr, response  
            print >>sys.stderr, "^^^^ Response"
        return response

    def get_search_page(self):
        return self.fetch_setting_cookie(urlparse.urljoin(self.base_url, self.search_form_url_end))

    def get_response_1(self, data):
        return self.fetch_setting_cookie(urlparse.urljoin(self.base_url, self.search_results_url_end), data)

    def get_data_1(self, replacement_dict):
        # It seems urllib.urlencode isn't happy with the generator here,
        # so we'd best make it a tuple...
        data_tuple = tuple(((key, value %replacement_dict) for (key, value) in self.data_template))

        data = urllib.urlencode(data_tuple)
        return data
        
    def get_replacement_dict(self, day, month, year, search_response):
        return {"day": day, 
                "month": month, 
                "year": year}
    
    def get_useful_response(self, day, month, year):
        # We're only doing this to get a cookie
        search_response = self.get_search_page()

        replacement_dict = self.get_replacement_dict(day, month, year, search_response)
        data = self.get_data_1(replacement_dict)

        return self.get_response_1(data)

    def get_contents(self, day, month, year):
        useful_response = self.get_useful_response(day, month, year)

        contents = fixNewlines(useful_response.read())

        if self.debug:
            print contents

        return contents

    def getResultsByDayMonthYear(self, day, month, year):
        search_date = datetime.date(year, month, day)

        contents = self.get_contents(day, month, year)

        soup = BeautifulSoup.BeautifulSoup(contents)

        results_table = soup.find("ul", {"id": "searchresults"})

        for li in results_table.findAll("li"):
            application = PlanningApplication()
            
            application.date_received = search_date
            application.info_url = urlparse.urljoin(self.base_url, li.a['href'])
            application.description = li.a.string.strip()
            application.address = li.findAll("p", {"class": "address"})[0].string.strip()
            
            # The reference number is in a string like "Ref. No: xx/yyyy/zzz"
            application.council_reference = li.findAll("p", {"class": "metaInfo"})[0].contents[0].split()[2]
            application.comment_url = string.replace(application.info_url, "activeTab=summary", "activeTab=makeComment")

            self._results.addApplication(application)

        return self._results

    def getResults(self, day, month, year):
        return self.getResultsByDayMonthYear(int(day), int(month), int(year)).displayXML()

# Not sure what this block is supposed to do
if __name__ == '__main__':
    day = 31
    month = 01
    year = 2012

# Date 31/02/2012 should return a handful of results for test purposes
day = 31
month = 01
year = 2012

parser = NewPublicAccessParser("Kings Lynn and West Norfolk", "West Norfolk", "http://online.west-norfolk.gov.uk/online-applications/", debug=True)
print parser.getResults(day, month, year)
