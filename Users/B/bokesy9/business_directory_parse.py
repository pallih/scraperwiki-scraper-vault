# Blank Python
import scraperwiki
import lxml.html
import lxml
import urllib2
import datetime
import re


possibletitles = set(['Class: Estate Agents'])


def brtotext(el):
    res = [ el.text ]
    for br in el:
        assert br.tag == 'br'
        res.append(br.tail)
    return "; ".join(res)
#TODO:
#need to figure out strip of extra spaces from here
#also need to check for postcodes at some point

def convdate(sdate):
    if not sdate:
        return None
    mdate = re.match("(\d\d)/(\d\d)/(\d\d\d\d)$", sdate)
    return datetime.date(int(mdate.group(3)), int(mdate.group(2)), int(mdate.group(1)))


def Parse(url, html):
#def Parse(number, code, html):
    root = lxml.html.fromstring(html)
    divs = root.cssselect("div")
#    companyno = "%06d%s" % (number, code)

    for div in divs:
        rows = div.cssselect("div#enhanced")
        h2 = rows[0].cssselect("tag#h2")
        assert 1 <= len(h2) <= 2, html
        if len(h2[0]) == 1:
            title = h2[0][0].text.strip()
        else:
            title = h2[0].text.strip()
        assert title in possibletitles, html
    print title
#    root = lxml.html.fromstring(html)
#    divs = root.cssselect(["div#hplattop","div#standard-entry"])
#    divs = root.cssselect("div#hplattop")
    #print divs
    #companyno = "%06d%s" % (number, code)

#    for div in divs:
#        rows = div.cssselect("enhanced")
#        x += 1
#        print x
#        h2 = rows[0].cssselect("h2")
#        assert 1 <= len(h2) <= 2, html
#        if len(h2[0]) == 1:
#            title = h2[0][0].text.strip()
#        else:
#            title = h2[0].text.strip()
#        assert title in possibletitles, html

    




# only look at company details (deal with the other tables later)
#
# TODO: Need a list of the other tables expected
# Company Tables: "Isle of Man Company Details", "New Manx Vehicle Details",  "Foreign Company Details", "Business Name Details", "LLC Company Details", 
# Other Tables: "Previous Names", "Registered Agent Details", "Liquidators/receivers appointed", "Additional Information"
#
#        if not re.search("Class:", title):
#        if not re.search("Business Name", title):
#        if not re.search("New Manx", title):
#           return
#        print title
#        data = { }
#        for row in rows[1:]:
#            assert (len(row) == 2 and row[0].tag == "th" and row[1].tag == "td"), lxml.html.tostring(row)
# get rid of spaces and slashes from key
#            key = re.sub("[ \/]", "", row[0].text.strip())
# Urgh problem here, for Business Names table There is a Number instead of a CompanyNumber - need to figure out how to deal with that    
#            assert key in ['Status', 'CompanyName', 'DateRegistrationCancelled', 'RegisteredOffice', 'DateofRegistration', 
#                           'PresenceofCharges', 'CompanyNumber', 'PlaceofRegistration', 'PlaceofBusiness', 'CompanyType', 
#                           'DateofIncorporation', 'DateCompanyDissolved', 'DateRegistratonCancelled', 'BusinessName', 
#                           'Number', 'LiquidatorReceiverappointed', 'DateDissolved' ], (key, title)
#            val = brtotext(row[1]).strip()
#            if val:
#                if key[:4] == "Date":
#                    val = convdate(val)
#                data[key] = val
#
#        assert data["CompanyNumber"] == companyno, data
# 
#        scraperwiki.sqlite.save(unique_keys=["CompanyNumber"], data=data)


def MainParse():
    rows = scraperwiki.sqlite.attach("business_directory", "src")
    rows = scraperwiki.sqlite.select("url, html from src.initial")
    for row in rows:
        Parse(row["url"], row["html"])


MainParse()
