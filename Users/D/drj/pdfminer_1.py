import urllib2
import StringIO

# Code mostly from http://www.unixuser.org/~euske/python/pdfminer/programming.html

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice

# Tried setting it to not strict, but makes no difference:
# Falls over on line 457 anyway.
import pdfminer.pdfparser
pdfminer.pdfparser.STRICT = 0

# Open a PDF file.
fp = urllib2.urlopen('https://dl.dropbox.com/u/268010/2800.pdf')
fp=StringIO.StringIO(fp.read())
# Create a PDF parser object associated with the file object.
parser = PDFParser(fp)
# Create a PDF document object that stores the document structure.
doc = PDFDocument()
# Connect the parser and document objects.
parser.set_document(doc)
doc.set_parser(parser)
# Supply the password for initialization.
# (If no password is set, give an empty string.)
doc.initialize('')
# Create a PDF resource manager object that stores shared resources.
rsrcmgr = PDFResourceManager()
# Create a PDF device object.
device = PDFDevice(rsrcmgr)
# Create a PDF interpreter object.
interpreter = PDFPageInterpreter(rsrcmgr, device)
# Process each page contained in the document.
for page in doc.get_pages():
    interpreter.process_page(page)
