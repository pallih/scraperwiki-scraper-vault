###########################################################################################
# We use a ScraperWiki library called pdftoxml to scrape PDFs.
# This is an example of scraping a simple PDF.
###########################################################################################

import scraperwiki
import urllib2
import lxml.etree

import scraperwiki
import urllib
import lxml.etree, lxml.html
import re
pdfurl = "http://www.gobex.es/consejerias/contratos/2013_1_30_2.pdf"
pdfdata = urllib.urlopen(pdfurl).read()
pdfxml = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(pdfxml)
print "The first 99000 characters are: ", pdfxml[:99000]
pages = list(root)
print (pages)
for page in pages:
    assert page.tag == 'page'
    pagelines = { }
    pagenumber=int(page.attrib.get("number"))
    print(pagelines)
    
    for textchunk in (page.xpath('text')):
        leftcoord = int(textchunk.attrib.get('left'))

        if leftcoord>44 and leftcoord<46: #Get a fecha this is the restart signal            
            if textchunk.text is not None and not textchunk.text.isspace():
                Fech={}
                Fech=textchunk.text.strip()
        
        elif leftcoord>114 and leftcoord<118:  #Get a lifespan string - if this is a see... then we need to write an alias
             if textchunk.text is not None and not textchunk.text.isspace():
                Mot={}
                Mot=textchunk.text.strip()

        elif leftcoord>540 and leftcoord<562:  #Get a lifespan string - if this is a see... then we need to write an alias
             if textchunk.text is not None and not textchunk.text.isspace():
                Importe={}
                Importe=textchunk.text.strip()

        elif leftcoord>603 and leftcoord<607:  #Get a lifespan string - if this is a see... then we need to write an alias
            if textchunk.text is not None and not textchunk.text.isspace():
                Adjud={}
                Adjud=textchunk.text.strip()

        elif leftcoord>775 and leftcoord<785:  #Get a lifespan string - if this is a see... then we need to write an alias
             if textchunk.text is not None and not textchunk.text.isspace():
                NIF={}
                NIF=textchunk.text.strip()
    print (Fech, Mot, Importe, Adjud, NIF)
    scraperwiki.sqlite.save(unique_keys=[ 'CIF' ],data={ 'Motivo': Mot, 'Adjudicatario': Adjud, 'Fecha': Fech,'CIF': NIF, 'Importe sin IVA': Importe})


# If you have many PDF documents to extract data from, the trick is to find what's similar 
# in the way that the information is presented in them in terms of the top left bottom right 
# pixel locations.  It's real work, but you can use the position visualizer here:
#    http://scraperwikiviews.com/run/pdf-to-html-preview-1/






###########################################################################################
# We use a ScraperWiki library called pdftoxml to scrape PDFs.
# This is an example of scraping a simple PDF.
###########################################################################################

import scraperwiki
import urllib2
import lxml.etree

import scraperwiki
import urllib
import lxml.etree, lxml.html
import re
pdfurl = "http://www.gobex.es/consejerias/contratos/2013_1_30_2.pdf"
pdfdata = urllib.urlopen(pdfurl).read()
pdfxml = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(pdfxml)
print "The first 99000 characters are: ", pdfxml[:99000]
pages = list(root)
print (pages)
for page in pages:
    assert page.tag == 'page'
    pagelines = { }
    pagenumber=int(page.attrib.get("number"))
    print(pagelines)
    
    for textchunk in (page.xpath('text')):
        leftcoord = int(textchunk.attrib.get('left'))

        if leftcoord>44 and leftcoord<46: #Get a fecha this is the restart signal            
            if textchunk.text is not None and not textchunk.text.isspace():
                Fech={}
                Fech=textchunk.text.strip()
        
        elif leftcoord>114 and leftcoord<118:  #Get a lifespan string - if this is a see... then we need to write an alias
             if textchunk.text is not None and not textchunk.text.isspace():
                Mot={}
                Mot=textchunk.text.strip()

        elif leftcoord>540 and leftcoord<562:  #Get a lifespan string - if this is a see... then we need to write an alias
             if textchunk.text is not None and not textchunk.text.isspace():
                Importe={}
                Importe=textchunk.text.strip()

        elif leftcoord>603 and leftcoord<607:  #Get a lifespan string - if this is a see... then we need to write an alias
            if textchunk.text is not None and not textchunk.text.isspace():
                Adjud={}
                Adjud=textchunk.text.strip()

        elif leftcoord>775 and leftcoord<785:  #Get a lifespan string - if this is a see... then we need to write an alias
             if textchunk.text is not None and not textchunk.text.isspace():
                NIF={}
                NIF=textchunk.text.strip()
    print (Fech, Mot, Importe, Adjud, NIF)
    scraperwiki.sqlite.save(unique_keys=[ 'CIF' ],data={ 'Motivo': Mot, 'Adjudicatario': Adjud, 'Fecha': Fech,'CIF': NIF, 'Importe sin IVA': Importe})


# If you have many PDF documents to extract data from, the trick is to find what's similar 
# in the way that the information is presented in them in terms of the top left bottom right 
# pixel locations.  It's real work, but you can use the position visualizer here:
#    http://scraperwikiviews.com/run/pdf-to-html-preview-1/






