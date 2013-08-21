import scraperwiki,simplejson,urllib2
from lxml import etree
from copy import deepcopy


#--via @mhawksey
# query string crib https://views.scraperwiki.com/run/python_querystring_cheat_sheet/?
import cgi, os
qstring=os.getenv("QUERY_STRING")

key='65791' #Use the Isle of Wight as a default
typ='UTE'
#typs are:
'''
CTY (county council), CED (county ward), COI (Isles of Scilly), COP (Isles of Scilly parish), CPC (civil parish/community), CPW (civil parish/community ward), DIS (district council), DIW (district ward), EUR (Euro region), GLA (London Assembly), LAC (London Assembly constituency), LBO (London borough), LBW (London ward), LGD (NI council), LGE (NI electoral area), LGW (NI ward), MTD (Metropolitan district), MTW (Metropolitan ward), NIE (NI Assembly constituency), OLF (Lower Layer Super Output Area, Full), OLG (Lower Layer Super Output Area, Generalised), OMF (Middle Layer Super Output Area, Full), OMG (Middle Layer Super Output Area, Generalised), SPC (Scottish Parliament constituency), SPE (Scottish Parliament region), UTA (Unitary authority), UTE (Unitary authority electoral division), UTW (Unitary authority ward), WAC (Welsh Assembly constituency), WAE (Welsh Assembly region), WMC (UK Parliamentary constituency)
'''

if qstring!=None:
    get = dict(cgi.parse_qsl(qstring))
    if 'key' in get: key=get['key']
    if 'typ' in get: typ=get['typ'] 
#---


#Get a stub KML file for the local council level
url='http://mapit.mysociety.org/area/'+str(key)+'.kml'
xmlraw = urllib2.urlopen(url).read()
xml=etree.fromstring(xmlraw)

#Get the list of electoral wards covered by that council area
wards=simplejson.load(urllib2.urlopen('http://mapit.mysociety.org/area/'+str(key)+'/covers?type='+typ))

#Get the KML for each ward, extract the Placemark data, and add it to our comprehensive KML tree
for ward in wards:
    url='http://mapit.mysociety.org/area/'+ward+'.kml'
    xmlraw = scraperwiki.scrape(url)
    xml2=etree.fromstring(xmlraw)
    p= xml2.xpath('//geo:Placemark',namespaces={'geo':'http://www.opengis.net/kml/2.2'})
    xml.append( deepcopy(p[0] ))

scraperwiki.utils.httpresponseheader("Content-Type", "text/xml")
print etree.tostring(xml)