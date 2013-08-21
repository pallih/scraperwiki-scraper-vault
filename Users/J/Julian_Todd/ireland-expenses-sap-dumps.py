import scraperwiki
import urllib
import lxml.etree, lxml.html
import re
import datetime

# directory with all files:  http://seagrass.goatchurch.org.uk/~julian/sap_data_dump/

# work on just the smallest file
pdfurl = "http://seagrass.goatchurch.org.uk/~julian/sap_data_dump/01janto16mar%202010%20SAP%20Data%20Dump.pdf"
title = 'January 2010 SAP Data Dump'

# This data is questionable.  The claim-ids are repeated for several lines, 
# sometimes with the same and sometimes with different amounts.  
# It's possible they have given the historic value of each claim, rather than 
# the final claim.  You need to find what's going on with this data.  
# Page 750 is missing the names on some of the records.

# headers
#Description
#FM pstg d.
#Hdr text/Claim Id
#Pmt doc.no
#Vend/Cust Name
#FMAC Amnt


# example record

#<text top="202" left="53" width="65" height="11" font="0">Home Travel 1</text>
#<text top="202" left="305" width="333" height="11" font="0">25.02.2010 19112009-02022010-581631 2010072175 JOSEPHINE KELLY</text>
#<text top="202" left="754" width="25" height="11" font="0">13.71</text>

def parseline(iln, pagenumber, title):
    if len(iln) != 3:
        if iln:
            print [ lxml.etree.tostring(i)  for i in iln ]
        return

    print [ lxml.etree.tostring(i)  for i in iln ]

    data = { }
    data['Description'] = iln[0].text
    data['Amount'] = float(re.sub(',', '', iln[2].text))
    mmid = re.match('(\d\d)\.(\d\d)\.(\d\d\d\d) ([\d\-]+) (\d+) (.*)$', iln[1].text)
    if not mmid:
        print "Failed page", pagenumber, iln[1].text
        return

    # 21.01.2010 03122009-17122009-579265 2010019725 WILLIAM NEWE', iln[1].text)
    data['date'] = datetime.datetime(int(mmid.group(3)), int(mmid.group(2)), int(mmid.group(1)))
    data['claimid'] = mmid.group(4)
    data['docno'] = mmid.group(5)
    data['name'] = mmid.group(6)
    data['pagenumber'] = pagenumber
    data['title'] = title
    scraperwiki.datastore.save(unique_keys=['claimid'], data=data, date=data.get('date'))


def parsepage(lines, pagenumber, title):
    top = -1
    iln = [ ]
    print "%d" % pagenumber,
    for line in lines:
        ltop = int(line.attrib.get('top'))
        if ltop == top:
            iln.append(line)
        else:
            parseline(iln, pagenumber, title)
            iln = [ line ]
            top = ltop
    parseline(iln, pagenumber, title)


pdfdata = urllib.urlopen(pdfurl).read()
pdfxml = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(pdfxml)
#print pdfxml[:20000]

print "Pages:", len(root)

for page in list(root)[749:752]:   # skip what's already done
    assert page.tag == 'page'
    pagenumber = int(page.attrib.get('number'))
    lines = [ ]
    for v in page:
        if v.tag == 'text':
            lines.append(v)
        else:
            assert v.tag == 'fontspec'
    parsepage(lines, pagenumber, title)
    
    
    
import scraperwiki
import urllib
import lxml.etree, lxml.html
import re
import datetime

# directory with all files:  http://seagrass.goatchurch.org.uk/~julian/sap_data_dump/

# work on just the smallest file
pdfurl = "http://seagrass.goatchurch.org.uk/~julian/sap_data_dump/01janto16mar%202010%20SAP%20Data%20Dump.pdf"
title = 'January 2010 SAP Data Dump'

# This data is questionable.  The claim-ids are repeated for several lines, 
# sometimes with the same and sometimes with different amounts.  
# It's possible they have given the historic value of each claim, rather than 
# the final claim.  You need to find what's going on with this data.  
# Page 750 is missing the names on some of the records.

# headers
#Description
#FM pstg d.
#Hdr text/Claim Id
#Pmt doc.no
#Vend/Cust Name
#FMAC Amnt


# example record

#<text top="202" left="53" width="65" height="11" font="0">Home Travel 1</text>
#<text top="202" left="305" width="333" height="11" font="0">25.02.2010 19112009-02022010-581631 2010072175 JOSEPHINE KELLY</text>
#<text top="202" left="754" width="25" height="11" font="0">13.71</text>

