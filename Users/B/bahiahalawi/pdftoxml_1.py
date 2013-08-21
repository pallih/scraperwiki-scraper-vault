import scraperwiki

import scraperwiki
import urllib2
import lxml.etree


url = 'http://cdn.varner.eu/cdn-1ce36b6442a6146/Global/Varner/CSR/Downloads_CSR/Fabrikklister_VarnerGruppen_2013.pdf'


pdfdata = urllib2.urlopen(url).read() 
xmldata = scraperwiki.pdftoxml(pdfdata) 
root = lxml.etree.fromstring(xmldata)


pages = list(root) 
print "There are",len(pages),"pages" 

for page in pages: 
    for el in page:
        if el.tag == "text":   
            print el.text, el.attrib

for page in pages[1:]:
   for el in page:
     if el.tag == "text":
       if int(el.attrib['left']) < 100: data = { 'Country': el.text }
       elif int(el.attrib['left']) < 250: data['Factory name'] = el.text
       elif int(el.attrib['left']) < 500: data['Address'] = el.text
       elif int(el.attrib['left']) < 1000: data['City'] = el.text
       else:
         data['Region'] = el.text
         print data 


scraperwiki.sqlite.save(unique_keys=[], table_name='fabvarn', data=data)