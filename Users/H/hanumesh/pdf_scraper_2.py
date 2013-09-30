import scraperwiki

# Blank Pythonfrom pdfminer.pdfparser import PDFParser, PDFDocument

fp = open('mypdf.pdf', 'rb')
parser = PDFParser(fp)
doc = PDFDocument()
parser.set_document(doc)
doc.set_parser(parser)
doc.initialize(password)

# Get the outlines of the document.
outlines = doc.get_outlines()
for (level,title,dest,a,se) in outlines:
    print (level, title)