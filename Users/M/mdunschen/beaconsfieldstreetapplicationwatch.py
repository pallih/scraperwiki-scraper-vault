# what needs doing:
# - use sql to save 2nd table with number of docs
# - email when number of docs (or doc content?) changes


import scraperwiki
import mechanize, re
import urllib2
import httplib

import datetime

debug = False # used for debug prints

northgatebase = "http://northgate.liverpool.gov.uk%s"
liverpoolngtempl = northgatebase % "/PlanningExplorer17/Generic/%s"
liverpoolplanning = northgatebase % "/planningexplorer17/"

def cleanUrl(url):
    return url.replace("\t", "").replace("&amp;", "&").replace("&#xD;&#xA;", "").strip().replace(" ", "%20")

class RobustBrowser(mechanize.Browser):
    def __init__(self):
        mechanize.Browser.__init__(self)
        self.set_handle_refresh(False) # can sometimes hang without this 
        self.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')] 
    
    def robustOpen(self, url):
        if debug:
            print "url = ", url
        if type(url) != type("http"):
            assert False
        for i in range(5):
            try:
                return mechanize.Browser.open(self, url)
            except mechanize.URLError:
                if True:
                    print "Failed: %d" % i, url




def search(b=None, siteaddress="", appnum="", dateStart="", dateEnd=""):
    # the search is slow, Julian thinks I should scrape 'all' applications and then filter these.
    if not b:
        b = RobustBrowser()
    assert b
    b.robustOpen(liverpoolplanning)    
    def submit():
        try:
            b.select_form(nr=0)
            b.form["txtSiteAddress"] = siteaddress
            b.form["txtApplicationNumber"] = appnum
            if dateStart:
                if debug:
                    print "dates: ", dateStart, dateEnd
                b.form["dateStart"] = dateStart
                b.form["dateEnd"] = dateEnd or dateStart # would this search for one specific date?
                b.form["rbGroup"] = ["rbRange"]
                # search for date registered. 
                # Other options are: "DATE_RECEIVED", "DATE_VALID", "DATE_TARGET", "DATE_TO_COMMITTEE", "DATE_DECISION"
                b.form["cboSelectDateValue"] = ["DATE_REGISTERED"] 
            b.submit()
            return True
        except (urllib2.HTTPError, mechanize.URLError):
            return False

        except httplib.BadStatusLine as e:
            print "Exception = ", str(e)
            raise e
        
        except mechanize.FormNotFoundError as e:
            if debug:
                print b.read()
            raise e
        
    for i in range(3):
        success = submit()
        if success:
            break

    if success:
        return b.response().read()
    else:
        if debug:
            print "Form submission failed 3 times!!!"

def parsePage(r):
    if re.match('.*No Records Found.', r, re.DOTALL):
        return []
    
    m = re.match('.*<table .*? summary="Results of the Search" .*?>(.*?)</table>', r, re.DOTALL)
    t = m.group(1)
    rows = re.findall('<tr class=\"Row\d*?.*?>(.*?)</tr>', t, re.DOTALL)
    
    # row 0 has names of columns
    colnames = re.findall('<th .*?>(.*?)</th>', rows[0], re.DOTALL)   
    allPlans = [ ]
    for a in rows[1:]:
        values = re.findall('<td .*?>(.*?)</td>', a, re.DOTALL)
    
        # first value also contains a url
        m = re.match('.*?href="(.*?)">(.*?)</a>', values[0], re.DOTALL)
    
        # zip up into dict
        d = dict(zip(colnames[1:], values[1:]))
        d[colnames[0]] = m.group(2)
        
        # filter out all sorts of crap, from tabs to CR/LF...
        d['url'] = liverpoolngtempl % cleanUrl(m.group(1))    
        allPlans.append(d)
    return allPlans
    
    
def relatedDocs(detailsurl):
    b = RobustBrowser()
    b.set_handle_robots(False)
    r = b.robustOpen(detailsurl)
    t = r.read()
    m = re.match('.*href="(.*?)".*?>Related Documents</[Aa]>', t, re.DOTALL)
    if m:
        docsurl = northgatebase % cleanUrl(m.group(1))
        dd = b.robustOpen(docsurl)
        if not dd:
            return {}

        d = dd.read()
        tbl = re.match('.*?<table.*?>(.*?)</table>', d, re.DOTALL)

        if not tbl:
            if debug:
                print "no docs? docsurl = ", docsurl
            return

        # find all anchors
        r = re.findall('<a href="(.*?)">(.*?)</a>', tbl.group(1), re.DOTALL)
        docs = { }
        for l, d in r:
            docs[d] = northgatebase % cleanUrl(l)
        return docs

        


