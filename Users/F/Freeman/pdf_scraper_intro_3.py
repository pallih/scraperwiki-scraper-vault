# 1. Add some necessary libraries
import scraperwiki
import urllib2, lxml.etree

# 2. The URL/web address where we can find the PDF we want to scrape
url = 'http://cdn.varner.eu/cdn-1ce36b6442a6146/Global/Varner/CSR/Downloads_CSR/Fabrikklister_VarnerGruppen_2013.pdf'

# 3. Grab the file and convert it to an XML document we can work with
pdfdata = urllib2.urlopen(url).read()
xmldata = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(xmldata)

# 4. Have a peek at the XML (click the "more" link in the Console to preview it).
print lxml.etree.tostring(root, pretty_print=True)

# 5. How many pages in the PDF document?
pages = list(root)
print "There are",len(pages),"pages"


def dropper(table):
    if table!='':
        try: scraperwiki.sqlite.execute('drop table "'+table+'"')
        except: pass

dropper('fabvarn')

skiplist=['COUNTRY','FACTORY NAME','ADDRESS','CITY','REGION']
bigdata=[]
for page in pages[1:]:
    for el in page:
        if el.tag == "text" and el.text not in skiplist:
            if int(el.attrib['left']) < 100: data = { 'Country': el.text }
            elif int(el.attrib['left']) < 250: data['Factory name'] = el.text
            elif int(el.attrib['left']) < 500: data['Address'] = el.text
            elif int(el.attrib['left']) < 1000: data['City'] = el.text
            else:
                data['Region'] = el.text
                print data
                bigdata.append( data.copy() )
    scraperwiki.sqlite.save(unique_keys=[], table_name='fabvarn', data=bigdata)
    bigdata=[]# 1. Add some necessary libraries
import scraperwiki
import urllib2, lxml.etree

# 2. The URL/web address where we can find the PDF we want to scrape
url = 'http://cdn.varner.eu/cdn-1ce36b6442a6146/Global/Varner/CSR/Downloads_CSR/Fabrikklister_VarnerGruppen_2013.pdf'

# 3. Grab the file and convert it to an XML document we can work with
pdfdata = urllib2.urlopen(url).read()
xmldata = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(xmldata)

# 4. Have a peek at the XML (click the "more" link in the Console to preview it).
print lxml.etree.tostring(root, pretty_print=True)

# 5. How many pages in the PDF document?
pages = list(root)
print "There are",len(pages),"pages"


def dropper(table):
    if table!='':
        try: scraperwiki.sqlite.execute('drop table "'+table+'"')
        except: pass

dropper('fabvarn')

skiplist=['COUNTRY','FACTORY NAME','ADDRESS','CITY','REGION']
bigdata=[]
for page in pages[1:]:
    for el in page:
        if el.tag == "text" and el.text not in skiplist:
            if int(el.attrib['left']) < 100: data = { 'Country': el.text }
            elif int(el.attrib['left']) < 250: data['Factory name'] = el.text
            elif int(el.attrib['left']) < 500: data['Address'] = el.text
            elif int(el.attrib['left']) < 1000: data['City'] = el.text
            else:
                data['Region'] = el.text
                print data
                bigdata.append( data.copy() )
    scraperwiki.sqlite.save(unique_keys=[], table_name='fabvarn', data=bigdata)
    bigdata=[]