# -*- coding: utf-8 -*-

import urllib2
import urllib
import urlparse
import cgi
import re
import datetime
import scraperwiki

import BeautifulSoup

class PlanningAuthorityResults:
    """This class represents a set of results of a planning search.

       This should probably be separated out so that it can be used for
       authorities other than Cherwell.
       """

    def __init__(self, authority_name, authority_short_name):
        self.authority_name = authority_name
        self.authority_short_name = authority_short_name
    
    # this will be a list of PlanningApplication objects
        self.planning_applications = []


    def addApplication(self, application):
        self.planning_applications.append(application)

    def __repr__(self):
        return self.displayXML()

    def save(self): 
        [x.save() for x in self.planning_applications]
        
    def displayXML(self):
        """This should display the contents of this object in the planningalerts format.
           i.e. in the same format as this one:
           http://www.planningalerts.com/lambeth.xml
           """
        applications_bit = "".join([x.displayXML() for x in self.planning_applications])
    
        return u"""<?xml version="1.0" encoding="UTF-8"?>\n""" + \
                u"<planning>\n" +\
                u"<authority_name>%s</authority_name>\n" %self.authority_name +\
                u"<authority_short_name>%s</authority_short_name>\n" %self.authority_short_name +\
                u"<applications>\n" + applications_bit +\
                u"</applications>\n" +\
                u"</planning>\n"

class PlanningApplication:
    def __init__(self):
        self.council_reference = None
        self.address = None
        self.postcode = None
        self.description = None
        self.info_url = None
        self.comment_url = None

        # expecting this as a datetime.date object
        self.date_received = None

        # If we can get them, we may as well include OSGB.
        # These will be the entirely numeric version.
        self.osgb_x = None
        self.osgb_y = None

    def __repr__(self):
        return self.displayXML()

    def is_ready(self):
        # This method tells us if the application is complete
        # Because of the postcode default, we can't really
        # check the postcode - make sure it is filled in when
        # you do the address.
        return self.council_reference \
            and self.address \
            and self.description \
            and self.info_url \
            and self.comment_url \
            and self.date_received
    
    def save(self):
        scraperwiki.sqlite.save(['council_reference'], {'council_reference': self.council_reference or '',
                                                           'address': self.address or '',
                                                           'postcode': self.postcode or '',
                                                           'description': self.description or '',
                                                           'info_url': self.info_url or '',
                                                           'comment_url': self.comment_url or '',
                                                           'date_received': self.date_received}, date=self.date_received)
        
    def displayXML(self):
        #print self.council_reference, self.address, self.postcode, self.description, self.info_url, self.comment_url, self.date_received

        if not self.postcode:
            self.postcode = getPostcodeFromText(self.address)

        contents = [
            u"<council_reference><![CDATA[%s]]></council_reference>" %(self.council_reference),
            u"<address><![CDATA[%s]]></address>" %(self.address),
            u"<postcode><![CDATA[%s]]></postcode>" %self.postcode,
            u"<description><![CDATA[%s]]></description>" %(self.description),
            u"<info_url><![CDATA[%s]]></info_url>" %(self.info_url),
            u"<comment_url><![CDATA[%s]]></comment_url>" %(self.comment_url),
            u"<date_received><![CDATA[%s]]></date_received>" %self.date_received.strftime(date_format),
            ]
        if self.osgb_x:
            contents.append(u"<osgb_x>%s</osgb_x>" %(self.osgb_x))
        if self.osgb_y:
            contents.append(u"<osgb_y>%s</osgb_y>" %(self.osgb_y))

        return u"<application>\n%s\n</application>" %('\n'.join(contents))

postcode_regex = re.compile("[A-Z][A-Z]?\d(\d|[A-Z])? ?\d[A-Z][A-Z]")

def getPostcodeFromText(text, default_postcode="No Postcode"):
    """This function takes a piece of text and returns the first
    bit of it that looks like a postcode."""

    postcode_match = postcode_regex.search(text)

    return postcode_match.group() if postcode_match else default_postcode


# Date format to enter into search boxes
date_format = "%d/%m/%Y"

class SwiftLGParser:
    search_path = "WPHAPPCRITERIA"
    info_path = "WPHAPPDETAIL.DisplayUrl?theApnID=%s"
    comment_path ="wphmakerep.displayURL?ApnID=%s"

    def _fixHTML(self, html):
        return html

    def _findResultsTable(self, soup):
        """Unless there is just one table in the page, the resuts table,
        override this in a subclass."""
        return soup.table

    def _findTRs(self, results_table):
        """The usual situation is for the results table to contain
        one row of headers, followed by a row per app.
        If this is not the case, override this in a subclass."""