def followSiteHistory(detailsurl):
    b = RobustBrowser()
    r = b.robustOpen(detailsurl)
    if not r:
        return {}
    t = r.read()
    m = re.match('.*href="(.*?)".*?>Application Site History</[Aa]>', t, re.DOTALL)
    if m:
        # find all instances of applications
        x = re.findall('<a title="Link to planning application".*?href="(.*?)".*?>(.*?)</a>', b.robustOpen(liverpoolngtempl % cleanUrl(m.group(1))).read(), re.DOTALL)
        apps = { } 
        for l, t in x:
            apps[t] = liverpoolngtempl % cleanUrl(l)
        return apps


def searchAll(street, appnum, dateFrom, dateTo):
    b = RobustBrowser()
    r = search(b=b, siteaddress=street, appnum=appnum, dateStart=dateFrom, dateEnd=dateTo)
    allApps = [ ]
    ipage = 1
    while True:
        allApps.extend(parsePage(r))
        print "records so far: ", len(allApps)

        # next page
        np = re.match('.*<a class=".*?" href="(.*?)">.*<img.*?alt="Go to next page "', r, re.DOTALL)
        if np:
            r = b.robustOpen(liverpoolngtempl % cleanUrl(np.group(1))).read()
            ipage += 1
        else:
            break
    print "records found: ", len(allApps)
    return allApps



def collateApplications(streets, dates, alerts=None):
    print dates
    global bfollowHistory
    stack = [(s, "", "", "") for s in streets] # tuple is "street", "application id", "date from", "date to"
    stack.extend([("", "", d[0], d[1]) for d in dates])
    applications_scraped = {}
    while stack:
        street, appnum, dfrom, dto = stack.pop()
        allApps = searchAll(street, appnum, dfrom, dto)

        for d in allApps:
            if alerts:
                alertdate, alertlocations = alerts
                thisdate = d['Date Registered']
                dm = re.match(".*?(\d+)[/-](\d+)[-/](\d+\d+)", thisdate)
                if dm:
                    day = int(dm.group(1))
                    mnth = int(dm.group(2))
                    year = int(dm.group(3))
                    thisdate = datetime.date(year, mnth, day)
                elif dfrom:
                    thisdate = datetime.date(int(dfrom[6:]), int(dfrom[3:5]), int(dfrom[0:2]))
                else:
                    thisdate = alertdate - datetime.timedelta(1)

                if thisdate >= alertdate:
                    # does the site address contain any of the locations?
                    bfound = False
                    for loc in alertlocations:
                        bfound = bfound or re.search(loc, d['Site Address'], re.DOTALL|re.IGNORECASE)
                    if bfound:
                        message = "%s, New application since: %d-%.2d-%.2d" % (d['Application Number'], alertdate.year, alertdate.month, alertdate.day)
                        print message
                        print d['url']

            docs = relatedDocs(d['url'])
            if debug:
                if docs:    
                    print "%s, docs found: %d" % (d['Application Number'], len(docs.keys()))
                else:
                    print "%s, no related documents found!" % (d['Application Number'])

            if d['Application Number'] in applications_scraped.keys():
                continue # seen this application already

            # save to datastore
            scraperwiki.sqlite.save(unique_keys=['Application Number'], data=d)
            applications_scraped[d['Application Number']] = d['url']
            
            # parse site history
            if bfollowHistory:
                sitehist = followSiteHistory(d['url'])
                if sitehist:
                    for an in sitehist.keys():
                        if an not in applications_scraped.keys():
                            stack.append(("", an, "", ""))
                            applications_scraped[an] = sitehist[an]
    

# day since last run
today = datetime.date.today()
oldday = today - datetime.timedelta(1)

startday = "%.2d/%.2d/%.4d" % (oldday.day, oldday.month, oldday.year)
endday = "%.2d/%.2d/%.4d" % (today.day, today.month, today.year)

bfollowHistory = False
collateApplications([], [(startday, endday)], (oldday, ["[Bb]eaconsfield\s*Street", "[Kk]ingsley\s*[Rr]oad", "[Cc]airns\s*[Ss]treet", "[Jj]ermyn\s*[Ss]treet", "[Gg]ranby\s*[Ss]treet", "[Dd]ucie\s*[Ss]treet"])) # scrape all of the last days

if False:
    import tweepy
    consumer_token = 'gYXj04CFer4Q0u7NmKoYCw'
    consumer_secret = 'zmPLBKmCYia5165A5lzLhLcFBXYMbXDInv10ycLYI'
    auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
    
    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print 'Error! Failed to get request token.'
    
    # Get access token
    try:
        auth.get_access_token("382002263-hcmo2ar4XPD8GYMiSCtvFHClIvu56O2cVFrqT14I")
    except tweepy.TweepError:
        print 'Error! Failed to get access token.'
    
    # Construct the API instance
    api = tweepy.API(auth)

