import scraperwiki
# Code taken from http://www.travisglines.com/web-coding/python-xml-parser-tutorial
#import library to do http requests:
import urllib2
from lxml import etree
 
#import easy to use xml parser called minidom:
from xml.dom.minidom import parseString
#all these imports are standard on most modern python implementations
 

links = []
#pages = [1,2,3,4,5,6,7,8]
years = [2008, 2009,2010, 2011, 2012]
#URLstart = "http://api2.yp.com/listings/v1/search?searchloc=92025&radius=25&term=commercial+real+estate&sort=distance&listingcount=50&pagenum="
URLstart = "http://fts.unocha.org/api/v1/Emergency/year/"
#URLend = "&key=5c08b9f6fda6feae004e30aa3386684c"
URLend = ".xml"

for year in years:
    #download the file:
    URL = URLstart + str(year) + URLend
    print URL
    file = urllib2.urlopen(URL)
    #convert to string:
    data = file.read()
    #close file because we dont need it anymore:
    file.close()

    #parse the xml you downloaded
    dom = parseString(data)
    #retrieve the first xml tag (<tag>data</tag>) that the parser finds with name tagName:
    Emergencies = dom.getElementsByTagName('Emergency')
    print year


    for Emergency in Emergencies:
        EmergInfo = Emergency.getElementsByTagName('country')[0].toxml()        
        EmergInfo =EmergInfo.replace('<country>','').replace('</country>','')

        EmergInfo1 = Emergency.getElementsByTagName('glideid')[0].toxml()
        EmergInfo1 =EmergInfo1.replace('<glideid>','').replace('</glideid>','')

        EmergInfo2 = Emergency.getElementsByTagName('id')[0].toxml()
        EmergInfo2 =EmergInfo2.replace('<id>','').replace('</id>','')

        EmergInfo3 = Emergency.getElementsByTagName('title')[0].toxml()
        EmergInfo3 =EmergInfo3.replace('<title>','').replace('</title>','')

        EmergInfo4 = Emergency.getElementsByTagName('type')[0].toxml()
        EmergInfo4 =EmergInfo4.replace('<type>','').replace('</type>','')

        EmergInfo5 = Emergency.getElementsByTagName('year')[0].toxml()
        EmergInfo5 =EmergInfo5.replace('<year>','').replace('</year>','')
        
        #print "%s %s %s %s %s %s %s %s %s" % (EmergInfo,EmergInfo1,EmergInfo2,EmergInfo3,EmergInfo4,EmergInfo5)
        links.append((EmergInfo,EmergInfo1,EmergInfo2,EmergInfo3,EmergInfo4,EmergInfo5))

for info in links:
    data = {
        'country' : info[0],        
        'glideid' : info[1],   
        'id' : info[2],   
        'title' : info[3],   
        'type' : info[4],   
        'year' : info[5]   
    }
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)

