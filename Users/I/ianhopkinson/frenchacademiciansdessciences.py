import scraperwiki
import urllib2
import lxml.etree

# Academicians of the French Academie des Sciences
# Ian Hopkinson (9/12/12)
# URL's are of the form:
# http://www.academie-sciences.fr/academie/membre/memA.pdf

urlstub = "http://www.academie-sciences.fr/academie/membre/mem"
Letters=map(chr, range(65, 91))

# Loop over letters
for Letter in Letters:
# Put a resume condition here
    if Letter != 'A':
        break
    url=urlstub+Letter+".pdf"
    print url

    pdfdata = urllib2.urlopen(url).read()
    print "The pdf file has %d bytes" % len(pdfdata)

    # Put options here if we need them
    options=''
    #options="-f 5 -l 5"
    xmldata = scraperwiki.pdftoxml(pdfdata,options)

    print "After converting to xml it has %d bytes" % len(xmldata)
    print "The first 11000 characters are: ", xmldata
    
    root = lxml.etree.fromstring(xmldata)
    pages = list(root)

    for element in root.getiterator():
        #print element.tag, '-', element.text # Names are in b tags
        if element.tag == 'b':
            print element.text ,"- font = ", element.getparent().attrib.get("font")

#<text top="469" left="106" width="56" height="14" font="4"><b>Albert 1</b></text>
#<text top="465" left="162" width="9" height="9" font="8">er</text>
#<text top="469" left="171" width="462" height="14" font="4"><b>, prince souverain de Monaco (Albert, Honoré, Charles) Grimaldi</b> </text>
#<text top="491" left="106" width="327" height="14" font="3">13 novembre 1848 à Paris - 26 juin 1922 à Paris </text>

    #Loop over pages - 
    #for page in pages:
        #pagenumber=int(page.attrib.get("number"))
#<text top="437" left="106" width="144" height="14" font="4"><b>Abeille (Louis-Paul)</b> </text>
# Academician names (and letter heads such as A, are in font="4")