# what needs doing:
# - use sql to save 2nd table with number of docs
# - email when number of docs (or doc content?) changes


import scraperwiki
import mechanize, re
import urllib2
import httplib

import datetime

debug = False # used for debug prints

northgatebase = "http://northgate.liverpool.gov.uk%s"
liverpoolngtempl = northgatebase % "/PlanningExplorer17/Generic/%s"
liverpoolplanning = northgatebase % "/planningexplorer17/"

def cleanUrl(url):
    return url.replace("\t", "").replace("&amp;", "&").replace("&#xD;&#xA;", "").strip().replace(" ", "%20")

class RobustBrowser(mechanize.Browser):
    def __init__(self):
        mechanize.Browser.__init__(self)
        self.set_handle_refresh(False) # can sometimes hang without this 
        self.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')] 
    
    def robustOpen(self, url):
        if debug:
            print "url = ", url
        if type(url) != type("http"):
            assert False
        for i in range(5):
            try:
                return mechanize.Browser.open(self, url)
            except mechanize.URLError:
                if True:
                    print "Failed: %d" % i, url




def search(b=None, siteaddress="", appnum="", dateStart="", dateEnd=""):
    # the search is slow, Julian thinks I should scrape 'all' applications and then filter these.
    if not b:
        b = RobustBrowser()
    assert b
    b.robustOpen(liverpoolplanning)    
    def submit():
        try:
            b.select_form(nr=0)
            b.form["txtSiteAddress"] = siteaddress
            b.form["txtApplicationNumber"] = appnum
            if dateStart:
                if debug:
                    print "dates: ", dateStart, dateEnd
                b.form["dateStart"] = dateStart
                b.form["dateEnd"] = dateEnd or dateStart # would this search for one specific date?
                b.form["rbGroup"] = ["rbRange"]
                # search for date registered. 
                # Other options are: "DATE_RECEIVED", "DATE_VALID", "DATE_TARGET", "DATE_TO_COMMITTEE", "DATE_DECISION"
                b.form["cboSelectDateValue"] = ["DATE_REGISTERED"] 
            b.submit()
            return True
        except (urllib2.HTTPError, mechanize.URLError):
            return False

        except httplib.BadStatusLine as e:
            print "Exception = ", str(e)
            raise e
        
        except mechanize.FormNotFoundError as e:
            if debug:
                print b.read()
            raise e
        
    for i in range(3):
        success = submit()
        if success:
            break

    if success:
        return b.response().read()
    else:
        if debug:
            print "Form submission failed 3 times!!!"

def parsePage(r):
    if re.match('.*No Records Found.', r, re.DOTALL):
        return []
    
    m = re.match('.*<table .*? summary="Results of the Search" .*?>(.*?)</table>', r, re.DOTALL)
    t = m.group(1)
    rows = re.findall('<tr class=\"Row\d*?.*?>(.*?)</tr>', t, re.DOTALL)
    
    # row 0 has names of columns
    colnames = re.findall('<th .*?>(.*?)</th>', rows[0], re.DOTALL)   
    allPlans = [ ]
    for a in rows[1:]:
        values = re.findall('<td .*?>(.*?)</td>', a, re.DOTALL)
    
        # first value also contains a url
        m = re.match('.*?href="(.*?)">(.*?)</a>', values[0], re.DOTALL)
    
        # zip up into dict
        d = dict(zip(colnames[1:], values[1:]))
        d[colnames[0]] = m.group(2)
        
        # filter out all sorts of crap, from tabs to CR/LF...
        d['url'] = liverpoolngtempl % cleanUrl(m.group(1))    
        allPlans.append(d)
    return allPlans
    
    
def relatedDocs(detailsurl):
    b = RobustBrowser()
    b.set_handle_robots(False)
    r = b.robustOpen(detailsurl)
    t = r.read()
    m = re.match('.*href="(.*?)".*?>Related Documents</[Aa]>', t, re.DOTALL)
    if m:
        docsurl = northgatebase % cleanUrl(m.group(1))
        dd = b.robustOpen(docsurl)
        if not dd:
            return {}

        d = dd.read()
        tbl = re.match('.*?<table.*?>(.*?)</table>', d, re.DOTALL)

        if not tbl:
            if debug:
                print "no docs? docsurl = ", docsurl
            return

        # find all anchors
        r = re.findall('<a href="(.*?)">(.*?)</a>', tbl.group(1), re.DOTALL)
        docs = { }
        for l, d in r:
            docs[d] = northgatebase % cleanUrl(l)
        return docs

        