def parseline(iln, pagenumber, title):
    if len(iln) != 3:
        if iln:
            print [ lxml.etree.tostring(i)  for i in iln ]
        return

    print [ lxml.etree.tostring(i)  for i in iln ]

    data = { }
    data['Description'] = iln[0].text
    data['Amount'] = float(re.sub(',', '', iln[2].text))
    mmid = re.match('(\d\d)\.(\d\d)\.(\d\d\d\d) ([\d\-]+) (\d+) (.*)$', iln[1].text)
    if not mmid:
        print "Failed page", pagenumber, iln[1].text
        return

    # 21.01.2010 03122009-17122009-579265 2010019725 WILLIAM NEWE', iln[1].text)
    data['date'] = datetime.datetime(int(mmid.group(3)), int(mmid.group(2)), int(mmid.group(1)))
    data['claimid'] = mmid.group(4)
    data['docno'] = mmid.group(5)
    data['name'] = mmid.group(6)
    data['pagenumber'] = pagenumber
    data['title'] = title
    scraperwiki.datastore.save(unique_keys=['claimid'], data=data, date=data.get('date'))


def parsepage(lines, pagenumber, title):
    top = -1
    iln = [ ]
    print "%d" % pagenumber,
    for line in lines:
        ltop = int(line.attrib.get('top'))
        if ltop == top:
            iln.append(line)
        else:
            parseline(iln, pagenumber, title)
            iln = [ line ]
            top = ltop
    parseline(iln, pagenumber, title)


pdfdata = urllib.urlopen(pdfurl).read()
pdfxml = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(pdfxml)
#print pdfxml[:20000]

print "Pages:", len(root)

for page in list(root)[749:752]:   # skip what's already done
    assert page.tag == 'page'
    pagenumber = int(page.attrib.get('number'))
    lines = [ ]
    for v in page:
        if v.tag == 'text':
            lines.append(v)
        else:
            assert v.tag == 'fontspec'
    parsepage(lines, pagenumber, title)
    
    
    
import scraperwiki
import urllib
import lxml.etree, lxml.html
import re
import datetime

# directory with all files:  http://seagrass.goatchurch.org.uk/~julian/sap_data_dump/

# work on just the smallest file
pdfurl = "http://seagrass.goatchurch.org.uk/~julian/sap_data_dump/01janto16mar%202010%20SAP%20Data%20Dump.pdf"
title = 'January 2010 SAP Data Dump'

# This data is questionable.  The claim-ids are repeated for several lines, 
# sometimes with the same and sometimes with different amounts.  
# It's possible they have given the historic value of each claim, rather than 
# the final claim.  You need to find what's going on with this data.  
# Page 750 is missing the names on some of the records.

# headers
#Description
#FM pstg d.
#Hdr text/Claim Id
#Pmt doc.no
#Vend/Cust Name
#FMAC Amnt


# example record

#<text top="202" left="53" width="65" height="11" font="0">Home Travel 1</text>
#<text top="202" left="305" width="333" height="11" font="0">25.02.2010 19112009-02022010-581631 2010072175 JOSEPHINE KELLY</text>
#<text top="202" left="754" width="25" height="11" font="0">13.71</text>

def parseline(iln, pagenumber, title):
    if len(iln) != 3:
        if iln:
            print [ lxml.etree.tostring(i)  for i in iln ]
        return

    print [ lxml.etree.tostring(i)  for i in iln ]

    data = { }
    data['Description'] = iln[0].text
    data['Amount'] = float(re.sub(',', '', iln[2].text))
    mmid = re.match('(\d\d)\.(\d\d)\.(\d\d\d\d) ([\d\-]+) (\d+) (.*)$', iln[1].text)
    if not mmid:
        print "Failed page", pagenumber, iln[1].text
        return

    # 21.01.2010 03122009-17122009-579265 2010019725 WILLIAM NEWE', iln[1].text)
    data['date'] = datetime.datetime(int(mmid.group(3)), int(mmid.group(2)), int(mmid.group(1)))
    data['claimid'] = mmid.group(4)
    data['docno'] = mmid.group(5)
    data['name'] = mmid.group(6)
    data['pagenumber'] = pagenumber
    data['title'] = title
    scraperwiki.datastore.save(unique_keys=['claimid'], data=data, date=data.get('date'))


