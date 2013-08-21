import scraperwiki
# Code taken from http://www.travisglines.com/web-coding/python-xml-parser-tutorial
#import library to do http requests:
import urllib2
from lxml import etree
 
#import easy to use xml parser called minidom:
from xml.dom.minidom import parseString
#all these imports are standard on most modern python implementations
 

links = []
pages = [1,2,3,4,5,6,7,8]
URLstart = "http://api2.yp.com/listings/v1/search?searchloc=92025&radius=25&term=commercial+real+estate&sort=distance&listingcount=50&pagenum="
URLend = "&key=5c08b9f6fda6feae004e30aa3386684c"

for page in pages:
    #download the file:
    URL = URLstart + str(page) + URLend
    file = urllib2.urlopen(URL)
    #convert to string:
    data = file.read()
    #close file because we dont need it anymore:
    file.close()

    #parse the xml you downloaded
    dom = parseString(data)
    #retrieve the first xml tag (<tag>data</tag>) that the parser finds with name tagName:
    Listings = dom.getElementsByTagName('searchListing')
    print page


    for Listing in Listings:
        ListingInfo = Listing.getElementsByTagName('categories')[0].toxml()
        #categories = ListingInfo.firstChild.data

        ListingInfo1 = Listing.getElementsByTagName('businessName')[0].toxml()
        #categories = ListingInfo.replace('<categories>','').replace('</categories>','')

        ListingInfo2 = Listing.getElementsByTagName('street')[0].toxml()
        #categories = ListingInfo.replace('<categories>','').replace('</categories>','')

        ListingInfo3 = Listing.getElementsByTagName('city')[0].toxml()
        #categories = ListingInfo.replace('<categories>','').replace('</categories>','')

        ListingInfo4 = Listing.getElementsByTagName('state')[0].toxml()
        #categories = ListingInfo.replace('<categories>','').replace('</categories>','')
    
        ListingInfo5 = Listing.getElementsByTagName('zip')[0].toxml()
        #categories = ListingInfo.replace('<categories>','').replace('</categories>','')

        ListingInfo6 = Listing.getElementsByTagName('email')[0].toxml()
        #print ListingInfo6.firstChild.data

        ListingInfo7 = Listing.getElementsByTagName('phone')[0].toxml()
        #categories = ListingInfo.replace('<categories>','').replace('</categories>','')

        ListingInfo8 = Listing.getElementsByTagName('websiteURL')[0].toxml()
        #categories = ListingInfo.replace('<categories>','').replace('</categories>','')

        #print "%s %s %s %s %s %s %s %s %s" % (ListingInfo,ListingInfo1,ListingInfo2,ListingInfo3,ListingInfo4,ListingInfo5,ListingInfo6,ListingInfo7,ListingInfo8)
        links.append((ListingInfo,ListingInfo1,ListingInfo2,ListingInfo3,ListingInfo4,ListingInfo5,ListingInfo6,ListingInfo7,ListingInfo8))

for info in links:
    data = {
        'categories' : info[0],
        'businessName' : info[1], 
        'street' : info[2],
        'city' : info[3],
        'state' : info[4],
        'zip' : info[5],
        'email' : info[6],
        'phone' : info[7],
        'websiteURL' : info[8]
    }
    scraperwiki.sqlite.save(unique_keys=['businessName'], data=data)










'''
import scraperwiki
import requests
from bs4 import BeautifulSoup
from lxml import etree
import urllib2
import urllib
import simplejson

URL = 'http://api2.yp.com/listings/v1/search?searchloc=91203&term=pizza&sort=distance&radius=5&listingcount=50&key=5c08b9f6fda6feae004e30aa3386684c'
#response = requests.get(URL)
#print response.text
#soup = BeautifulSoup(response.text)
#print soup.content
#root = etree.fromstring(response.text)

req = urllib2.Request(URL, None, {'user-agent':'syncstream/vimeo'})
opener = urllib2.build_opener()
f = opener.open(req)
simplejson.load(f)
'''