#        import pdb;pdb.set_trace()
        return results_table.findAll("tr")[1:]

    def __init__(self,
                 authority_name,
                 authority_short_name,
                 base_url,
                 debug=False):
        
        self.authority_name = authority_name
        self.authority_short_name = authority_short_name
        self.base_url = base_url

        self.search_url = urlparse.urljoin(base_url, self.search_path)
        self.info_url = urlparse.urljoin(base_url, self.info_path)
        self.comment_url = urlparse.urljoin(base_url, self.comment_path)

        self.debug = debug

        self._results = PlanningAuthorityResults(self.authority_name, self.authority_short_name)


    def getResultsByDayMonthYear(self, day, month, year):
        search_date = datetime.date(year, month, day)
        
        post_data = urllib.urlencode((
                ("REGFROMDATE.MAINBODY.WPACIS.1.", search_date.strftime(date_format)),
                ("REGTODATE.MAINBODY.WPACIS.1.", search_date.strftime(date_format)),
                ("SEARCHBUTTON.MAINBODY.WPACIS.1.", "Search"),
                ))
        
        response = urllib2.urlopen(self.search_url, post_data)
        contents = response.read()

        # Let's give scrapers the change to tidy up any rubbish - I'm looking
        # at you Cannock Chase
        contents = self._fixHTML(contents)

        # Check for the no results warning
        if not contents.count("No Matching Applications Found"):
            soup = BeautifulSoup.BeautifulSoup(contents)

            # Get the links to later pages of results.
            later_pages = soup.findAll("a", {"href": re.compile("WPHAPPSEARCHRES\.displayResultsURL.*StartIndex=\d*.*")})

            for a in ["initial_search"] + later_pages:
                if a != "initial_search":
                    url = a['href']

                    # urllib2 doesn't like this url, to make it happy, we'll
                    # get rid of the BackURL parameter, which we don't need.

                    split_url = urlparse.urlsplit(url)
                    qs = split_url[3]

                    # This gets us a dictionary of key to lists of values
                    qsl = cgi.parse_qsl(qs)

                    # Get rid of BackURL
                    qsl.pop(-1)

                    # I think this is safe, as there are no repeats of parameters
                    new_qs = urllib.urlencode(qsl)

                    url = urlparse.urlunsplit(split_url[:3] + (new_qs,) + split_url[4:])

                    this_page_url = urlparse.urljoin(self.base_url, url)
                    response = urllib2.urlopen(this_page_url)
                    contents = response.read()
                    soup = BeautifulSoup.BeautifulSoup(contents)

                results_table = self._findResultsTable(soup)#.body.find("table", {"class": "apas_tbl"})

                trs = self._findTRs(results_table)

                for tr in trs:
                    self._current_application = PlanningApplication()

                    tds = tr.findAll("td")

                    first_link = tds[0].a['href']

                    app_id = cgi.parse_qs(urlparse.urlsplit(first_link)[3])['theApnID'][0]

                    self._current_application.date_received = search_date
                    self._current_application.council_reference = app_id
                    self._current_application.info_url = self.info_url %(app_id)
                    self._current_application.comment_url = self.comment_url %(app_id)
                    self._current_application.description = tds[1].string.strip()

                    address = ' '.join([x for x in tds[2].contents if isinstance(x, BeautifulSoup.NavigableString)]).strip()

                    self._current_application.address = address
                    self._current_application.postcode = getPostcodeFromText(address)

                    self._results.addApplication(self._current_application)

        return self._results

    def getResults(self, day, month, year):
        return self.getResultsByDayMonthYear(int(day), int(month), int(year)).displayXML()

    def saveResults(self, day, month, year):
        return self.getResultsByDayMonthYear(int(day), int(month), int(year)).save()

if __name__ == 'scraper':
    parser = SwiftLGParser("Dun Laoghaire-Rathdown County Council", "Dun Laoghaire-Rathdown", "http://planning.dlrcoco.ie/swiftlg/apas/run/WPHAPPCRITERIA")
    today = datetime.date.today()
    for i in range(365):
        day = today - datetime.timedelta(days=i)
        parser.saveResults(day.day, day.month, day.year)
