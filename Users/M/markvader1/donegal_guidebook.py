import scraperwiki
# Code taken from http://www.travisglines.com/web-coding/python-xml-parser-tutorial
#import library to do http requests:
import urllib2
from lxml import etree
 
#import easy to use xml parser called minidom:
from xml.dom.minidom import parseString
#all these imports are standard on most modern python implementations

links = []

# need to find a way to parse all pages linked on http://www.pete-smith.co.uk/dynamic/guidebook/add_a_crag.php 
# at the minute this is approx 150 pages in the range of 1 to 200 i.e. there are gaps in the range and also this number will increase in future.
# scraper will need to run without breaking when it comes to a page that is missing, also are a number of pages that arent formatted correctly e.g. 6
# Can run the following line to parse multiple pages
# pages = [1,3,4,5,7,8,10,11,12,14,15,16,17,18,19,20,144]

pages = [144,1,3,4,5,7,8,10,11,12,14,15,16,17,18,19,20]
URLstart = "http://www.pete-smith.co.uk/dynamic/guidebook/crag_in.xml?crag_no="

for page in pages:
    #download the file:
    URL = URLstart + str(page)
    file = urllib2.urlopen(URL)
    #convert to string:
    data = file.read()
    #close file because we dont need it anymore:
    file.close()

    #parse the xml you downloaded
    dom = parseString(data)
    #retrieve the first xml tag (<route>data</route>) that the parser finds with name tagName:
    Listings = dom.getElementsByTagName('route')
    print page


    for Listing in Listings:
        ListingInfo = Listing.getElementsByTagName('routename')[0].toxml()
        ListingInfo1 = Listing.getElementsByTagName('description')[0].toxml()
        ListingInfo2 = Listing.getElementsByTagName('first_ascensionist')[0].toxml()
        ListingInfo3 = Listing.getElementsByTagName('number_of_comments')[0].toxml()
        ListingInfo4 = Listing.getElementsByTagName('further_details')[0].toxml()

        links.append((ListingInfo,ListingInfo1,ListingInfo2,ListingInfo3,ListingInfo4))

for info in links:
    data = {
        'routename' : info[0],
        'description' : info[1],
        'first_ascensionist' : info[2],
        'number_of_comments' : info[3],
        'further_details' : info[4]
    }
    scraperwiki.sqlite.save(unique_keys=['routename'], data=data)

