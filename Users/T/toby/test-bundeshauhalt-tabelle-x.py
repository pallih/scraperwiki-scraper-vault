import scraperwiki
import urllib
import lxml.etree, lxml.html, lxml.cssselect

# data
pdfurl = "http://www.bundesfinanzministerium.de/nn_67914/DE/Wirtschaft__und__Verwaltung/Finanz__und__Wirtschaftspolitik/Bundeshaushalt/Bundeshaushalt__2009/Finanzplan__08__012,templateId=raw,property=publicationFile.pdf"
TABLE="Tabelle "
TABLE_NUMBER="5 \n"
PATTERN=TABLE+TABLE_NUMBER

# load
pdfdata = urllib.urlopen(pdfurl).read()
pdfxml = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(pdfxml)

# parse
for page in root:
  pagenumber = int(page.attrib.get('number'))
  #if (pagenumber==42):
  text = page.xpath("string()")
  #if re.match(PATTERN,t.text):
  if (text.find(PATTERN)>0):
    print pagenumber
    print lxml.etree.tostring(page)
    #for elem in page.cssselect('text'):
    #  print elem.xpath("string()")
    for elem in page:
      colno = elem.attrib.get('left')
      if ( colno=="70" ):
        print elem.xpath("string()")
