import scraperwiki
import urllib2, urlparse
import lxml.html
import re
import time

#Get a page and check for msql request errors using regex
def GetPage(url):
    for n in range(4):
        html = urllib2.urlopen(url).read()
        if not re.search("mysql_connect\(\)",html):
            return html
        print "Retrying attempt", n, url
        time.sleep(n+1)
    assert False, ("Failed to read", url)

#Create a database containing society info
def GetSocNames():
    print "Getting list of societies... ",
    url = "http://www.ubu.org.uk/activities/societies/"
    html = GetPage(url)
    root = lxml.html.fromstring(html)
    area = root.cssselect("div ul li a.msl-gl-link")
    socurls = [ (urlparse.urljoin(url, a.attrib.get("href")), a.text.strip())  for a in area ]
    print "Done"
    print "Exploring society pages for data... "
    socdata=[]
    for soc in range(len(socurls)):
        socdict = {}
        socdict["Society UBU URL"], socdict["Society Name"] = socurls[soc]
        sochtml = GetPage(socdict["Society UBU URL"])
        socroot = lxml.html.fromstring(sochtml)
        try:
            socdict["Society Website"] = socroot.cssselect("a.msl_web")[0].text.strip()
        except Exception, e:
            print "No external website found for:", socdict["Society Name"],"on listing at:",socdict["Society UBU URL"],e
        try:
            socdict["Owner Email"] = socroot.cssselect("a.msl_email")[0].text.strip()
        except Exception, e:
            print "No email found for:", socdict["Society Name"],"on listing at:",socdict["Society UBU URL"],e

        socdata.append(socdict)
    print "Done"
    print "Deleting old database...",
    scraperwiki.sqlite.execute("DROP table if exists soclist")
    print "Done!"
    print "Writing to database:"
    scraperwiki.sqlite.save(["Society Name"], socdata, "soclist")
    print "Write Done!"

def GetSportNames():
    print "Getting list of sports teams... ",
    url = "http://www.ubu.org.uk/activities/sports/clubs/"
    html = GetPage(url)
    root = lxml.html.fromstring(html)
    area = root.cssselect("div ul li a.msl-gl-link")
    socurls = [ (urlparse.urljoin(url, a.attrib.get("href")), a.text.strip())  for a in area ]
    print "Done"
    print "Exploring team pages for data... "
    socdata=[]
    for soc in range(len(socurls)):
        socdict = {}
        socdict["Society UBU URL"], socdict["Society Name"] = socurls[soc]
        sochtml = GetPage(socdict["Society UBU URL"])
        socroot = lxml.html.fromstring(sochtml)
        try:
            socdict["Society Website"] = socroot.cssselect("a.msl_web")[0].text.strip()
        except Exception, e:
            print "No external website found for:", socdict["Society Name"],"on listing at:",socdict["Society UBU URL"],e
        try:
            socdict["Owner Email"] = socroot.cssselect("a.msl_email")[0].text.strip()
        except Exception, e:
            print "No email found for:", socdict["Society Name"],"on listing at:",socdict["Society UBU URL"],e

        socdata.append(socdict)
    print "Done"
    print "Writing to database:"
    scraperwiki.sqlite.save(["Society Name"], socdata, "soclist")
    print "Write Done!"

#generate a mailstring from our database
def GetMailString():
    odata = scraperwiki.sqlite.execute("select * from soclist")
    print "Generating Mailstring"
    maillist = []
    for soc in range(len(odata["data"])):
        cdata = odata["data"][soc]
        if cdata[2] and cdata[2] not in maillist:
            maillist.append(cdata[2])
    mailstring = "; ".join(maillist)
    print "Mailstring is:",mailstring

#Main
#GetSocNames()
#GetSportNames()
GetMailString()