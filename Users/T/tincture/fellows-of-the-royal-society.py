import scraperwiki
#import lxml.html
import BeautifulSoup
import os.path

# List of current fellows of the royal society extracted from the pdf on their website
pdfurl = "http://royalsociety.org/WorkArea/DownloadAsset.aspx?id=4294969200"

gongs = ['FRS', 'FREng', 'CBE', 'OBE', 'OM', 'CH', 'CVO', 'DBE', 'AM' ] # Attenborough is responsible for most of these :P
titles = ['Professor', 'Dr', 'Sir', 'Dame', 'Lord' ]

a = scraperwiki.scrape(pdfurl)

tree = BeautifulSoup.BeautifulSoup(scraperwiki.pdftoxml(a))

#print tree.prettify()

for t in tree.recursiveChildGenerator() :
    try : # AttributeError is thrown if no t.name
        if t.name == 'b' and t.string and t.string is not None : # we're probably at a surname
            #print t.string #surname
            if len(t.parent) > 1 :
                prefix = t.parent.contents[1] # something like ', Sir Eric Albert CBE FREng FRS'
                bits = prefix.strip().split(' ') # bits[2] will mostly be first name
                print bits[2], t.string
                data = { 'fellow': '%s %s' % (bits[2], t.string) }
                scraperwiki.datastore.save( unique_keys=['fellow'], data=data )                
    except AttributeError :
        next 


