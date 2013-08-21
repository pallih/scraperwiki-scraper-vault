import scraperwiki
import os, tarfile
from StringIO import StringIO
import requests
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import HTMLConverter, XMLConverter, TextConverter
from pdfminer.layout import LAParams
from pdfminer.cmapdb import CMapDB


cmap = requests.get('http://dl.dropboxusercontent.com/u/250221/cmap.tar')
cmap_sio = StringIO(cmap.content)
tar = tarfile.open(fileobj=cmap_sio)
tar.extractall()
tar.close()
cmap_sio.close()

os.environ['CMAP_PATH'] = '/home/scriptrunner/cmap'

FREEMYPDF = 'http://freemypdf.com/'
url = 'http://kanpou.npb.go.jp/20130426/20130426g00090/pdf/20130426g000900068.pdf'

pdf = requests.get(url)

fmp = requests.Session()
fmp.get(FREEMYPDF)
freed_pdf = fmp.post(FREEMYPDF, files={'origpdf': ('test.pdf', pdf.content)})

pdf_fp = StringIO(freed_pdf.content)

rsrcmgr = PDFResourceManager()
retstr = StringIO()
laparams = LAParams(detect_vertical=True)
device = TextConverter(rsrcmgr, retstr,  laparams=laparams)

process_pdf(rsrcmgr, device, pdf_fp, check_extractable=False)
device.close()

print  retstr.getvalue()
retstr.close()
pdf_fp.close()

