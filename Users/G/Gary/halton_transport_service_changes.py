import scraperwiki
import mechanize
import re
import urlparse
import lxml.html


# ASPX pages are some of the hardest challenges because they use javascript and forms to navigate
# Almost always the links go through the function function __doPostBack(eventTarget, eventArgument)
# which you have to simulate in the mechanize form handling library

# This example shows how to follow the Next page link

url3 = 'http://home.btconnect.com/haltontransport/servicechanges.htm'
br3 = mechanize.Browser()

    # sometimes the server is sensitive to this information
br3.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
response3 = br3.open(url3)


html3 = response3.read()
print html3
videoimgs = re.findall('<TD.*?>(.*?)</TD>', html3, re.MULTILINE | re.DOTALL | re.VERBOSE )
print videoimgs



scraperwiki.sqlite.execute("delete from swdata") 

record = {}
idnumber = 1
for videoimg in videoimgs:
    if videoimgs:
        record['id'] = idnumber
        record['block'] = videoimg

        # Print out the data we've gathered
        print record, '------------'
        # Finally, save the record to the datastore - 'Artist' is our unique key
        scraperwiki.sqlite.save(["id"], record)
    idnumber = int(float(idnumber)) + 1