# -*- coding: utf-8 -*-

import urllib2
import urllib
import urlparse
import cgi
import re
import datetime
import scraperwiki

import BeautifulSoup

class PlanningAuthorityResults:
    """This class represents a set of results of a planning search.

       This should probably be separated out so that it can be used for
       authorities other than Cherwell.
       """

    def __init__(self, authority_name, authority_short_name):
        self.authority_name = authority_name
        self.authority_short_name = authority_short_name
    
    # this will be a list of PlanningApplication objects
        self.planning_applications = []


    def addApplication(self, application):
        self.planning_applications.append(application)

    def __repr__(self):
        return self.displayXML()

    def save(self): 
        [x.save() for x in self.planning_applications]
        
    def displayXML(self):
        """This should display the contents of this object in the planningalerts format.
           i.e. in the same format as this one:
           http://www.planningalerts.com/lambeth.xml
           """
        applications_bit = "".join([x.displayXML() for x in self.planning_applications])
    
        return u"""<?xml version="1.0" encoding="UTF-8"?>\n""" + \
                u"<planning>\n" +\
                u"<authority_name>%s</authority_name>\n" %self.authority_name +\
                u"<authority_short_name>%s</authority_short_name>\n" %self.authority_short_name +\
                u"<applications>\n" + applications_bit +\
                u"</applications>\n" +\
                u"</planning>\n"

class PlanningApplication:
    def __init__(self):
        self.council_reference = None
        self.address = None
        self.postcode = None
        self.description = None
        self.info_url = None
        self.comment_url = None

        # expecting this as a datetime.date object
        self.date_received = None

        # If we can get them, we may as well include OSGB.
        # These will be the entirely numeric version.
        self.osgb_x = None
        self.osgb_y = None

    def __repr__(self):
        return self.displayXML()

    def is_ready(self):
        # This method tells us if the application is complete
        # Because of the postcode default, we can't really
        # check the postcode - make sure it is filled in when
        # you do the address.
        return self.council_reference \
            and self.address \
            and self.description \
            and self.info_url \
            and self.comment_url \
            and self.date_received
    
    def save(self):
        scraperwiki.sqlite.save(['council_reference'], {'council_reference': self.council_reference or '',
                                                           'address': self.address or '',
                                                           'postcode': self.postcode or '',
                                                           'description': self.description or '',
                                                           'info_url': self.info_url or '',
                                                           'comment_url': self.comment_url or '',
                                                           'date_received': self.date_received}, date=self.date_received)
        
    def displayXML(self):
        #print self.council_reference, self.address, self.postcode, self.description, self.info_url, self.comment_url, self.date_received

        if not self.postcode:
            self.postcode = getPostcodeFromText(self.address)

        contents = [
            u"<council_reference><![CDATA[%s]]></council_reference>" %(self.council_reference),
            u"<address><![CDATA[%s]]></address>" %(self.address),
            u"<postcode><![CDATA[%s]]></postcode>" %self.postcode,
            u"<description><![CDATA[%s]]></description>" %(self.description),
            u"<info_url><![CDATA[%s]]></info_url>" %(self.info_url),
            u"<comment_url><![CDATA[%s]]></comment_url>" %(self.comment_url),
            u"<date_received><![CDATA[%s]]></date_received>" %self.date_received.strftime(date_format),
            ]
        if self.osgb_x:
            contents.append(u"<osgb_x>%s</osgb_x>" %(self.osgb_x))
        if self.osgb_y:
            contents.append(u"<osgb_y>%s</osgb_y>" %(self.osgb_y))

        return u"<application>\n%s\n</application>" %('\n'.join(contents))

postcode_regex = re.compile("[A-Z][A-Z]?\d(\d|[A-Z])? ?\d[A-Z][A-Z]")

def getPostcodeFromText(text, default_postcode="No Postcode"):
    """This function takes a piece of text and returns the first
    bit of it that looks like a postcode."""

    postcode_match = postcode_regex.search(text)

    return postcode_match.group() if postcode_match else default_postcode


# Date format to enter into search boxes
date_format = "%d/%m/%Y"

class SwiftLGParser:
    search_path = "WPHAPPCRITERIA"
    info_path = "WPHAPPDETAIL.DisplayUrl?theApnID=%s"
    comment_path ="wphmakerep.displayURL?ApnID=%s"

    def _fixHTML(self, html):
        return html

    def _findResultsTable(self, soup):
        """Unless there is just one table in the page, the resuts table,
        override this in a subclass."""
        return soup.table

    def _findTRs(self, results_table):
        """The usual situation is for the results table to contain
        one row of headers, followed by a row per app.
        If this is not the case, override this in a subclass."""
