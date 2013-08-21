import scraperwiki
import lxml.html
import re
import dateutil.parser
import datetime


# Scrape EA Impoundment License Applications
#
# Notices of Licence Applications to Abstract or Impound water (index)
# http://www.environment-agency.gov.uk/research/library/consultations/65549.aspx
#
# Applications for full licences to abstract or impound water *
# http://www.environment-agency.gov.uk/research/library/consultations/65560.aspx
#
# Applications to vary or revoke existing licences to abstract or impound water
# http://www.environment-agency.gov.uk/research/library/consultations/65558.aspx
#
# Licensing Decision Statements
# http://www.environment-agency.gov.uk/research/library/consultations/65551.aspx
#
def parseDecidedApplications(url):
    html = scraperwiki.scrape(url)
    apps = lxml.html.fromstring(html)
    for app in apps.cssselect("ul[id='highlights'] li"):
        try:
            appAnchor = safeXPath(app.cssselect("a"), 0)
            appHref = safeXPath(appAnchor.xpath("@href"), 0)
            appTitle = safeXPath(appAnchor.xpath("@title"), 0)

            appPara = safeXPath(app.cssselect("p"), 0)
            try:
                appAddress = safeXPath(appPara.xpath("text()"), 0)
            except:
                appAddress = appPara

            print "link=",appHref," title=",appTitle, "address=",appAddress ;
            #parseAppDetail(appTitle, appAddress, baseURL+appHref, "decided")

        except IndexError as ex:
            print u"parseDecidedApplications: err={1}: url={0} app={2}".format(url, str(ex), app)


def parseNewApplications(url):
    html = scraperwiki.scrape(url)
    apps = lxml.html.fromstring(html)
    for app in apps.cssselect("ul[id='highlights'] li"):
        try:
            appAnchor = safeXPath(app.cssselect("a"), 0)
            appHref = safeXPath(appAnchor.xpath("@href"), 0)
            appTitle = safeXPath(appAnchor.xpath("@title"), 0)

            appPara = safeXPath(app.cssselect("p"), 0)
            appDescr = safeXPath(appPara.xpath("text()"), 0)

            # print "link=",appHref," title=",appTitle, "descr=",appDescr;
            parseAppDetail(appTitle, appDescr, baseURL+appHref, "new")

        except IndexError as ex:
            print "parseNewApplications: ex={1}: url={0} app={2}".format(url, str(ex), app)


def safeXPath(xpath, index):
    try :
        return xpath[index];
    except IndexError as ex:
        print "safeXpath: ex={2}: xpath={0} index={1}".format(xpath, index, str(ex))
    return ""


def parseAppDetail(applicant, appDescr, appUrl, appState):

    appClosingDate = None;
    appPlaceName = None
    appAddress = None;

    appIdRE = re.compile(".*/(\d+)\.aspx$", re.I)
    match = appIdRE.match(appUrl)
    if (match == None):
        print "NO MATCH for ID in",appUrl
        return
    appId = match.group(1)

    today = datetime.date.today()
    appRow = {"appid":appId, "scrape_date":today, "applicant":applicant, "url":appUrl, "state":appState}

    html = scraperwiki.scrape(appUrl)
    parsed = lxml.html.fromstring(html)
    content = parsed.cssselect("div[id='content']")
    contentText = content[0].text_content()

    if (re.search("(hydropower|hydro.*electric)", contentText, re.I) != None):
        appRow["hydroelectric"] = True

    intro = content[0].cssselect("p[class='intro']")
    introText = intro[0].text_content()
    introRE = re.compile("Closin. date.*:\s*(\d{1,2}\s+\w+\s+\d{2,4})\.+\s+(.*)\s+(at|between)", re.I)
    match = introRE.match(introText)
    if (match == None):
        print "NO MATCH! line=",introText
        return

    if (match.group(1) != None):
        appClosingDate = dateutil.parser.parse( match.group(1) )
        appRow["closing_date"] = appClosingDate.date()

    if (match.group(2) != None):
        appSiteName = match.group(2)
        appRow["site_name"] = appSiteName

    print u"parseAppDetail: {2}\n"\
          "    id: {4}    state: {3}    startDate: {5}    closeDate: {6}\n"\
          "    who: {0}\n    site: {7}\n    description: {1}".format(
        applicant, appDescr, appUrl, appState, 
        appRow["appid"], appRow["scrape_date"], appRow["closing_date"], appRow["site_name"])

    existingRow = scraperwiki.sqlite.execute('select * from licence_applications WHERE appid=?', [ appRow['appid'] ]);
    if (existingRow == None):
        scraperwiki.sqlite.save(unique_keys = ["appid"], 
                                data = appRow,
                                table_name = "licence_applications",
                                verbose = 2)

        locationRE = re.compile("([A-Z]{2}\s+[0-9]+\s+[0-9]+)", re.I)
        locId = 0
        for locMatch in locationRE .finditer(introText):
            loc = locMatch.group(1)
            lng, lat = scraperwiki.geo.osgb_to_lonlat(loc)
            locId = locId + 1
            scraperwiki.sqlite.save(unique_keys = ["appid", "locid"],
                                    data = {"appid":appId, "locid":locId, "location":loc, "lat":lat, "lng":lng },
                                    table_name = "licence_locations",
                                    verbose = 2)



baseURL = "http://www.environment-agency.gov.uk"
parseNewApplications(baseURL+"/research/library/consultations/65560.aspx")
parseDecidedApplications(baseURL+"/research/library/consultations/65551.aspx")
