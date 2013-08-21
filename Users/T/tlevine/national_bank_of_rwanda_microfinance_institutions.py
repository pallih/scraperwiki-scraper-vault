from scraperwiki import pdftoxml,swimport
from scraperwiki.sqlite import save,show_tables
from urllib2 import urlopen
from lxml.etree import fromstring,tostring
keyify=swimport('keyify').keyify

def main():
  pages = getTablePages()
  print tostring(pages[0])

def getTablePages():
  url = "http://www.bnr.rw/docs/publicnotices/List%20of%20MFIs%20Update_Sept_%202011.pdf"
  pdfdata = urlopen(url).read()
  xmldata = pdftoxml(pdfdata)
  root = fromstring(xmldata)
  pages = list(root)
  return pages

main()