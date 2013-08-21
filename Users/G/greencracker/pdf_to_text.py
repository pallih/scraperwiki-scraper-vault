import scraperwiki
import os

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice

# Open a PDF file.

pdf = scraperwiki.scrape('http://greencracker.net/wp-content/uploads/2013/04/ExportReportToPDF.pdf')

f = open('doc.pdf', 'w') # Save it locallyBack to scraper overview
f.write(pdf)
f.close()
text = os.system('pdf2txt.py -n doc.pdf > doc.txt')
f = open('doc.txt', 'r')
print f.read()