def parsepage(lines, pagenumber, title):
    top = -1
    iln = [ ]
    print "%d" % pagenumber,
    for line in lines:
        ltop = int(line.attrib.get('top'))
        if ltop == top:
            iln.append(line)
        else:
            parseline(iln, pagenumber, title)
            iln = [ line ]
            top = ltop
    parseline(iln, pagenumber, title)


pdfdata = urllib.urlopen(pdfurl).read()
pdfxml = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(pdfxml)
#print pdfxml[:20000]

print "Pages:", len(root)

for page in list(root)[749:752]:   # skip what's already done
    assert page.tag == 'page'
    pagenumber = int(page.attrib.get('number'))
    lines = [ ]
    for v in page:
        if v.tag == 'text':
            lines.append(v)
        else:
            assert v.tag == 'fontspec'
    parsepage(lines, pagenumber, title)
    
    
    
import scraperwiki
import urllib
import lxml.etree, lxml.html
import re
import datetime

# directory with all files:  http://seagrass.goatchurch.org.uk/~julian/sap_data_dump/

# work on just the smallest file
pdfurl = "http://seagrass.goatchurch.org.uk/~julian/sap_data_dump/01janto16mar%202010%20SAP%20Data%20Dump.pdf"
title = 'January 2010 SAP Data Dump'

# This data is questionable.  The claim-ids are repeated for several lines, 
# sometimes with the same and sometimes with different amounts.  
# It's possible they have given the historic value of each claim, rather than 
# the final claim.  You need to find what's going on with this data.  
# Page 750 is missing the names on some of the records.

# headers
#Description
#FM pstg d.
#Hdr text/Claim Id
#Pmt doc.no
#Vend/Cust Name
#FMAC Amnt


# example record

#<text top="202" left="53" width="65" height="11" font="0">Home Travel 1</text>
#<text top="202" left="305" width="333" height="11" font="0">25.02.2010 19112009-02022010-581631 2010072175 JOSEPHINE KELLY</text>
#<text top="202" left="754" width="25" height="11" font="0">13.71</text>

def parseline(iln, pagenumber, title):
    if len(iln) != 3:
        if iln:
            print [ lxml.etree.tostring(i)  for i in iln ]
        return

    print [ lxml.etree.tostring(i)  for i in iln ]

    data = { }
    data['Description'] = iln[0].text
    data['Amount'] = float(re.sub(',', '', iln[2].text))
    mmid = re.match('(\d\d)\.(\d\d)\.(\d\d\d\d) ([\d\-]+) (\d+) (.*)$', iln[1].text)
    if not mmid:
        print "Failed page", pagenumber, iln[1].text
        return

    # 21.01.2010 03122009-17122009-579265 2010019725 WILLIAM NEWE', iln[1].text)
    data['date'] = datetime.datetime(int(mmid.group(3)), int(mmid.group(2)), int(mmid.group(1)))
    data['claimid'] = mmid.group(4)
    data['docno'] = mmid.group(5)
    data['name'] = mmid.group(6)
    data['pagenumber'] = pagenumber
    data['title'] = title
    scraperwiki.datastore.save(unique_keys=['claimid'], data=data, date=data.get('date'))


def parsepage(lines, pagenumber, title):
    top = -1
    iln = [ ]
    print "%d" % pagenumber,
    for line in lines:
        ltop = int(line.attrib.get('top'))
        if ltop == top:
            iln.append(line)
        else:
            parseline(iln, pagenumber, title)
            iln = [ line ]
            top = ltop
    parseline(iln, pagenumber, title)


pdfdata = urllib.urlopen(pdfurl).read()
pdfxml = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(pdfxml)
#print pdfxml[:20000]

print "Pages:", len(root)

for page in list(root)[749:752]:   # skip what's already done
    assert page.tag == 'page'
    pagenumber = int(page.attrib.get('number'))
    lines = [ ]
    for v in page:
        if v.tag == 'text':
            lines.append(v)
        else:
            assert v.tag == 'fontspec'
    parsepage(lines, pagenumber, title)
    
    
    
import scraperwiki
import urllib
import lxml.etree, lxml.html
import re
import datetime

# directory with all files:  http://seagrass.goatchurch.org.uk/~julian/sap_data_dump/

# work on just the smallest file
pdfurl = "http://seagrass.goatchurch.org.uk/~julian/sap_data_dump/01janto16mar%202010%20SAP%20Data%20Dump.pdf"
title = 'January 2010 SAP Data Dump'

# This data is questionable.  The claim-ids are repeated for several lines, 
# sometimes with the same and sometimes with different amounts.  
# It's possible they have given the historic value of each claim, rather than 
# the final claim.  You need to find what's going on with this data.  
# Page 750 is missing the names on some of the records.