#        import pdb;pdb.set_trace()
        return results_table.findAll("tr")[1:]

    def __init__(self,
                 authority_name,
                 authority_short_name,
                 base_url,
                 debug=False):
        
        self.authority_name = authority_name
        self.authority_short_name = authority_short_name
        self.base_url = base_url

        self.search_url = urlparse.urljoin(base_url, self.search_path)
        self.info_url = urlparse.urljoin(base_url, self.info_path)
        self.comment_url = urlparse.urljoin(base_url, self.comment_path)

        self.debug = debug

        self._results = PlanningAuthorityResults(self.authority_name, self.authority_short_name)


    def getResultsByDayMonthYear(self, day, month, year):
        search_date = datetime.date(year, month, day)
        
        post_data = urllib.urlencode((
                ("REGFROMDATE.MAINBODY.WPACIS.1.", search_date.strftime(date_format)),
                ("REGTODATE.MAINBODY.WPACIS.1.", search_date.strftime(date_format)),
                ("SEARCHBUTTON.MAINBODY.WPACIS.1.", "Search"),
                ))
        
        response = urllib2.urlopen(self.search_url, post_data)
        contents = response.read()

        # Let's give scrapers the change to tidy up any rubbish - I'm looking
        # at you Cannock Chase
        contents = self._fixHTML(contents)

        # Check for the no results warning
        if not contents.count("No Matching Applications Found"):
            soup = BeautifulSoup.BeautifulSoup(contents)

            # Get the links to later pages of results.
            later_pages = soup.findAll("a", {"href": re.compile("WPHAPPSEARCHRES\.displayResultsURL.*StartIndex=\d*.*")})

            for a in ["initial_search"] + later_pages:
                if a != "initial_search":
                    url = a['href']

                    # urllib2 doesn't like this url, to make it happy, we'll
                    # get rid of the BackURL parameter, which we don't need.

                    split_url = urlparse.urlsplit(url)
                    qs = split_url[3]

                    # This gets us a dictionary of key to lists of values
                    qsl = cgi.parse_qsl(qs)

                    # Get rid of BackURL
                    qsl.pop(-1)

                    # I think this is safe, as there are no repeats of parameters
                    new_qs = urllib.urlencode(qsl)

                    url = urlparse.urlunsplit(split_url[:3] + (new_qs,) + split_url[4:])

                    this_page_url = urlparse.urljoin(self.base_url, url)
                    response = urllib2.urlopen(this_page_url)
                    contents = response.read()
                    soup = BeautifulSoup.BeautifulSoup(contents)

                results_table = self._findResultsTable(soup)#.body.find("table", {"class": "apas_tbl"})

                trs = self._findTRs(results_table)

                for tr in trs:
                    self._current_application = PlanningApplication()

                    tds = tr.findAll("td")

                    first_link = tds[0].a['href']

                    app_id = cgi.parse_qs(urlparse.urlsplit(first_link)[3])['theApnID'][0]

                    self._current_application.date_received = search_date
                    self._current_application.council_reference = app_id
                    self._current_application.info_url = self.info_url %(app_id)
                    self._current_application.comment_url = self.comment_url %(app_id)
                    self._current_application.description = tds[1].string.strip()

                    address = ' '.join([x for x in tds[2].contents if isinstance(x, BeautifulSoup.NavigableString)]).strip()

                    self._current_application.address = address
                    self._current_application.postcode = getPostcodeFromText(address)

                    self._results.addApplication(self._current_application)

        return self._results

    def getResults(self, day, month, year):
        return self.getResultsByDayMonthYear(int(day), int(month), int(year)).displayXML()

    def saveResults(self, day, month, year):
        return self.getResultsByDayMonthYear(int(day), int(month), int(year)).save()

if __name__ == 'scraper':
    parser = SwiftLGParser("Dun Laoghaire-Rathdown County Council", "Dun Laoghaire-Rathdown", "http://planning.dlrcoco.ie/swiftlg/apas/run/WPHAPPCRITERIA")
    today = datetime.date.today()
    for i in range(365):
        day = today - datetime.timedelta(days=i)
        parser.saveResults(day.day, day.month, day.year)
