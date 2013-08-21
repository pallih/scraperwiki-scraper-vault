import scraperwiki
import lxml.html
import urllib
import datetime


emaillibrary = scraperwiki.utils.swimport("general-emails-on-scrapers")
subjectline, headerlines, bodylines, footerlines = emaillibrary.EmailMessageParts("onlyexceptions")

weatherlines = [ ]
if datetime.date.today().weekday() == 2:
    url = "http://www.metoffice.gov.uk/weather/uk/wl/holyhead_forecast_weather.html"
    html = urllib.urlopen(url).read()
    root = lxml.html.fromstring(html)
    rows = root.cssselect("div.tableWrapper table tr")
    for row in rows:
        #print lxml.html.tostring(row)
        metweatherline = row.text_content().strip()
        if metweatherline[:3] == "Sat":
            subjectline += " With added weather"
            weatherlines.append("*** Weather warning for the weekend:")
            weatherlines.append("   " + metweatherline)
            weatherlines.append("")


if bodylines or weatherlines:
    if not bodylines:
        headerlines, footerlines = [ ], [ ]   # kill off cruft surrounding no message
    print "\n".join([subjectline] + weatherlines + headerlines + bodylines + footerlines)
#else:
#    print "nothing to email you about"
import scraperwiki
import lxml.html
import urllib
import datetime


emaillibrary = scraperwiki.utils.swimport("general-emails-on-scrapers")
subjectline, headerlines, bodylines, footerlines = emaillibrary.EmailMessageParts("onlyexceptions")

weatherlines = [ ]
if datetime.date.today().weekday() == 2:
    url = "http://www.metoffice.gov.uk/weather/uk/wl/holyhead_forecast_weather.html"
    html = urllib.urlopen(url).read()
    root = lxml.html.fromstring(html)
    rows = root.cssselect("div.tableWrapper table tr")
    for row in rows:
        #print lxml.html.tostring(row)
        metweatherline = row.text_content().strip()
        if metweatherline[:3] == "Sat":
            subjectline += " With added weather"
            weatherlines.append("*** Weather warning for the weekend:")
            weatherlines.append("   " + metweatherline)
            weatherlines.append("")


if bodylines or weatherlines:
    if not bodylines:
        headerlines, footerlines = [ ], [ ]   # kill off cruft surrounding no message
    print "\n".join([subjectline] + weatherlines + headerlines + bodylines + footerlines)
#else:
#    print "nothing to email you about"
import scraperwiki
import lxml.html
import urllib
import datetime


emaillibrary = scraperwiki.utils.swimport("general-emails-on-scrapers")
subjectline, headerlines, bodylines, footerlines = emaillibrary.EmailMessageParts("onlyexceptions")

weatherlines = [ ]
if datetime.date.today().weekday() == 2:
    url = "http://www.metoffice.gov.uk/weather/uk/wl/holyhead_forecast_weather.html"
    html = urllib.urlopen(url).read()
    root = lxml.html.fromstring(html)
    rows = root.cssselect("div.tableWrapper table tr")
    for row in rows:
        #print lxml.html.tostring(row)
        metweatherline = row.text_content().strip()
        if metweatherline[:3] == "Sat":
            subjectline += " With added weather"
            weatherlines.append("*** Weather warning for the weekend:")
            weatherlines.append("   " + metweatherline)
            weatherlines.append("")


if bodylines or weatherlines:
    if not bodylines:
        headerlines, footerlines = [ ], [ ]   # kill off cruft surrounding no message
    print "\n".join([subjectline] + weatherlines + headerlines + bodylines + footerlines)
#else:
#    print "nothing to email you about"
import scraperwiki
import lxml.html
import urllib
import datetime


emaillibrary = scraperwiki.utils.swimport("general-emails-on-scrapers")
subjectline, headerlines, bodylines, footerlines = emaillibrary.EmailMessageParts("onlyexceptions")

weatherlines = [ ]
if datetime.date.today().weekday() == 2:
    url = "http://www.metoffice.gov.uk/weather/uk/wl/holyhead_forecast_weather.html"
    html = urllib.urlopen(url).read()
    root = lxml.html.fromstring(html)
    rows = root.cssselect("div.tableWrapper table tr")
    for row in rows:
        #print lxml.html.tostring(row)
        metweatherline = row.text_content().strip()
        if metweatherline[:3] == "Sat":
            subjectline += " With added weather"
            weatherlines.append("*** Weather warning for the weekend:")
            weatherlines.append("   " + metweatherline)
            weatherlines.append("")


if bodylines or weatherlines:
    if not bodylines:
        headerlines, footerlines = [ ], [ ]   # kill off cruft surrounding no message
    print "\n".join([subjectline] + weatherlines + headerlines + bodylines + footerlines)
#else:
#    print "nothing to email you about"
import scraperwiki
import lxml.html
import urllib
import datetime


emaillibrary = scraperwiki.utils.swimport("general-emails-on-scrapers")
subjectline, headerlines, bodylines, footerlines = emaillibrary.EmailMessageParts("onlyexceptions")

weatherlines = [ ]
if datetime.date.today().weekday() == 2:
    url = "http://www.metoffice.gov.uk/weather/uk/wl/holyhead_forecast_weather.html"
    html = urllib.urlopen(url).read()
    root = lxml.html.fromstring(html)
    rows = root.cssselect("div.tableWrapper table tr")
    for row in rows:
        #print lxml.html.tostring(row)
        metweatherline = row.text_content().strip()
        if metweatherline[:3] == "Sat":
            subjectline += " With added weather"
            weatherlines.append("*** Weather warning for the weekend:")
            weatherlines.append("   " + metweatherline)
            weatherlines.append("")


if bodylines or weatherlines:
    if not bodylines:
        headerlines, footerlines = [ ], [ ]   # kill off cruft surrounding no message
    print "\n".join([subjectline] + weatherlines + headerlines + bodylines + footerlines)
#else:
#    print "nothing to email you about"
