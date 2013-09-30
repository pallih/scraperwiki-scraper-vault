import scraperwiki

# Blank Python

import urllib2, lxml.etree

url = 'http://cdn.varner.eu/cdn-1ce36b6442a6146/Global/Varner/CSR/Downloads_CSR/Fabrikklister_VarnerGruppen_2013.pdf'

pdfdata = urllib2.urlopen(url).read()
xmldata = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(xmldata)

pages = list(root)
print "There are",len(pages),"pages"

skiplist=['COUNTRY','FACTORY NAME','ADDRESS','CITY','REGION']

for page in pages[1:]:
  for el in page:
    if el.tag == "text" and el.text not in skiplist:
      if int(el.attrib['left']) < 100: data = { 'Country': el.text }
      elif int(el.attrib['left']) < 250: data['Factory name'] = el.text
      elif int(el.attrib['left']) < 500: data['Address'] = el.text
      elif int(el.attrib['left']) < 1000: data['City'] = el.text
      else:
        data['Region'] = el.text
        scraperwiki.sqlite.save(unique_keys=[], table_name='fabvarn', data=data)
        #print data

def dropper(table):
  if table!='':
    try: scraperwiki.sqlite.execute('drop table "'+table+'"')
    except: pass

def gettext_with_bi_tags(el):
  res = [ ]
  if el.text:
    res.append(el.text)
  for lel in el:
    res.append("<%s>" % lel.tag)
    res.append(gettext_with_bi_tags(lel))
    res.append("" % lel.tag)
    if el.tail:
      res.append(el.tail)
  return "".join(res).strip()

import scraperwiki

# Blank Python

import urllib2, lxml.etree

url = 'http://cdn.varner.eu/cdn-1ce36b6442a6146/Global/Varner/CSR/Downloads_CSR/Fabrikklister_VarnerGruppen_2013.pdf'

pdfdata = urllib2.urlopen(url).read()
xmldata = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(xmldata)

pages = list(root)
print "There are",len(pages),"pages"

skiplist=['COUNTRY','FACTORY NAME','ADDRESS','CITY','REGION']

for page in pages[1:]:
  for el in page:
    if el.tag == "text" and el.text not in skiplist:
      if int(el.attrib['left']) < 100: data = { 'Country': el.text }
      elif int(el.attrib['left']) < 250: data['Factory name'] = el.text
      elif int(el.attrib['left']) < 500: data['Address'] = el.text
      elif int(el.attrib['left']) < 1000: data['City'] = el.text
      else:
        data['Region'] = el.text
        scraperwiki.sqlite.save(unique_keys=[], table_name='fabvarn', data=data)
        #print data

def dropper(table):
  if table!='':
    try: scraperwiki.sqlite.execute('drop table "'+table+'"')
    except: pass

def gettext_with_bi_tags(el):
  res = [ ]
  if el.text:
    res.append(el.text)
  for lel in el:
    res.append("<%s>" % lel.tag)
    res.append(gettext_with_bi_tags(lel))
    res.append("" % lel.tag)
    if el.tail:
      res.append(el.tail)
  return "".join(res).strip()

import scraperwiki

# Blank Python

import urllib2, lxml.etree

url = 'http://cdn.varner.eu/cdn-1ce36b6442a6146/Global/Varner/CSR/Downloads_CSR/Fabrikklister_VarnerGruppen_2013.pdf'

pdfdata = urllib2.urlopen(url).read()
xmldata = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(xmldata)

pages = list(root)
print "There are",len(pages),"pages"

skiplist=['COUNTRY','FACTORY NAME','ADDRESS','CITY','REGION']

for page in pages[1:]:
  for el in page:
    if el.tag == "text" and el.text not in skiplist:
      if int(el.attrib['left']) < 100: data = { 'Country': el.text }
      elif int(el.attrib['left']) < 250: data['Factory name'] = el.text
      elif int(el.attrib['left']) < 500: data['Address'] = el.text
      elif int(el.attrib['left']) < 1000: data['City'] = el.text
      else:
        data['Region'] = el.text
        scraperwiki.sqlite.save(unique_keys=[], table_name='fabvarn', data=data)
        #print data

def dropper(table):
  if table!='':
    try: scraperwiki.sqlite.execute('drop table "'+table+'"')
    except: pass

def gettext_with_bi_tags(el):
  res = [ ]
  if el.text:
    res.append(el.text)
  for lel in el:
    res.append("<%s>" % lel.tag)
    res.append(gettext_with_bi_tags(lel))
    res.append("" % lel.tag)
    if el.tail:
      res.append(el.tail)
  return "".join(res).strip()