# headers
#Description
#FM pstg d.
#Hdr text/Claim Id
#Pmt doc.no
#Vend/Cust Name
#FMAC Amnt


# example record

#<text top="202" left="53" width="65" height="11" font="0">Home Travel 1</text>
#<text top="202" left="305" width="333" height="11" font="0">25.02.2010 19112009-02022010-581631 2010072175 JOSEPHINE KELLY</text>
#<text top="202" left="754" width="25" height="11" font="0">13.71</text>

def parseline(iln, pagenumber, title):
    if len(iln) != 3:
        if iln:
            print [ lxml.etree.tostring(i)  for i in iln ]
        return

    print [ lxml.etree.tostring(i)  for i in iln ]

    data = { }
    data['Description'] = iln[0].text
    data['Amount'] = float(re.sub(',', '', iln[2].text))
    mmid = re.match('(\d\d)\.(\d\d)\.(\d\d\d\d) ([\d\-]+) (\d+) (.*)$', iln[1].text)
    if not mmid:
        print "Failed page", pagenumber, iln[1].text
        return

    # 21.01.2010 03122009-17122009-579265 2010019725 WILLIAM NEWE', iln[1].text)
    data['date'] = datetime.datetime(int(mmid.group(3)), int(mmid.group(2)), int(mmid.group(1)))
    data['claimid'] = mmid.group(4)
    data['docno'] = mmid.group(5)
    data['name'] = mmid.group(6)
    data['pagenumber'] = pagenumber
    data['title'] = title
    scraperwiki.datastore.save(unique_keys=['claimid'], data=data, date=data.get('date'))


def parsepage(lines, pagenumber, title):
    top = -1
    iln = [ ]
    print "%d" % pagenumber,
    for line in lines:
        ltop = int(line.attrib.get('top'))
        if ltop == top:
            iln.append(line)
        else:
            parseline(iln, pagenumber, title)
            iln = [ line ]
            top = ltop
    parseline(iln, pagenumber, title)


pdfdata = urllib.urlopen(pdfurl).read()
pdfxml = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(pdfxml)
#print pdfxml[:20000]

print "Pages:", len(root)

for page in list(root)[749:752]:   # skip what's already done
    assert page.tag == 'page'
    pagenumber = int(page.attrib.get('number'))
    lines = [ ]
    for v in page:
        if v.tag == 'text':
            lines.append(v)
        else:
            assert v.tag == 'fontspec'
    parsepage(lines, pagenumber, title)
    
    
    
import scraperwiki
import urllib
import lxml.etree, lxml.html
import re
import datetime

# directory with all files:  http://seagrass.goatchurch.org.uk/~julian/sap_data_dump/

# work on just the smallest file
pdfurl = "http://seagrass.goatchurch.org.uk/~julian/sap_data_dump/01janto16mar%202010%20SAP%20Data%20Dump.pdf"
title = 'January 2010 SAP Data Dump'

# This data is questionable.  The claim-ids are repeated for several lines, 
# sometimes with the same and sometimes with different amounts.  
# It's possible they have given the historic value of each claim, rather than 
# the final claim.  You need to find what's going on with this data.  
# Page 750 is missing the names on some of the records.

# headers
#Description
#FM pstg d.
#Hdr text/Claim Id
#Pmt doc.no
#Vend/Cust Name
#FMAC Amnt


# example record

#<text top="202" left="53" width="65" height="11" font="0">Home Travel 1</text>
#<text top="202" left="305" width="333" height="11" font="0">25.02.2010 19112009-02022010-581631 2010072175 JOSEPHINE KELLY</text>
#<text top="202" left="754" width="25" height="11" font="0">13.71</text>

def parseline(iln, pagenumber, title):
    if len(iln) != 3:
        if iln:
            print [ lxml.etree.tostring(i)  for i in iln ]
        return

    print [ lxml.etree.tostring(i)  for i in iln ]

    data = { }
    data['Description'] = iln[0].text
    data['Amount'] = float(re.sub(',', '', iln[2].text))
    mmid = re.match('(\d\d)\.(\d\d)\.(\d\d\d\d) ([\d\-]+) (\d+) (.*)$', iln[1].text)
    if not mmid:
        print "Failed page", pagenumber, iln[1].text
        return

    # 21.01.2010 03122009-17122009-579265 2010019725 WILLIAM NEWE', iln[1].text)
    data['date'] = datetime.datetime(int(mmid.group(3)), int(mmid.group(2)), int(mmid.group(1)))
    data['claimid'] = mmid.group(4)
    data['docno'] = mmid.group(5)
    data['name'] = mmid.group(6)
    data['pagenumber'] = pagenumber
    data['title'] = title
    scraperwiki.datastore.save(unique_keys=['claimid'], data=data, date=data.get('date'))


