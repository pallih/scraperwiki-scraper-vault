import scraperwiki
import lxml.etree
import re
from geopy import geocoders

url = "http://www.regionofwaterloo.ca/en/gettingAround/resources/RegionalTrafficVolumes-AllLocations.pdf"
pdfdata = scraperwiki.scrape(url)
print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)
print "After converting to xml it has %d bytes" % len(xmldata)
print "The first 2000 characters are: ", xmldata[:2000]

root = lxml.etree.fromstring(xmldata)
pages = list(root)

localMuni = ''
lastStreet = ''
count = 0
munis = {'CAM': 'Cambridge', 
         'KIT': 'Kitchener', 
         'NDF': 'North Dumfries', 
         'WAT': 'Waterloo', 
         'WIL': 'Wilmot', 
         'WEL': 'Wellesley', 
         'WOO': 'Woolwich'}

g = geocoders.Google(domain='maps.google.ca')

for page in pages:
    for el in list(page):
        if el.tag == "text":
            bold = el.find('b')
            if bold is not None:
                text = bold.text
            else:
                text = el.text
            if el.attrib['font'] == '2':
                localMuni = text
            elif el.attrib['font'] == '1' and ('*' not in text) and ('Location' not in text):
                count = int(text)
            elif el.attrib['font'] == '3':
                match = re.search(r'(?P<street>[^()/]+)(/[^()]+)? +\(.+\) +(BTWN (?P<start>[^()]+)( ?\(.+\))? ([&]|to) (\(.*\) )?(?P<end>[^()]+)|(AT|BTWN) (\(.*\) )?(?P<intersection>[^()]+)( \((?P<nsew>North|South|East|West)erly Intersection\))?)', text)
                if localMuni == 'KIT' and count < 15000:
                        print count, text
                if match and match.group('intersection'):
                    locString = match.expand('\g<street> and \g<intersection>, ') + munis[localMuni] + ', ON'
                    
                    #results = g.geocode(locString, exactly_one=False)
                    #if len(results) == 0:
                        #print text
                