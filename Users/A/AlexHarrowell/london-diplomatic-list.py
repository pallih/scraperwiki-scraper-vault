###############################################################################
# Gets the current state of the London corps diplomatique and hopefully eventually generates a nice RSS feed
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
import time
import urllib

urltemplate = 'http://www.fco.gov.uk/resources/en/protocol/ldl-'
date = time.strftime('%A %d %B %Y')
month = (date.split(' '))[2]
year = (date.split(' '))[3]

#url = urltemplate + month + year
url = 'http://www.fco.gov.uk/resources/en/protocol/ldl-August2010'
pdfinput = urllib.urlopen(url)
print 'got pdf'
scraped = scraperwiki.pdftoxml(pdfinput.read())
print 'pdftohtml complete'
output = []

def getlastrow():
    l = len(output)
    r = output[(l)]
    return r
print 'finished setup'
soup = BeautifulSoup(scraped)
print 'soup cooked'
# this document is a right dog

# note - 153 Ambs or High Comms, presumably that's one per country or rather, accrediting entity - but watch out for the consuls and international organisations
fontspecs = soup.findAll('fontspec')
for spec in fontspecs:
    print spec  
text = soup.findAll('text')
print 'text tags retrieved'

rowstate = ''

for item in text:
    # ok chaps, we're going in
        # countries, embassy styles, and section titles are font 1, bold, as are 'married' flags if they're on a newline
        # countries (and other accrediting agencies) are CAPITALISED
        if item['font'] == '1' and item.find('b') and item.b.string != ' ' and item.b.string != 'm':
                    if (item.b.string).isupper():
                        # this is a country
                        print item
                        print 'ACCREDITING PARTY: ' + item.b.string
                        sibs = item.findNextSiblings()
                        rowstate = 'country'
                        for item in sibs:
                            if item['font'] == 1 and item.b.string and (item.b.string).isupper():
                                break
                            else:
                                if item['font'] == 1:
                                    if rowstate == 'country':
                                        print item
                                        print 'DETAIL: ' + item.b.string
                                        rowstate = 'detail'
                                    elif rowstate == 'detail':
                                        print item
                                        print 'SECTION: ' + item.b.string
                                if item['font'] == 2 or 7 or 8:
                                    if item.string:
                                        if (item.string).isupper():
                                            print item
                                            print 'AMBASSADOR: ' + item.string
                                            rowstate = 'ambassador'
                                        else:
                                            if rowstate == 'ambassador':
                                                print item
                                                print 'SPOUSE: ' + item.string
                                            else:
                                                print 'CONTACT: ' + item.string
                                        
                                    else:
                                        if (item.contents[0].string).isupper():
                                            print item
                                            print 'AMBASSADOR: ' + item.contents[0].string
                                            rowstate = 'ambassador'
                                        elif item.contents[0].i:
                                            print item
                                            print 'STYLE: ' + item.i.string
                                            rowstate = 'style'
                                        elif rowstate == 'ambassador':
                                            job = item.i.string
                                            name = str(item[0])
                                            print item
                                            print job + ': ' + name
                        