def followSiteHistory(detailsurl):
    b = RobustBrowser()
    r = b.robustOpen(detailsurl)
    if not r:
        return {}
    t = r.read()
    m = re.match('.*href="(.*?)".*?>Application Site History</[Aa]>', t, re.DOTALL)
    if m:
        # find all instances of applications
        x = re.findall('<a title="Link to planning application".*?href="(.*?)".*?>(.*?)</a>', b.robustOpen(liverpoolngtempl % cleanUrl(m.group(1))).read(), re.DOTALL)
        apps = { } 
        for l, t in x:
            apps[t] = liverpoolngtempl % cleanUrl(l)
        return apps


def searchAll(street, appnum, dateFrom, dateTo):
    b = RobustBrowser()
    r = search(b=b, siteaddress=street, appnum=appnum, dateStart=dateFrom, dateEnd=dateTo)
    allApps = [ ]
    ipage = 1
    while True:
        allApps.extend(parsePage(r))
        print "records so far: ", len(allApps)

        # next page
        np = re.match('.*<a class=".*?" href="(.*?)">.*<img.*?alt="Go to next page "', r, re.DOTALL)
        if np:
            r = b.robustOpen(liverpoolngtempl % cleanUrl(np.group(1))).read()
            ipage += 1
        else:
            break
    print "records found: ", len(allApps)
    return allApps



def collateApplications(streets, dates, alerts=None):
    print dates
    global bfollowHistory
    stack = [(s, "", "", "") for s in streets] # tuple is "street", "application id", "date from", "date to"
    stack.extend([("", "", d[0], d[1]) for d in dates])
    applications_scraped = {}
    while stack:
        street, appnum, dfrom, dto = stack.pop()
        allApps = searchAll(street, appnum, dfrom, dto)

        for d in allApps:
            if alerts:
                alertdate, alertlocations = alerts
                thisdate = d['Date Registered']
                dm = re.match(".*?(\d+)[/-](\d+)[-/](\d+\d+)", thisdate)
                if dm:
                    day = int(dm.group(1))
                    mnth = int(dm.group(2))
                    year = int(dm.group(3))
                    thisdate = datetime.date(year, mnth, day)
                elif dfrom:
                    thisdate = datetime.date(int(dfrom[6:]), int(dfrom[3:5]), int(dfrom[0:2]))
                else:
                    thisdate = alertdate - datetime.timedelta(1)

                if thisdate >= alertdate:
                    # does the site address contain any of the locations?
                    bfound = False
                    for loc in alertlocations:
                        bfound = bfound or re.search(loc, d['Site Address'], re.DOTALL|re.IGNORECASE)
                    if bfound:
                        message = "%s, New application since: %d-%.2d-%.2d" % (d['Application Number'], alertdate.year, alertdate.month, alertdate.day)
                        print message
                        print d['url']

            docs = relatedDocs(d['url'])
            if debug:
                if docs:    
                    print "%s, docs found: %d" % (d['Application Number'], len(docs.keys()))
                else:
                    print "%s, no related documents found!" % (d['Application Number'])

            if d['Application Number'] in applications_scraped.keys():
                continue # seen this application already

            # save to datastore
            scraperwiki.sqlite.save(unique_keys=['Application Number'], data=d)
            applications_scraped[d['Application Number']] = d['url']
            
            # parse site history
            if bfollowHistory:
                sitehist = followSiteHistory(d['url'])
                if sitehist:
                    for an in sitehist.keys():
                        if an not in applications_scraped.keys():
                            stack.append(("", an, "", ""))
                            applications_scraped[an] = sitehist[an]
    

# day since last run
today = datetime.date.today()
oldday = today - datetime.timedelta(1)

startday = "%.2d/%.2d/%.4d" % (oldday.day, oldday.month, oldday.year)
endday = "%.2d/%.2d/%.4d" % (today.day, today.month, today.year)

bfollowHistory = False
collateApplications([], [(startday, endday)], (oldday, ["[Bb]eaconsfield\s*Street", "[Kk]ingsley\s*[Rr]oad", "[Cc]airns\s*[Ss]treet", "[Jj]ermyn\s*[Ss]treet", "[Gg]ranby\s*[Ss]treet", "[Dd]ucie\s*[Ss]treet"])) # scrape all of the last days

if False:
    import tweepy
    consumer_token = 'gYXj04CFer4Q0u7NmKoYCw'
    consumer_secret = 'zmPLBKmCYia5165A5lzLhLcFBXYMbXDInv10ycLYI'
    auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
    
    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print 'Error! Failed to get request token.'
    
    # Get access token
    try:
        auth.get_access_token("382002263-hcmo2ar4XPD8GYMiSCtvFHClIvu56O2cVFrqT14I")
    except tweepy.TweepError:
        print 'Error! Failed to get access token.'
    
    # Construct the API instance
    api = tweepy.API(auth)