def parsepage(lines, pagenumber, title):
    top = -1
    iln = [ ]
    print "%d" % pagenumber,
    for line in lines:
        ltop = int(line.attrib.get('top'))
        if ltop == top:
            iln.append(line)
        else:
            parseline(iln, pagenumber, title)
            iln = [ line ]
            top = ltop
    parseline(iln, pagenumber, title)


pdfdata = urllib.urlopen(pdfurl).read()
pdfxml = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(pdfxml)
#print pdfxml[:20000]

print "Pages:", len(root)

for page in list(root)[749:752]:   # skip what's already done
    assert page.tag == 'page'
    pagenumber = int(page.attrib.get('number'))
    lines = [ ]
    for v in page:
        if v.tag == 'text':
            lines.append(v)
        else:
            assert v.tag == 'fontspec'
    parsepage(lines, pagenumber, title)
    
    
    
import scraperwiki
import urllib
import lxml.etree, lxml.html
import re
import datetime

# directory with all files:  http://seagrass.goatchurch.org.uk/~julian/sap_data_dump/

# work on just the smallest file
pdfurl = "http://seagrass.goatchurch.org.uk/~julian/sap_data_dump/01janto16mar%202010%20SAP%20Data%20Dump.pdf"
title = 'January 2010 SAP Data Dump'

# This data is questionable.  The claim-ids are repeated for several lines, 
# sometimes with the same and sometimes with different amounts.  
# It's possible they have given the historic value of each claim, rather than 
# the final claim.  You need to find what's going on with this data.  
# Page 750 is missing the names on some of the records.

# headers
#Description
#FM pstg d.
#Hdr text/Claim Id
#Pmt doc.no
#Vend/Cust Name
#FMAC Amnt


# example record

#<text top="202" left="53" width="65" height="11" font="0">Home Travel 1</text>
#<text top="202" left="305" width="333" height="11" font="0">25.02.2010 19112009-02022010-581631 2010072175 JOSEPHINE KELLY</text>
#<text top="202" left="754" width="25" height="11" font="0">13.71</text>

def parseline(iln, pagenumber, title):
    if len(iln) != 3:
        if iln:
            print [ lxml.etree.tostring(i)  for i in iln ]
        return

    print [ lxml.etree.tostring(i)  for i in iln ]

    data = { }
    data['Description'] = iln[0].text
    data['Amount'] = float(re.sub(',', '', iln[2].text))
    mmid = re.match('(\d\d)\.(\d\d)\.(\d\d\d\d) ([\d\-]+) (\d+) (.*)$', iln[1].text)
    if not mmid:
        print "Failed page", pagenumber, iln[1].text
        return

    # 21.01.2010 03122009-17122009-579265 2010019725 WILLIAM NEWE', iln[1].text)
    data['date'] = datetime.datetime(int(mmid.group(3)), int(mmid.group(2)), int(mmid.group(1)))
    data['claimid'] = mmid.group(4)
    data['docno'] = mmid.group(5)
    data['name'] = mmid.group(6)
    data['pagenumber'] = pagenumber
    data['title'] = title
    scraperwiki.datastore.save(unique_keys=['claimid'], data=data, date=data.get('date'))


def parsepage(lines, pagenumber, title):
    top = -1
    iln = [ ]
    print "%d" % pagenumber,
    for line in lines:
        ltop = int(line.attrib.get('top'))
        if ltop == top:
            iln.append(line)
        else:
            parseline(iln, pagenumber, title)
            iln = [ line ]
            top = ltop
    parseline(iln, pagenumber, title)


pdfdata = urllib.urlopen(pdfurl).read()
pdfxml = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(pdfxml)
#print pdfxml[:20000]

print "Pages:", len(root)

for page in list(root)[749:752]:   # skip what's already done
    assert page.tag == 'page'
    pagenumber = int(page.attrib.get('number'))
    lines = [ ]
    for v in page:
        if v.tag == 'text':
            lines.append(v)
        else:
            assert v.tag == 'fontspec'
    parsepage(lines, pagenumber, title)
    
    
    
