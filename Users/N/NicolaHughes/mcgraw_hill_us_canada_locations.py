import re
import scraperwiki
import lxml.html
from lxml import etree

html = scraperwiki.scrape("http://www.mcgraw-hill.com/site/about-us/office-locations/united-states-and-canada")
root = lxml.html.fromstring(html)

for b in root.cssselect('p'):
    entry = etree.tostring(b).replace('<br />', "\n").replace('<p>', "").replace('</p>', "").replace("<b>","").replace("</b>", "")
    segments = entry.split('\n')
    print segments
    name = segments[0].replace('&amp;', '&').replace('&#8212;', '-')
    print name
    if name == 'Corporate':
        name = 'McGraw-Hill Corporate'
    if len(segments) == 3:
        address = segments[1] + ', ' + segments[2]
        contact = ''
    if len(segments) == 4:
        address = segments[1] + ', ' + segments[2]
        contact = segments[3]
    if len(segments) == 5:
        if (name == 'J.D. Power and Associates: Corporate Headquarters' or name == 'J.D. Power and Associates' or name == 'McGraw-Hill Financial Communications' ):
            address = segments[1] + ', ' + segments[2]
            contact = segments[3] + ', ' + segments[4]
        else:
            address = segments[1] + ', ' + segments[2] + ', ' + segments[3]
            contact = segments[4]
    if len(segments) == 6:
        address = segments[1] + ', ' + segments[2] + ', ' + segments[3]
        contact = segments[4] + ', ' + segments[5]
    if name == "Standard & Poor's Capital IQ, Inc.":
        address = segments[1] + ', ' + segments[2] + ', ' + segments[3]
        contact = segments[4] + ', ' + segments[5] + ', ' + segments[6]
    if (name == "Platts, J.D. Power and Associates (Web Intelligence Division)" or name == 'Corporate, McGraw-Hill Education, Platts, Aviation Week Group, J.D. Power and Associates'):
        address = segments[1] + ', ' + segments[2]
        contact = segments[3] + ', ' + segments[4] + ', ' + segments[5] + ', ' + segments[6]
    data = {'Text': name, 'Location': address, 'Notes': contact}
    scraperwiki.sqlite.save(['Location'], data)
        
        

#    for s in segments:
#        if re.match('^\w+,.[A-ZA-Z].*\d+.*$', s): 
            # It is state information, need to try and gauge relationship to surrounding data.
#            print 'State: ', s
#        else:
#            print s
