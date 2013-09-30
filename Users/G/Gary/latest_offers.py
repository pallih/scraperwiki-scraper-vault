import scraperwiki
import mechanize
import re
import urlparse
import lxml.html


# ASPX pages are some of the hardest challenges because they use javascript and forms to navigate
# Almost always the links go through the function function __doPostBack(eventTarget, eventArgument)
# which you have to simulate in the mechanize form handling library

# This example shows how to follow the Next page link

url3 = 'http://feeds.feedburner.com/EasyfundraisingLatestOffers'
br3 = mechanize.Browser()

    # sometimes the server is sensitive to this information
br3.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
response3 = br3.open(url3)


html3 = response3.read()
re.DOTALL
offername = re.findall('<title>(.*?)</title>', html3)
offerlink = re.findall('<link>(.*?)</link>', html3)
offerlogo = re.findall('<a .*?">(.*?)</a>', html3)
offerdonation = re.findall("                (.*?)<br/><br/>",html3)
offername.pop(0)
offername.pop(0)
offerlink.pop(0)
offerlink.pop(0)
print offername
print offerlink
print offerlogo
print offerdonation

allattributes = offername, offerlink, offerlogo, offerdonation
sortedattributes = [[row[i] for row in allattributes] for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49]]

scraperwiki.sqlite.execute("delete from swdata") 

record = {}
for sortedattribute in sortedattributes:
    if offername:
        record['Company'] = sortedattribute[0]
        record['Link'] = sortedattribute[1]
        record['Logo'] = sortedattribute[2]
        record['Donation'] = sortedattribute[3]

        # Print out the data we've gathered
        print record, '------------'
        # Finally, save the record to the datastore - 'Artist' is our unique key
        scraperwiki.sqlite.save(["Link"], record)import scraperwiki
import mechanize
import re
import urlparse
import lxml.html


# ASPX pages are some of the hardest challenges because they use javascript and forms to navigate
# Almost always the links go through the function function __doPostBack(eventTarget, eventArgument)
# which you have to simulate in the mechanize form handling library

# This example shows how to follow the Next page link

url3 = 'http://feeds.feedburner.com/EasyfundraisingLatestOffers'
br3 = mechanize.Browser()

    # sometimes the server is sensitive to this information
br3.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
response3 = br3.open(url3)


html3 = response3.read()
re.DOTALL
offername = re.findall('<title>(.*?)</title>', html3)
offerlink = re.findall('<link>(.*?)</link>', html3)
offerlogo = re.findall('<a .*?">(.*?)</a>', html3)
offerdonation = re.findall("                (.*?)<br/><br/>",html3)
offername.pop(0)
offername.pop(0)
offerlink.pop(0)
offerlink.pop(0)
print offername
print offerlink
print offerlogo
print offerdonation

allattributes = offername, offerlink, offerlogo, offerdonation
sortedattributes = [[row[i] for row in allattributes] for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49]]

scraperwiki.sqlite.execute("delete from swdata") 

record = {}
for sortedattribute in sortedattributes:
    if offername:
        record['Company'] = sortedattribute[0]
        record['Link'] = sortedattribute[1]
        record['Logo'] = sortedattribute[2]
        record['Donation'] = sortedattribute[3]

        # Print out the data we've gathered
        print record, '------------'
        # Finally, save the record to the datastore - 'Artist' is our unique key
        scraperwiki.sqlite.save(["Link"], record)