import scraperwiki

# Blank Python

import urllib
import StringIO

import pdfminer

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice

from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator

page1=urllib.urlopen('http://www.justice.gov.uk/downloads/tribunals/lands/court-appeal-cases.pdf')
page2=urllib.urlopen('http://www.landstribunal.gov.uk/judgmentfiles/j397/LRX-107-2005-Final.pdf')
page=page2
page_object=StringIO.StringIO(page.read())



#Ghastly library: https://github.com/euske/pdfminer/blob/master/pdfminer/layout.py


# Create a PDF parser object associated with the file object.
parser = PDFParser(page_object)
# Create a PDF document object that stores the document structure.
doc = PDFDocument()
# Connect the parser and document objects.
parser.set_document(doc)
doc.set_parser(parser)
# Supply the password for initialization.
# (If no password is set, give an empty string.)
doc.initialize('')
# Check if the document allows text extraction. If not, abort.
if not doc.is_extractable:
    raise PDFTextExtractionNotAllowed
# Create a PDF resource manager object that stores shared resources.
rsrcmgr = PDFResourceManager()

## Create a PDF device object.
#device = PDFDevice(rsrcmgr)
## Create a PDF interpreter object.
#interpreter = PDFPageInterpreter(rsrcmgr, device)


# Set parameters for analysis.
laparams = LAParams()
# Create a PDF page aggregator object.
device = PDFPageAggregator(rsrcmgr, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)
for page in doc.get_pages():
    interpreter.process_page(page)
    # receive the LTPage object for the page.
    layout = device.get_result()

# Process each page contained in the document.

def analyse1(page):
    i=1
    for page in doc.get_pages():
        if i > 1:
            break
        interpreter.process_page(page)
        layout=device.get_result()
        print(layout)
        rows={}
        for hbox in layout:
            if isinstance(hbox, pdfminer.layout.LTTextBoxHorizontal):
                (x0, y0, x1, y1)=hbox.bbox
                text=hbox.get_text()
                row_key=int(y1 * 1000)
                if row_key not in rows:
                    rows[row_key]=[]
                rows[row_key].append((x0, text))
                print(y1, x0, text)
                if 370 < y1 and y1 < 390:
                    print(hbox)
                    print(len(hbox))
                    for thing in hbox:
                        print(thing)
                
        for key in sorted(rows.keys(), reverse=True):
            row=sorted(rows[key], key=lambda t:t[0])
            print(key, '\t'.join(x[1] for x in row))
            #print(row)
        
        i=i+1

def analyse2(page):
    i=1
    for page in doc.get_pages():
        if i > 2:
            break
        interpreter.process_page(page)
        layout=device.get_result()
        print(layout)
        for thing in layout:
            print(thing)
        
        i=i+1

analyse2(page)