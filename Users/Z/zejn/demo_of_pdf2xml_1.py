import scraperwiki
import urllib

pdf2xml = scraperwiki.swimport("pdf2xml")
pdfurl = "http://samplepdf.com/sample.pdf"

# example PDF
pdfurl = 'http://samplepdf.com/sample.pdf'
pdf = urllib.urlopen(pdfurl).read()

   # The C executable:
print scraperwiki.pdftoxml(pdf)
   # The PDFminder version from https://github.com/zejn/pypdf2xml/blob/master/pdf2xml
print pdf2xml.pdf2xml(pdf)

# Notes: 
#  It may be that is better delivered as a scraperwiki view where you pass in the url as an argument, and the view 
#  downloads and parses it, so it can be used in all languages.  
#  Disadvantage is you don't get to hold and be able to cache the PDF source itself.  

# The software version is better at "handling non-ascii or otherwise custom glyphs, which supplied glyph to
# character maps."  -- [example?]

# Also it is my (Julian_Todd's) intention to get a version that preserves borders of table cells, which nothing does.  
