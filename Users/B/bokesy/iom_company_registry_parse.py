import scraperwiki
import lxml.html
import urllib2
import datetime
import re

#
possibletitles = set(['Isle of Man Company Details', 'Foreign Company Details', 'New Manx Vehicle Details', 'LLC Company Details', 'Business Name Details', 
                      'Previous Names', 'Liquidators/receivers appointed', 'Registered Agent Details', 'Additional Information'])


def brtotext(el):
    res = [ el.text ]
    for br in el:
        assert br.tag == 'br'
        res.append(br.tail)
    return "; ".join(res)
#TODO:
##need to figure out strip of extra spaces from here
#also need to check for postcodes at some point

def convdate(sdate):
    if not sdate:
        return None
    mdate = re.match("(\d\d)/(\d\d)/(\d\d\d\d)$", sdate)
#    print mdate
    return datetime.date(int(mdate.group(3)), int(mdate.group(2)), int(mdate.group(1)))


def Parse(number, code, html):
    root = lxml.html.fromstring(html)
    tables = root.cssselect("table")
    companyno = "%06d%s" % (number, code)

    for table in tables:
        rows = table.cssselect("tr")
        th = rows[0].cssselect("th")
        assert 1 <= len(th) <= 2, html
        if len(th[0]) == 1:
            title = th[0][0].text.strip()
        else:
            title = th[0].text.strip()
        assert title in possibletitles, html


# only look at company details (deal with the other tables later)
#
# TODO: Need a list of the other tables expected
# Company Tables: "Isle of Man Company Details", "New Manx Vehicle Details",  "Foreign Company Details", "Business Name Details", "LLC Company Details", 
# Other Tables: "Previous Names", "Registered Agent Details", "Liquidators/receivers appointed", "Additional Information"
#
        if not re.search("Company Details", title):
#        if not re.search("Business Name", title):
#        if not re.search("New Manx", title):
            return

        data = { }
        for row in rows[1:]:
            assert (len(row) == 2 and row[0].tag == "th" and row[1].tag == "td"), lxml.html.tostring(row)
# get rid of spaces and slashes from key
            key = re.sub("[ \/]", "", row[0].text.strip())
# Urgh problem here, for Business Names table There is a Number instead of a CompanyNumber - need to figure out how to deal with that    
            assert key in ['Status', 'CompanyName', 'DateRegistrationCancelled', 'RegisteredOffice', 'DateofRegistration', 
                           'PresenceofCharges', 'CompanyNumber', 'PlaceofRegistration', 'PlaceofBusiness', 'CompanyType', 
                           'DateofIncorporation', 'DateCompanyDissolved', 'DateRegistratonCancelled', 'BusinessName', 
                           'Number', 'LiquidatorReceiverappointed', 'DateDissolved' ], (key, title)
            print data
            val = brtotext(row[1]).strip()
            if val:
                if key[:4] == "Date":
                    val = convdate(val)
                data[key] = val
        
        scraperwiki.sqlite.save(unique_keys=["CompanyNumber"], data=data)


def MainParse():
    rows = scraperwiki.sqlite.attach("iom_company_registry", "src")
    rows = scraperwiki.sqlite.select("number, code, html from src.otable where code = 'C'")
    for row in rows:
        Parse(row["number"], row["code"], row["html"])


MainParse()
import scraperwiki
import lxml.html
import urllib2
import datetime
import re

#
possibletitles = set(['Isle of Man Company Details', 'Foreign Company Details', 'New Manx Vehicle Details', 'LLC Company Details', 'Business Name Details', 
                      'Previous Names', 'Liquidators/receivers appointed', 'Registered Agent Details', 'Additional Information'])


def brtotext(el):
    res = [ el.text ]
    for br in el:
        assert br.tag == 'br'
        res.append(br.tail)
    return "; ".join(res)
#TODO:
##need to figure out strip of extra spaces from here
#also need to check for postcodes at some point

def convdate(sdate):
    if not sdate:
        return None
    mdate = re.match("(\d\d)/(\d\d)/(\d\d\d\d)$", sdate)
#    print mdate
    return datetime.date(int(mdate.group(3)), int(mdate.group(2)), int(mdate.group(1)))


def Parse(number, code, html):
    root = lxml.html.fromstring(html)
    tables = root.cssselect("table")
    companyno = "%06d%s" % (number, code)

    for table in tables:
        rows = table.cssselect("tr")
        th = rows[0].cssselect("th")
        assert 1 <= len(th) <= 2, html
        if len(th[0]) == 1:
            title = th[0][0].text.strip()
        else:
            title = th[0].text.strip()
        assert title in possibletitles, html


# only look at company details (deal with the other tables later)
#
# TODO: Need a list of the other tables expected
# Company Tables: "Isle of Man Company Details", "New Manx Vehicle Details",  "Foreign Company Details", "Business Name Details", "LLC Company Details", 
# Other Tables: "Previous Names", "Registered Agent Details", "Liquidators/receivers appointed", "Additional Information"
#
        if not re.search("Company Details", title):
#        if not re.search("Business Name", title):
#        if not re.search("New Manx", title):
            return

        data = { }
        for row in rows[1:]:
            assert (len(row) == 2 and row[0].tag == "th" and row[1].tag == "td"), lxml.html.tostring(row)
# get rid of spaces and slashes from key
            key = re.sub("[ \/]", "", row[0].text.strip())
# Urgh problem here, for Business Names table There is a Number instead of a CompanyNumber - need to figure out how to deal with that    
            assert key in ['Status', 'CompanyName', 'DateRegistrationCancelled', 'RegisteredOffice', 'DateofRegistration', 
                           'PresenceofCharges', 'CompanyNumber', 'PlaceofRegistration', 'PlaceofBusiness', 'CompanyType', 
                           'DateofIncorporation', 'DateCompanyDissolved', 'DateRegistratonCancelled', 'BusinessName', 
                           'Number', 'LiquidatorReceiverappointed', 'DateDissolved' ], (key, title)
            print data
            val = brtotext(row[1]).strip()
            if val:
                if key[:4] == "Date":
                    val = convdate(val)
                data[key] = val
        
        scraperwiki.sqlite.save(unique_keys=["CompanyNumber"], data=data)


def MainParse():
    rows = scraperwiki.sqlite.attach("iom_company_registry", "src")
    rows = scraperwiki.sqlite.select("number, code, html from src.otable where code = 'C'")
    for row in rows:
        Parse(row["number"], row["code"], row["html"])


MainParse()
