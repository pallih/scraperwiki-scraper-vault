import scraperwiki
import mechanize
import re
import urlparse
import lxml.html


# ASPX pages are some of the hardest challenges because they use javascript and forms to navigate
# Almost always the links go through the function function __doPostBack(eventTarget, eventArgument)
# which you have to simulate in the mechanize form handling library

# This example shows how to follow the Next page link

url3 = 'http://www.dabs.com/category/networking,routers-and-switches,routers/11304-4294948534-4294944422-4294963789'
br3 = mechanize.Browser()

    # sometimes the server is sensitive to this information
br3.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
response3 = br3.open(url3)


html3 = response3.read()
jobtitlemonster = re.findall('<img.*?src="/images/product(.*?)"', html3)
locationmonster = re.findall('<img.*?src="/images/product.*?alt="(.*?)"', html3) + re.findall('<img alt="(.*?)" src="/images/product', html3)
companymonster = re.findall('<span class="lprice">(.*?)</span>',html3)
print jobtitlemonster
print locationmonster
print companymonster

allattsmonster = jobtitlemonster, locationmonster, companymonster
attssortmonsters = [[row[i] for row in allattsmonster] for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]


scraperwiki.sqlite.execute("delete from swdata")

record = {}
for attssortmonster in attssortmonsters:
    if jobtitlemonster:
        record['Image'] = attssortmonster[0]
        record['Name'] = attssortmonster[1]
        record['Price'] = attssortmonster[2]

        # Print out the data we've gathered
        print record, '------------'
        # Finally, save the record to the datastore - 'Artist' is our unique key
        scraperwiki.sqlite.save(["Image"], record)
import scraperwiki
import mechanize
import re
import urlparse
import lxml.html


# ASPX pages are some of the hardest challenges because they use javascript and forms to navigate
# Almost always the links go through the function function __doPostBack(eventTarget, eventArgument)
# which you have to simulate in the mechanize form handling library

# This example shows how to follow the Next page link

url3 = 'http://www.dabs.com/category/networking,routers-and-switches,routers/11304-4294948534-4294944422-4294963789'
br3 = mechanize.Browser()

    # sometimes the server is sensitive to this information
br3.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
response3 = br3.open(url3)


html3 = response3.read()
jobtitlemonster = re.findall('<img.*?src="/images/product(.*?)"', html3)
locationmonster = re.findall('<img.*?src="/images/product.*?alt="(.*?)"', html3) + re.findall('<img alt="(.*?)" src="/images/product', html3)
companymonster = re.findall('<span class="lprice">(.*?)</span>',html3)
print jobtitlemonster
print locationmonster
print companymonster

allattsmonster = jobtitlemonster, locationmonster, companymonster
attssortmonsters = [[row[i] for row in allattsmonster] for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]


scraperwiki.sqlite.execute("delete from swdata")

record = {}
for attssortmonster in attssortmonsters:
    if jobtitlemonster:
        record['Image'] = attssortmonster[0]
        record['Name'] = attssortmonster[1]
        record['Price'] = attssortmonster[2]

        # Print out the data we've gathered
        print record, '------------'
        # Finally, save the record to the datastore - 'Artist' is our unique key
        scraperwiki.sqlite.save(["Image"], record)
