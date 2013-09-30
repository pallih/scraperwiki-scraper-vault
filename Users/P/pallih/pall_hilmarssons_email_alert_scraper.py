
# PLEASE READ THIS BEFORE EDITING
#
# This script generates your email alerts, to tell you when your scrapers
# are broken or someone has edited them.
#
# It works by emailing you the output of this script. If you read the code and
# know what you're doing, you can customise it, and make it send other emails
# for other purposes.

import scraperwiki
import datetime
import urllib
import lxml.html
emaillibrary = scraperwiki.utils.swimport("general-emails-on-scrapers")
subjectline, headerlines, bodylines, footerlines = emaillibrary.EmailMessageParts()


weatherlines = [ ]
if datetime.date.today().weekday() == 0:
    #url = "http://www.metoffice.gov.uk/weather/uk/wl/holyhead_forecast_weather.html"
    #url = "http://www.metoffice.gov.uk/loutdoor/mountainsafety/westhighland/westhighland_forecast_weather.html"
    url = "http://www.metoffice.gov.uk/loutdoor/mountainsafety/westhighland/westhighland_forecast_print.html"
    html = urllib.urlopen(url).read()
    root = lxml.html.fromstring(html)
    rows = root.cssselect("div.section div.section")
   
    # rows = root.cssselect("div.tableWrapper table tr")
    for row in rows:
        #print lxml.html.tostring(row)
        metweatherline = row.text_content().strip()
        if metweatherline[:3] == "Mon":
            subjectline += " With added weather"
            weatherlines.append("*** Weather warning for the weekend:")
            weatherlines.append("   " + metweatherline)
            weatherlines.append("")

print weatherlines

exit()
if bodylines or weatherlines:
    if not bodylines:
        headerlines, footerlines = [ ], [ ]   # kill off cruft surrounding no message
    print "\n".join([subjectline] + weatherlines + headerlines + bodylines + footerlines)
#else:
#    print "nothing to email you about"


# PLEASE READ THIS BEFORE EDITING
#
# This script generates your email alerts, to tell you when your scrapers
# are broken or someone has edited them.
#
# It works by emailing you the output of this script. If you read the code and
# know what you're doing, you can customise it, and make it send other emails
# for other purposes.

import scraperwiki
import datetime
import urllib
import lxml.html
emaillibrary = scraperwiki.utils.swimport("general-emails-on-scrapers")
subjectline, headerlines, bodylines, footerlines = emaillibrary.EmailMessageParts()


weatherlines = [ ]
if datetime.date.today().weekday() == 0:
    #url = "http://www.metoffice.gov.uk/weather/uk/wl/holyhead_forecast_weather.html"
    #url = "http://www.metoffice.gov.uk/loutdoor/mountainsafety/westhighland/westhighland_forecast_weather.html"
    url = "http://www.metoffice.gov.uk/loutdoor/mountainsafety/westhighland/westhighland_forecast_print.html"
    html = urllib.urlopen(url).read()
    root = lxml.html.fromstring(html)
    rows = root.cssselect("div.section div.section")
   
    # rows = root.cssselect("div.tableWrapper table tr")
    for row in rows:
        #print lxml.html.tostring(row)
        metweatherline = row.text_content().strip()
        if metweatherline[:3] == "Mon":
            subjectline += " With added weather"
            weatherlines.append("*** Weather warning for the weekend:")
            weatherlines.append("   " + metweatherline)
            weatherlines.append("")

print weatherlines

exit()
if bodylines or weatherlines:
    if not bodylines:
        headerlines, footerlines = [ ], [ ]   # kill off cruft surrounding no message
    print "\n".join([subjectline] + weatherlines + headerlines + bodylines + footerlines)
#else:
#    print "nothing to email you about"

