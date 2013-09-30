# 1. Add some necessary libraries
import scraperwiki
import urllib2, lxml.etree

# 2. The URL/web address where we can find the PDF we want to scrape
#url = 'http://cdn.varner.eu/cdn-1ce36b6442a6146/Global/Varner/CSR/Downloads_CSR/Fabrikklister_VarnerGruppen_2013.pdf'
url = 'http://www.budget.gov.au/2013-14/content/bp1/download/bp1_bs6.pdf'

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

dropper('fedbudget2013expenses')

skiplist=['Actuals','Estimates','Projections','$m','2011-12','2012-13','2013-14','2014-15','2015-16','2016-17']
bigdata=[]
for page in pages[59:62]:
    for el in page:
        if el.tag == "text" and int(el.attrib['font']) >= 30 and el.text not in skiplist:
            if int(el.attrib['left']) < 422: data = { 'function': el.text }
            elif int(el.attrib['left']) < 481: data['2011-12'] = el.text
            elif int(el.attrib['left']) < 538: data['2012-13'] = el.text
            elif int(el.attrib['left']) < 594: data['2013-14'] = el.text
            elif int(el.attrib['left']) < 653: data['2014-15'] = el.text
            elif int(el.attrib['left']) < 710: data['2015-16'] = el.text
            else:
                data['2016-17'] = el.text
                print data
                bigdata.append( data.copy() )
scraperwiki.sqlite.save(unique_keys=[], table_name='fedbudget2013expenses', data=bigdata)
bigdata=[]# 1. Add some necessary libraries
import scraperwiki
import urllib2, lxml.etree

# 2. The URL/web address where we can find the PDF we want to scrape
#url = 'http://cdn.varner.eu/cdn-1ce36b6442a6146/Global/Varner/CSR/Downloads_CSR/Fabrikklister_VarnerGruppen_2013.pdf'
url = 'http://www.budget.gov.au/2013-14/content/bp1/download/bp1_bs6.pdf'

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

dropper('fedbudget2013expenses')

skiplist=['Actuals','Estimates','Projections','$m','2011-12','2012-13','2013-14','2014-15','2015-16','2016-17']
bigdata=[]
for page in pages[59:62]:
    for el in page:
        if el.tag == "text" and int(el.attrib['font']) >= 30 and el.text not in skiplist:
            if int(el.attrib['left']) < 422: data = { 'function': el.text }
            elif int(el.attrib['left']) < 481: data['2011-12'] = el.text
            elif int(el.attrib['left']) < 538: data['2012-13'] = el.text
            elif int(el.attrib['left']) < 594: data['2013-14'] = el.text
            elif int(el.attrib['left']) < 653: data['2014-15'] = el.text
            elif int(el.attrib['left']) < 710: data['2015-16'] = el.text
            else:
                data['2016-17'] = el.text
                print data
                bigdata.append( data.copy() )
scraperwiki.sqlite.save(unique_keys=[], table_name='fedbudget2013expenses', data=bigdata)
bigdata=[]