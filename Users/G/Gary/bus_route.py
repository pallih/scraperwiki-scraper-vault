import scraperwiki
import mechanize
import re
import urlparse
import lxml.html


# ASPX pages are some of the hardest challenges because they use javascript and forms to navigate
# Almost always the links go through the function function __doPostBack(eventTarget, eventArgument)
# which you have to simulate in the mechanize form handling library

# This example shows how to follow the Next page link

url3 = 'http://placr.mobi/timetable?u=bus%2Fuk%2Fstop%2F2800S41209A'
br3 = mechanize.Browser()

    # sometimes the server is sensitive to this information
br3.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
response3 = br3.open(url3)


html3 = response3.read()
jobtitlemonster = re.findall('<td>(.*?)</td>', html3)
print jobtitlemonster

times = jobtitlemonster[1], jobtitlemonster[5], jobtitlemonster[9]
print times

destination = jobtitlemonster[3], jobtitlemonster[7], jobtitlemonster[11]
print destination



#scraperwiki.sqlite.execute("delete from swdata")

record = {}
record['Time'] = times[0]
record['Destination'] = destination[0]
print record, '------------'
scraperwiki.sqlite.save(["Time"], record)
record['Time'] = times[1]
record['Destination'] = destination[1]

# Print out the data we've gathered
print record, '------------'
# Finally, save the record to the datastore - 'Artist' is our unique key
scraperwiki.sqlite.save(["Time"], record)

record['Time'] = times[2]
record['Destination'] = destination[2]
print record, '------------'
scraperwiki.sqlite.save(["Time"], record)
import scraperwiki
import mechanize
import re
import urlparse
import lxml.html


# ASPX pages are some of the hardest challenges because they use javascript and forms to navigate
# Almost always the links go through the function function __doPostBack(eventTarget, eventArgument)
# which you have to simulate in the mechanize form handling library

# This example shows how to follow the Next page link

url3 = 'http://placr.mobi/timetable?u=bus%2Fuk%2Fstop%2F2800S41209A'
br3 = mechanize.Browser()

    # sometimes the server is sensitive to this information
br3.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
response3 = br3.open(url3)


html3 = response3.read()
jobtitlemonster = re.findall('<td>(.*?)</td>', html3)
print jobtitlemonster

times = jobtitlemonster[1], jobtitlemonster[5], jobtitlemonster[9]
print times

destination = jobtitlemonster[3], jobtitlemonster[7], jobtitlemonster[11]
print destination



#scraperwiki.sqlite.execute("delete from swdata")

record = {}
record['Time'] = times[0]
record['Destination'] = destination[0]
print record, '------------'
scraperwiki.sqlite.save(["Time"], record)
record['Time'] = times[1]
record['Destination'] = destination[1]

# Print out the data we've gathered
print record, '------------'
# Finally, save the record to the datastore - 'Artist' is our unique key
scraperwiki.sqlite.save(["Time"], record)

record['Time'] = times[2]
record['Destination'] = destination[2]
print record, '------------'
scraperwiki.sqlite.save(["Time"], record)
